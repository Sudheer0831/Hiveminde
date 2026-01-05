from typing import Optional


class AudioCodecManager:
    def __init__(self, use_compression: bool = True, sample_rate: int = 48000, channels: int = 2):
        self.use_compression = use_compression
        self.sample_rate = sample_rate
        self.channels = channels
        self._encoder = None
        self._decoder = None

        if use_compression:
            try:
                from opuslib import Encoder, Decoder

                self._encoder = Encoder(self.sample_rate, self.channels, 'audio')
                self._decoder = Decoder(self.sample_rate, self.channels)
            except Exception:
                # Fallback to no compression
                self._encoder = None
                self._decoder = None

    def encode(self, pcm_frames: Optional[bytes]):
        """Encode PCM frames (bytes) into Opus if available, else return raw bytes."""
        if not pcm_frames:
            return b"", False

        # Normalize input to bytes (16-bit signed little-endian PCM expected)
        data = None
        if isinstance(pcm_frames, (bytes, bytearray)):
            data = bytes(pcm_frames)
        else:
            try:
                import array

                if isinstance(pcm_frames, array.array):
                    data = pcm_frames.tobytes()
                elif isinstance(pcm_frames, list):
                    arr = array.array('h', pcm_frames)
                    data = arr.tobytes()
            except Exception:
                data = None

        if data is None:
            return b"", False

        if self._encoder:
            try:
                # Use a 20ms frame size (typical): samples_per_channel = sample_rate * 20 / 1000
                frame_size = int(self.sample_rate * 20 / 1000)
                encoded = self._encoder.encode(data, frame_size)
                return encoded, True
            except Exception:
                pass

        # fallback
        return pcm_frames if isinstance(pcm_frames, (bytes, bytearray)) else b"", False

    def decode(self, data: Optional[bytes]):
        """Decode Opus bytes back to PCM if decoder present; else return data."""
        if not data:
            return b""

        if self._decoder:
            try:
                pcm = self._decoder.decode(data, 960)
                return pcm
            except Exception:
                pass

        return data
