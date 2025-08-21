"""
Panneau Acquisition Moderne - Interface temps réel d'acquisition
Design 2025 avec visualisations avancées et monitoring des capteurs
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QFrame, QScrollArea, QPushButton, QProgressBar, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox, QGroupBox, QTabWidget,
    QSplitter, QTextEdit, QListWidget, QListWidgetItem, QSlider
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor

from ...components.app_state import ProjectInfo
from ...resources.modern_design_system import ModernDesignSystem
from ...components.modern.modern_card import ModernCard, InfoCard, StatusCard, ActionCard
from ...components.modern.modern_button import ModernButton, IconButton


class AcquisitionWorker(QThread):
    """Worker thread pour l'acquisition de données en arrière-plan"""
    data_received = Signal(dict)           # données reçues
    acquisition_status = Signal(str, str)  # status, message
    sensor_error = Signal(str, str)        # sensor_id, error
    
    def __init__(self, acquisition_params):
        super().__init__()
        self.acquisition_params = acquisition_params
        self.is_running = True
        self.sample_rate = acquisition_params.get('sample_rate', 32)
        
    def run(self):
        """Exécution de l'acquisition"""
        try:
            # Simulation de l'acquisition
            sample_count = 0
            while self.is_running:
                # Générer des données simulées
                data = {
                    'timestamp': sample_count,
                    'sensors': {
                        'NIV-001': {'value': 1.5 + 0.1 * (sample_count % 100) / 100, 'unit': 'm'},
                        'VIT-002': {'value': 2.3 + 0.05 * (sample_count % 50) / 50, 'unit': 'm/s'},
                        'TEMP-003': {'value': 20.5 + 0.2 * (sample_count % 200) / 200, 'unit': '°C'},
                        'PRESS-004': {'value': 1013.25 + 0.5 * (sample_count % 150) / 150, 'unit': 'hPa'}
                    }
                }
                
                self.data_received.emit(data)
                self.acquisition_status.emit('running', f'Échantillon {sample_count}')
                
                sample_count += 1
                self.msleep(1000 // self.sample_rate)  # Fréquence d'échantillonnage
                
        except Exception as e:
            self.sensor_error.emit('ALL', str(e))
    
    def stop(self):
        """Arrêter l'acquisition"""
        self.is_running = False


class ModernAcquisitionPanel(QWidget):
    """Panneau d'acquisition moderne avec design 2025"""
    
    def __init__(self, project: ProjectInfo = None, parent=None):
        super().__init__(parent)
        self.current_project = project
        self.acquisition_worker = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
        # Initialisation de l'interface
        self._setup_modern_ui()
        self._setup_acquisition_controls()
        self._setup_sensor_monitoring()
        self._setup_real_time_charts()
        self._setup_data_logging()
        self._setup_acquisition_settings()
        
    def _setup_modern_ui(self):
        """Configuration de l'interface moderne"""
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Scroll area pour le contenu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Widget de contenu
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(18, 18, 18, 18)
        self.content_layout.setSpacing(6)
        
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
        
    def _setup_acquisition_controls(self):
        """Contrôles d'acquisition principaux"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        controls_container = QFrame()
        controls_container.setObjectName("acquisition_controls")
        controls_container.setStyleSheet(f"""
            QFrame#acquisition_controls {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        controls_layout = QVBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Contrôles d'Acquisition")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        controls_layout.addWidget(section_title)
        
        # Boutons de contrôle principaux
        main_controls_layout = QHBoxLayout()
        main_controls_layout.setSpacing(spacing['lg'])
        
        self.start_acquisition_btn = ModernButton(
            text="Démarrer l'Acquisition",
            style="success"
        )
        self.start_acquisition_btn.clicked.connect(self._start_acquisition)
        
        self.stop_acquisition_btn = ModernButton(
            text="Arrêter l'Acquisition",
            style="danger"
        )
        self.stop_acquisition_btn.clicked.connect(self._stop_acquisition)
        self.stop_acquisition_btn.setEnabled(False)
        
        self.pause_acquisition_btn = ModernButton(
            text="Pause",
            style="warning"
        )
        self.pause_acquisition_btn.clicked.connect(self._pause_acquisition)
        self.pause_acquisition_btn.setEnabled(False)
        
        main_controls_layout.addWidget(self.start_acquisition_btn)
        main_controls_layout.addWidget(self.stop_acquisition_btn)
        main_controls_layout.addWidget(self.pause_acquisition_btn)
        main_controls_layout.addStretch()
        
        controls_layout.addLayout(main_controls_layout)
        
        # Barre de progression et statut
        status_layout = QHBoxLayout()
        status_layout.setSpacing(spacing['lg'])
        
        # Barre de progression
        self.acquisition_progress = QProgressBar()
        self.acquisition_progress.setRange(0, 100)
        self.acquisition_progress.setValue(0)
        self.acquisition_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                text-align: center;
                background: {colors['surface_light']};
                min-height: 20px;
            }}
            QProgressBar::chunk {{
                background: {colors['gradient_accent']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
            }}
        """)
        
        # Message de statut
        self.status_label = QLabel("Prêt pour l'acquisition")
        self.status_label.setFont(ModernDesignSystem.get_font('body'))
        self.status_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        status_layout.addWidget(self.acquisition_progress, 1)
        status_layout.addWidget(self.status_label, 0)
        
        controls_layout.addLayout(status_layout)
        self.content_layout.addWidget(controls_container)
        
    def _setup_sensor_monitoring(self):
        """Monitoring des capteurs en temps réel"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        monitoring_container = QFrame()
        monitoring_container.setObjectName("sensor_monitoring")
        monitoring_container.setStyleSheet(f"""
            QFrame#sensor_monitoring {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        monitoring_layout = QVBoxLayout(monitoring_container)
        monitoring_layout.setContentsMargins(0, 0, 0, 0)
        monitoring_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Monitoring des Capteurs")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        monitoring_layout.addWidget(section_title)
        
        # Grille de capteurs
        sensors_grid = QGridLayout()
        sensors_grid.setSpacing(spacing['lg'])
        
        # Capteurs disponibles
        self.sensor_cards = {}
        sensor_types = [
            ("CHNeoWave Niveau", "NIV-001", "m", "success"),
            ("CHNeoWave Vitesse", "VIT-002", "m/s", "success"),
            ("CHNeoWave Température", "TEMP-003", "°C", "warning"),
            ("CHNeoWave Pression", "PRESS-004", "hPa", "error")
        ]
        
        for i, (name, code, unit, status_type) in enumerate(sensor_types):
            # Carte de capteur
            sensor_card = StatusCard(
                title=name,
                value=f"0.0 {unit}",
                status=status_type,
                description=f"Capteur {code}"
            )
            
            # Stocker la référence pour mise à jour
            self.sensor_cards[code] = sensor_card
            
            sensors_grid.addWidget(sensor_card, i // 2, i % 2)
        
        monitoring_layout.addLayout(sensors_grid)
        self.content_layout.addWidget(monitoring_container)
        
    def _setup_real_time_charts(self):
        """Graphiques temps réel d'acquisition"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        charts_container = QFrame()
        charts_container.setObjectName("real_time_charts")
        charts_container.setStyleSheet(f"""
            QFrame#real_time_charts {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        charts_layout = QVBoxLayout(charts_container)
        charts_layout.setContentsMargins(0, 0, 0, 0)
        charts_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Visualisations Temps Réel")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        charts_layout.addWidget(section_title)
        
        # Onglets pour différents graphiques
        self.charts_tabs = QTabWidget()
        self.charts_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                background: {colors['surface_light']};
            }}
            QTabBar::tab {{
                background: {colors['surface']};
                color: {colors['text_secondary']};
                padding: {spacing['md']}px {spacing['lg']}px;
                border: 1px solid {colors['border']};
                border-bottom: none;
                border-top-left-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                border-top-right-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
            }}
            QTabBar::tab:selected {{
                background: {colors['surface_light']};
                color: {colors['text_primary']};
                border-bottom: 1px solid {colors['surface_light']};
            }}
        """)
        
        # Onglet Graphique Temps Réel
        realtime_tab = QWidget()
        realtime_layout = QVBoxLayout(realtime_tab)
        
        # Placeholder pour le graphique temps réel
        chart_placeholder = QLabel("Graphique Temps Réel\n(Intégration PyQtGraph en cours)")
        chart_placeholder.setFont(ModernDesignSystem.get_font('h3'))
        chart_placeholder.setStyleSheet(f"color: {colors['text_muted']}; text-align: center;")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setMinimumHeight(36)
        realtime_layout.addWidget(chart_placeholder)
        
        self.charts_tabs.addTab(realtime_tab, "Temps Réel")
        
        # Onglet Données Brutes
        rawdata_tab = QWidget()
        rawdata_layout = QVBoxLayout(rawdata_tab)
        
        rawdata_placeholder = QLabel("Données Brutes\n(Tableau de données en cours)")
        rawdata_placeholder.setFont(ModernDesignSystem.get_font('h3'))
        rawdata_placeholder.setStyleSheet(f"color: {colors['text_muted']}; text-align: center;")
        rawdata_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rawdata_placeholder.setMinimumHeight(36)
        rawdata_layout.addWidget(rawdata_placeholder)
        
        self.charts_tabs.addTab(rawdata_tab, "Données Brutes")
        
        # Onglet Analyse Spectrale
        spectral_tab = QWidget()
        spectral_layout = QVBoxLayout(spectral_tab)
        
        spectral_placeholder = QLabel("Analyse Spectrale\n(FFT et analyse fréquentielle en cours)")
        spectral_placeholder.setFont(ModernDesignSystem.get_font('h3'))
        spectral_placeholder.setStyleSheet(f"color: {colors['text_muted']}; text-align: center;")
        spectral_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spectral_placeholder.setMinimumHeight(36)
        spectral_layout.addWidget(spectral_placeholder)
        
        self.charts_tabs.addTab(spectral_tab, "Analyse Spectrale")
        
        charts_layout.addWidget(self.charts_tabs)
        self.content_layout.addWidget(charts_container)
        
    def _setup_data_logging(self):
        """Journalisation des données"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        logging_container = QFrame()
        logging_container.setObjectName("data_logging")
        logging_container.setStyleSheet(f"""
            QFrame#data_logging {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        logging_layout = QVBoxLayout(logging_container)
        logging_layout.setContentsMargins(0, 0, 0, 0)
        logging_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Journalisation des Données")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        logging_layout.addWidget(section_title)
        
        # Informations de journalisation
        info_layout = QGridLayout()
        info_layout.setSpacing(spacing['lg'])
        
        # Nombre d'échantillons
        samples_label = QLabel("Échantillons acquis:")
        samples_label.setFont(ModernDesignSystem.get_font('body'))
        samples_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.samples_count_label = QLabel("0")
        self.samples_count_label.setFont(ModernDesignSystem.get_font('h3'))
        self.samples_count_label.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        
        info_layout.addWidget(samples_label, 0, 0)
        info_layout.addWidget(self.samples_count_label, 0, 1)
        
        # Taux d'échantillonnage
        rate_label = QLabel("Taux d'Échantillonnage:")
        rate_label.setFont(ModernDesignSystem.get_font('body'))
        rate_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.sample_rate_label = QLabel("32 Hz")
        self.sample_rate_label.setFont(ModernDesignSystem.get_font('h3'))
        self.sample_rate_label.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        
        info_layout.addWidget(rate_label, 1, 0)
        info_layout.addWidget(self.sample_rate_label, 1, 1)
        
        # Taille du buffer
        buffer_label = QLabel("Taille du Buffer:")
        buffer_label.setFont(ModernDesignSystem.get_font('body'))
        buffer_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.buffer_size_label = QLabel("0 / 1000")
        self.buffer_size_label.setFont(ModernDesignSystem.get_font('h3'))
        self.buffer_size_label.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        
        info_layout.addWidget(buffer_label, 2, 0)
        info_layout.addWidget(self.buffer_size_label, 2, 1)
        
        logging_layout.addLayout(info_layout)
        
        # Boutons de gestion des données
        data_controls_layout = QHBoxLayout()
        data_controls_layout.setSpacing(spacing['md'])
        
        self.save_data_btn = ModernButton(
            text="Sauvegarder les Données",
            style="primary"
        )
        self.save_data_btn.clicked.connect(self._save_data)
        
        self.clear_buffer_btn = ModernButton(
            text="Vider le Buffer",
            style="secondary"
        )
        self.clear_buffer_btn.clicked.connect(self._clear_buffer)
        
        self.export_data_btn = ModernButton(
            text="Exporter en HDF5",
            style="success"
        )
        self.export_data_btn.clicked.connect(self._export_data)
        
        data_controls_layout.addWidget(self.save_data_btn)
        data_controls_layout.addWidget(self.clear_buffer_btn)
        data_controls_layout.addWidget(self.export_data_btn)
        data_controls_layout.addStretch()
        
        logging_layout.addLayout(data_controls_layout)
        self.content_layout.addWidget(logging_container)
        
    def _setup_acquisition_settings(self):
        """Paramètres d'acquisition"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        settings_container = QFrame()
        settings_container.setObjectName("acquisition_settings")
        settings_container.setStyleSheet(f"""
            QFrame#acquisition_settings {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Paramètres d'Acquisition")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        settings_layout.addWidget(section_title)
        
        # Configuration des paramètres
        config_layout = QGridLayout()
        config_layout.setSpacing(spacing['lg'])
        
        # Taux d'échantillonnage
        sample_rate_label = QLabel("Taux d'Échantillonnage (Hz):")
        sample_rate_label.setFont(ModernDesignSystem.get_font('body'))
        sample_rate_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.sample_rate_spin = QSpinBox()
        self.sample_rate_spin.setRange(1, 1000)
        self.sample_rate_spin.setValue(32)
        self.sample_rate_spin.setFont(ModernDesignSystem.get_font('body'))
        self.sample_rate_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                padding: {spacing['sm']}px;
                color: {colors['text_primary']};
            }}
        """)
        
        config_layout.addWidget(sample_rate_label, 0, 0)
        config_layout.addWidget(self.sample_rate_spin, 0, 1)
        
        # Taille du buffer
        buffer_size_label = QLabel("Taille du Buffer:")
        buffer_size_label.setFont(ModernDesignSystem.get_font('body'))
        buffer_size_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.buffer_size_spin = QSpinBox()
        self.buffer_size_spin.setRange(100, 10000)
        self.buffer_size_spin.setValue(1000)
        self.buffer_size_spin.setFont(ModernDesignSystem.get_font('body'))
        self.buffer_size_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                padding: {spacing['sm']}px;
                color: {colors['text_primary']};
            }}
        """)
        
        config_layout.addWidget(buffer_size_label, 1, 0)
        config_layout.addWidget(self.buffer_size_spin, 1, 1)
        
        # Auto-sauvegarde
        autosave_label = QLabel("Auto-sauvegarde:")
        autosave_label.setFont(ModernDesignSystem.get_font('body'))
        autosave_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.autosave_checkbox = QCheckBox("Activée")
        self.autosave_checkbox.setFont(ModernDesignSystem.get_font('body'))
        self.autosave_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {colors['text_primary']};
                spacing: {spacing['sm']}px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                background: {colors['surface_light']};
            }}
            QCheckBox::indicator:checked {{
                background: {colors['primary']};
                border-color: {colors['primary']};
            }}
        """)
        
        config_layout.addWidget(autosave_label, 2, 0)
        config_layout.addWidget(self.autosave_checkbox, 2, 1)
        
        settings_layout.addLayout(config_layout)
        
        # Bouton d'application des paramètres
        apply_btn = ModernButton(text="Appliquer les Paramètres", style="success")
        apply_btn.clicked.connect(self._apply_settings)
        settings_layout.addWidget(apply_btn)
        
        self.content_layout.addWidget(settings_container)
        
    def _start_acquisition(self):
        """Démarrer l'acquisition"""
        # Paramètres d'acquisition
        acquisition_params = {
            'sample_rate': self.sample_rate_spin.value(),
            'buffer_size': self.buffer_size_spin.value(),
            'autosave': self.autosave_checkbox.isChecked()
        }
        
        # Créer et démarrer le worker
        self.acquisition_worker = AcquisitionWorker(acquisition_params)
        self.acquisition_worker.data_received.connect(self._on_data_received)
        self.acquisition_worker.acquisition_status.connect(self._on_acquisition_status)
        self.acquisition_worker.sensor_error.connect(self._on_sensor_error)
        
        self.acquisition_worker.start()
        
        # Mettre à jour l'interface
        self.start_acquisition_btn.setEnabled(False)
        self.stop_acquisition_btn.setEnabled(True)
        self.pause_acquisition_btn.setEnabled(True)
        self.status_label.setText("Acquisition en cours...")
        
        # Mettre à jour la taille du buffer
        self.max_buffer_size = acquisition_params['buffer_size']
        self.buffer_size_label.setText(f"0 / {self.max_buffer_size}")
        
    def _stop_acquisition(self):
        """Arrêter l'acquisition"""
        if self.acquisition_worker and self.acquisition_worker.isRunning():
            self.acquisition_worker.stop()
            self.acquisition_worker.wait()
        
        # Réinitialiser l'interface
        self.start_acquisition_btn.setEnabled(True)
        self.stop_acquisition_btn.setEnabled(False)
        self.pause_acquisition_btn.setEnabled(False)
        self.status_label.setText("Acquisition arrêtée")
        
    def _pause_acquisition(self):
        """Mettre en pause l'acquisition"""
        if self.acquisition_worker and self.acquisition_worker.isRunning():
            self.acquisition_worker.stop()
            self.acquisition_worker.wait()
        
        # Mettre à jour l'interface
        self.start_acquisition_btn.setEnabled(True)
        self.stop_acquisition_btn.setEnabled(False)
        self.pause_acquisition_btn.setEnabled(False)
        self.status_label.setText("Acquisition en pause")
        
    def _on_data_received(self, data):
        """Données reçues du worker"""
        # Ajouter au buffer
        self.data_buffer.append(data)
        if len(self.data_buffer) > self.max_buffer_size:
            self.data_buffer.pop(0)
        
        # Mettre à jour les compteurs
        self.samples_count_label.setText(str(len(self.data_buffer)))
        self.buffer_size_label.setText(f"{len(self.data_buffer)} / {self.max_buffer_size}")
        
        # Mettre à jour les cartes de capteurs
        for sensor_id, sensor_data in data['sensors'].items():
            if sensor_id in self.sensor_cards:
                value_text = f"{sensor_data['value']:.3f} {sensor_data['unit']}"
                self.sensor_cards[sensor_id].update_value(value_text)
        
        # Mettre à jour la barre de progression
        progress = min(100, int((len(self.data_buffer) / self.max_buffer_size) * 100))
        self.acquisition_progress.setValue(progress)
        
    def _on_acquisition_status(self, status, message):
        """Mise à jour du statut d'acquisition"""
        self.status_label.setText(message)
        
    def _on_sensor_error(self, sensor_id, error):
        """Erreur de capteur"""
        if sensor_id == 'ALL':
            self.status_label.setText(f"Erreur système: {error}")
        else:
            self.status_label.setText(f"Erreur capteur {sensor_id}: {error}")
        
    def _save_data(self):
        """Sauvegarder les données"""
        if not self.data_buffer:
            return
        
        # Simulation de sauvegarde
        self.status_label.setText("Données sauvegardées avec succès")
        
    def _clear_buffer(self):
        """Vider le buffer de données"""
        self.data_buffer.clear()
        self.samples_count_label.setText("0")
        self.buffer_size_label.setText(f"0 / {self.max_buffer_size}")
        self.acquisition_progress.setValue(0)
        self.status_label.setText("Buffer vidé")
        
    def _export_data(self):
        """Exporter les données en HDF5"""
        if not self.data_buffer:
            return
        
        # Simulation d'export
        self.status_label.setText("Données exportées en HDF5")
        
    def _apply_settings(self):
        """Appliquer les nouveaux paramètres"""
        # Mettre à jour la taille du buffer
        self.max_buffer_size = self.buffer_size_spin.value()
        self.buffer_size_label.setText(f"{len(self.data_buffer)} / {self.max_buffer_size}")
        
        # Mettre à jour le taux d'échantillonnage
        self.sample_rate_label.setText(f"{self.sample_rate_spin.value()} Hz")
        
        self.status_label.setText("Paramètres appliqués")
        
    def closeEvent(self, event):
        """Arrêter le worker lors de la fermeture"""
        if self.acquisition_worker and self.acquisition_worker.isRunning():
            self.acquisition_worker.stop()
            self.acquisition_worker.wait()
        event.accept()
