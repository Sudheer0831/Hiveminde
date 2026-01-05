import asyncio
import logging

logger = logging.getLogger(__name__)


class HiveMindClient:
    def __init__(self, session_code: str):
        self.session_code = session_code
        self.connected = False

    async def connect(self, host: str, port: int):
        logger.info(f"Connecting to {host}:{port} (stub)")
        await asyncio.sleep(0.01)
        self.connected = True

    async def run(self):
        # Simple stub main loop that waits until disconnected
        while self.connected:
            await asyncio.sleep(0.5)

    async def disconnect(self):
        if self.connected:
            self.connected = False
            logger.info("Client disconnected")

    async def send_message(self, message):
        # Stub message sender
        logger.debug(f"Client send_message: {message}")
