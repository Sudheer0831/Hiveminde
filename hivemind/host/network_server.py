import asyncio
import logging

logger = logging.getLogger(__name__)


class NetworkServer:
    def __init__(self, port: int = 7878):
        self.port = port
        self.handlers = {}
        self.clients = {}
        self._running = False

    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    async def start(self):
        self._running = True
        logger.info(f"NetworkServer listening on port {self.port} (stub)")
        # Block until stopped
        while self._running:
            await asyncio.sleep(0.5)

    async def stop(self):
        self._running = False
        logger.info("NetworkServer stopped")

    async def broadcast(self, message):
        # Iterate client objects and call send_message if present
        for client in list(self.clients.values()):
            if hasattr(client, "send_message"):
                try:
                    await client.send_message(message)
                except Exception:
                    pass
