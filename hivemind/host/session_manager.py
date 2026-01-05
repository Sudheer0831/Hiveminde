import time


class SessionManager:
    def __init__(self):
        self.session_code = "HM-0000"
        self.nodes = {}
        self.scheduled_tracks = []

    def accept_node(self, device_id: str, device_name: str, metadata: dict) -> bool:
        if device_id in self.nodes:
            return False
        self.nodes[device_id] = {"name": device_name, "metadata": metadata, "last_seen": time.time()}
        return True

    def get_session_info(self):
        return {"code": self.session_code, "node_count": len(self.nodes), "scheduled": list(self.scheduled_tracks)}

    def generate_session_code(self):
        import random
        code = f"HM-{random.randint(1000, 9999)}"
        self.session_code = code
        return code

    def add_scheduled_track(self, track_url: str, start_at: float, duration: float = 0.0):
        item = {"track_url": track_url, "start_at": start_at, "duration": duration}
        self.scheduled_tracks.append(item)
        return item

    def update_heartbeat(self, device_id: str):
        if device_id in self.nodes:
            self.nodes[device_id]["last_seen"] = time.time()

    def check_stale_nodes(self, timeout: float = 30.0):
        now = time.time()
        stale = [nid for nid, info in self.nodes.items() if now - info.get("last_seen", 0) > timeout]
        return stale

    def remove_node(self, device_id: str):
        if device_id in self.nodes:
            del self.nodes[device_id]
