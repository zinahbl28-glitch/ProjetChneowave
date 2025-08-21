"""
Module de Calibration Scientifique - Interface Complète
Calibration précise des sondes d'élévation d'eau et de pression
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QGroupBox, QPushButton, QSpinBox, QDoubleSpinBox, QComboBox,
    QProgressBar, QTableWidget, QTableWidgetItem, QTextEdit,
    QSplitter, QScrollArea, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread, pyqtSignal
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

import numpy as np
import json
import os
from datetime import datetime


class ScientificCalibrationPanel(QWidget):
    """Interface scientifique complète pour calibration des sondes"""
    
    # Signaux
    calibration_completed = Signal(dict)  # Résultats de calibration
    calibration_error = Signal(str)       # Erreur de calibration
    probe_status_changed = Signal(int, str)  # Statut sonde (id, status)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.calibration_data = {}
        self.current_probe = 0
        self.calibration_points = []
        
        self.setup_ui()
        self.setup_connections()
        self.apply_scientific_styles()
        
    def setup_ui(self):
        """Configuration de l'interface scientifique"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # En-tête scientifique
        self.setup_scientific_header(main_layout)
        
        # Zone principale avec splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Panneau de contrôle (gauche)
        control_panel = self.create_control_panel()
        main_splitter.addWidget(control_panel)
        
        # Zone de travail (droite)
        work_area = self.create_work_area()
        main_splitter.addWidget(work_area)
        
        # Répartition 40% - 60%
        main_splitter.setSizes([400, 600])
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
                border: 2px solid #1E40AF;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F8FAFC, stop:1 #E2E8F0);
                padding: 8px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Titre principal
        title_label = QLabel("⚙️ CALIBRATION SCIENTIFIQUE")
        title_label.setFont(QFont("Inter", 16, QFont.Bold))
        title_label.setStyleSheet("color: #1E40AF;")
        
        # Informations projet
        project_info = QLabel("Projet: [Nom Projet] | Sondes: 0/8 | État: Prêt")
        project_info.setFont(QFont("Inter", 12))
        project_info.setStyleSheet("color: #475569;")
        
        # Statut global
        status_label = QLabel("🟢 SYSTÈME PRÊT")
        status_label.setFont(QFont("Inter", 12, QFont.Bold))
        status_label.setStyleSheet("color: #16A34A;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(project_info)
        header_layout.addWidget(status_label)
        
        layout.addWidget(header_frame)
        
    def create_control_panel(self):
        """Panneau de contrôle scientifique"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setSpacing(12)
        
        # 1. Configuration des sondes
        probe_config_group = self.create_probe_config_group()
        control_layout.addWidget(probe_config_group)
        
        # 2. Paramètres de calibration
        calib_params_group = self.create_calibration_params_group()
        control_layout.addWidget(calib_params_group)
        
        # 3. Contrôles de calibration
        calib_controls_group = self.create_calibration_controls_group()
        control_layout.addWidget(calib_controls_group)
        
        # 4. Sélection de sonde active
        active_probe_group = self.create_active_probe_group()
        control_layout.addWidget(active_probe_group)
        
        # 5. Points de calibration
        calibration_points_group = self.create_calibration_points_group()
        control_layout.addWidget(calibration_points_group)
        
        control_layout.addStretch()
        
        return control_widget
        
    def create_probe_config_group(self):
        """Groupe de configuration des sondes"""
        group = QGroupBox("📡 Configuration des Sondes")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        # Nombre de sondes
        layout.addWidget(QLabel("Nombre de sondes:"), 0, 0)
        self.probe_count_spin = QSpinBox()
        self.probe_count_spin.setRange(1, 8)
        self.probe_count_spin.setValue(4)
        self.probe_count_spin.setFont(QFont("Inter", 11))
        layout.addWidget(self.probe_count_spin, 0, 1)
        
        # Type de sonde
        layout.addWidget(QLabel("Type de sonde:"), 1, 0)
        self.probe_type_combo = QComboBox()
        self.probe_type_combo.addItems(["Élévation d'eau", "Pression", "Mixte"])
        self.probe_type_combo.setFont(QFont("Inter", 11))
        layout.addWidget(self.probe_type_combo, 1, 1)
        
        # Échelle de mesure
        layout.addWidget(QLabel("Échelle:"), 2, 0)
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["Centimètres (cm)", "Millimètres (mm)"])
        self.scale_combo.setFont(QFont("Inter", 11))
        layout.addWidget(self.scale_combo, 2, 1)
        
        return group
        
    def create_calibration_params_group(self):
        """Groupe des paramètres de calibration"""
        group = QGroupBox("⚙️ Paramètres de Calibration")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        # Nombre de points par sonde
        layout.addWidget(QLabel("Points par sonde:"), 0, 0)
        self.points_per_probe_spin = QSpinBox()
        self.points_per_probe_spin.setRange(3, 10)
        self.points_per_probe_spin.setValue(5)
        self.points_per_probe_spin.setFont(QFont("Inter", 11))
        layout.addWidget(self.points_per_probe_spin, 0, 1)
        
        # Tolérance de linéarité
        layout.addWidget(QLabel("Tolérance (%):"), 1, 0)
        self.tolerance_spin = QDoubleSpinBox()
        self.tolerance_spin.setRange(0.1, 5.0)
        self.tolerance_spin.setValue(1.0)
        self.tolerance_spin.setSuffix(" %")
        self.tolerance_spin.setFont(QFont("Inter", 11))
        layout.addWidget(self.tolerance_spin, 1, 1)
        
        # Temps de stabilisation
        layout.addWidget(QLabel("Stabilisation (s):"), 2, 0)
        self.stabilization_spin = QSpinBox()
        self.stabilization_spin.setRange(1, 30)
        self.stabilization_spin.setValue(3)
        self.stabilization_spin.setFont(QFont("Inter", 11))
        layout.addWidget(self.stabilization_spin, 2, 1)
        
        return group
        
    def create_calibration_controls_group(self):
        """Groupe des contrôles de calibration"""
        group = QGroupBox("🎛️ Contrôles de Calibration")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Boutons de contrôle
        button_layout = QHBoxLayout()
        
        self.start_calib_btn = QPushButton("🚀 Démarrer Calibration")
        self.start_calib_btn.setFont(QFont("Inter", 11, QFont.Bold))
        self.start_calib_btn.setStyleSheet("""
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
        
        self.stop_calib_btn = QPushButton("⏹️ Arrêter")
        self.stop_calib_btn.setFont(QFont("Inter", 11))
        self.stop_calib_btn.setStyleSheet("""
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
        self.stop_calib_btn.setEnabled(False)
        
        self.reset_calib_btn = QPushButton("🔄 Réinitialiser")
        self.reset_calib_btn.setFont(QFont("Inter", 11))
        self.reset_calib_btn.setStyleSheet("""
            QPushButton {
                background: #7C3AED;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #6D28D9;
            }
        """)
        
        button_layout.addWidget(self.start_calib_btn)
        button_layout.addWidget(self.stop_calib_btn)
        button_layout.addWidget(self.reset_calib_btn)
        
        layout.addLayout(button_layout)
        
        # Barre de progression
        self.calibration_progress = QProgressBar()
        self.calibration_progress.setFont(QFont("Inter", 10))
        self.calibration_progress.setStyleSheet("""
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
        layout.addWidget(self.calibration_progress)
        
        return group
        
    def create_active_probe_group(self):
        """Groupe de sélection de sonde active"""
        group = QGroupBox("🎯 Sonde Active")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Sélecteur de sonde
        probe_layout = QHBoxLayout()
        probe_layout.addWidget(QLabel("Sonde:"))
        
        self.active_probe_combo = QComboBox()
        self.active_probe_combo.setFont(QFont("Inter", 11, QFont.Bold))
        self.active_probe_combo.addItems([f"Sonde {i+1}" for i in range(8)])
        self.active_probe_combo.currentIndexChanged.connect(self.on_probe_changed)
        probe_layout.addWidget(self.active_probe_combo)
        
        layout.addLayout(probe_layout)
        
        # Statut de la sonde
        self.probe_status_label = QLabel("🟡 En attente de calibration")
        self.probe_status_label.setFont(QFont("Inter", 11))
        self.probe_status_label.setStyleSheet("color: #D97706;")
        self.probe_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.probe_status_label)
        
        return group
        
    def create_calibration_points_group(self):
        """Groupe des points de calibration"""
        group = QGroupBox("📊 Points de Calibration")
        group.setFont(QFont("Inter", 12, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Tableau des points
        self.points_table = QTableWidget()
        self.points_table.setColumnCount(3)
        self.points_table.setHorizontalHeaderLabels(["Point", "Valeur (cm)", "Tension (V)"])
        self.points_table.setFont(QFont("Inter", 10))
        self.points_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                background: white;
                gridline-color: #F1F5F9;
            }
            QHeaderView::section {
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                padding: 4px;
                font-weight: bold;
            }
        """)
        
        # Initialiser avec les points par défaut
        self.update_calibration_points()
        
        layout.addWidget(self.points_table)
        
        # Boutons de points
        points_buttons_layout = QHBoxLayout()
        
        self.add_point_btn = QPushButton("➕ Ajouter Point")
        self.add_point_btn.setFont(QFont("Inter", 10))
        self.add_point_btn.clicked.connect(self.add_calibration_point)
        
        self.remove_point_btn = QPushButton("➖ Supprimer")
        self.remove_point_btn.setFont(QFont("Inter", 10))
        self.remove_point_btn.clicked.connect(self.remove_calibration_point)
        
        points_buttons_layout.addWidget(self.add_point_btn)
        points_buttons_layout.addWidget(self.remove_point_btn)
        
        layout.addLayout(points_buttons_layout)
        
        return group
        
    def create_work_area(self):
        """Zone de travail principale"""
        work_widget = QWidget()
        work_layout = QVBoxLayout(work_widget)
        work_layout.setSpacing(12)
        
        # Splitter vertical pour graphiques et validation
        work_splitter = QSplitter(Qt.Vertical)
        
        # Zone des graphiques
        charts_area = self.create_charts_area()
        work_splitter.addWidget(charts_area)
        
        # Zone de validation
        validation_area = self.create_validation_area()
        work_splitter.addWidget(validation_area)
        
        # Répartition 70% - 30%
        work_splitter.setSizes([700, 300])
        work_layout.addWidget(work_splitter)
        
        return work_widget
        
    def create_charts_area(self):
        """Zone des graphiques de calibration"""
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        
        # Titre des graphiques
        charts_title = QLabel("📈 Graphiques de Calibration")
        charts_title.setFont(QFont("Inter", 14, QFont.Bold))
        charts_title.setStyleSheet("color: #1E40AF; margin-bottom: 8px;")
        charts_layout.addWidget(charts_title)
        
        # Graphique principal
        self.calibration_chart = QChart()
        self.calibration_chart.setTitle("Courbe de Calibration - Linéarité")
        self.calibration_chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        chart_view = QChartView(self.calibration_chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("""
            QChartView {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                background: white;
            }
        """)
        
        charts_layout.addWidget(chart_view)
        
        return charts_widget
        
    def create_validation_area(self):
        """Zone de validation scientifique"""
        validation_widget = QWidget()
        validation_layout = QVBoxLayout(validation_widget)
        
        # Titre de validation
        validation_title = QLabel("✅ Validation Scientifique")
        validation_title.setFont(QFont("Inter", 14, QFont.Bold))
        validation_title.setStyleSheet("color: #059669; margin-bottom: 8px;")
        validation_layout.addWidget(validation_title)
        
        # Métriques de validation
        metrics_layout = QGridLayout()
        
        # Coefficient de corrélation
        metrics_layout.addWidget(QLabel("Coefficient R²:"), 0, 0)
        self.r_squared_label = QLabel("0.000")
        self.r_squared_label.setFont(QFont("Inter", 12, QFont.Bold))
        self.r_squared_label.setStyleSheet("color: #1E40AF;")
        metrics_layout.addWidget(self.r_squared_label, 0, 1)
        
        # Écart type
        metrics_layout.addWidget(QLabel("Écart type:"), 1, 0)
        self.std_dev_label = QLabel("0.000")
        self.std_dev_label.setFont(QFont("Inter", 12, QFont.Bold))
        self.std_dev_label.setStyleSheet("color: #1E40AF;")
        metrics_layout.addWidget(self.std_dev_label, 1, 1)
        
        # Linéarité
        metrics_layout.addWidget(QLabel("Linéarité:"), 2, 0)
        self.linearity_label = QLabel("Non calculé")
        self.linearity_label.setFont(QFont("Inter", 12, QFont.Bold))
        self.linearity_label.setStyleSheet("color: #D97706;")
        metrics_layout.addWidget(self.linearity_label, 2, 1)
        
        validation_layout.addLayout(metrics_layout)
        
        # Zone de rapport
        self.validation_report = QTextEdit()
        self.validation_report.setFont(QFont("Inter", 10))
        self.validation_report.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                background: #F8FAFC;
                padding: 8px;
            }
        """)
        self.validation_report.setMaximumHeight(120)
        self.validation_report.setPlaceholderText("Rapport de validation de calibration...")
        
        validation_layout.addWidget(self.validation_report)
        
        return validation_widget
        
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
        self.general_status = QLabel("🟢 Système prêt pour calibration")
        self.general_status.setFont(QFont("Inter", 10))
        self.general_status.setStyleSheet("color: #16A34A;")
        
        # Progression
        self.progress_status = QLabel("Progression: 0/0 sondes calibrées")
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
        self.start_calib_btn.clicked.connect(self.start_calibration)
        self.stop_calib_btn.clicked.connect(self.stop_calibration)
        self.reset_calib_btn.clicked.connect(self.reset_calibration)
        
        # Changements de paramètres
        self.probe_count_spin.valueChanged.connect(self.on_probe_count_changed)
        self.points_per_probe_spin.valueChanged.connect(self.update_calibration_points)
        
        # Timer pour mise à jour de l'heure
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        
    def apply_scientific_styles(self):
        """Application des styles scientifiques"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: #1E40AF;
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
        """)
        
    # ===== MÉTHODES DE CALIBRATION =====
    
    def start_calibration(self):
        """Démarrage de la calibration"""
        try:
            # Validation des paramètres
            if not self.validate_calibration_params():
                return
                
            # Mise à jour de l'interface
            self.start_calib_btn.setEnabled(False)
            self.stop_calib_btn.setEnabled(True)
            self.general_status.setText("🟡 Calibration en cours...")
            self.general_status.setStyleSheet("color: #D97706;")
            
            # Initialisation des données
            self.calibration_data = {}
            self.current_probe = 0
            
            # Configuration de la progression
            total_probes = self.probe_count_spin.value()
            self.calibration_progress.setMaximum(total_probes)
            self.calibration_progress.setValue(0)
            
            # Démarrage du processus
            self.start_probe_calibration()
            
        except Exception as e:
            self.calibration_error.emit(f"Erreur lors du démarrage: {str(e)}")
            
    def stop_calibration(self):
        """Arrêt de la calibration"""
        self.start_calib_btn.setEnabled(True)
        self.stop_calib_btn.setEnabled(False)
        self.general_status.setText("🔴 Calibration arrêtée")
        self.general_status.setStyleSheet("color: #DC2626;")
        
    def reset_calibration(self):
        """Réinitialisation de la calibration"""
        reply = QMessageBox.question(
            self, "Réinitialisation",
            "Voulez-vous réinitialiser toutes les données de calibration ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.calibration_data = {}
            self.current_probe = 0
            self.calibration_progress.setValue(0)
            self.clear_calibration_chart()
            self.reset_validation_metrics()
            self.general_status.setText("🟢 Système prêt pour calibration")
            self.general_status.setStyleSheet("color: #16A34A;")
            
    def validate_calibration_params(self):
        """Validation des paramètres de calibration"""
        if self.probe_count_spin.value() < 1:
            QMessageBox.warning(self, "Erreur", "Le nombre de sondes doit être au moins 1")
            return False
            
        if self.points_per_probe_spin.value() < 3:
            QMessageBox.warning(self, "Erreur", "Le nombre de points doit être au moins 3")
            return False
            
        return True
        
    def start_probe_calibration(self):
        """Démarrage de la calibration d'une sonde"""
        if self.current_probe >= self.probe_count_spin.value():
            self.complete_calibration()
            return
            
        # Mise à jour de l'interface
        probe_name = f"Sonde {self.current_probe + 1}"
        self.active_probe_combo.setCurrentIndex(self.current_probe)
        self.probe_status_label.setText(f"🟡 Calibration de {probe_name} en cours...")
        self.probe_status_label.setStyleSheet("color: #D97706;")
        
        # Initialisation des données pour cette sonde
        self.calibration_data[f"probe_{self.current_probe}"] = {
            'name': probe_name,
            'points': [],
            'status': 'calibrating'
        }
        
        # Simulation de la calibration (remplacer par vraie logique)
        self.simulate_probe_calibration()
        
    def simulate_probe_calibration(self):
        """Simulation de la calibration d'une sonde"""
        # Simulation des points de calibration
        points = self.points_per_probe_spin.value()
        probe_data = self.calibration_data[f"probe_{self.current_probe}"]
        
        for i in range(points):
            # Simulation des valeurs (remplacer par vraies mesures)
            height = i * 1.0  # cm
            voltage = height * 0.5 + np.random.normal(0, 0.02)  # V avec bruit
            
            probe_data['points'].append({
                'point': i + 1,
                'height': height,
                'voltage': voltage,
                'timestamp': datetime.now().isoformat()
            })
            
        # Validation de la calibration
        self.validate_probe_calibration()
        
    def validate_probe_calibration(self):
        """Validation de la calibration d'une sonde"""
        probe_data = self.calibration_data[f"probe_{self.current_probe}"]
        points = probe_data['points']
        
        if len(points) < 3:
            probe_data['status'] = 'failed'
            self.probe_status_changed.emit(self.current_probe, 'failed')
            return
            
        # Calcul des métriques
        heights = [p['height'] for p in points]
        voltages = [p['voltage'] for p in points]
        
        # Régression linéaire
        coeffs = np.polyfit(heights, voltages, 1)
        r_squared = self.calculate_r_squared(heights, voltages, coeffs)
        
        # Validation
        if r_squared >= 0.99:  # 99% de corrélation
            probe_data['status'] = 'validated'
            probe_data['r_squared'] = r_squared
            probe_data['coefficients'] = coeffs.tolist()
            
            self.probe_status_label.setText(f"✅ {probe_data['name']} validée (R²={r_squared:.3f})")
            self.probe_status_label.setStyleSheet("color: #16A34A;")
        else:
            probe_data['status'] = 'failed'
            self.probe_status_label.setText(f"❌ {probe_data['name']} échouée (R²={r_squared:.3f})")
            self.probe_status_label.setStyleSheet("color: #DC2626;")
            
        # Mise à jour du graphique
        self.update_calibration_chart()
        
        # Passage à la sonde suivante
        self.current_probe += 1
        self.calibration_progress.setValue(self.current_probe)
        
        # Délai avant sonde suivante
        QTimer.singleShot(2000, self.start_probe_calibration)
        
    def calculate_r_squared(self, x, y, coeffs):
        """Calcul du coefficient de détermination R²"""
        y_pred = np.polyval(coeffs, x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
    def complete_calibration(self):
        """Finalisation de la calibration"""
        self.start_calib_btn.setEnabled(True)
        self.stop_calib_btn.setEnabled(False)
        
        # Calcul des statistiques globales
        validated_probes = sum(1 for p in self.calibration_data.values() if p['status'] == 'validated')
        total_probes = len(self.calibration_data)
        
        if validated_probes == total_probes:
            self.general_status.setText(f"✅ Calibration terminée - {validated_probes}/{total_probes} sondes validées")
            self.general_status.setStyleSheet("color: #16A34A;")
        else:
            self.general_status.setText(f"⚠️ Calibration terminée - {validated_probes}/{total_probes} sondes validées")
            self.general_status.setStyleSheet("color: #D97706;")
            
        # Génération du rapport
        self.generate_calibration_report()
        
        # Émission du signal de completion
        self.calibration_completed.emit(self.calibration_data)
        
    def generate_calibration_report(self):
        """Génération du rapport de calibration"""
        report = "=== RAPPORT DE CALIBRATION ===\n\n"
        
        for probe_id, probe_data in self.calibration_data.items():
            report += f"Sonde: {probe_data['name']}\n"
            report += f"Statut: {probe_data['status']}\n"
            
            if 'r_squared' in probe_data:
                report += f"Coefficient R²: {probe_data['r_squared']:.3f}\n"
                report += f"Coefficients: {probe_data['coefficients']}\n"
                
            report += f"Points calibrés: {len(probe_data['points'])}\n"
            report += "-" * 30 + "\n"
            
        self.validation_report.setText(report)
        
    # ===== MÉTHODES D'INTERFACE =====
    
    def on_probe_changed(self, index):
        """Changement de sonde active"""
        self.current_probe = index
        self.update_calibration_chart()
        
    def on_probe_count_changed(self, value):
        """Changement du nombre de sondes"""
        self.active_probe_combo.clear()
        self.active_probe_combo.addItems([f"Sonde {i+1}" for i in range(value)])
        
    def update_calibration_points(self):
        """Mise à jour des points de calibration"""
        points = self.points_per_probe_spin.value()
        self.points_table.setRowCount(points)
        
        # Points par défaut
        default_points = [0, 1, 2, 3, 5, 7, 10, 15, 20, 25]
        
        for i in range(points):
            # Point
            point_item = QTableWidgetItem(f"Point {i+1}")
            point_item.setFlags(point_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.points_table.setItem(i, 0, point_item)
            
            # Valeur (cm)
            value_item = QTableWidgetItem(str(default_points[i] if i < len(default_points) else i))
            self.points_table.setItem(i, 1, value_item)
            
            # Tension (V) - vide pour remplissage
            voltage_item = QTableWidgetItem("")
            self.points_table.setItem(i, 2, voltage_item)
            
    def add_calibration_point(self):
        """Ajout d'un point de calibration"""
        current_rows = self.points_table.rowCount()
        self.points_table.setRowCount(current_rows + 1)
        
        # Nouveau point
        point_item = QTableWidgetItem(f"Point {current_rows + 1}")
        point_item.setFlags(point_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.points_table.setItem(current_rows, 0, point_item)
        
        # Valeur vide
        value_item = QTableWidgetItem("")
        self.points_table.setItem(current_rows, 1, value_item)
        
        # Tension vide
        voltage_item = QTableWidgetItem("")
        self.points_table.setItem(current_rows, 2, voltage_item)
        
    def remove_calibration_point(self):
        """Suppression d'un point de calibration"""
        current_row = self.points_table.currentRow()
        if current_row >= 0:
            self.points_table.removeRow(current_row)
            
    def update_calibration_chart(self):
        """Mise à jour du graphique de calibration"""
        self.calibration_chart.removeAllSeries()
        
        # Série pour la sonde active
        if f"probe_{self.current_probe}" in self.calibration_data:
            probe_data = self.calibration_data[f"probe_{self.current_probe}"]
            
            if probe_data['points']:
                series = QLineSeries()
                series.setName(f"Calibration {probe_data['name']}")
                
                for point in probe_data['points']:
                    series.append(point['height'], point['voltage'])
                    
                self.calibration_chart.addSeries(series)
                
                # Axes
                axis_x = QValueAxis()
                axis_x.setTitleText("Hauteur (cm)")
                axis_x.setRange(0, max(p['height'] for p in probe_data['points']) + 1)
                
                axis_y = QValueAxis()
                axis_y.setTitleText("Tension (V)")
                axis_y.setRange(0, max(p['voltage'] for p in probe_data['points']) + 0.1)
                
                self.calibration_chart.setAxisX(axis_x, series)
                self.calibration_chart.setAxisY(axis_y, series)
                
    def clear_calibration_chart(self):
        """Effacement du graphique de calibration"""
        self.calibration_chart.removeAllSeries()
        
    def reset_validation_metrics(self):
        """Réinitialisation des métriques de validation"""
        self.r_squared_label.setText("0.000")
        self.std_dev_label.setText("0.000")
        self.linearity_label.setText("Non calculé")
        self.linearity_label.setStyleSheet("color: #D97706;")
        self.validation_report.clear()
        
    def update_time(self):
        """Mise à jour de l'heure"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_status.setText(f"Heure: {current_time}")
        
    def update_progress_status(self):
        """Mise à jour du statut de progression"""
        validated = sum(1 for p in self.calibration_data.values() if p['status'] == 'validated')
        total = len(self.calibration_data) if self.calibration_data else 0
        self.progress_status.setText(f"Progression: {validated}/{total} sondes calibrées")
        
    def save_calibration_data(self):
        """Sauvegarde des données de calibration"""
        if not self.calibration_data:
            QMessageBox.warning(self, "Erreur", "Aucune donnée de calibration à sauvegarder")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder les données de calibration",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.calibration_data, f, indent=2, ensure_ascii=False)
                    
                QMessageBox.information(self, "Succès", f"Données sauvegardées dans {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
                
    def load_calibration_data(self):
        """Chargement des données de calibration"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Charger des données de calibration",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.calibration_data = json.load(f)
                    
                # Mise à jour de l'interface
                self.update_calibration_chart()
                self.generate_calibration_report()
                self.update_progress_status()
                
                QMessageBox.information(self, "Succès", f"Données chargées depuis {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")


# ===== WIDGETS SPÉCIALISÉS =====

class ProbeSelectorWidget(QWidget):
    """Widget de sélection des sondes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Interface de sélection des sondes
        pass


class CalibrationConfigWidget(QWidget):
    """Widget de configuration de calibration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Interface de configuration
        pass


class CalibrationProcessWidget(QWidget):
    """Widget de processus de calibration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Interface de processus
        pass


class CalibrationValidationWidget(QWidget):
    """Widget de validation de calibration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Interface de validation
        pass