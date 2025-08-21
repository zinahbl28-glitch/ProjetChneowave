"""
CHNeoWave - Interface Scientifique Moderne
Dashboard principal avec design maritime professionnel et navigation scientifique
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QLabel, QFrame, QMenuBar, QStatusBar, QStackedWidget,
    QPushButton, QGroupBox, QGridLayout, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPalette, QAction, QIcon, QPixmap

from ..components.app_state import ProjectInfo
from ..resources.scientific_design_system import ScientificDesignSystem
from ..components.scientific.scientific_sidebar import ScientificNavigationSidebar
from ..components.scientific.scientific_header import ScientificHeader
from ..panels.scientific.calibration_scientific_panel import CalibrationScientificPanel
from ..panels.scientific.acquisition_scientific_panel import AcquisitionScientificPanel
from ..panels.scientific.analysis_scientific_panel import AnalysisScientificPanel
from ..panels.scientific.advanced_analysis_panel import AdvancedAnalysisPanel
from ..panels.scientific.export_scientific_panel import ExportScientificPanel


class ScientificMainDashboard(QMainWindow):
    """Dashboard scientifique principal avec design maritime professionnel"""
    
    def __init__(self, project: ProjectInfo = None, parent=None):
        super().__init__(parent)
        self.current_project = project
        self.current_module = "dashboard"
        
        # Initialisation de l'interface scientifique
        self._setup_scientific_window()
        self._setup_scientific_ui()
        self._setup_scientific_menu()
        self._setup_scientific_status()
        self._setup_module_panels()
        self._setup_animations()
        self._setup_timers()
        
        # Afficher le dashboard
        self.show()
        
    def _setup_scientific_window(self):
        """Configuration de la fenêtre scientifique"""
        self.setWindowTitle("CHNeoWave - Interface Scientifique Maritime")
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
        # Taille optimale pour travail scientifique
        self.resize(1400, 900)
        self.setMinimumSize(1200, 700)
        
        # Style scientifique maritime
        ScientificDesignSystem.apply_scientific_stylesheet(self, 'scientific_window')
        self.setPalette(ScientificDesignSystem.create_scientific_palette())
        
    def _setup_scientific_ui(self):
        """Interface scientifique complète"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # ===== SIDEBAR SCIENTIFIQUE =====
        self.scientific_sidebar = ScientificNavigationSidebar(self.current_project)
        self.scientific_sidebar.module_changed.connect(self._on_module_changed)
        self.scientific_sidebar.return_to_projects.connect(self._on_return_to_projects)
        
        # ===== CONTENT AREA SCIENTIFIQUE =====
        self.content_area = self._create_scientific_content_area()
        
        # ===== SPLITTER AVEC ANIMATIONS =====
        self.setup_scientific_splitter()
        
    def _create_scientific_content_area(self):
        """Crée la zone de contenu scientifique"""
        content_widget = QWidget()
        content_widget.setObjectName("scientific_content_area")
        
        # Style scientifique pour la zone de contenu
        colors = ScientificDesignSystem.get_scientific_colors()
        content_widget.setStyleSheet(f"""
            QWidget#scientific_content_area {{
                background: {colors['bg_primary']};
                border: none;
            }}
        """)
        
        # Layout du contenu
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(6)
        
        # Header scientifique
        header_container = self._create_scientific_header()
        content_layout.addWidget(header_container)
        
        # Zone des modules (stacked widget)
        self.module_stack = QStackedWidget()
        self.module_stack.setObjectName("scientific_module_stack")
        content_layout.addWidget(self.module_stack)
        
        return content_widget
        
    def _create_scientific_header(self):
        """Crée l'en-tête scientifique"""
        header_widget = ScientificHeader(self.current_project)
        return header_widget
        
    def setup_scientific_splitter(self):
        """Configure le splitter avec animations"""
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(2)
        
        # Ajouter les widgets
        self.main_splitter.addWidget(self.scientific_sidebar)
        self.main_splitter.addWidget(self.content_area)
        
        # Proportions selon le ratio d'or (61.8% / 38.2%)
        self.main_splitter.setSizes([382, 618])
        
        self.main_layout.addWidget(self.main_splitter)
        
    def _setup_scientific_menu(self):
        """Configuration du menu scientifique"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu('&Fichier')
        
        new_project_action = QAction('&Nouveau Projet', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.triggered.connect(self._on_new_project)
        file_menu.addAction(new_project_action)
        
        open_project_action = QAction('&Ouvrir Projet', self)
        open_project_action.setShortcut('Ctrl+O')
        open_project_action.triggered.connect(self._on_open_project)
        file_menu.addAction(open_project_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('&Exporter Données', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self._on_export_data)
        file_menu.addAction(export_action)
        
        # Menu Édition
        edit_menu = menubar.addMenu('&Édition')
        
        preferences_action = QAction('&Préférences', self)
        preferences_action.triggered.connect(self._on_preferences)
        edit_menu.addAction(preferences_action)
        
        # Menu Affichage
        view_menu = menubar.addMenu('&Affichage')
        
        fullscreen_action = QAction('&Plein Écran', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.triggered.connect(self._on_toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu('&Outils')
        
        calibration_action = QAction('&Calibration', self)
        calibration_action.triggered.connect(lambda: self._switch_module('calibration'))
        tools_menu.addAction(calibration_action)
        
        acquisition_action = QAction('&Acquisition', self)
        acquisition_action.triggered.connect(lambda: self._switch_module('acquisition'))
        tools_menu.addAction(acquisition_action)
        
        # Menu Aide
        help_menu = menubar.addMenu('&Aide')
        
        about_action = QAction('&À Propos', self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
        
    def _setup_scientific_status(self):
        """Configuration de la barre de statut scientifique"""
        status_bar = self.statusBar()
        
        # Indicateur de projet
        self.project_status_label = QLabel("Aucun projet actif")
        status_bar.addWidget(self.project_status_label)
        
        # Indicateur de module
        self.module_status_label = QLabel("Dashboard")
        status_bar.addPermanentWidget(self.module_status_label)
        
        # Indicateur de connexion
        self.connection_status_label = QLabel("●")
        self.connection_status_label.setStyleSheet("color: #10B981; font-weight: bold;")
        status_bar.addPermanentWidget(self.connection_status_label)
        
    def _setup_module_panels(self):
        """Configuration des panneaux de modules scientifiques"""
        # Dashboard principal
        self.dashboard_panel = self._create_scientific_dashboard()
        self.module_stack.addWidget(self.dashboard_panel)
        
        # Module Calibration
        self.calibration_panel = CalibrationScientificPanel()
        self.module_stack.addWidget(self.calibration_panel)
        
        # Module Acquisition
        self.acquisition_panel = AcquisitionScientificPanel()
        self.module_stack.addWidget(self.acquisition_panel)
        
        # Module Analyse Statistique
        self.analysis_panel = AnalysisScientificPanel()
        self.module_stack.addWidget(self.analysis_panel)
        
        # Module Analyse Avancée
        self.advanced_panel = AdvancedAnalysisPanel()
        self.module_stack.addWidget(self.advanced_panel)
        
        # Module Export
        self.export_panel = ExportScientificPanel()
        self.module_stack.addWidget(self.export_panel)
        
    def _create_scientific_dashboard(self):
        """Crée le dashboard scientifique principal"""
        dashboard_widget = QWidget()
        dashboard_widget.setObjectName("scientific_dashboard")
        
        # Style du dashboard
        colors = ScientificDesignSystem.get_scientific_colors()
        dashboard_widget.setStyleSheet(f"""
            QWidget#scientific_dashboard {{
                background: {colors['bg_primary']};
                color: {colors['text_primary']};
            }}
        """)
        
        # Layout principal
        layout = QVBoxLayout(dashboard_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Titre du dashboard
        title_label = QLabel("Dashboard Scientifique CHNeoWave")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet(f"color: {colors['primary']}; margin-bottom: 8px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Sous-titre
        subtitle_label = QLabel("Interface d'acquisition et d'analyse de données maritimes")
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setStyleSheet(f"color: {colors['text_secondary']}; margin-bottom: 20px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Grille des modules
        modules_grid = QGridLayout()
        modules_grid.setSpacing(16)
        
        # Cartes des modules
        modules = [
            ("Calibration", "Calibration des sondes et capteurs", "🔧"),
            ("Acquisition", "Acquisition de données en temps réel", "📡"),
            ("Analyse", "Analyse statistique des données", "📊"),
            ("Analyse Avancée", "Analyse spectrale et Goda", "🔬"),
            ("Export", "Export et génération de rapports", "📤")
        ]
        
        for i, (title, description, icon) in enumerate(modules):
            card = self._create_module_card(title, description, icon)
            row = i // 3
            col = i % 3
            modules_grid.addWidget(card, row, col)
        
        layout.addLayout(modules_grid)
        layout.addStretch()
        
        return dashboard_widget
        
    def _create_module_card(self, title, description, icon):
        """Crée une carte de module"""
        card = QFrame()
        card.setObjectName("module_card")
        card.setFixedSize(300, 150)
        
        colors = ScientificDesignSystem.get_scientific_colors()
        card.setStyleSheet(f"""
            QFrame#module_card {{
                background: {colors['surface']};
                border: 2px solid {colors['border']};
                border-radius: 12px;
                padding: 16px;
            }}
            QFrame#module_card:hover {{
                border-color: {colors['primary']};
                background: {colors['surface_hover']};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Icône
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 24))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Titre
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {colors['primary']};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setStyleSheet(f"color: {colors['text_secondary']};")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return card
        
    def _setup_animations(self):
        """Configuration des animations"""
        self.animations = {}
        
    def _setup_timers(self):
        """Configuration des timers"""
        # Timer pour mise à jour du statut
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(1000)  # Mise à jour chaque seconde
        
    def _on_module_changed(self, module_name):
        """Gestion du changement de module"""
        module_map = {
            "dashboard": 0,
            "calibration": 1,
            "acquisition": 2,
            "analysis": 3,
            "advanced": 4,
            "export": 5
        }
        
        if module_name in module_map:
            self.module_stack.setCurrentIndex(module_map[module_name])
            self.current_module = module_name
            self.module_status_label.setText(module_name.title())
            
    def _switch_module(self, module_name):
        """Change de module programmatiquement"""
        self.scientific_sidebar.select_module(module_name)
        
    def _on_return_to_projects(self):
        """Retour à la gestion des projets"""
        # Émettre un signal pour retourner à la fenêtre de projets
        pass
        
    def _update_status(self):
        """Mise à jour du statut"""
        # Mise à jour de la date/heure
        from datetime import datetime
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Mise à jour du statut du projet
        if self.current_project:
            self.project_status_label.setText(f"Projet: {self.current_project.name}")
        else:
            self.project_status_label.setText("Aucun projet actif")
            
    def _on_new_project(self):
        """Création d'un nouveau projet"""
        # Ouvrir le wizard de création de projet
        pass
        
    def _on_open_project(self):
        """Ouverture d'un projet existant"""
        # Ouvrir le dialogue d'import de projet
        pass
        
    def _on_export_data(self):
        """Export des données"""
        self._switch_module('export')
        
    def _on_preferences(self):
        """Ouverture des préférences"""
        pass
        
    def _on_toggle_fullscreen(self):
        """Basculement plein écran"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def _on_about(self):
        """Affichage de la boîte de dialogue À propos"""
        pass