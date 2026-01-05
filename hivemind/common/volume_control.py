class VolumeController:
    def __init__(self, master_volume: float = 1.0):
        self.master_volume = float(master_volume)

    def apply_volume(self, audio_chunk):
        # Stub: return chunk unchanged
        return audio_chunk
