from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalibrationReport:
    project_code: str
    generated_at: datetime
    summary: str

    def to_text(self) -> str:
        return f"Calibration Report\nProject: {self.project_code}\nGenerated: {self.generated_at.isoformat()}\n\n{self.summary}\n"



