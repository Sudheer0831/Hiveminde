import logging
logger = logging.getLogger(__name__)


class WebDashboard:
    def __init__(self, host_app, port: int = 5000):
        self.host_app = host_app
        self.port = port

    def run(self):
        logger.info(f"WebDashboard stub running on port {self.port}")
