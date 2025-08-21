from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QListWidget, QListWidgetItem, QFrame,
    QScrollArea, QWidget, QSizePolicy
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QIcon
from typing import List, Optional
import os
from datetime import datetime

from ..components.app_state import ProjectInfo
from ..components.ui_config_manager import UIConfigManager
from ..components.recent_projects_manager import RecentProjectsManager
from ..resources.styles import COLORS


class ProjectCard(QFrame):
    """Widget pour afficher un projet dans la liste des projets récents"""
    
    def __init__(self, project: ProjectInfo, parent=None):
        super().__init__(parent)
        self.project = project
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface de la carte projet"""
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        self.setMidLineWidth(1)
        self.setStyleSheet(f"""
            ProjectCard {{
                background-color: {COLORS['surface']};
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
            }}
            ProjectCard:hover {{
                border-color: {COLORS['secondary']};
                background-color: {COLORS['background']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        # Nom du projet (gras)
        name_label = QLabel(self.project.name)
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        name_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(name_label)
        
        # Code projet
        code_label = QLabel(f"Code: {self.project.code}")
        code_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(code_label)
        
        # Ingénieur
        engineer_label = QLabel(f"Ingénieur: {self.project.engineer}")
        engineer_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(engineer_label)
        
        # Échelle et type
        details_label = QLabel(f"Échelle: {self.project.scale} | Type: {self.project.basin_type}")
        details_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(details_label)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(36)


class ProjectManager(QDialog):
    """Fenêtre d'accueil principale - Créer/Importer projet + projets récents"""
    
    project_selected = Signal(ProjectInfo)
    new_project_requested = Signal()
    import_project_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__()
        self.config_manager = UIConfigManager()
        self.recent_projects_manager = RecentProjectsManager()
        self.setup_ui()
        self.load_recent_projects()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface principale"""
        self.setWindowTitle("CHNeoWave - Gestionnaire de Projets")
        self.setModal(True)
        self.resize(900, 700)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # En-tête avec logo
        self.setup_header(main_layout)
        
        # Boutons d'action principaux
        self.setup_action_buttons(main_layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['primary']};")
        main_layout.addWidget(separator)
        
        # Section projets récents
        self.setup_recent_projects_section(main_layout)
        
    def setup_header(self, layout):
        """Configuration de l'en-tête avec logo et titre"""
        header_layout = QHBoxLayout()
        
        # Logo CHNeoWave (texte stylisé pour l'instant)
        logo_label = QLabel("CHNeoWave")
        logo_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        logo_label.setStyleSheet(f"color: {COLORS['primary']};")
        header_layout.addWidget(logo_label)
        
        header_layout.addStretch()
        
        # Sous-titre
        subtitle_label = QLabel("Système d'Acquisition et d'Analyse Maritime")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        
    def setup_action_buttons(self, layout):
        """Configuration des boutons d'action principaux"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)
        
        # Bouton Créer Nouveau Projet
        new_project_btn = QPushButton("Créer Nouveau Projet")
        new_project_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        new_project_btn.setMinimumHeight(36)
        new_project_btn.clicked.connect(self.on_new_project_clicked)
        new_project_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #2F855A;
            }}
        """)
        buttons_layout.addWidget(new_project_btn)
        
        # Bouton Importer Projet
        import_btn = QPushButton("Importer Projet Existant")
        import_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        import_btn.setMinimumHeight(36)
        import_btn.clicked.connect(self.on_import_project_clicked)
        import_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #2C5AA0;
            }}
        """)
        buttons_layout.addWidget(import_btn)
        
        layout.addLayout(buttons_layout)
        
    def setup_recent_projects_section(self, layout):
        """Configuration de la section projets récents"""
        # Titre de section
        section_title = QLabel(" Projets Récents")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        section_title.setStyleSheet(f"color: {COLORS['text_primary']}; margin-bottom: 10px;")
        layout.addWidget(section_title)
        
        # Zone de défilement pour les projets
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                background-color: {COLORS['background']};
            }}
        """)
        
        # Widget conteneur pour les projets
        self.projects_container = QWidget()
        self.projects_layout = QVBoxLayout(self.projects_container)
        self.projects_layout.setSpacing(8)
        self.projects_layout.setContentsMargins(16, 16, 16, 16)
        
        scroll_area.setWidget(self.projects_container)
        layout.addWidget(scroll_area)
        
    def load_recent_projects(self):
        """Chargement des projets récents depuis QSettings"""
        try:
            # Charger depuis le gestionnaire de projets récents
            recent_projects = self.recent_projects_manager.get_recent_projects()
            
            if not recent_projects:
                # Si aucun projet récent, afficher des projets de démonstration
                demo_projects = [
                    ProjectInfo(
                        name="Projet Canal de Suez",
                        code="CHW-2024-001",
                        engineer="Dr. Ahmed Hassan",
                        manager="Prof. Marie Dubois",
                        scale="1:100",
                        basin_type="Canal"
                    ),
                    ProjectInfo(
                        name="Étude Port de Marseille",
                        code="CHW-2024-002", 
                        engineer="Ing. Jean Moreau",
                        manager="Dr. Sophie Martin",
                        scale="1:50",
                        basin_type="Port"
                    ),
                    ProjectInfo(
                        name="Test Bassin de Carène",
                        code="CHW-2024-003",
                        engineer="Tech. Pierre Durand",
                        manager="Prof. Claude Bernard",
                        scale="1:25",
                        basin_type="Bassin"
                    )
                ]
                self.display_projects(demo_projects)
            else:
                self.display_projects(recent_projects)
                
        except Exception as e:
            print(f"[ProjectManager] Erreur lors du chargement des projets récents: {e}")
            # Fallback vers projets de démonstration
            self.load_demo_projects()
            
    def load_demo_projects(self):
        """Chargement des projets de démonstration en cas d'erreur"""
        demo_projects = [
            ProjectInfo(
                name="Projet Canal de Suez",
                code="CHW-2024-001",
                engineer="Dr. Ahmed Hassan",
                manager="Prof. Marie Dubois",
                scale="1:100",
                basin_type="Canal"
            ),
            ProjectInfo(
                name="Étude Port de Marseille",
                code="CHW-2024-002", 
                engineer="Ing. Jean Moreau",
                manager="Dr. Sophie Martin",
                scale="1:50",
                basin_type="Port"
            ),
            ProjectInfo(
                name="Test Bassin de Carène",
                code="CHW-2024-003",
                engineer="Tech. Pierre Durand",
                manager="Prof. Claude Bernard",
                scale="1:25",
                basin_type="Bassin"
            )
        ]
        self.display_projects(demo_projects)
        
    def display_projects(self, projects: List[ProjectInfo]):
        """Affichage de la liste des projets"""
        # Nettoyer la liste existante
        for i in reversed(range(self.projects_layout.count())):
            child = self.projects_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        if not projects:
            # Message si aucun projet
            no_projects_label = QLabel("Aucun projet récent trouvé.\nCréez votre premier projet !")
            no_projects_label.setAlignment(Qt.AlignCenter)
            no_projects_label.setStyleSheet(f"""
                color: {COLORS['text_secondary']};
                font-style: italic;
                padding: 8px;
            """)
            self.projects_layout.addWidget(no_projects_label)
        else:
            # Ajouter chaque projet
            for project in projects:
                project_card = ProjectCard(project)
                project_card.mousePressEvent = lambda e, p=project: self.on_project_selected(p)
                self.projects_layout.addWidget(project_card)
        
        self.projects_layout.addStretch()
        
    def on_new_project_clicked(self):
        """Gestionnaire clic bouton nouveau projet"""
        self.new_project_requested.emit()
        
    def on_import_project_clicked(self):
        """Gestionnaire clic bouton importer projet"""
        self.import_project_requested.emit()
        
    def on_project_selected(self, project: ProjectInfo):
        """Gestionnaire sélection d'un projet"""
        self.project_selected.emit(project)
        
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet(f"""
            ProjectManager {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
