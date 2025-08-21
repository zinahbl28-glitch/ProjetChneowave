from __future__ import annotations

from typing import Tuple

from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtWidgets import QSplashScreen


SPLASH_CONFIG = {
    'size': (600, 400),
    'background_color': '#2C5282',
    'progress_bar_color': '#38A169',
    'text_color': '#FFFFFF',
    'font_size': 12,
}


class LoadingWorker(QThread):
    """Worker thread pour chargement en arrière-plan."""

    step_completed = Signal(str, float)  # (message, progress 0..1)
    loading_finished = Signal()

    def run(self) -> None:
        steps = [
            ("Initialisation système...", 0.2),
            ("Chargement modules core...", 0.4),
            ("Configuration interface...", 0.6),
            ("Connexion capteurs...", 0.8),
            ("Finalisation...", 1.0),
        ]
        for message, progress in steps:
            self.step_completed.emit(message, progress)
            self.msleep(500)  # 500ms par étape (2.5s au total)
        self.loading_finished.emit()


class SplashScreen(QSplashScreen):
    """Splash screen CHNeoWave avec progression et fermeture automatique."""

    finished = Signal()

    def __init__(self) -> None:
        size = SPLASH_CONFIG['size']  # type: ignore[index]
        pixmap = QPixmap(size[0], size[1])
        super().__init__(pixmap)
        self._progress = 0.0
        self._message = ""
        self.setWindowFlag(Qt.FramelessWindowHint)
        self._render(self._progress, "Démarrage...")
        self._setup_loading()

    def _setup_loading(self) -> None:
        self._worker = LoadingWorker()
        self._worker.step_completed.connect(self.update_progress)  # type: ignore[attr-defined]
        self._worker.loading_finished.connect(self.finish_loading)  # type: ignore[attr-defined]
        self._worker.start()

        # Filet de sécurité: fermer après 2.7s si jamais non-terminé
        QTimer.singleShot(2700, lambda: self.finish_loading(force=True))

    def update_progress(self, message: str, progress: float) -> None:
        self._progress = max(0.0, min(1.0, progress))
        self._message = message
        self._render(self._progress, self._message)

    def finish_loading(self, force: bool = False) -> None:
        if force or self._progress >= 1.0:
            # Laisser un léger délai pour un fondu (optionnel)
            QTimer.singleShot(200, self._close_and_emit)

    def _close_and_emit(self) -> None:
        # Assurer que le worker est terminé avant fermeture
        try:
            if hasattr(self, '_worker') and self._worker.isRunning():  # type: ignore[attr-defined]
                # Attendre brièvement la fin du thread
                if not self._worker.wait(800):  # type: ignore[attr-defined]
                    try:
                        self._worker.terminate()  # type: ignore[attr-defined]
                    except Exception:
                        pass
        except Exception:
            pass
        self.finished.emit()
        self.close()

    # ---------- Rendering ----------
    def _render(self, progress: float, message: str) -> None:
        pixmap = self.pixmap()
        if pixmap.isNull():
            size = SPLASH_CONFIG['size']  # type: ignore[index]
            pixmap = QPixmap(size[0], size[1])
        painter = QPainter(pixmap)
        self._paint_background(painter, pixmap.size().width(), pixmap.size().height())
        self._paint_title(painter, pixmap.size().width(), pixmap.size().height())
        self._paint_progress(painter, pixmap.size().width(), pixmap.size().height(), progress)
        self._paint_message(painter, pixmap.size().width(), pixmap.size().height(), message)
        painter.end()
        self.setPixmap(pixmap)
        self.repaint()

    def _paint_background(self, p: QPainter, w: int, h: int) -> None:
        color = QColor(SPLASH_CONFIG['background_color'])  # type: ignore[index]
        p.fillRect(0, 0, w, h, color)

    def _paint_title(self, p: QPainter, w: int, h: int) -> None:
        p.setPen(QColor(SPLASH_CONFIG['text_color']))  # type: ignore[index]
        font = QFont("Segoe UI", 14, QFont.Bold)
        p.setFont(font)
        p.drawText(0, 0, w, int(h * 0.5), Qt.AlignHCenter | Qt.AlignVCenter, "CHNeoWave")

    def _paint_progress(self, p: QPainter, w: int, h: int, progress: float) -> None:
        bar_w = int(w * 0.7)
        bar_h = 14
        bar_x = int((w - bar_w) / 2)
        bar_y = int(h * 0.65)
        # Fond barre
        p.fillRect(bar_x, bar_y, bar_w, bar_h, QColor(255, 255, 255, 60))
        # Remplissage
        fill_w = int(bar_w * progress)
        p.fillRect(bar_x, bar_y, fill_w, bar_h, QColor(SPLASH_CONFIG['progress_bar_color']))  # type: ignore[index]

    def _paint_message(self, p: QPainter, w: int, h: int, message: str) -> None:
        p.setPen(QColor(SPLASH_CONFIG['text_color']))  # type: ignore[index]
        font = QFont("Segoe UI", SPLASH_CONFIG['font_size'])  # type: ignore[index]
        p.setFont(font)
        p.drawText(0, int(h * 0.75), w, int(h * 0.2), Qt.AlignHCenter | Qt.AlignTop, message)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        # Nettoyage prudent du thread au cas où
        try:
            if hasattr(self, '_worker') and self._worker.isRunning():  # type: ignore[attr-defined]
                if not self._worker.wait(800):  # type: ignore[attr-defined]
                    try:
                        self._worker.terminate()  # type: ignore[attr-defined]
                    except Exception:
                        pass
        except Exception:
            pass
        super().closeEvent(event)


