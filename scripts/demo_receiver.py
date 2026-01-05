"""Demo receiver: connect to server, listen for audio_chunk messages, decode and write raw PCM to a WAV file."""
import asyncio
import base64
import json
import wave
import time

import websockets

from hivemind.common.audio_codec import AudioCodecManager


async def run(host='localhost', port=7878, out='received.wav', timeout=5.0):
    uri = f"ws://{host}:{port}"
    codec = AudioCodecManager(use_compression=True)

    pcm_frames = bytearray()

    async with websockets.connect(uri) as ws:
        start = time.time()
        while time.time() - start < timeout:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            except asyncio.TimeoutError:
                break
            try:
                msg = json.loads(raw)
            except Exception:
                continue
            if msg.get('type') != 'audio_chunk':
                continue
            audio = msg.get('audio_data')
            if isinstance(audio, str):
                audio = base64.b64decode(audio)

            pcm = codec.decode(audio)
            if pcm:
                pcm_frames.extend(pcm)

    if pcm_frames:
        # write 16-bit mono WAV
        with wave.open(out, 'wb') as wf:
            wf.setnchannels(codec.channels)
            wf.setsampwidth(2)
            wf.setframerate(codec.sample_rate)
            wf.writeframes(bytes(pcm_frames))
        print('Wrote', out)
    else:
        print('No audio received')


if __name__ == '__main__':
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7878
    out = sys.argv[3] if len(sys.argv) > 3 else 'received.wav'
    asyncio.run(run(host, port, out))
