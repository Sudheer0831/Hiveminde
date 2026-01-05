import asyncio
import json

import pytest
import websockets

from hivemind.host.network_server import NetworkServer


@pytest.mark.asyncio
async def test_ws_server_accepts_connection():
    server = NetworkServer(port=0)

    # start server in background
    task = asyncio.create_task(server.start())

    # wait for server object to be assigned
    while server._server is None:
        await asyncio.sleep(0.01)

    sock = server._server.sockets[0]
    port = sock.getsockname()[1]

    uri = f"ws://localhost:{port}"

    async with websockets.connect(uri) as ws:
        # send a simple JSON message
        await ws.send(json.dumps({"type": "ping", "payload": {}}))

    # stop server
    await server.stop()
    await task
