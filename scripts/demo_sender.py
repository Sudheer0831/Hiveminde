"""Demo sender: generate a sine PCM, encode with AudioCodecManager, send audio_chunk messages to server."""
import asyncio
import base64
import json
import math
import time

import websockets

from hivemind.common.audio_codec import AudioCodecManager


async def run(host='localhost', port=7878, duration=1.0):
    uri = f"ws://{host}:{port}"
    codec = AudioCodecManager(use_compression=True)

    # generate 48000Hz, 16-bit mono PCM for `duration` seconds
    sr = codec.sample_rate
    channels = codec.channels
    freq = 440.0
    samples = int(sr * duration)
    pcm = bytearray()
    for n in range(samples):
        t = n / sr
        val = int(0.5 * 32767.0 * math.sin(2.0 * math.pi * freq * t))
        pcm.extend(int(val).to_bytes(2, 'little', signed=True))

    encoded, compressed = codec.encode(bytes(pcm))
    data_b64 = base64.b64encode(encoded).decode('ascii')

    msg = {
        'type': 'audio_chunk',
        'payload': {
            'play_at': time.time() + 0.5,
            'sample_rate': sr,
            'channels': channels,
        },
        'audio_data': data_b64,
    }

    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps(msg))
        print('Sent audio_chunk')


if __name__ == '__main__':
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7878
    dur = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    asyncio.run(run(host, port, dur))
