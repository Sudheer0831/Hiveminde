import random


class LatencyCalibrator:
    def calibrate(self, device_id: str) -> float:
        # Return a fake latency in milliseconds
        return random.uniform(10.0, 50.0)
