from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QFrame, QStatusBar, QMenuBar, QMenu
)
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtCore import Qt, Signal, QTimer

from ..components.app_state import ProjectInfo
from ..components.navigation_sidebar import NavigationSidebar
from ..panels.project_dashboard_panel import ProjectDashboardPanel
from ..panels.calibration_panel import CalibrationPanel
from ..panels.acquisition_panel import AcquisitionPanel
from ..panels.stats_panel import StatsPanel
from ..panels.advanced_panel import AdvancedPanel
from ..panels.export_panel import ExportPanel
from ..resources.styles import COLORS
from ..resources.universal_golden_system import UniversalGoldenSystem as UGS


class MainDashboard(QMainWindow):
    """Dashboard principal CHNeoWave avec navigation 5 modules"""
    
    module_changed = Signal(str)  # nom du module
    project_updated = Signal(ProjectInfo)
    
    def __init__(self, project: ProjectInfo, file_path: str = ""):
        super().__init__()
        self.current_project = project
        self.current_file_path = file_path
        self.current_module = "dashboard"
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface principale"""
        self.setWindowTitle(f"CHNeoWave - {self.current_project.name} - Dashboard")
        # Dimensions basées sur UGS
        dims = UGS.get_main_layout_dimensions()
        self.setMinimumSize(1200, 800)
        self.resize(dims['window_width'], 900)
        
        # Widget central avec splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter pour sidebar + contenu principal
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Sidebar de navigation (30%)
        self.setup_sidebar()
        
        # Zone principale (70%)
        self.setup_main_content()
        
        # Configuration du splitter (φ exact 38.2/61.8)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setSizes([dims['sidebar_width'], dims['content_width']])
        self.main_splitter.setStretchFactor(0, 0)  # Sidebar ne s'étire pas
        self.main_splitter.setStretchFactor(1, 1)  # Contenu s'étire
        
    def setup_sidebar(self):
        """Configuration de la sidebar de navigation"""
        self.navigation_sidebar = NavigationSidebar(self.current_project)
        self.navigation_sidebar.module_changed.connect(self.on_module_changed)
        self.main_splitter.addWidget(self.navigation_sidebar)
        
    def setup_main_content(self):
        """Configuration de la zone de contenu principal"""
        # Widget conteneur pour le contenu
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(6)
        
        # Panneau d'accueil par défaut
        self.current_panel = ProjectDashboardPanel(self.current_project)
        self.content_layout.addWidget(self.current_panel)
        
        # Dictionnaire des panels de modules
        self.module_panels = {
            "dashboard": self.current_panel,
            "calibration": CalibrationPanel(),
            "acquisition": AcquisitionPanel(),
            "stats": StatsPanel(),
            "advanced": AdvancedPanel(),
            "export": ExportPanel()
        }
        
        self.main_splitter.addWidget(self.content_widget)
        
    def resizeEvent(self, event):
        """Maintenir les proportions φ lors du redimensionnement."""
        try:
            dims = UGS.get_main_layout_dimensions(self.width())
            # Ajuster largeur sidebar et splitter
            if hasattr(self, 'navigation_sidebar') and self.navigation_sidebar:
                self.navigation_sidebar.setFixedWidth(dims['sidebar_width'])
            if hasattr(self, 'main_splitter') and self.main_splitter:
                self.main_splitter.setSizes([dims['sidebar_width'], dims['content_width']])
        except Exception:
            pass
        super().resizeEvent(event)

    def setup_menu(self):
        """Configuration de la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("&Fichier")
        
        # Action Nouveau Projet
        new_project_action = QAction("&Nouveau Projet", self)
        new_project_action.setShortcut("Ctrl+N")
        new_project_action.triggered.connect(self.on_new_project)
        file_menu.addAction(new_project_action)
        
        # Action Ouvrir Projet
        open_project_action = QAction("&Ouvrir Projet", self)
        open_project_action.setShortcut("Ctrl+O")
        open_project_action.triggered.connect(self.on_open_project)
        file_menu.addAction(open_project_action)
        
        file_menu.addSeparator()
        
        # Action Quitter
        quit_action = QAction("&Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Projet
        project_menu = menubar.addMenu("&Projet")
        
        # Action Informations Projet
        project_info_action = QAction("&Informations Projet", self)
        project_info_action.triggered.connect(self.on_project_info)
        project_menu.addAction(project_info_action)
        
        # Action Paramètres Projet
        project_settings_action = QAction("&Paramètres Projet", self)
        project_settings_action.triggered.connect(self.on_project_settings)
        project_menu.addAction(project_settings_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("&Outils")
        
        # Action Préférences
        preferences_action = QAction("&Préférences", self)
        preferences_action.triggered.connect(self.on_preferences)
        tools_menu.addAction(preferences_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("&Aide")
        
        # Action À propos
        about_action = QAction("&À propos", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Configuration de la barre de statut"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Informations de base
        self.status_bar.addPermanentWidget(
            QLabel(f"Projet: {self.current_project.code}")
        )
        self.status_bar.addPermanentWidget(
            QLabel(f"Module: {self.current_module.title()}")
        )
        
        # Message principal
        self.status_bar.showMessage("Prêt")
        
    def on_module_changed(self, module_name: str):
        """Gestionnaire de changement de module"""
        self.current_module = module_name
        self.update_window_title()
        self.update_status_bar()
        
        # Changer le panel selon le module sélectionné
        self.switch_module_panel(module_name)
        
        self.status_bar.showMessage(f"Module {module_name} sélectionné")
        
    def update_window_title(self):
        """Mise à jour du titre de la fenêtre"""
        self.setWindowTitle(f"CHNeoWave - {self.current_project.name} - {self.current_module.title()}")
        
    def update_status_bar(self):
        """Mise à jour de la barre de statut"""
        # Mettre à jour le label du module
        for i in range(self.status_bar.children().__len__()):
            child = self.status_bar.children()[i]
            if isinstance(child, QLabel) and "Module:" in child.text():
                child.setText(f"Module: {self.current_module.title()}")
                break
                
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet(f"""
            MainDashboard {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QMainWindow {{
                background-color: {COLORS['background']};
            }}
            QMenuBar {{
                background-color: {COLORS['surface']};
                border-bottom: 2px solid {COLORS['primary']};
                color: {COLORS['text_primary']};
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
            QStatusBar {{
                background-color: {COLORS['surface']};
                border-top: 1px solid {COLORS['primary']};
                color: {COLORS['text_primary']};
            }}
        """)
        
    def set_module_panel(self, module_name: str, widget: QWidget):
        """Remplace le panel d'un module par un widget spécifique."""
        if not hasattr(self, 'module_panels'):
            return
        if module_name not in self.module_panels:
            return
        # Retirer l'ancien widget du layout
        old_widget = self.module_panels[module_name]
        if old_widget is not None:
            old_widget.setVisible(False)
            self.content_layout.removeWidget(old_widget)
            old_widget.setParent(None)
        # Ajouter et enregistrer le nouveau widget
        self.content_layout.addWidget(widget)
        widget.setVisible(False)
        self.module_panels[module_name] = widget
        # Si on remplace le panel courant, le réassigner
        if self.current_module == module_name:
            self.current_panel = widget

    # Gestionnaires d'actions du menu
    def on_new_project(self):
        """Gestionnaire action nouveau projet"""
        # TODO: Retourner au Project Manager
        self.status_bar.showMessage("Nouveau projet demandé")
        
    def on_open_project(self):
        """Gestionnaire action ouvrir projet"""
        # TODO: Ouvrir dialogue de sélection projet
        self.status_bar.showMessage("Ouverture projet demandée")
        
    def on_project_info(self):
        """Gestionnaire action informations projet"""
        # TODO: Afficher dialogue informations projet
        self.status_bar.showMessage("Informations projet demandées")
        
    def on_project_settings(self):
        """Gestionnaire action paramètres projet"""
        # TODO: Afficher dialogue paramètres projet
        self.status_bar.showMessage("Paramètres projet demandés")
        
    def on_preferences(self):
        """Gestionnaire action préférences"""
        # TODO: Afficher dialogue préférences
        self.status_bar.showMessage("Préférences demandées")
        
    def on_about(self):
        """Gestionnaire action à propos"""
        # TODO: Afficher dialogue à propos
        self.status_bar.showMessage("À propos demandé")
        
    def switch_module_panel(self, module_name: str):
        """Changer le panel affiché selon le module sélectionné"""
        if module_name not in self.module_panels:
            print(f"[MainDashboard] Module inconnu: {module_name}")
            return
            
        # Masquer le panel actuel
        if self.current_panel:
            self.current_panel.setVisible(False)
            
        # Récupérer et afficher le nouveau panel
        new_panel = self.module_panels[module_name]
        new_panel.setVisible(True)
        
        # Mettre à jour la référence
        self.current_panel = new_panel
        
        print(f"[MainDashboard] Panel changé vers: {module_name}")
        
    def update_project_info(self, project: ProjectInfo):
        """Mise à jour des informations projet"""
        self.current_project = project
        self.navigation_sidebar.update_project_info(project)
        self.update_window_title()
        self.update_status_bar()
        self.project_updated.emit(project)
        
    def closeEvent(self, event):
        """Gestion de la fermeture de la fenêtre"""
        # TODO: Sauvegarder l'état de la fenêtre
        event.accept()
