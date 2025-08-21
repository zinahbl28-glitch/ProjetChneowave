from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...resources.styles import COLORS
from ...resources.universal_golden_system import UniversalGoldenSystem as UGS


class CalibrationWizard(QWidget):
    """Assistant de calibration en 5 étapes (UI only, logique simulée)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self._setup_ui()

    def _setup_ui(self):
        spacing = UGS.get_spacing_system()
        fonts = UGS.get_font_sizes()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(spacing['sm'])

        # Barre de progression
        self.step_progress = QProgressBar(); self.step_progress.setRange(0, 4); self.step_progress.setValue(0)
        self.step_progress.setFixedHeight(14)
        root.addWidget(self.step_progress)

        # Conteneur d'étapes
        self.stack = QStackedWidget()
        for i, title in enumerate([
            "1. Vérification matériel",
            "2. Configuration paramètres",
            "3. Tests préliminaires",
            "4. Calibration automatique",
            "5. Validation des résultats",
        ]):
            page = QWidget(); v = QVBoxLayout(page); v.setSpacing(spacing['xs'])
            lab = QLabel(title); lab.setFont(QFont("Segoe UI", fonts['base'], QFont.Bold)); lab.setStyleSheet(f"color: {COLORS['warning']};")
            info = QLabel("Interface d'étape (démo)")
            info.setAlignment(Qt.AlignCenter)
            v.addWidget(lab)
            v.addWidget(info, 1)
            self.stack.addWidget(page)
        root.addWidget(self.stack, 1)

        # Contrôles navigation
        nav = QHBoxLayout(); nav.setSpacing(spacing['sm'])
        self.prev_btn = QPushButton("← Précédent")
        self.next_btn = QPushButton("Suivant →")
        for b in (self.prev_btn, self.next_btn):
            b.setStyleSheet(f"QPushButton {{ background: {COLORS['warning']}; color: white; border: none; border-radius: 6px; padding: 6px 12px; }}")
        self.prev_btn.clicked.connect(self.prev_step)
        self.next_btn.clicked.connect(self.next_step)
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.next_btn)
        root.addLayout(nav)

        self._sync_controls()

    def _sync_controls(self):
        self.stack.setCurrentIndex(self.current_step)
        self.step_progress.setValue(self.current_step)
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setEnabled(self.current_step < 4)

    def next_step(self):
        if self.current_step < 4:
            self.current_step += 1
            self._sync_controls()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._sync_controls()




