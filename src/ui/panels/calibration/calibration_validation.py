from dataclasses import dataclass


@dataclass
class CalibrationThresholds:
    linearity_tolerance: float = 0.02
    noise_max: float = 0.01
    drift_max: float = 0.005


class CalibrationValidator:
    """Valide des métriques simples de calibration (placeholder)."""

    def __init__(self, thresholds: CalibrationThresholds | None = None):
        self.thresholds = thresholds or CalibrationThresholds()

    def validate(self, metrics: dict) -> bool:
        return (
            metrics.get("linearity_error", 0.0) <= self.thresholds.linearity_tolerance
            and metrics.get("noise", 0.0) <= self.thresholds.noise_max
            and metrics.get("drift", 0.0) <= self.thresholds.drift_max
        )




