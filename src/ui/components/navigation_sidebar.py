from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QIcon

from .app_state import ProjectInfo
from ..resources.styles import COLORS
from ..resources.universal_golden_system import UniversalGoldenSystem as UGS


class NavigationSidebar(QWidget):
    """Sidebar de navigation avec 5 modules et informations projet"""
    
    module_changed = Signal(str)  # nom du module
    return_to_project_manager = Signal()
    
    def __init__(self, project: ProjectInfo, parent=None):
        super().__init__(parent)
        self.current_project = project
        self.current_module = "dashboard"
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface de la sidebar"""
        # Largeur basée sur φ (38.2% de 1400px => ~533px)
        dims = UGS.get_main_layout_dimensions()
        self.setFixedWidth(dims['sidebar_width'])
        
        # Layout principal avec système φ
        spacing = UGS.get_spacing_system()
        heights = UGS.get_height_sequence()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
        main_layout.setSpacing(spacing['sm'])

        self.setup_header(main_layout)
        self.setup_project_info(main_layout)
        self.setup_module_navigation(main_layout)
        self.setup_system_status(main_layout)
        self.setup_return_button(main_layout)

        main_layout.addStretch()
        
    def setup_header(self, layout):
        """Configuration de l'en-tête de la sidebar"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setLineWidth(2)
        header_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                background-color: {COLORS['surface']};
                padding: 10px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(5)
        
        # Logo CHNeoWave
        logo_label = QLabel("CHNeoWave")
        logo_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"color: {COLORS['primary']};")
        header_layout.addWidget(logo_label)
        
        # Sous-titre
        subtitle_label = QLabel("Système d'Acquisition Maritime")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
    def setup_project_info(self, layout):
        """Configuration des informations projet"""
        project_group = QGroupBox("Informations Projet")
        project_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['secondary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        project_layout = QVBoxLayout(project_group)
        project_layout.setSpacing(8)
        
        # Nom du projet
        self.project_name_label = QLabel(f"Nom: {self.current_project.name}")
        self.project_name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: normal;")
        project_layout.addWidget(self.project_name_label)
        
        # Code projet
        self.project_code_label = QLabel(f"Code: {self.current_project.code}")
        self.project_code_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: normal;")
        project_layout.addWidget(self.project_code_label)
        
        # Ingénieur
        self.project_engineer_label = QLabel(f"Ingénieur: {self.current_project.engineer}")
        self.project_engineer_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: normal;")
        project_layout.addWidget(self.project_engineer_label)
        
        # Échelle et type
        self.project_details_label = QLabel(f"Échelle: {self.current_project.scale} | Type: {self.current_project.basin_type}")
        self.project_details_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: normal;")
        project_layout.addWidget(self.project_details_label)
        
        layout.addWidget(project_group)
        
    def setup_module_navigation(self, layout):
        """Configuration de la navigation des modules"""
        navigation_group = QGroupBox("Navigation Modules")
        navigation_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        navigation_layout = QVBoxLayout(navigation_group)
        navigation_layout.setSpacing(8)
        
        # Définition des modules
        self.modules = [
            ("dashboard", "Dashboard", "Vue d'ensemble du projet", COLORS['success']),
            ("calibration", "Calibration", "Calibration des sondes", COLORS['warning']),
            ("acquisition", "Acquisition", "Acquisition temps réel", COLORS['primary']),
            ("stats", "Statistique", "Analyse statistique", COLORS['secondary']),
            ("advanced", "Avancée", "Analyses avancées (Goda, FFT)", COLORS['warning']),
            ("export", "Export", "Export des résultats", COLORS['success'])
        ]
        
        # Création des boutons de navigation
        self.module_buttons = {}
        for module_id, module_name, module_desc, module_color in self.modules:
            button = self.create_module_button(module_id, module_name, module_desc, module_color)
            self.module_buttons[module_id] = button
            navigation_layout.addWidget(button)
            
        # Marquer le dashboard comme actif par défaut
        self.set_active_module("dashboard")
        
        layout.addWidget(navigation_group)

        # Ajuster dynamiquement la hauteur des boutons pour remplir la section
        section_height = UGS.get_height_sequence()['section_xl']
        margins = 40
        per_btn = max(36, int((section_height - margins) / max(1, len(self.modules))))
        for btn in self.module_buttons.values():
            btn.setFixedHeight(per_btn)
        
    def create_module_button(self, module_id: str, module_name: str, module_desc: str, module_color: str):
        """Création d'un bouton de module"""
        button = QPushButton()
        button.setObjectName(f"module_{module_id}")
        # Hauteur fixe et fonctionnelle
        button.setMinimumHeight(UGS.get_height_sequence()['button'])
        button.setCheckable(True)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['surface']};
                border: 2px solid {COLORS['primary']};
                border-radius: 6px;
                padding: 8px;
                text-align: left;
                font-weight: bold;
                color: {COLORS['text_primary']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['background']};
                border-color: {module_color};
            }}
            QPushButton:checked {{
                background-color: {module_color};
                color: white;
                border-color: {module_color};
            }}
        """)
        
        # Layout du bouton avec icône, nom et description
        button_layout = QVBoxLayout(button)
        button_layout.setContentsMargins(8, 8, 8, 8)
        button_layout.setSpacing(2)
        
        # Nom du module
        name_label = QLabel(module_name)
        name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_label.setStyleSheet("color: inherit;")
        button_layout.addWidget(name_label)
        
        # Description du module
        desc_label = QLabel(module_desc)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet("color: inherit; font-weight: normal;")
        button_layout.addWidget(desc_label)
        
        # Connexion du signal
        button.clicked.connect(lambda checked, mid=module_id: self.on_module_button_clicked(mid))
        
        return button
        
    def setup_system_status(self, layout):
        """Configuration de l'état système"""
        status_group = QGroupBox("État Système")
        status_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['warning']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(8)
        
        # État des capteurs
        self.sensors_status_label = QLabel("• Capteurs: ● Non connectés")
        self.sensors_status_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: normal;")
        status_layout.addWidget(self.sensors_status_label)
        
        # État de l'acquisition
        self.acquisition_status_label = QLabel("• Acquisition: ● Arrêtée")
        self.acquisition_status_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: normal;")
        status_layout.addWidget(self.acquisition_status_label)
        
        # État de la calibration
        self.calibration_status_label = QLabel("• Calibration: ● Non effectuée")
        self.calibration_status_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: normal;")
        status_layout.addWidget(self.calibration_status_label)
        
        # État de l'analyse
        self.analysis_status_label = QLabel("• Analyse: ● Aucune donnée")
        self.analysis_status_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: normal;")
        status_layout.addWidget(self.analysis_status_label)
        
        layout.addWidget(status_group)
        
    def setup_return_button(self, layout):
        """Configuration du bouton retour"""
        return_button = QPushButton("← Retour au Gestionnaire de Projets")
        return_button.setMinimumHeight(40)
        return_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['text_secondary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['text_primary']};
            }}
        """)
        return_button.clicked.connect(self.on_return_clicked)
        
        layout.addWidget(return_button)
        
    def on_module_button_clicked(self, module_id: str):
        """Gestionnaire de clic sur un bouton de module"""
        # Désélectionner tous les boutons
        for button in self.module_buttons.values():
            button.setChecked(False)
            
        # Sélectionner le bouton cliqué
        if module_id in self.module_buttons:
            self.module_buttons[module_id].setChecked(True)
            self.current_module = module_id
            
        # Émettre le signal de changement de module
        self.module_changed.emit(module_id)
        
    def set_active_module(self, module_id: str):
        """Définir le module actif"""
        if module_id in self.module_buttons:
            self.on_module_button_clicked(module_id)
            
    def on_return_clicked(self):
        """Gestionnaire de clic sur le bouton retour"""
        self.return_to_project_manager.emit()
        
    def update_project_info(self, project: ProjectInfo):
        """Mise à jour des informations projet"""
        self.current_project = project
        
        # Mettre à jour les labels
        self.project_name_label.setText(f"Nom: {project.name}")
        self.project_code_label.setText(f"Code: {project.code}")
        self.project_engineer_label.setText(f"Ingénieur: {project.engineer}")
        self.project_details_label.setText(f"Échelle: {project.scale} | Type: {project.basin_type}")
        
    def update_system_status(self, status_updates: dict):
        """Mise à jour de l'état système"""
        # Exemple: status_updates = {"sensors": "connected", "acquisition": "running"}
        if "sensors" in status_updates:
            status = status_updates["sensors"]
            if status == "connected":
                self.sensors_status_label.setText("• Capteurs: ✓ Connectés")
                self.sensors_status_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: normal;")
            elif status == "warning":
                self.sensors_status_label.setText("• Capteurs: ◆ Attention")
                self.sensors_status_label.setStyleSheet(f"color: {COLORS['warning']}; font-weight: normal;")
            else:
                self.sensors_status_label.setText("• Capteurs: ● Non connectés")
                self.sensors_status_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: normal;")
                
        if "acquisition" in status_updates:
            status = status_updates["acquisition"]
            if status == "running":
                self.acquisition_status_label.setText("• Acquisition: ✓ En cours")
                self.acquisition_status_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: normal;")
            elif status == "paused":
                self.acquisition_status_label.setText("• Acquisition: ◆ En pause")
                self.acquisition_status_label.setStyleSheet(f"color: {COLORS['warning']}; font-weight: normal;")
            else:
                self.acquisition_status_label.setText("• Acquisition: ● Arrêtée")
                self.acquisition_status_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: normal;")
                
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet(f"""
            NavigationSidebar {{
                background-color: {COLORS['sidebar_bg'] if 'sidebar_bg' in COLORS else COLORS['background']};
                border-right: 2px solid {COLORS['primary']};
            }}
        """)
