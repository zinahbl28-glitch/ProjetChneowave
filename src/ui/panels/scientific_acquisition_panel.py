"""
Module d'Acquisition Scientifique - Interface Complète
Acquisition temps réel des signaux des sondes avec métriques statistiques
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QGroupBox, QPushButton, QSpinBox, QDoubleSpinBox, QComboBox,
    QProgressBar, QTableWidget, QTableWidgetItem, QTextEdit,
    QSplitter, QScrollArea, QMessageBox, QFileDialog, QCheckBox
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread, pyqtSignal
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis

import numpy as np
import json
import os
from datetime import datetime, timedelta
import random


class ScientificAcquisitionPanel(QWidget):
    """Interface scientifique complète pour acquisition temps réel"""
    
    # Signaux
    acquisition_started = Signal()
    acquisition_stopped = Signal()
    acquisition_error = Signal(str)
    data_updated = Signal(dict)  # Nouvelles données
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.acquisition_active = False
        self.acquisition_data = {}
        self.real_time_data = {}
        self.statistical_metrics = {}
        
        # Paramètres d'acquisition
        self.sampling_frequency = 10  # Hz
        self.cycle_time = 1.0  # secondes
        self.active_probes = [0, 1, 2, 3]  # Sondes actives
        
        self.setup_ui()
        self.setup_connections()
        self.apply_scientific_styles()
        self.initialize_data_structures()
        
    def setup_ui(self):
        """Configuration de l'interface scientifique"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # En-tête scientifique
        self.setup_scientific_header(main_layout)
        
        # Zone principale avec splitter horizontal
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Panneau de contrôle (gauche)
        control_panel = self.create_control_panel()
        main_splitter.addWidget(control_panel)
        
        # Zone de visualisation (droite)
        visualization_area = self.create_visualization_area()
        main_splitter.addWidget(visualization_area)
        
        # Répartition 35% - 65%
        main_splitter.setSizes([350, 650])
        main_layout.addWidget(main_splitter)
        
        # Barre de statut
        self.setup_status_bar(main_layout)
        
    def setup_scientific_header(self, layout):
        """En-tête scientifique avec informations projet"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setLineWidth(2)
        header_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #059669;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F0FDF4, stop:1 #DCFCE7);
                padding: 8px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Titre principal
        title_label = QLabel("📡 ACQUISITION TEMPS RÉEL")
        title_label.setFont(QFont("Inter", 16, QFont.Bold))
        title_label.setStyleSheet("color: #059669;")
        
        # Informations projet
        project_info = QLabel("Projet: [Nom Projet] | Sondes: 4/8 | Fréquence: 10 Hz")
        project_info.setFont(QFont("Inter", 12))
        project_info.setStyleSheet("color: #475569;")
        
        # Statut global
        self.acquisition_status_label = QLabel("🔴 ACQUISITION ARRÊTÉE")
        self.acquisition_status_label.setFont(QFont("Inter", 12, QFont.Bold))
        self.acquisition_status_label.setStyleSheet("color: #DC2626;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(project_info)
        header_layout.addWidget(self.acquisition_status_label)
        
        layout.addWidget(header_frame)
        
    def create_control_panel(self):
        """Panneau de contrôle scientifique"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setSpacing(12)
        
        # 1. Paramètres d'acquisition
        acquisition_params_group = self.create_acquisition_params_group()
        control_layout.addWidget(acquisition_params_group)
        
        # 2. Contrôles d'acquisition
        acquisition_controls_group = self.create_acquisition_controls_group()
        control_layout.addWidget(acquisition_controls_group)
        
        # 3. Sélection des sondes
        probe_selection_group = self.create_probe_selection_group()
        control_layout.addWidget(probe_selection_group)
        
        # 4. Métriques statistiques temps réel
        realtime_metrics_group = self.create_realtime_metrics_group()
        control_layout.addWidget(realtime_metrics_group)
        
        control_layout.addStretch()
        
        return control_widget
        
    def create_acquisition_params_group(self):
        """Groupe des paramètres d'acquisition"""
        group = QGroupBox("⚙️ Paramètres d'Acquisition")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        # Fréquence d'échantillonnage
        layout.addWidget(QLabel("Fréquence (Hz):"), 0, 0)
        self.frequency_spin = QSpinBox()
        self.frequency_spin.setRange(1, 100)
        self.frequency_spin.setValue(10)
        self.frequency_spin.setFont(QFont("Inter", 11))
        self.frequency_spin.valueChanged.connect(self.on_frequency_changed)
        layout.addWidget(self.frequency_spin, 0, 1)
        
        # Cycle de temps
        layout.addWidget(QLabel("Cycle (s):"), 1, 0)
        self.cycle_spin = QDoubleSpinBox()
        self.cycle_spin.setRange(0.1, 10.0)
        self.cycle_spin.setValue(1.0)
        self.cycle_spin.setSuffix(" s")
        self.cycle_spin.setFont(QFont("Inter", 11))
        self.cycle_spin.valueChanged.connect(self.on_cycle_changed)
        layout.addWidget(self.cycle_spin, 1, 1)
        
        # Durée d'acquisition
        layout.addWidget(QLabel("Durée (min):"), 2, 0)
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 1440)  # 1 min à 24h
        self.duration_spin.setValue(30)
        self.duration_spin.setSuffix(" min")
        self.duration_spin.setFont(QFont("Inter", 11))
        layout.addWidget(self.duration_spin, 2, 1)
        
        # Mode d'acquisition
        layout.addWidget(QLabel("Mode:"), 3, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Continu", "Par cycles", "Manuel"])
        self.mode_combo.setFont(QFont("Inter", 11))
        layout.addWidget(self.mode_combo, 3, 1)
        
        return group
        
    def create_acquisition_controls_group(self):
        """Groupe des contrôles d'acquisition"""
        group = QGroupBox("🎛️ Contrôles d'Acquisition")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Boutons de contrôle
        button_layout = QHBoxLayout()
        
        self.start_acq_btn = QPushButton("🚀 Démarrer Acquisition")
        self.start_acq_btn.setFont(QFont("Inter", 11, QFont.Bold))
        self.start_acq_btn.setStyleSheet("""
            QPushButton {
                background: #059669;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #047857;
            }
        """)
        
        self.stop_acq_btn = QPushButton("⏹️ Arrêter")
        self.stop_acq_btn.setFont(QFont("Inter", 11))
        self.stop_acq_btn.setStyleSheet("""
            QPushButton {
                background: #DC2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #B91C1C;
            }
        """)
        self.stop_acq_btn.setEnabled(False)
        
        self.pause_acq_btn = QPushButton("⏸️ Pause")
        self.pause_acq_btn.setFont(QFont("Inter", 11))
        self.pause_acq_btn.setStyleSheet("""
            QPushButton {
                background: #D97706;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #B45309;
            }
        """)
        self.pause_acq_btn.setEnabled(False)
        
        button_layout.addWidget(self.start_acq_btn)
        button_layout.addWidget(self.stop_acq_btn)
        button_layout.addWidget(self.pause_acq_btn)
        
        layout.addLayout(button_layout)
        
        # Barre de progression
        self.acquisition_progress = QProgressBar()
        self.acquisition_progress.setFont(QFont("Inter", 10))
        self.acquisition_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E2E8F0;
                border-radius: 6px;
                text-align: center;
                background: #F8FAFC;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #059669, stop:1 #10B981);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.acquisition_progress)
        
        # Informations d'acquisition
        self.acquisition_info_label = QLabel("Prêt pour acquisition")
        self.acquisition_info_label.setFont(QFont("Inter", 10))
        self.acquisition_info_label.setStyleSheet("color: #475569;")
        self.acquisition_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.acquisition_info_label)
        
        return group
        
    def create_probe_selection_group(self):
        """Groupe de sélection des sondes"""
        group = QGroupBox("📡 Sélection des Sondes")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Checkboxes pour chaque sonde
        self.probe_checkboxes = []
        for i in range(8):
            checkbox = QCheckBox(f"Sonde {i+1}")
            checkbox.setFont(QFont("Inter", 11))
            checkbox.setChecked(i < 4)  # Par défaut, 4 premières sondes actives
            checkbox.stateChanged.connect(self.on_probe_selection_changed)
            self.probe_checkboxes.append(checkbox)
            layout.addWidget(checkbox)
            
        # Boutons de sélection rapide
        quick_selection_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Tout sélectionner")
        select_all_btn.setFont(QFont("Inter", 10))
        select_all_btn.clicked.connect(self.select_all_probes)
        
        deselect_all_btn = QPushButton("Tout désélectionner")
        deselect_all_btn.setFont(QFont("Inter", 10))
        deselect_all_btn.clicked.connect(self.deselect_all_probes)
        
        quick_selection_layout.addWidget(select_all_btn)
        quick_selection_layout.addWidget(deselect_all_btn)
        
        layout.addLayout(quick_selection_layout)
        
        return group
        
    def create_realtime_metrics_group(self):
        """Groupe des métriques temps réel"""
        group = QGroupBox("📊 Métriques Statistiques")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        # Métriques pour chaque sonde
        self.metrics_labels = {}
        metrics = ['Hmax', 'Hmin', 'H1/3', 'Hs', 'Tp', 'Tm']
        
        for i, metric in enumerate(metrics):
            # Label de la métrique
            layout.addWidget(QLabel(f"{metric}:"), i, 0)
            
            # Valeur de la métrique
            value_label = QLabel("0.000")
            value_label.setFont(QFont("Inter", 11, QFont.Bold))
            value_label.setStyleSheet("color: #1E40AF;")
            value_label.setAlignment(Qt.AlignRight)
            layout.addWidget(value_label, i, 1)
            
            # Unité
            unit_label = QLabel("cm" if metric.startswith('H') else "s")
            unit_label.setFont(QFont("Inter", 10))
            unit_label.setStyleSheet("color: #64748B;")
            layout.addWidget(unit_label, i, 2)
            
            self.metrics_labels[metric] = value_label
            
        return group
        
    def create_visualization_area(self):
        """Zone de visualisation temps réel"""
        visualization_widget = QWidget()
        visualization_layout = QVBoxLayout(visualization_widget)
        visualization_layout.setSpacing(12)
        
        # Titre de visualisation
        viz_title = QLabel("📈 Visualisation Temps Réel")
        viz_title.setFont(QFont("Inter", 14, QFont.Bold))
        viz_title.setStyleSheet("color: #059669; margin-bottom: 8px;")
        visualization_layout.addWidget(viz_title)
        
        # Splitter vertical pour les graphiques
        charts_splitter = QSplitter(Qt.Vertical)
        
        # Graphiques individuels (haut)
        individual_charts_area = self.create_individual_charts_area()
        charts_splitter.addWidget(individual_charts_area)
        
        # Graphique multi-sondes (bas)
        multi_chart_area = self.create_multi_chart_area()
        charts_splitter.addWidget(multi_chart_area)
        
        # Répartition 60% - 40%
        charts_splitter.setSizes([600, 400])
        visualization_layout.addWidget(charts_splitter)
        
        return visualization_widget
        
    def create_individual_charts_area(self):
        """Zone des graphiques individuels"""
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        
        # Titre des graphiques individuels
        individual_title = QLabel("📊 Graphiques Individuels")
        individual_title.setFont(QFont("Inter", 12, QFont.Bold))
        individual_title.setStyleSheet("color: #1E40AF;")
        charts_layout.addWidget(individual_title)
        
        # Splitter horizontal pour 2 graphiques
        individual_splitter = QSplitter(Qt.Horizontal)
        
        # Graphique Sonde 1
        self.probe1_chart = self.create_probe_chart("Sonde 1", "#059669")
        individual_splitter.addWidget(self.probe1_chart)
        
        # Graphique Sonde 2
        self.probe2_chart = self.create_probe_chart("Sonde 2", "#DC2626")
        individual_splitter.addWidget(self.probe2_chart)
        
        # Répartition 50% - 50%
        individual_splitter.setSizes([500, 500])
        charts_layout.addWidget(individual_splitter)
        
        return charts_widget
        
    def create_multi_chart_area(self):
        """Zone du graphique multi-sondes"""
        multi_widget = QWidget()
        multi_layout = QVBoxLayout(multi_widget)
        
        # Titre du graphique multi-sondes
        multi_title = QLabel("📈 Vue Multi-Sondes")
        multi_title.setFont(QFont("Inter", 12, QFont.Bold))
        multi_title.setStyleSheet("color: #1E40AF;")
        multi_layout.addWidget(multi_title)
        
        # Graphique multi-sondes
        self.multi_chart = self.create_multi_probe_chart()
        multi_layout.addWidget(self.multi_chart)
        
        return multi_widget
        
    def create_probe_chart(self, title, color):
        """Création d'un graphique pour une sonde"""
        chart = QChart()
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Série de données
        series = QLineSeries()
        series.setName(f"Signal {title}")
        series.setColor(QColor(color))
        chart.addSeries(series)
        
        # Axes
        axis_x = QDateTimeAxis()
        axis_x.setTitleText("Temps")
        axis_x.setFormat("HH:mm:ss")
        
        axis_y = QValueAxis()
        axis_y.setTitleText("Amplitude (cm)")
        axis_y.setRange(-5, 15)
        
        chart.setAxisX(axis_x, series)
        chart.setAxisY(axis_y, series)
        
        # Vue du graphique
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("""
            QChartView {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                background: white;
            }
        """)
        
        return chart_view
        
    def create_multi_probe_chart(self):
        """Création du graphique multi-sondes"""
        chart = QChart()
        chart.setTitle("Signaux Multi-Sondes")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Séries pour chaque sonde
        colors = ["#059669", "#DC2626", "#7C3AED", "#D97706", "#3B82F6", "#EC4899", "#10B981", "#F59E0B"]
        
        for i in range(8):
            series = QLineSeries()
            series.setName(f"Sonde {i+1}")
            series.setColor(QColor(colors[i]))
            chart.addSeries(series)
            
        # Axes
        axis_x = QDateTimeAxis()
        axis_x.setTitleText("Temps")
        axis_x.setFormat("HH:mm:ss")
        
        axis_y = QValueAxis()
        axis_y.setTitleText("Amplitude (cm)")
        axis_y.setRange(-5, 15)
        
        # Appliquer les axes à toutes les séries
        for series in chart.series():
            chart.setAxisX(axis_x, series)
            chart.setAxisY(axis_y, series)
            
        # Vue du graphique
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("""
            QChartView {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                background: white;
            }
        """)
        
        return chart_view
        
    def setup_status_bar(self, layout):
        """Barre de statut scientifique"""
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Box)
        status_frame.setLineWidth(1)
        status_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                background: #F8FAFC;
                padding: 4px;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(8, 4, 8, 4)
        
        # Statut général
        self.general_status = QLabel("🔴 Acquisition arrêtée")
        self.general_status.setFont(QFont("Inter", 10))
        self.general_status.setStyleSheet("color: #DC2626;")
        
        # Progression
        self.progress_status = QLabel("Durée: 00:00:00 | Échantillons: 0")
        self.progress_status.setFont(QFont("Inter", 10))
        self.progress_status.setStyleSheet("color: #475569;")
        
        # Heure
        self.time_status = QLabel("")
        self.time_status.setFont(QFont("Inter", 10))
        self.time_status.setStyleSheet("color: #64748B;")
        
        status_layout.addWidget(self.general_status)
        status_layout.addStretch()
        status_layout.addWidget(self.progress_status)
        status_layout.addWidget(self.time_status)
        
        layout.addWidget(status_frame)
        
    def setup_connections(self):
        """Configuration des connexions"""
        # Boutons de contrôle
        self.start_acq_btn.clicked.connect(self.start_acquisition)
        self.stop_acq_btn.clicked.connect(self.stop_acquisition)
        self.pause_acq_btn.clicked.connect(self.pause_acquisition)
        
        # Timer pour mise à jour de l'heure
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        
        # Timer pour simulation des données
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.update_real_time_data)
        
    def apply_scientific_styles(self):
        """Application des styles scientifiques"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: #059669;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                color: #0F172A;
                font-family: 'Inter';
            }
            QPushButton {
                font-family: 'Inter';
                border-radius: 6px;
                padding: 6px 12px;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                font-family: 'Inter';
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                padding: 4px;
                background: white;
            }
            QCheckBox {
                font-family: 'Inter';
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #E2E8F0;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background: #059669;
                border-color: #059669;
            }
        """)
        
    def initialize_data_structures(self):
        """Initialisation des structures de données"""
        self.acquisition_start_time = None
        self.acquisition_duration = timedelta()
        self.sample_count = 0
        
        # Initialisation des données pour chaque sonde
        for i in range(8):
            self.real_time_data[f"probe_{i}"] = {
                'timestamps': [],
                'values': [],
                'max_points': 1000  # Limite pour éviter la surcharge mémoire
            }
            
        # Initialisation des métriques statistiques
        self.statistical_metrics = {
            'Hmax': 0.0,
            'Hmin': 0.0,
            'H1/3': 0.0,
            'Hs': 0.0,
            'Tp': 0.0,
            'Tm': 0.0
        }
        
    # ===== MÉTHODES D'ACQUISITION =====
    
    def start_acquisition(self):
        """Démarrage de l'acquisition"""
        try:
            # Validation des paramètres
            if not self.validate_acquisition_params():
                return
                
            # Mise à jour de l'interface
            self.acquisition_active = True
            self.start_acq_btn.setEnabled(False)
            self.stop_acq_btn.setEnabled(True)
            self.pause_acq_btn.setEnabled(True)
            
            self.acquisition_status_label.setText("🟢 ACQUISITION EN COURS")
            self.acquisition_status_label.setStyleSheet("color: #16A34A;")
            self.general_status.setText("🟢 Acquisition en cours...")
            self.general_status.setStyleSheet("color: #16A34A;")
            
            # Initialisation des données
            self.acquisition_start_time = datetime.now()
            self.sample_count = 0
            self.clear_all_charts()
            
            # Configuration du timer de données
            interval = int(1000 / self.sampling_frequency)  # ms
            self.data_timer.start(interval)
            
            # Émission du signal
            self.acquisition_started.emit()
            
        except Exception as e:
            self.acquisition_error.emit(f"Erreur lors du démarrage: {str(e)}")
            
    def stop_acquisition(self):
        """Arrêt de l'acquisition"""
        self.acquisition_active = False
        self.data_timer.stop()
        
        # Mise à jour de l'interface
        self.start_acq_btn.setEnabled(True)
        self.stop_acq_btn.setEnabled(False)
        self.pause_acq_btn.setEnabled(False)
        
        self.acquisition_status_label.setText("🔴 ACQUISITION ARRÊTÉE")
        self.acquisition_status_label.setStyleSheet("color: #DC2626;")
        self.general_status.setText("🔴 Acquisition arrêtée")
        self.general_status.setStyleSheet("color: #DC2626;")
        
        # Calcul de la durée totale
        if self.acquisition_start_time:
            self.acquisition_duration = datetime.now() - self.acquisition_start_time
            
        # Émission du signal
        self.acquisition_stopped.emit()
        
        # Sauvegarde automatique
        self.auto_save_acquisition_data()
        
    def pause_acquisition(self):
        """Pause de l'acquisition"""
        if self.data_timer.isActive():
            self.data_timer.stop()
            self.pause_acq_btn.setText("▶️ Reprendre")
            self.general_status.setText("⏸️ Acquisition en pause")
            self.general_status.setStyleSheet("color: #D97706;")
        else:
            interval = int(1000 / self.sampling_frequency)
            self.data_timer.start(interval)
            self.pause_acq_btn.setText("⏸️ Pause")
            self.general_status.setText("🟢 Acquisition en cours...")
            self.general_status.setStyleSheet("color: #16A34A;")
            
    def validate_acquisition_params(self):
        """Validation des paramètres d'acquisition"""
        if self.frequency_spin.value() < 1:
            QMessageBox.warning(self, "Erreur", "La fréquence doit être au moins 1 Hz")
            return False
            
        if self.cycle_spin.value() <= 0:
            QMessageBox.warning(self, "Erreur", "Le cycle doit être positif")
            return False
            
        # Vérifier qu'au moins une sonde est sélectionnée
        active_probes = [i for i, cb in enumerate(self.probe_checkboxes) if cb.isChecked()]
        if not active_probes:
            QMessageBox.warning(self, "Erreur", "Au moins une sonde doit être sélectionnée")
            return False
            
        return True
        
    def update_real_time_data(self):
        """Mise à jour des données temps réel"""
        if not self.acquisition_active:
            return
            
        current_time = datetime.now()
        self.sample_count += 1
        
        # Génération de données simulées pour chaque sonde active
        active_probes = [i for i, cb in enumerate(self.probe_checkboxes) if cb.isChecked()]
        
        for probe_id in active_probes:
            # Simulation d'un signal de houle
            time_factor = current_time.timestamp() * 0.1
            base_amplitude = 5.0  # cm
            wave_frequency = 0.5  # Hz
            noise_level = 0.2     # cm
            
            # Signal principal + bruit
            signal_value = base_amplitude * np.sin(2 * np.pi * wave_frequency * time_factor + probe_id * np.pi/4)
            noise = np.random.normal(0, noise_level)
            final_value = signal_value + noise
            
            # Ajout des données
            self.add_data_point(probe_id, current_time, final_value)
            
        # Mise à jour des graphiques
        self.update_all_charts()
        
        # Mise à jour des métriques statistiques
        self.update_statistical_metrics()
        
        # Mise à jour de la progression
        self.update_acquisition_progress()
        
        # Émission du signal de données
        self.data_updated.emit(self.real_time_data)
        
    def add_data_point(self, probe_id, timestamp, value):
        """Ajout d'un point de données pour une sonde"""
        probe_data = self.real_time_data[f"probe_{probe_id}"]
        
        # Ajout des nouvelles données
        probe_data['timestamps'].append(timestamp)
        probe_data['values'].append(value)
        
        # Limitation du nombre de points pour éviter la surcharge mémoire
        if len(probe_data['timestamps']) > probe_data['max_points']:
            probe_data['timestamps'] = probe_data['timestamps'][-probe_data['max_points']:]
            probe_data['values'] = probe_data['values'][-probe_data['max_points']:]
            
    def update_all_charts(self):
        """Mise à jour de tous les graphiques"""
        # Mise à jour des graphiques individuels
        self.update_probe_chart(self.probe1_chart, 0)
        self.update_probe_chart(self.probe2_chart, 1)
        
        # Mise à jour du graphique multi-sondes
        self.update_multi_chart()
        
    def update_probe_chart(self, chart_view, probe_id):
        """Mise à jour d'un graphique de sonde individuelle"""
        if not self.real_time_data[f"probe_{probe_id}"]['timestamps']:
            return
            
        chart = chart_view.chart()
        series = chart.series()[0] if chart.series() else None
        
        if series:
            # Nettoyer la série
            series.clear()
            
            # Ajouter les points
            probe_data = self.real_time_data[f"probe_{probe_id}"]
            for i, (timestamp, value) in enumerate(zip(probe_data['timestamps'], probe_data['values'])):
                series.append(timestamp.toMSecsSinceEpoch(), value)
                
            # Ajuster les axes
            if probe_data['timestamps']:
                min_time = probe_data['timestamps'][0].toMSecsSinceEpoch()
                max_time = probe_data['timestamps'][-1].toMSecsSinceEpoch()
                
                axis_x = chart.axisX()
                axis_x.setRange(min_time, max_time)
                
                axis_y = chart.axisY()
                values = probe_data['values']
                if values:
                    min_val = min(values)
                    max_val = max(values)
                    margin = (max_val - min_val) * 0.1
                    axis_y.setRange(min_val - margin, max_val + margin)
                    
    def update_multi_chart(self):
        """Mise à jour du graphique multi-sondes"""
        chart = self.multi_chart.chart()
        
        # Mettre à jour chaque série
        for i, series in enumerate(chart.series()):
            if i < 8:  # Limite à 8 sondes
                probe_data = self.real_time_data[f"probe_{i}"]
                
                # Nettoyer la série
                series.clear()
                
                # Ajouter les points
                for timestamp, value in zip(probe_data['timestamps'], probe_data['values']):
                    series.append(timestamp.toMSecsSinceEpoch(), value)
                    
        # Ajuster les axes si nécessaire
        if chart.series():
            all_timestamps = []
            all_values = []
            
            for probe_data in self.real_time_data.values():
                all_timestamps.extend(probe_data['timestamps'])
                all_values.extend(probe_data['values'])
                
            if all_timestamps and all_values:
                min_time = min(all_timestamps).toMSecsSinceEpoch()
                max_time = max(all_timestamps).toMSecsSinceEpoch()
                
                axis_x = chart.axisX()
                axis_x.setRange(min_time, max_time)
                
                axis_y = chart.axisY()
                min_val = min(all_values)
                max_val = max(all_values)
                margin = (max_val - min_val) * 0.1
                axis_y.setRange(min_val - margin, max_val + margin)
                
    def update_statistical_metrics(self):
        """Mise à jour des métriques statistiques"""
        # Calcul des métriques pour toutes les sondes actives
        all_values = []
        active_probes = [i for i, cb in enumerate(self.probe_checkboxes) if cb.isChecked()]
        
        for probe_id in active_probes:
            probe_data = self.real_time_data[f"probe_{probe_id}"]
            if probe_data['values']:
                all_values.extend(probe_data['values'])
                
        if all_values:
            # Calcul des métriques
            self.statistical_metrics['Hmax'] = max(all_values)
            self.statistical_metrics['Hmin'] = min(all_values)
            
            # H1/3 (hauteur significative - 1/3 des plus grandes vagues)
            sorted_values = sorted(all_values, reverse=True)
            third_count = max(1, len(sorted_values) // 3)
            self.statistical_metrics['H1/3'] = np.mean(sorted_values[:third_count])
            
            # Hs (hauteur significative spectrale)
            self.statistical_metrics['Hs'] = 4 * np.std(all_values)
            
            # Tp et Tm (périodes - simulation)
            self.statistical_metrics['Tp'] = 2.0 + np.random.normal(0, 0.1)
            self.statistical_metrics['Tm'] = 1.5 + np.random.normal(0, 0.1)
            
            # Mise à jour des labels
            for metric, value in self.statistical_metrics.items():
                if metric in self.metrics_labels:
                    self.metrics_labels[metric].setText(f"{value:.3f}")
                    
    def update_acquisition_progress(self):
        """Mise à jour de la progression d'acquisition"""
        if self.acquisition_start_time:
            elapsed = datetime.now() - self.acquisition_start_time
            total_duration = timedelta(minutes=self.duration_spin.value())
            
            # Progression en pourcentage
            progress_percent = min(100, (elapsed.total_seconds() / total_duration.total_seconds()) * 100)
            self.acquisition_progress.setValue(int(progress_percent))
            
            # Informations de progression
            elapsed_str = str(elapsed).split('.')[0]  # Sans microsecondes
            self.progress_status.setText(f"Durée: {elapsed_str} | Échantillons: {self.sample_count}")
            
            # Arrêt automatique si durée atteinte
            if elapsed >= total_duration:
                self.stop_acquisition()
                
    def clear_all_charts(self):
        """Effacement de tous les graphiques"""
        # Effacer les graphiques individuels
        for chart_view in [self.probe1_chart, self.probe2_chart]:
            chart = chart_view.chart()
            for series in chart.series():
                series.clear()
                
        # Effacer le graphique multi-sondes
        chart = self.multi_chart.chart()
        for series in chart.series():
            series.clear()
            
    def auto_save_acquisition_data(self):
        """Sauvegarde automatique des données d'acquisition"""
        if not self.real_time_data:
            return
            
        # Créer le nom de fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"acquisition_data_{timestamp}.json"
        
        # Préparer les données pour sauvegarde
        save_data = {
            'metadata': {
                'timestamp': timestamp,
                'duration': str(self.acquisition_duration),
                'sample_count': self.sample_count,
                'sampling_frequency': self.sampling_frequency,
                'active_probes': [i for i, cb in enumerate(self.probe_checkboxes) if cb.isChecked()]
            },
            'statistical_metrics': self.statistical_metrics,
            'acquisition_data': {}
        }
        
        # Convertir les données de chaque sonde
        for probe_id, probe_data in self.real_time_data.items():
            save_data['acquisition_data'][probe_id] = {
                'timestamps': [ts.isoformat() for ts in probe_data['timestamps']],
                'values': probe_data['values']
            }
            
        # Sauvegarder
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
                
            self.acquisition_info_label.setText(f"Données sauvegardées: {filename}")
            
        except Exception as e:
            self.acquisition_error.emit(f"Erreur lors de la sauvegarde: {str(e)}")
            
    # ===== MÉTHODES D'INTERFACE =====
    
    def on_frequency_changed(self, value):
        """Changement de fréquence d'échantillonnage"""
        self.sampling_frequency = value
        if self.data_timer.isActive():
            interval = int(1000 / value)
            self.data_timer.start(interval)
            
    def on_cycle_changed(self, value):
        """Changement du cycle de temps"""
        self.cycle_time = value
        
    def on_probe_selection_changed(self):
        """Changement de sélection des sondes"""
        active_probes = [i for i, cb in enumerate(self.probe_checkboxes) if cb.isChecked()]
        self.active_probes = active_probes
        
        # Mise à jour des informations
        probe_info = f"Projet: [Nom Projet] | Sondes: {len(active_probes)}/8 | Fréquence: {self.sampling_frequency} Hz"
        # Note: Il faudrait mettre à jour le label project_info ici
        
    def select_all_probes(self):
        """Sélectionner toutes les sondes"""
        for checkbox in self.probe_checkboxes:
            checkbox.setChecked(True)
            
    def deselect_all_probes(self):
        """Désélectionner toutes les sondes"""
        for checkbox in self.probe_checkboxes:
            checkbox.setChecked(False)
            
    def update_time(self):
        """Mise à jour de l'heure"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_status.setText(f"Heure: {current_time}")
        
    def save_acquisition_data(self):
        """Sauvegarde manuelle des données d'acquisition"""
        if not self.real_time_data:
            QMessageBox.warning(self, "Erreur", "Aucune donnée d'acquisition à sauvegarder")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder les données d'acquisition",
            "",
            "Fichiers JSON (*.json);;Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.save_as_csv(file_path)
                else:
                    self.save_as_json(file_path)
                    
                QMessageBox.information(self, "Succès", f"Données sauvegardées dans {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
                
    def save_as_json(self, file_path):
        """Sauvegarde au format JSON"""
        save_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'duration': str(self.acquisition_duration),
                'sample_count': self.sample_count,
                'sampling_frequency': self.sampling_frequency,
                'active_probes': self.active_probes
            },
            'statistical_metrics': self.statistical_metrics,
            'acquisition_data': {}
        }
        
        for probe_id, probe_data in self.real_time_data.items():
            save_data['acquisition_data'][probe_id] = {
                'timestamps': [ts.isoformat() for ts in probe_data['timestamps']],
                'values': probe_data['values']
            }
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
            
    def save_as_csv(self, file_path):
        """Sauvegarde au format CSV"""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # En-tête
            header = ['Timestamp']
            active_probes = [i for i, cb in enumerate(self.probe_checkboxes) if cb.isChecked()]
            for probe_id in active_probes:
                header.append(f'Sonde_{probe_id+1}')
            writer.writerow(header)
            
            # Données
            # Trouver le nombre maximum de points
            max_points = max(len(self.real_time_data[f"probe_{i}"]['timestamps']) for i in active_probes)
            
            for i in range(max_points):
                row = []
                if i < len(self.real_time_data[f"probe_0"]['timestamps']):
                    row.append(self.real_time_data[f"probe_0"]['timestamps'][i].isoformat())
                else:
                    row.append("")
                    
                for probe_id in active_probes:
                    probe_data = self.real_time_data[f"probe_{probe_id}"]
                    if i < len(probe_data['values']):
                        row.append(str(probe_data['values'][i]))
                    else:
                        row.append("")
                        
                writer.writerow(row)