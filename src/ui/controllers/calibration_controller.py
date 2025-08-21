from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMessageBox

from ..components.base_controller import BaseController
from ..panels.calibration_panel import CalibrationPanel
from ..components.app_state import ProjectInfo


class CalibrationController(BaseController):
    calibration_started = Signal()
    calibration_prepared = Signal()
    calibration_validated = Signal(bool)

    def __init__(self, project: ProjectInfo):
        super().__init__()
        self.project = project
        self.panel = CalibrationPanel()
        self._wire_panel_actions()

    def _wire_panel_actions(self):
        self.panel.btn_prepare.clicked.connect(self.on_prepare)
        self.panel.btn_start.clicked.connect(self.on_start)
        self.panel.btn_validate.clicked.connect(self.on_validate)

    def on_prepare(self):
        self.calibration_prepared.emit()
        QMessageBox.information(self.panel, "Calibration", "Préparation terminée.")

    def on_start(self):
        self.calibration_started.emit()
        QMessageBox.information(self.panel, "Calibration", "Calibration démarrée (démo).")

    def on_validate(self):
        is_ok = True
        self.calibration_validated.emit(is_ok)
        QMessageBox.information(self.panel, "Calibration", "Calibration validée (démo).")
