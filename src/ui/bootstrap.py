from __future__ import annotations

import sys
import os

# Ensure project 'src' directory is on sys.path for imports like 'hrneowave'
_here = os.path.dirname(os.path.abspath(__file__))
_src_root = os.path.normpath(os.path.join(_here, '..', '..'))
if _src_root not in sys.path:
    sys.path.insert(0, _src_root)

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

from src.ui.components.ui_config_manager import UIConfigManager
from src.ui.windows.splash_screen import SplashScreen


class CHNeoWaveBootstrap(QMainWindow):
    """Bootstrap minimal pour validation Phase 1."""

    def __init__(self) -> None:
        super().__init__()
        self.setup_ui_infrastructure()
        self.setup_demo_ui()

    def setup_ui_infrastructure(self) -> None:
        """Initialiser config et signaux."""
        # Configuration UI
        self.config_manager = UIConfigManager()
        app = QApplication.instance()
        if app is not None:
            self.config_manager.apply_styles(app)

        # Adaptateur signaux
        try:
            from src.ui.components.signal_adapter import UISignalAdapter  # defer import to avoid heavy deps at import time
            self.signal_adapter = UISignalAdapter()
            self.signal_adapter.core_error_occurred.connect(self.on_core_error)  # type: ignore[attr-defined]
            self.signal_adapter.acquisition_data_received.connect(self.on_data_received)  # type: ignore[attr-defined]
        except Exception as exc:
            # Degrade gracefully if core deps are missing; splash and UI can still run
            self.signal_adapter = None  # type: ignore[assignment]
            print(f"[UI] Signal adapter unavailable: {exc}")

    def setup_demo_ui(self) -> None:
        """Interface démo pour validation."""
        central = QLabel("CHNeoWave UI Infrastructure Ready")
        central.setObjectName("demo_label")
        self.setCentralWidget(central)
        self.setWindowTitle("CHNeoWave - Phase 1 Demo")
        self.resize(800, 600)

    def on_core_error(self, message: str) -> None:
        print(f"[UI] Core Error: {message}")

    def on_data_received(self, data: dict) -> None:
        print(f"[UI] Data Received: {len(data)} keys")


def main() -> int:
    """Point d'entrée bootstrap avec splash screen."""
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    def on_finished() -> None:
        window = CHNeoWaveBootstrap()
        window.show()

    splash.finished.connect(on_finished)  # type: ignore[attr-defined]
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())


