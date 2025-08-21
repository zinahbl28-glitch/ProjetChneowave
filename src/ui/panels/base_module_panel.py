from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGroupBox, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from ..components.app_state import ProjectInfo
from ..resources.styles import COLORS


class BaseModulePanel(QWidget):
    """Base pour tous les panels de modules"""
    
    def __init__(self, module_name: str, module_title: str, module_description: str, parent=None):
        super().__init__(parent)
        self.module_name = module_name
        self.module_title = module_title
        self.module_description = module_description
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface de base"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        
        # En-tête du module
        self.setup_module_header(main_layout)
        
        # Zone de contenu principal (placeholder)
        self.setup_content_area(main_layout)
        
        # Zone d'état et actions
        self.setup_status_area(main_layout)
        
        # Espace flexible
        main_layout.addStretch()
        
    def setup_module_header(self, layout):
        """Configuration de l'en-tête du module"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setLineWidth(2)
        header_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                background-color: {COLORS['surface']};
                padding: 15px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(8)
        
        # Titre du module
        title_label = QLabel(self.module_title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {COLORS['primary']};")
        header_layout.addWidget(title_label)
        
        # Description du module
        desc_label = QLabel(self.module_description)
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        desc_label.setWordWrap(True)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def setup_content_area(self, layout):
        """Configuration de la zone de contenu principal"""
        content_group = QGroupBox("Contenu du Module")
        content_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['secondary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        content_layout = QVBoxLayout(content_group)
        content_layout.setSpacing(15)
        
        # Message "Coming Soon"
        coming_soon_label = QLabel("Module en cours de développement")
        coming_soon_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        coming_soon_label.setAlignment(Qt.AlignCenter)
        coming_soon_label.setStyleSheet(f"color: {COLORS['warning']};")
        content_layout.addWidget(coming_soon_label)
        
        # Description détaillée
        detailed_desc = QLabel(
            f"Le module '{self.module_title}' sera implémenté dans les phases suivantes.\n"
            "Il fournira toutes les fonctionnalités nécessaires pour {self.module_description.lower()}."
        )
        detailed_desc.setAlignment(Qt.AlignCenter)
        detailed_desc.setStyleSheet(f"color: {COLORS['text_secondary']};")
        detailed_desc.setWordWrap(True)
        content_layout.addWidget(detailed_desc)
        
        # Barre de progression de développement
        dev_progress_label = QLabel("Progression du développement:")
        dev_progress_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold;")
        content_layout.addWidget(dev_progress_label)
        
        self.dev_progress_bar = QProgressBar()
        self.dev_progress_bar.setRange(0, 100)
        self.dev_progress_bar.setValue(15)  # Valeur de démonstration
        self.dev_progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['primary']};
                border-radius: 6px;
                text-align: center;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['warning']};
                border-radius: 4px;
            }}
        """)
        content_layout.addWidget(self.dev_progress_bar)
        
        layout.addWidget(content_group)
        
    def setup_status_area(self, layout):
        """Configuration de la zone d'état et actions"""
        status_group = QGroupBox("Informations et Actions")
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
        status_layout.setSpacing(15)
        
        # Informations sur le module
        info_label = QLabel(
            f"Module: {self.module_name}\n"
            f"Phase de développement: Phase 5+\n"
            f"Disponibilité estimée: Prochaine itération"
        )
        info_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: normal;")
        info_label.setWordWrap(True)
        status_layout.addWidget(info_label)
        
        # Boutons d'action (placeholder)
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        # Bouton de démonstration
        demo_btn = QPushButton("Démo Module")
        demo_btn.setMinimumHeight(40)
        demo_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary']};
            }}
        """)
        demo_btn.clicked.connect(self.on_demo_clicked)
        actions_layout.addWidget(demo_btn)
        
        # Bouton d'aide
        help_btn = QPushButton("Aide")
        help_btn.setMinimumHeight(40)
        help_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
            }}
        """)
        help_btn.clicked.connect(self.on_help_clicked)
        actions_layout.addWidget(help_btn)
        
        status_layout.addLayout(actions_layout)
        
        layout.addWidget(status_group)
        
    def on_demo_clicked(self):
        """Gestionnaire de clic sur le bouton démo"""
        # Simulation d'une démonstration
        self.dev_progress_bar.setValue(25)
        
        # Message d'information
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Démo Module",
            f"Ceci est une démonstration du module '{self.module_title}'.\n\n"
            "Le module sera pleinement fonctionnel dans les phases suivantes."
        )
        
    def on_help_clicked(self):
        """Gestionnaire de clic sur le bouton d'aide"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Aide Module",
            f"Module: {self.module_title}\n\n"
            f"Description: {self.module_description}\n\n"
            "Ce module est en cours de développement et sera disponible dans les prochaines phases.\n\n"
            "Pour plus d'informations, consultez la documentation du projet."
        )
        
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet(f"""
            BaseModulePanel {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
        
    def update_development_progress(self, progress: int):
        """Mettre à jour la barre de progression de développement"""
        if hasattr(self, 'dev_progress_bar'):
            self.dev_progress_bar.setValue(max(0, min(100, progress)))
            
    def set_module_info(self, title: str = None, description: str = None):
        """Mettre à jour les informations du module"""
        if title:
            self.module_title = title
        if description:
            self.module_description = description
            
        # TODO: Mettre à jour l'affichage si nécessaire
