import asyncio
import json
import logging
from typing import Callable, Dict

import websockets

logger = logging.getLogger(__name__)


class WSClient:
    def __init__(self, ws, addr: str, server: "NetworkServer"):
        self.ws = ws
        self.addr = addr
        self.server = server
        self.device_id = None
        self.authenticated = False

    async def send_message(self, message):
        try:
            await self.ws.send(json.dumps(message))
        except Exception:
            logger.exception("Failed to send to client %s", self.addr)


class NetworkServer:
    """Simple asyncio WebSocket server.

    Exposes `register_handler(message_type, handler)` where handler is
    `async def handler(client, payload, audio_data)` and `broadcast(message)`.
    """

    def __init__(self, port: int = 7878, host: str = "0.0.0.0"):
        self.port = port
        self.host = host
        self.handlers: Dict[str, Callable] = {}
        self.clients: Dict[str, WSClient] = {}
        self._server = None
        self._stop_event = asyncio.Event()

    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    async def _handler(self, websocket, path=None):
        addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        client = WSClient(websocket, addr, self)
        client_id = addr
        self.clients[client_id] = client
        logger.info(f"Client connected: {addr}")

        try:
            async for raw in websocket:
                try:
                    msg = json.loads(raw)
                except Exception:
                    logger.warning("Received non-JSON from %s", addr)
                    continue

                mtype = msg.get("type")
                payload = msg.get("payload")
                audio_data = msg.get("audio_data")

                handler = self.handlers.get(mtype)
                if handler:
                    # Call handler but don't block other clients
                    asyncio.create_task(handler(client, payload or {}, audio_data))

        except websockets.ConnectionClosed:
            logger.info(f"Client disconnected: {addr}")
        finally:
            self.clients.pop(client_id, None)

    async def start(self):
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        self._server = await websockets.serve(self._handler, self.host, self.port)
        await self._stop_event.wait()
        # shutdown
        self._server.close()
        await self._server.wait_closed()
        logger.info("WebSocket server stopped")

    async def stop(self):
        self._stop_event.set()

    async def broadcast(self, message):
        data = json.dumps(message)
        for client in list(self.clients.values()):
            try:
                await client.ws.send(data)
            except Exception:
                logger.exception("Broadcast to client failed")
