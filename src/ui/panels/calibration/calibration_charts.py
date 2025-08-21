from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QFileDialog, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from ...resources.universal_golden_system import UniversalGoldenSystem as UGS
from ...resources.styles import COLORS
from .calibration_data_sim import CalibrationDataSimulator


class CalibrationCharts(QWidget):
    """Graphiques temps réel (pyqtgraph si dispo)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_state()
        self._setup_ui()

    def _init_state(self):
        self.sim = CalibrationDataSimulator()
        self.timer = QTimer()
        self.timer.setInterval(100)  # 10 fps
        self.timer.timeout.connect(self.update_charts)
        # buffers par sonde
        self.probe_ids = ["P001", "P002", "P003", "P004"]
        self.buffers = {pid: [] for pid in self.probe_ids}
        self.max_points = 1000
        # pyqtgraph import
        try:
            import pyqtgraph as pg  # noqa: F401
            self._pg = __import__("pyqtgraph")
        except Exception:
            self._pg = None

    def _setup_ui(self):
        spacing = UGS.get_spacing_system()
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(spacing['sm'])

        # Header tools
        tools = QHBoxLayout(); tools.setSpacing(spacing['xs'])
        title = QLabel("Statistique Graphiques Calibration")
        title.setStyleSheet(f"color: {COLORS['primary']};")
        self.btn_start = QPushButton("Démarrer")
        self.btn_stop = QPushButton("Arrêter")
        self.btn_export = QPushButton("Exporter PNG")
        for b in (self.btn_start, self.btn_stop, self.btn_export):
            b.setStyleSheet(f"QPushButton {{ background: {COLORS['primary']}; color: white; border: none; border-radius: 6px; padding: 4px 10px; }}")
        self.btn_start.clicked.connect(self.start_real_time_monitoring)
        self.btn_stop.clicked.connect(self.stop_real_time_monitoring)
        self.btn_export.clicked.connect(self.export_png)
        tools.addWidget(title, 1); tools.addWidget(self.btn_start); tools.addWidget(self.btn_stop); tools.addWidget(self.btn_export)
        v.addLayout(tools)

        self.tabs = QTabWidget(); v.addWidget(self.tabs, 1)

        if self._pg is None:
            placeholder = QLabel("pyqtgraph non installé — graphiques désactivés")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet(f"background: {COLORS['surface']}; border: 1px dashed {COLORS['primary']}; padding: 12px;")
            self.tabs.addTab(placeholder, "Temps réel")
            return

        # Temps réel (4 sondes)
        self.realtime_plot = self._pg.PlotWidget()
        self.realtime_plot.addLegend()
        self.realtime_plot.showGrid(x=True, y=True, alpha=0.3)
        self.curves = {}
        colors = ['r', 'g', 'b', 'y']
        for i, pid in enumerate(self.probe_ids):
            self.curves[pid] = self.realtime_plot.plot(pen=self._pg.mkPen(colors[i], width=2), name=pid)
        self.tabs.addTab(self.realtime_plot, "Temps réel")

        # Historique (placeholder)
        self.history_plot = self._pg.PlotWidget(); self.history_plot.showGrid(x=True, y=True, alpha=0.3)
        self.tabs.addTab(self.history_plot, "Historique")

        # Comparaison (placeholder)
        self.compare_plot = self._pg.PlotWidget(); self.compare_plot.showGrid(x=True, y=True, alpha=0.3)
        self.tabs.addTab(self.compare_plot, "Comparaison")

    def start_real_time_monitoring(self):
        if self._pg is None:
            return
        self.timer.start()

    def stop_real_time_monitoring(self):
        self.timer.stop()

    def update_charts(self):
        if self._pg is None:
            return
        # alimenter buffers
        for pid in self.probe_ids:
            val = self.sim.generate_probe_data(pid, 1)[0]
            buf = self.buffers[pid]
            buf.append(val)
            if len(buf) > self.max_points:
                del buf[: len(buf) - self.max_points]
            # update courbe
            self.curves[pid].setData(buf)

    def export_png(self):
        if self._pg is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Exporter PNG", "calibration.png", "PNG Files (*.png)")
        if path:
            exporter = self._pg.exporters.ImageExporter(self.realtime_plot.plotItem)
            exporter.parameters()['width'] = 1200
            exporter.export(path)



