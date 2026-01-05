from enum import Enum


class MessageType(Enum):
    JOIN_REQUEST = "join_request"
    TIME_SYNC_REQUEST = "time_sync_request"
    HEARTBEAT = "heartbeat"


class Protocol:
    @staticmethod
    def create_join_reject(reason: str):
        return {"type": "join_reject", "reason": reason}

    @staticmethod
    def create_join_accept(device_id: str, session_info: dict):
        return {"type": "join_accept", "device_id": device_id, "session": session_info}

    @staticmethod
    def create_time_sync_response(host_time: float, client_time: float):
        return {"type": "time_sync_response", "host_time": host_time, "client_time": client_time}

    @staticmethod
    def create_heartbeat_ack(device_id: str):
        return {"type": "heartbeat_ack", "device_id": device_id}

    @staticmethod
    def create_audio_chunk(play_at: float, sample_rate: int, channels: int, audio_data: bytes):
        return {
            "type": "audio_chunk",
            "play_at": play_at,
            "sample_rate": sample_rate,
            "channels": channels,
            "audio_data": audio_data,
        }
