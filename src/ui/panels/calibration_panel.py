from .base_module_panel import BaseModulePanel
from .calibration import CalibrationMainPanel
from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QSpinBox, QFormLayout, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt
from ..resources.styles import COLORS


class CalibrationPanel(BaseModulePanel):
    """Panel du module Calibration"""
    
    def __init__(self, parent=None):
        super().__init__(
            module_name="calibration",
            module_title="Module Calibration",
            module_description="Calibration des sondes et capteurs",
            parent=parent
        )
        
        # Remplacer le contenu par l'interface complète
        self.setup_calibration_specific_ui()
        
    def setup_calibration_specific_ui(self):
        main = CalibrationMainPanel(self)
        # Nettoyer le layout par défaut du BaseModulePanel et injecter
        lay = self.layout()
        if lay is not None:
            # retirer tous les widgets existants
            while lay.count():
                item = lay.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.setParent(None)
        v = lay or QVBoxLayout(self)
        v.addWidget(main)
