class AudioCodecManager:
    def __init__(self, use_compression: bool = True):
        self.use_compression = use_compression

    def encode(self, audio_chunk):
        # Return raw bytes and a flag indicating compression was used
        try:
            data = bytes(audio_chunk) if isinstance(audio_chunk, (bytes, bytearray)) else b""
        except Exception:
            data = b""
        return data, False
