class AudioScheduler:
    def schedule_chunk(self, audio_chunk):
        # Return simple schedule metadata
        return {"play_at": 0.0, "sample_rate": 48000, "channels": 2}
