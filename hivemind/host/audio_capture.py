class AudioCapture:
    def __init__(self):
        self._running = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def get_chunk(self, timeout: float = 0.1):
        return None
