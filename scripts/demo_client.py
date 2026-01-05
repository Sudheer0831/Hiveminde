"""Simple demo client to connect to the WebSocket NetworkServer and send a join request."""
import asyncio
import json
import sys

import websockets


async def run(host='localhost', port=7878, session_code='HM-0000'):
    uri = f"ws://{host}:{port}"
    async with websockets.connect(uri) as ws:
        msg = {
            "type": "join_request",
            "payload": {
                "device_id": "demo-1",
                "device_name": "Demo Client",
                "session_code": session_code,
                "metadata": {}
            }
        }
        await ws.send(json.dumps(msg))
        print('Sent join_request')


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7878
    asyncio.run(run(host, port))
