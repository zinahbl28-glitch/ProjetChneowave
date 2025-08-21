import random
from dataclasses import dataclass


@dataclass
class ProbeSimulator:
    probe_type: str = "pressure"
    probe_id: str = "P001"

    def get_current_reading(self) -> float:
        base = 1.0 if self.probe_type == "pressure" else 0.5
        noise = random.uniform(-0.02, 0.02)
        return base + noise

    def calibration_response(self, calibration_signal: float) -> float:
        return self.get_current_reading() * (1.0 - 0.1 * calibration_signal)


class CalibrationDataSimulator:
    def generate_probe_data(self, probe_id: str, duration_minutes: int = 30) -> list[float]:
        return [1.0 + random.uniform(-0.05, 0.05) for _ in range(duration_minutes)]

    def simulate_calibration_process(self) -> list[float]:
        vals = []
        value = 1.0
        for _ in range(100):
            value *= 0.995  # légère décroissance simulant l'ajustement
            value += random.uniform(-0.01, 0.01)
            vals.append(value)
        return vals




