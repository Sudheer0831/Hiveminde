import asyncio
import json
import base64
import time

import pytest

from hivemind.host.network_server import NetworkServer


async def relay_handler(server_client, payload, audio_data):
    # Relay the incoming message to all connected clients
    msg = {
        'type': 'audio_chunk',
        'payload': payload,
        'audio_data': audio_data,
    }
    await server_client.server.broadcast(msg)


@pytest.mark.asyncio
async def test_e2e_audio_roundtrip():
    server = NetworkServer(port=0)

    # register handler for incoming audio_chunk
    server.register_handler('audio_chunk', relay_handler)

    task = asyncio.create_task(server.start())

    # wait for server sockets
    while server._server is None:
        await asyncio.sleep(0.01)

    port = server._server.sockets[0].getsockname()[1]

    # run sender and receiver concurrently using websockets
    import websockets
    from hivemind.common.audio_codec import AudioCodecManager

    codec = AudioCodecManager(use_compression=False)

    async def sender():
        uri = f"ws://localhost:{port}"
        async with websockets.connect(uri) as ws:
            pcm = (b"\x00\x00\x00\x00" * 240)  # small silent frames
            msg = {'type': 'audio_chunk', 'payload': {'play_at': time.time() + 0.5, 'sample_rate': codec.sample_rate, 'channels': codec.channels}, 'audio_data': base64.b64encode(pcm).decode('ascii')}
            await ws.send(json.dumps(msg))

    received = []

    async def receiver():
        uri = f"ws://localhost:{port}"
        async with websockets.connect(uri) as ws:
            # wait for relayed message
            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            m = json.loads(raw)
            if m.get('type') == 'audio_chunk':
                received.append(m)

    await asyncio.gather(sender(), receiver())

    await server.stop()
    await task

    assert len(received) == 1