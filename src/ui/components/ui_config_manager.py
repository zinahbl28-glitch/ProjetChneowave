from __future__ import annotations

import os
from typing import Any

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QSettings
except Exception:  # pragma: no cover - allow import without Qt in some envs
    class QApplication:  # type: ignore
        def setStyleSheet(self, *_: Any, **__: Any) -> None:
            pass
    class QSettings:  # type: ignore
        def __init__(self, *_: Any, **__: Any) -> None:
            pass
        def setValue(self, *_: Any, **__: Any) -> None:
            pass
        def value(self, *_: Any, **__: Any) -> Any:
            return None


class UIConfigManager:
    """Gestionnaire configuration UI (styles, préférences)."""

    def __init__(self) -> None:
        self.settings = QSettings("CHNeoWave", "UI")

    def _qss_path(self) -> str:
        here = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(here, '..', 'resources', 'styles.qss'))

    def load_styles(self) -> str:
        """Charger le contenu QSS depuis les ressources UI."""
        path = self._qss_path()
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def apply_styles(self, app: QApplication) -> None:
        """Appliquer les styles à l'application Qt."""
        stylesheet = self.load_styles()
        app.setStyleSheet(stylesheet)

    def save_window_geometry(self, window_name: str, geometry: Any) -> None:
        """Sauvegarder position/taille d'une fenêtre."""
        self.settings.setValue(f"{window_name}/geometry", geometry)

    def restore_window_geometry(self, window_name: str) -> Any:
        """Restaurer position/taille d'une fenêtre (si disponible)."""
        return self.settings.value(f"{window_name}/geometry")


