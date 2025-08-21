from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

try:
    from PySide6.QtCore import QObject, Signal
except Exception:  # pragma: no cover - allow import without Qt in some envs
    class QObject:  # type: ignore
        pass
    class Signal:  # type: ignore
        def __init__(self, *_: Any, **__: Any) -> None:
            pass


@dataclass
class ProjectInfo:
    name: str = ""
    code: str = ""
    engineer: str = ""
    manager: str = ""
    scale: str = ""
    basin_type: str = ""


class AppState(QObject):
    """Global application state for the UI layer.

    This state mirrors project/session metadata required for the UI. Persistent
    storage and canonical metadata handling remain in `hrneowave.core`.
    """

    project_changed = Signal(object)  # ProjectInfo

    def __init__(self) -> None:
        super().__init__()
        self.current_project: Optional[ProjectInfo] = None
        self.calibration_data: Dict[str, Any] = {}
        self.acquisition_data: Dict[str, Any] = {}

    def set_project(self, project: ProjectInfo) -> None:
        self.current_project = project
        self.project_changed.emit(project)


