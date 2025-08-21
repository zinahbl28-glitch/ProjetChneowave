from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from ...resources.styles import COLORS
from ...resources.universal_golden_system import UniversalGoldenSystem as UGS


class ProbeManagementWidget(QWidget):
    """Gestion simple des sondes (démo)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        spacing = UGS.get_spacing_system()
        fonts = UGS.get_font_sizes()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(spacing['sm'])

        # Liste des sondes
        self.tree = QTreeWidget(); self.tree.setHeaderLabels(["Sonde", "Type", "Statut", "Dernière calibration"]) 
        for i in range(1, 7):
            item = QTreeWidgetItem([f"P{i:02d}", "pressure", "Erreur", "—"])
            self.tree.addTopLevelItem(item)
        root.addWidget(self.tree, 1)

        # Actions
        actions = QHBoxLayout(); actions.setSpacing(spacing['sm'])
        self.btn_test = QPushButton("Tester")
        self.btn_config = QPushButton("Configurer")
        self.btn_calibrate = QPushButton("Étalonner")
        for b in (self.btn_test, self.btn_config, self.btn_calibrate):
            b.setStyleSheet(f"QPushButton {{ background: {COLORS['warning']}; color: white; border: none; border-radius: 6px; padding: 6px 10px; }}")
        actions.addWidget(self.btn_test)
        actions.addWidget(self.btn_config)
        actions.addWidget(self.btn_calibrate)
        root.addLayout(actions)




