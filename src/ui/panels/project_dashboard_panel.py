from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QPushButton, QProgressBar,
    QScrollArea, QSizePolicy, QSplitter
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap

from ..components.app_state import ProjectInfo
from ..resources.styles import COLORS
from ..resources.universal_golden_system import UniversalGoldenSystem as UGS


class ProjectDashboardPanel(QWidget):
    """Panneau d'information projet et système - Vue d'ensemble"""
    
    def __init__(self, project: ProjectInfo, parent=None):
        super().__init__(parent)
        self.current_project = project
        
        self.setup_ui()
        self.setup_timers()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface du panneau"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(UGS.get_spacing_system()['md'], UGS.get_spacing_system()['md'], UGS.get_spacing_system()['md'], UGS.get_spacing_system()['md'])
        main_layout.setSpacing(UGS.get_spacing_system()['lg'])
        
        # En-tête du dashboard
        self.setup_dashboard_header(main_layout)
        
        # Contenu principal: splitter horizontal selon φ
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setChildrenCollapsible(False)

        # Colonne principale (61.8%)
        dims = UGS.get_main_layout_dimensions()
        heights = UGS.get_height_sequence()
        spacing = UGS.get_spacing_system()
        main_column = self._create_main_column_phi(heights, spacing)
        main_column.setMinimumWidth(dims['main_column_width'])
        main_column.setMaximumWidth(dims['main_column_width'])

        # Colonne secondaire (38.2%)
        side_column = self._create_side_column_phi(heights, spacing)
        side_column.setMinimumWidth(dims['side_column_width'])
        side_column.setMaximumWidth(dims['side_column_width'])

        content_splitter.addWidget(main_column)
        content_splitter.addWidget(side_column)
        content_splitter.setSizes([dims['main_column_width'], dims['side_column_width']])
        content_splitter.setStretchFactor(0, 618)
        content_splitter.setStretchFactor(1, 382)

        main_layout.addWidget(content_splitter)
        
        # Espace flexible
        main_layout.addStretch()
        
    def setup_dashboard_header(self, layout):
        """Configuration de l'en-tête du dashboard (compact <= 60px)."""
        header_frame = QFrame()
        header_frame.setFixedHeight(36)
        header_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                background-color: {COLORS['surface']};
                padding: 6px;
            }}
        """)

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 4, 8, 4)
        header_layout.setSpacing(8)

        title_label = QLabel("Acquisition Dashboard Projet")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLORS['primary']};")

        self.datetime_label = QLabel("")
        self.datetime_label.setFont(QFont("Segoe UI", 11))
        self.datetime_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.datetime_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(title_label, 1)
        header_layout.addWidget(self.datetime_label, 0)

        layout.addWidget(header_frame)
        
    def setup_project_details(self, layout):
        """Configuration des détails du projet"""
        details_group = QGroupBox(" Détails du Projet")
        details_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['secondary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        details_layout = QGridLayout(details_group)
        details_layout.setSpacing(15)
        details_layout.setColumnStretch(1, 1)
        
        # Informations de base
        details_layout.addWidget(QLabel("Nom du Projet:"), 0, 0)
        details_layout.addWidget(QLabel(self.current_project.name), 0, 1)
        
        details_layout.addWidget(QLabel("Code Projet:"), 1, 0)
        details_layout.addWidget(QLabel(self.current_project.code), 1, 1)
        
        details_layout.addWidget(QLabel("Ingénieur Principal:"), 2, 0)
        details_layout.addWidget(QLabel(self.current_project.engineer), 2, 1)
        
        details_layout.addWidget(QLabel("Chef de Projet:"), 3, 0)
        details_layout.addWidget(QLabel(self.current_project.manager), 3, 1)
        
        details_layout.addWidget(QLabel("Échelle:"), 4, 0)
        details_layout.addWidget(QLabel(self.current_project.scale), 4, 1)
        
        details_layout.addWidget(QLabel("Type de Bassin:"), 5, 0)
        details_layout.addWidget(QLabel(self.current_project.basin_type), 5, 1)
        
        # Styliser les labels de valeurs
        for row in range(6):
            value_label = details_layout.itemAtPosition(row, 1).widget()
            if value_label:
                value_label.setStyleSheet(f"""
                    color: {COLORS['text_primary']};
                    font-weight: normal;
                    padding: 5px;
                    background-color: {COLORS['surface']};
                    border-radius: 4px;
                """)
                
        layout.addWidget(details_group)
        
    def setup_system_metrics(self, layout):
        """Configuration des métriques système"""
        metrics_group = QGroupBox("Calibration Métriques Système")
        metrics_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        metrics_layout = QGridLayout(metrics_group)
        metrics_layout.setSpacing(15)
        metrics_layout.setColumnStretch(1, 1)
        
        # État des capteurs
        metrics_layout.addWidget(QLabel("État Capteurs:"), 0, 0)
        self.sensors_status = QLabel("● Non connectés")
        self.sensors_status.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")
        metrics_layout.addWidget(self.sensors_status, 0, 1)
        
        # État de l'acquisition
        metrics_layout.addWidget(QLabel("État Acquisition:"), 1, 0)
        self.acquisition_status = QLabel("● Arrêtée")
        self.acquisition_status.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")
        metrics_layout.addWidget(self.acquisition_status, 1, 1)
        
        # État de la calibration
        metrics_layout.addWidget(QLabel("État Calibration:"), 2, 0)
        self.calibration_status = QLabel("● Non effectuée")
        self.calibration_status.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")
        metrics_layout.addWidget(self.calibration_status, 2, 1)
        
        # État de l'analyse
        metrics_layout.addWidget(QLabel("État Analyse:"), 3, 0)
        self.analysis_status = QLabel("● Aucune donnée")
        self.analysis_status.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")
        metrics_layout.addWidget(self.analysis_status, 3, 1)
        
        # Barre de progression système
        metrics_layout.addWidget(QLabel("Progression Système:"), 4, 0)
        self.system_progress = QProgressBar()
        self.system_progress.setRange(0, 100)
        self.system_progress.setValue(25)  # Valeur de démonstration
        self.system_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['primary']};
                border-radius: 6px;
                text-align: center;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['success']};
                border-radius: 4px;
            }}
        """)
        metrics_layout.addWidget(self.system_progress, 4, 1)
        
        layout.addWidget(metrics_group)
        
    def setup_recent_activity(self, layout):
        """Configuration de l'activité récente"""
        activity_group = QGroupBox("Activité Activité Récente")
        activity_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['warning']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        activity_layout = QVBoxLayout(activity_group)
        activity_layout.setSpacing(10)
        
        # Liste des activités récentes
        activities = [
            "Heure 14:30 - Projet créé et ouvert",
            "Heure 14:31 - Interface dashboard initialisée",
            "Heure 14:32 - Navigation modules configurée",
            "Heure 14:33 - Métriques système affichées"
        ]
        
        for activity in activities:
            activity_label = QLabel(activity)
            activity_label.setStyleSheet(f"""
                color: {COLORS['text_secondary']};
                font-weight: normal;
                padding: 5px;
                background-color: {COLORS['surface']};
                border-radius: 4px;
                border-left: 3px solid {COLORS['warning']};
            """)
            activity_layout.addWidget(activity_label)
            
        layout.addWidget(activity_group)
        
    def setup_module_shortcuts(self, layout):
        """Configuration des raccourcis vers modules"""
        shortcuts_group = QGroupBox("Démarrer Accès Rapide aux Modules")
        shortcuts_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['success']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        shortcuts_layout = QGridLayout(shortcuts_group)
        shortcuts_layout.setSpacing(15)
        
        # Boutons de raccourcis
        shortcuts = [
            ("Calibration Calibration", "calibration", COLORS['warning']),
            ("Acquisition Acquisition", "acquisition", COLORS['primary']),
            ("Statistique Statistique", "stats", COLORS['secondary']),
            ("Analyses Avancée", "advanced", COLORS['warning']),
            ("Export Export", "export", COLORS['success'])
        ]
        
        for i, (name, module_id, color) in enumerate(shortcuts):
            row = i // 3
            col = i % 3
            
            shortcut_btn = QPushButton(name)
            shortcut_btn.setMinimumHeight(30)
            shortcut_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            
            shortcuts_layout.addWidget(shortcut_btn, row, col)
            
        layout.addWidget(shortcuts_group)

    # ===== φ-based compact columns =====
    def _create_main_column_phi(self, heights, spacing) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setSpacing(spacing['md'])
        details_container = QWidget()
        details_container.setFixedHeight(heights['section_xl'])
        v1 = QVBoxLayout(details_container)
        self.setup_project_details_compact(v1)
        v.addWidget(details_container)

        metrics_container = QWidget()
        metrics_container.setFixedHeight(heights['section_l'])
        v2 = QVBoxLayout(metrics_container)
        self.setup_system_metrics_compact(v2)
        v.addWidget(metrics_container)
        v.addStretch()
        return w

    def _create_side_column_phi(self, heights, spacing) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setSpacing(spacing['md'])
        activity_container = QWidget()
        activity_container.setFixedHeight(heights['section_l'])
        v1 = QVBoxLayout(activity_container)
        self.setup_recent_activity_compact(v1)
        v.addWidget(activity_container)

        shortcuts_container = QWidget()
        shortcuts_container.setFixedHeight(heights['section_xl'])
        v2 = QVBoxLayout(shortcuts_container)
        self.setup_module_shortcuts_compact(v2)
        v.addWidget(shortcuts_container)
        v.addStretch()
        return w

    def get_groupbox_style(self, border_color: str) -> str:
        return f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {border_color};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """

    def setup_project_details_compact(self, layout):
        details_group = QGroupBox(" Détails du Projet")
        details_group.setStyleSheet(self.get_groupbox_style(COLORS['secondary']))
        grid = QGridLayout(details_group)
        grid.setSpacing(UGS.get_spacing_system()['sm'])
        infos = [
            ("Nom:", self.current_project.name),
            ("Code:", self.current_project.code),
            ("Ingénieur:", self.current_project.engineer),
            ("Manager:", self.current_project.manager),
            ("Échelle:", self.current_project.scale),
            ("Type:", self.current_project.basin_type),
        ]
        for i, (label, value) in enumerate(infos):
            row, col = i // 2, (i % 2) * 2
            l = QLabel(label); l.setFixedHeight(UGS.get_height_sequence()['label']); l.setStyleSheet("font-weight: bold;")
            v = QLabel(value); v.setFixedHeight(UGS.get_height_sequence()['label']); v.setStyleSheet(f"background-color: {COLORS['surface']}; padding: 4px 8px; border-radius: 4px;")
            grid.addWidget(l, row, col)
            grid.addWidget(v, row, col + 1)
        layout.addWidget(details_group)

    def setup_system_metrics_compact(self, layout):
        metrics_group = QGroupBox("Calibration Métriques Système")
        metrics_group.setStyleSheet(self.get_groupbox_style(COLORS['primary']))
        grid = QGridLayout(metrics_group)
        grid.setSpacing(UGS.get_spacing_system()['xs'])

        # Créer et attacher les attributs requis
        self.sensors_status = QLabel("● Non connectés")
        self.acquisition_status = QLabel("● Arrêtée")
        self.calibration_status = QLabel("● Non effectuée")
        self.analysis_status = QLabel("● Aucune donnée")
        for lab in (
            self.sensors_status,
            self.acquisition_status,
            self.calibration_status,
            self.analysis_status,
        ):
            lab.setFixedHeight(UGS.get_height_sequence()['label'])
            lab.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")

        grid.addWidget(QLabel("Capteurs:"), 0, 0)
        grid.addWidget(self.sensors_status, 0, 1)
        grid.addWidget(QLabel("Acquisition:"), 1, 0)
        grid.addWidget(self.acquisition_status, 1, 1)
        grid.addWidget(QLabel("Calibration:"), 2, 0)
        grid.addWidget(self.calibration_status, 2, 1)
        grid.addWidget(QLabel("Analyse:"), 3, 0)
        grid.addWidget(self.analysis_status, 3, 1)

        # Barre de progression système
        self.system_progress = QProgressBar()
        self.system_progress.setRange(0, 100)
        self.system_progress.setValue(25)
        grid.addWidget(QLabel("Progression:"), 4, 0)
        grid.addWidget(self.system_progress, 4, 1)

        layout.addWidget(metrics_group)

    def setup_recent_activity_compact(self, layout):
        activity_group = QGroupBox("Activité Activité Récente")
        activity_group.setStyleSheet(self.get_groupbox_style(COLORS['warning']))
        v = QVBoxLayout(activity_group); v.setSpacing(UGS.get_spacing_system()['xs'])
        for text in ["Projet créé et ouvert", "Interface dashboard initialisée", "Navigation modules configurée"]:
            lab = QLabel(f"• {text}"); lab.setFixedHeight(UGS.get_height_sequence()['label'])
            lab.setStyleSheet(f"color: {COLORS['text_secondary']}; background-color: {COLORS['surface']}; padding: 4px 8px; border-radius: 4px;")
            v.addWidget(lab)
        layout.addWidget(activity_group)

    def setup_module_shortcuts_compact(self, layout):
        shortcuts_group = QGroupBox("Démarrer Accès Rapide")
        shortcuts_group.setStyleSheet(self.get_groupbox_style(COLORS['success']))
        grid = QGridLayout(shortcuts_group); grid.setSpacing(UGS.get_spacing_system()['sm'])
        shortcuts = [
            ("Calibration Calibration", COLORS['warning']),
            ("Acquisition Acquisition", COLORS['primary']),
            ("Statistique Statistique", COLORS['secondary']),
            ("Analyses Avancée", COLORS['warning']),
            ("Export Export", COLORS['success']),
        ]
        positions = [(0,0), (0,1), (0,2), (1,0), (1,1)]
        for (name, color), (r, c) in zip(shortcuts, positions):
            btn = QPushButton(name); btn.setFixedHeight(UGS.get_height_sequence()['button'])
            btn.setStyleSheet(f"""
                QPushButton {{ background-color: {color}; color: white; border: none; border-radius: 6px; font-weight: bold; font-size: 11px; }}
                QPushButton:hover {{ background-color: {self.darken_color(color)}; }}
            """)
            grid.addWidget(btn, r, c)
        layout.addWidget(shortcuts_group)
        
    def setup_timers(self):
        """Configuration des timers pour mises à jour"""
        # Timer pour la date/heure
        self.datetime_timer = QTimer()
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start(1000)  # Mise à jour toutes les secondes
        
        # Timer pour les métriques système (simulation)
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.update_system_metrics)
        self.metrics_timer.start(5000)  # Mise à jour toutes les 5 secondes
        
        # Initialisation immédiate
        self.update_datetime()
        
    def update_datetime(self):
        """Mise à jour de la date et heure"""
        from datetime import datetime
        now = datetime.now()
        self.datetime_label.setText(now.strftime("%A %d %B %Y - %H:%M:%S"))
        
    def update_system_metrics(self):
        """Mise à jour des métriques système (simulation)"""
        # Protéger contre des attributs manquants
        if not hasattr(self, "sensors_status") or not hasattr(self, "system_progress"):
            return
        import random
        if random.random() < 0.3 and self.sensors_status.text() == "● Non connectés":
            self.sensors_status.setText("✓ Connectés")
            self.sensors_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
        current_value = self.system_progress.value()
        if current_value < 100:
            self.system_progress.setValue(min(100, current_value + random.randint(1, 5)))
            
    def darken_color(self, color: str) -> str:
        """Assombrir une couleur pour l'effet hover"""
        # Simplification - retourner une couleur plus sombre
        if color == COLORS['primary']:
            return '#1A365D'
        elif color == COLORS['secondary']:
            return '#2C5AA0'
        elif color == COLORS['success']:
            return '#2F855A'
        elif color == COLORS['warning']:
            return '#C05621'
        else:
            return color
            
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet(f"""
            ProjectDashboardPanel {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
        
    def update_project_info(self, project: ProjectInfo):
        """Mise à jour des informations projet"""
        self.current_project = project
        
        # Mettre à jour les labels
        # TODO: Implémenter la mise à jour des labels de détails du projet
        
    def update_system_status(self, status_updates: dict):
        """Mise à jour de l'état système"""
        # TODO: Implémenter la mise à jour des états système
        pass
