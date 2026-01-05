from enum import Enum


class MessageType(Enum):
    JOIN_REQUEST = "join_request"
    JOIN_ACCEPT = "join_accept"
    JOIN_REJECT = "join_reject"
    TIME_SYNC_REQUEST = "time_sync_request"
    TIME_SYNC_RESPONSE = "time_sync_response"
    HEARTBEAT = "heartbeat"
    SCHEDULE_TRACK = "schedule_track"
    AUDIO_CHUNK = "audio_chunk"


class Protocol:
    @staticmethod
    def create_join_reject(reason: str):
        return {"type": MessageType.JOIN_REJECT.value, "reason": reason}

    @staticmethod
    def create_join_accept(device_id: str, session_info: dict):
        return {"type": MessageType.JOIN_ACCEPT.value, "device_id": device_id, "session": session_info}

    @staticmethod
    def create_time_sync_response(host_time: float, client_time: float):
        return {"type": MessageType.TIME_SYNC_RESPONSE.value, "host_time": host_time, "client_time": client_time}

    @staticmethod
    def create_heartbeat_ack(device_id: str):
        return {"type": MessageType.HEARTBEAT.value, "device_id": device_id}

    @staticmethod
    def create_audio_chunk(play_at: float, sample_rate: int, channels: int, audio_data: bytes):
        return {
            "type": MessageType.AUDIO_CHUNK.value,
            "play_at": play_at,
            "sample_rate": sample_rate,
            "channels": channels,
            "audio_data": audio_data,
        }

    @staticmethod
    def create_schedule_message(track_url: str, start_at: float, duration: float = 0.0):
        return {
            "type": MessageType.SCHEDULE_TRACK.value,
            "track_url": track_url,
            "start_at": start_at,
            "duration": duration,
        }
