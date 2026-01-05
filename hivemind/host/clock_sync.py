import time


class ClockSyncService:
    def handle_sync_request(self, device_id: str, client_time: float):
        host_time = time.time()
        return {"host_time": host_time, "client_time": client_time}
