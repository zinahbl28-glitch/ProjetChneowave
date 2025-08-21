"""
Panneau Calibration Moderne - Interface avancée de calibration
Design 2025 avec processus guidé et visualisations temps réel
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QFrame, QScrollArea, QPushButton, QProgressBar, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox, QGroupBox, QTabWidget,
    QSplitter, QTextEdit, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor

from ...components.app_state import ProjectInfo
from ...resources.modern_design_system import ModernDesignSystem
from ...components.modern.modern_card import ModernCard, InfoCard, StatusCard, ActionCard
from ...components.modern.modern_button import ModernButton, IconButton


class CalibrationWorker(QThread):
    """Worker thread pour la calibration en arrière-plan"""
    calibration_progress = Signal(int, str)  # progress, message
    calibration_complete = Signal(dict)      # results
    calibration_error = Signal(str)          # error message
    
    def __init__(self, probe_type, calibration_params):
        super().__init__()
        self.probe_type = probe_type
        self.calibration_params = calibration_params
        self.is_running = True
        
    def run(self):
        """Exécution de la calibration"""
        try:
            # Simulation de la calibration
            steps = [
                (10, "Initialisation des sondes..."),
                (25, "Vérification de la connectivité..."),
                (40, "Mesures de référence..."),
                (60, "Calcul des coefficients..."),
                (80, "Validation des résultats..."),
                (100, "Calibration terminée!")
            ]
            
            for progress, message in steps:
                if not self.is_running:
                    break
                self.calibration_progress.emit(progress, message)
                self.msleep(1000)  # 1 seconde par étape
            
            if self.is_running:
                # Résultats simulés
                results = {
                    'probe_type': self.probe_type,
                    'calibration_date': '2025-01-27',
                    'coefficients': {'a': 1.023, 'b': 0.015, 'c': -0.002},
                    'accuracy': 99.8,
                    'status': 'success'
                }
                self.calibration_complete.emit(results)
                
        except Exception as e:
            self.calibration_error.emit(str(e))
    
    def stop(self):
        """Arrêter la calibration"""
        self.is_running = False


class ModernCalibrationPanel(QWidget):
    """Panneau de calibration moderne avec design 2025"""
    
    def __init__(self, project: ProjectInfo = None, parent=None):
        super().__init__(parent)
        self.current_project = project
        self.calibration_worker = None
        
        # Initialisation de l'interface
        self._setup_modern_ui()
        self._setup_probe_management()
        self._setup_calibration_wizard()
        self._setup_real_time_charts()
        self._setup_calibration_history()
        self._setup_validation_tools()
        
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
        
    def _setup_probe_management(self):
        """Section gestion des sondes"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        probe_container = QFrame()
        probe_container.setObjectName("probe_management")
        probe_container.setStyleSheet(f"""
            QFrame#probe_management {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        probe_layout = QVBoxLayout(probe_container)
        probe_layout.setContentsMargins(0, 0, 0, 0)
        probe_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Gestion des Sondes")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        probe_layout.addWidget(section_title)
        
        # Grille de sondes
        probe_grid = QGridLayout()
        probe_grid.setSpacing(spacing['lg'])
        
        # Sondes disponibles
        probe_types = [
            ("CHNeoWave Sonde de Niveau", "NIV-001", "Connectée", "success"),
            ("CHNeoWave Sonde de Vitesse", "VIT-002", "Connectée", "success"),
            ("CHNeoWave Sonde de Température", "TEMP-003", "Déconnectée", "error"),
            ("CHNeoWave Sonde de Pression", "PRESS-004", "En maintenance", "warning")
        ]
        
        for i, (name, code, status, status_type) in enumerate(probe_types):
            # Carte de sonde
            probe_card = QFrame()
            probe_card.setObjectName("probe_card")
            probe_card.setStyleSheet(f"""
                QFrame#probe_card {{
                    background: {colors['surface_light']};
                    border: 1px solid {colors['border']};
                    border-radius: {ModernDesignSystem.get_border_radius()['lg']}px;
                    padding: {spacing['lg']}px;
                }}
            """)
            
            card_layout = QVBoxLayout(probe_card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(spacing['md'])
            
            # Nom de la sonde
            name_label = QLabel(name)
            name_label.setFont(ModernDesignSystem.get_font('h3'))
            name_label.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
            card_layout.addWidget(name_label)
            
            # Code de la sonde
            code_label = QLabel(f"Code: {code}")
            code_label.setFont(ModernDesignSystem.get_font('body'))
            code_label.setStyleSheet(f"color: {colors['text_secondary']};")
            card_layout.addWidget(code_label)
            
            # Statut
            status_label = QLabel(status)
            status_label.setFont(ModernDesignSystem.get_font('body'))
            status_color = colors.get(f'{status_type}_dark', colors['text_secondary'])
            status_label.setStyleSheet(f"color: {status_color}; font-weight: 500;")
            card_layout.addWidget(status_label)
            
            # Bouton d'action
            action_btn = ModernButton(
                text="Configurer" if status_type == "success" else "Connecter",
                style="primary" if status_type == "success" else "secondary"
            )
            card_layout.addWidget(action_btn)
            
            probe_grid.addWidget(probe_card, i // 2, i % 2)
        
        probe_layout.addLayout(probe_grid)
        self.content_layout.addWidget(probe_container)
        
    def _setup_calibration_wizard(self):
        """Assistant de calibration guidée"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        wizard_container = QFrame()
        wizard_container.setObjectName("calibration_wizard")
        wizard_container.setStyleSheet(f"""
            QFrame#calibration_wizard {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        wizard_layout = QVBoxLayout(wizard_container)
        wizard_layout.setContentsMargins(0, 0, 0, 0)
        wizard_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Assistant de Calibration")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        wizard_layout.addWidget(section_title)
        
        # Configuration de la calibration
        config_group = QGroupBox("Configuration")
        config_group.setFont(ModernDesignSystem.get_font('h3'))
        config_group.setStyleSheet(f"""
            QGroupBox {{
                color: {colors['text_primary']};
                font-weight: 600;
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                margin-top: {spacing['lg']}px;
                padding-top: {spacing['md']}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {spacing['md']}px;
                padding: 0 {spacing['sm']}px 0 {spacing['sm']}px;
            }}
        """)
        
        config_layout = QGridLayout(config_group)
        config_layout.setSpacing(spacing['md'])
        
        # Type de sonde
        probe_type_label = QLabel("Type de Sonde:")
        probe_type_label.setFont(ModernDesignSystem.get_font('body'))
        probe_type_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.probe_type_combo = QComboBox()
        self.probe_type_combo.addItems(["Niveau", "Vitesse", "Température", "Pression"])
        self.probe_type_combo.setFont(ModernDesignSystem.get_font('body'))
        self.probe_type_combo.setStyleSheet(f"""
            QComboBox {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                padding: {spacing['sm']}px;
                color: {colors['text_primary']};
            }}
        """)
        
        config_layout.addWidget(probe_type_label, 0, 0)
        config_layout.addWidget(self.probe_type_combo, 0, 1)
        
        # Nombre de points de calibration
        points_label = QLabel("Points de Calibration:")
        points_label.setFont(ModernDesignSystem.get_font('body'))
        points_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.points_spin = QSpinBox()
        self.points_spin.setRange(5, 20)
        self.points_spin.setValue(10)
        self.points_spin.setFont(ModernDesignSystem.get_font('body'))
        self.points_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                padding: {spacing['sm']}px;
                color: {colors['text_primary']};
            }}
        """)
        
        config_layout.addWidget(points_label, 1, 0)
        config_layout.addWidget(self.points_spin, 1, 1)
        
        # Précision cible
        precision_label = QLabel("Précision Cible (%):")
        precision_label.setFont(ModernDesignSystem.get_font('body'))
        precision_label.setStyleSheet(f"color: {colors['text_secondary']};")
        
        self.precision_spin = QDoubleSpinBox()
        self.precision_spin.setRange(95.0, 99.9)
        self.precision_spin.setValue(99.0)
        self.precision_spin.setDecimals(1)
        self.precision_spin.setFont(ModernDesignSystem.get_font('body'))
        self.precision_spin.setStyleSheet(f"""
            QDoubleSpinBox {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['sm']}px;
                padding: {spacing['sm']}px;
                color: {colors['text_primary']};
            }}
        """)
        
        config_layout.addWidget(precision_label, 2, 0)
        config_layout.addWidget(self.precision_spin, 2, 1)
        
        wizard_layout.addWidget(config_group)
        
        # Boutons de contrôle
        control_layout = QHBoxLayout()
        control_layout.setSpacing(spacing['md'])
        
        self.start_calibration_btn = ModernButton(text="Démarrer la Calibration", style="success")
        self.start_calibration_btn.clicked.connect(self._start_calibration)
        
        self.stop_calibration_btn = ModernButton(text="Arrêter", style="danger")
        self.stop_calibration_btn.clicked.connect(self._stop_calibration)
        self.stop_calibration_btn.setEnabled(False)
        
        control_layout.addWidget(self.start_calibration_btn)
        control_layout.addWidget(self.stop_calibration_btn)
        control_layout.addStretch()
        
        wizard_layout.addLayout(control_layout)
        
        # Barre de progression
        self.calibration_progress = QProgressBar()
        self.calibration_progress.setRange(0, 100)
        self.calibration_progress.setValue(0)
        self.calibration_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                text-align: center;
                background: {colors['surface_light']};
            }}
            QProgressBar::chunk {{
                background: {colors['gradient_accent']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
            }}
        """)
        wizard_layout.addWidget(self.calibration_progress)
        
        # Message de statut
        self.status_label = QLabel("Prêt pour la calibration")
        self.status_label.setFont(ModernDesignSystem.get_font('body'))
        self.status_label.setStyleSheet(f"color: {colors['text_secondary']}; text-align: center;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wizard_layout.addWidget(self.status_label)
        
        self.content_layout.addWidget(wizard_container)
        
    def _setup_real_time_charts(self):
        """Graphiques temps réel de calibration"""
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
        section_title = QLabel("Graphiques Temps Réel")
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
        
        # Onglet Historique
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        
        history_placeholder = QLabel("Graphique Historique\n(Intégration Matplotlib en cours)")
        history_placeholder.setFont(ModernDesignSystem.get_font('h3'))
        history_placeholder.setStyleSheet(f"color: {colors['text_muted']}; text-align: center;")
        history_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        history_placeholder.setMinimumHeight(36)
        history_layout.addWidget(history_placeholder)
        
        self.charts_tabs.addTab(history_tab, "Historique")
        
        # Onglet Comparaison
        comparison_tab = QWidget()
        comparison_layout = QVBoxLayout(comparison_tab)
        
        comparison_placeholder = QLabel("Graphique Comparaison\n(Intégration Plotly en cours)")
        comparison_placeholder.setFont(ModernDesignSystem.get_font('h3'))
        comparison_placeholder.setStyleSheet(f"color: {colors['text_muted']}; text-align: center;")
        comparison_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        comparison_placeholder.setMinimumHeight(36)
        comparison_layout.addWidget(comparison_placeholder)
        
        self.charts_tabs.addTab(comparison_tab, "Comparaison")
        
        charts_layout.addWidget(self.charts_tabs)
        self.content_layout.addWidget(charts_container)
        
    def _setup_calibration_history(self):
        """Historique des calibrations"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        history_container = QFrame()
        history_container.setObjectName("calibration_history")
        history_container.setStyleSheet(f"""
            QFrame#calibration_history {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        history_layout = QVBoxLayout(history_container)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Historique des Calibrations")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        history_layout.addWidget(section_title)
        
        # Liste des calibrations
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(f"""
            QListWidget {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                padding: {spacing['sm']}px;
                color: {colors['text_primary']};
            }}
            QListWidget::item {{
                padding: {spacing['md']}px;
                border-bottom: 1px solid {colors['border']};
            }}
            QListWidget::item:selected {{
                background: {colors['primary']};
                color: {colors['text_inverse']};
            }}
        """)
        
        # Données d'exemple
        history_data = [
            ("Calibration Sonde Niveau", "2025-01-26", "Succès", "99.8%"),
            ("Calibration Sonde Vitesse", "2025-01-25", "Succès", "99.5%"),
            ("Calibration Sonde Température", "2025-01-24", "Échec", "85.2%"),
            ("Calibration Sonde Pression", "2025-01-23", "Succès", "99.9%")
        ]
        
        for title, date, status, accuracy in history_data:
            item_text = f"{title} | {date} | {status} | {accuracy}"
            item = QListWidgetItem(item_text)
            self.history_list.addItem(item)
        
        history_layout.addWidget(self.history_list)
        self.content_layout.addWidget(history_container)
        
    def _setup_validation_tools(self):
        """Outils de validation de calibration"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container principal
        validation_container = QFrame()
        validation_container.setObjectName("validation_tools")
        validation_container.setStyleSheet(f"""
            QFrame#validation_tools {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['xl']}px;
                padding: {spacing['xl']}px;
            }}
        """)
        
        # Layout
        validation_layout = QVBoxLayout(validation_container)
        validation_layout.setContentsMargins(0, 0, 0, 0)
        validation_layout.setSpacing(spacing['lg'])
        
        # Titre de section
        section_title = QLabel("Outils de Validation")
        section_title.setFont(ModernDesignSystem.get_font('h2'))
        section_title.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        validation_layout.addWidget(section_title)
        
        # Grille d'outils
        tools_grid = QGridLayout()
        tools_grid.setSpacing(spacing['lg'])
        
        # Validation de dérive
        drift_card = ActionCard(
            title="Validation Dérive",
            description="Vérifier la stabilité temporelle",
            action_text="Valider",
            icon="▤"
        )
        tools_grid.addWidget(drift_card, 0, 0)
        
        # Validation de bruit
        noise_card = ActionCard(
            title="Validation Bruit",
            description="Analyser le niveau de bruit",
            action_text="Analyser",
            icon="×"
        )
        tools_grid.addWidget(noise_card, 0, 1)
        
        # Validation de linéarité
        linearity_card = ActionCard(
            title="Validation Linéarité",
            description="Vérifier la réponse linéaire",
            action_text="Vérifier",
            icon="△"
        )
        tools_grid.addWidget(linearity_card, 1, 0)
        
        # Validation de stabilité
        stability_card = ActionCard(
            title="Validation Stabilité",
            description="Tester la stabilité des mesures",
            action_text="Tester",
            icon="◐"
        )
        tools_grid.addWidget(stability_card, 1, 1)
        
        validation_layout.addLayout(tools_grid)
        self.content_layout.addWidget(validation_container)
        
    def _start_calibration(self):
        """Démarrer la calibration"""
        probe_type = self.probe_type_combo.currentText()
        points = self.points_spin.value()
        precision = self.precision_spin.value()
        
        # Paramètres de calibration
        calibration_params = {
            'probe_type': probe_type,
            'points': points,
            'precision_target': precision
        }
        
        # Créer et démarrer le worker
        self.calibration_worker = CalibrationWorker(probe_type, calibration_params)
        self.calibration_worker.calibration_progress.connect(self._update_calibration_progress)
        self.calibration_worker.calibration_complete.connect(self._on_calibration_complete)
        self.calibration_worker.calibration_error.connect(self._on_calibration_error)
        
        self.calibration_worker.start()
        
        # Mettre à jour l'interface
        self.start_calibration_btn.setEnabled(False)
        self.stop_calibration_btn.setEnabled(True)
        self.status_label.setText("Calibration en cours...")
        
    def _stop_calibration(self):
        """Arrêter la calibration"""
        if self.calibration_worker and self.calibration_worker.isRunning():
            self.calibration_worker.stop()
            self.calibration_worker.wait()
        
        # Réinitialiser l'interface
        self.start_calibration_btn.setEnabled(True)
        self.stop_calibration_btn.setEnabled(False)
        self.calibration_progress.setValue(0)
        self.status_label.setText("Calibration arrêtée")
        
    def _update_calibration_progress(self, progress, message):
        """Mettre à jour la progression de la calibration"""
        self.calibration_progress.setValue(progress)
        self.status_label.setText(message)
        
    def _on_calibration_complete(self, results):
        """Calibration terminée avec succès"""
        self.start_calibration_btn.setEnabled(True)
        self.stop_calibration_btn.setEnabled(False)
        self.status_label.setText(f"Calibration terminée! Précision: {results['accuracy']}%")
        
        # Ajouter à l'historique
        history_item = f"Calibration {results['probe_type']} | {results['calibration_date']} | Succès | {results['accuracy']}%"
        self.history_list.insertItem(0, history_item)
        
    def _on_calibration_error(self, error_message):
        """Erreur lors de la calibration"""
        self.start_calibration_btn.setEnabled(True)
        self.stop_calibration_btn.setEnabled(False)
        self.status_label.setText(f"Erreur: {error_message}")
        
    def closeEvent(self, event):
        """Arrêter le worker lors de la fermeture"""
        if self.calibration_worker and self.calibration_worker.isRunning():
            self.calibration_worker.stop()
            self.calibration_worker.wait()
        event.accept()
