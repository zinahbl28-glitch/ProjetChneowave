from __future__ import annotations

from typing import Dict, Any

try:
    from PySide6.QtCore import QObject, Signal
except Exception:  # pragma: no cover - allow import without Qt in some envs
    class QObject:  # type: ignore
        pass
    class Signal:  # type: ignore
        def __init__(self, *_: Any, **__: Any) -> None:
            pass


class BaseController(QObject):
    """Base controller following MVC for the CHNeoWave UI layer.

    Controllers emit `data_changed` and `error_occurred` signals, and expose a
    minimal lifecycle with `initialize` and `dispose` hooks. Business logic and
    heavy processing must live in core modules under `src/hrneowave/`.
    """

    data_changed = Signal(dict)
    error_occurred = Signal(str)

    def initialize(self) -> None:
        """Initialize controller resources and connect signals.

        Subclasses must implement this method.
        """
        raise NotImplementedError("initialize() must be implemented by subclasses")

    def dispose(self) -> None:
        """Optional cleanup hook.

        Subclasses can override to release resources and disconnect signals.
        """
        return None


