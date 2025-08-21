"""
Dashboard Principal Moderne - Design 2025
Interface principale avec sidebar moderne et contenu dynamique
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QLabel, QFrame, QMenuBar, QStatusBar, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QPalette, QAction

from ..resources.modern_design_system import ModernDesignSystem
from ..components.modern.modern_sidebar import ModernNavigationSidebar
from ..components.modern.modern_card import ModernCard, InfoCard, StatusCard, ActionCard
from ..components.app_state import ProjectInfo


class ModernMainDashboard(QMainWindow):
    """Dashboard principal moderne avec design 2025"""
    
    def __init__(self, project: ProjectInfo = None, parent=None):
        super().__init__(parent)
        self.current_project = project
        self.current_module = "dashboard"
        
        # Initialisation de l'interface
        self._setup_modern_window()
        self._setup_modern_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._setup_module_panels()
        self._setup_animations()
        self._setup_timers()
        
        # Afficher le dashboard
        self.show()
        
    def _setup_modern_window(self):
        """Configuration de la fenêtre moderne"""
        # Titre et icône
        self.setWindowTitle("CHNeoWave - Dashboard Moderne 2025")
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
        # Taille et position
        self.resize(1200, 800)
        self.setMinimumSize(1024, 600)
        
        # Style moderne
        ModernDesignSystem.apply_modern_stylesheet(self, 'modern_window')
        
        # Palette moderne
        self.setPalette(ModernDesignSystem.create_modern_palette())
        
    def _setup_modern_ui(self):
        """Interface moderne complète"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # ===== SIDEBAR MODERNE =====
        self.modern_sidebar = ModernNavigationSidebar(self.current_project)
        self.modern_sidebar.module_changed.connect(self._on_module_changed)
        self.modern_sidebar.return_to_projects.connect(self._on_return_to_projects)
        
        # ===== CONTENT AREA MODERNE =====
        self.content_area = self._create_modern_content_area()
        
        # ===== SPLITTER AVEC ANIMATIONS =====
        self.setup_modern_splitter()
        
    def _create_modern_content_area(self):
        """Crée la zone de contenu moderne"""
        content_widget = QWidget()
        content_widget.setObjectName("content_area")
        
        # Style moderne pour la zone de contenu
        colors = ModernDesignSystem.get_color_palette()
        content_widget.setStyleSheet(f"""
            QWidget#content_area {{
                background: {colors['bg_primary']};
                border: none;
            }}
        """)
        
        # Layout du contenu
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(6, 6, 6, 6)
        content_layout.setSpacing(4)
        
        # Header moderne
        header_container = self._create_modern_header()
        content_layout.addWidget(header_container)
        
        # Zone des modules (stacked widget)
        self.module_stack = QStackedWidget()
        self.module_stack.setObjectName("module_stack")
        self.module_stack.setStyleSheet(f"""
            QStackedWidget#module_stack {{
                background: transparent;
                border: none;
            }}
        """)
        content_layout.addWidget(self.module_stack)
        
        return content_widget
        
    def _create_modern_header(self):
        """Crée le header moderne"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Header container
        header_container = QFrame()
        header_container.setObjectName("modern_header")
        header_container.setStyleSheet(f"""
            QFrame#modern_header {{
                background: {colors['surface']};
                border-bottom: 1px solid {colors['border']};
                padding: {spacing['md']}px;
                min-height: 60px;
            }}
        """)
        
        # Layout du header
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(spacing['lg'])
        
        # Logo et titre
        logo_section = QWidget()
        logo_layout = QVBoxLayout(logo_section)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(spacing['xs'])
        
        # Logo CHNeoWave moderne
        logo_label = QLabel("CHNeoWave")
        logo_label.setFont(ModernDesignSystem.get_font('h1'))
        logo_label.setStyleSheet(f"color: {colors['primary']}; font-weight: bold;")
        logo_layout.addWidget(logo_label)
        
        # Sous-titre
        subtitle_label = QLabel("Dashboard Moderne 2025")
        subtitle_label.setFont(ModernDesignSystem.get_font('body_small'))
        subtitle_label.setStyleSheet(f"color: {colors['text_secondary']};")
        logo_layout.addWidget(subtitle_label)
        
        header_layout.addWidget(logo_section)
        header_layout.addStretch()
        
        # Informations du projet
        if self.current_project:
            self._create_project_header_info(header_layout)
        else:
            self._create_default_header_info(header_layout)
            
        # Actions rapides
        self._create_header_actions(header_layout)
        
        return header_container
        
    def _create_project_header_info(self, header_layout):
        """Crée les informations du projet dans le header"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container projet
        project_container = QFrame()
        project_container.setStyleSheet(f"""
            QFrame {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                padding: {spacing['md']}px;
            }}
        """)
        
        project_layout = QVBoxLayout(project_container)
        project_layout.setContentsMargins(0, 0, 0, 0)
        project_layout.setSpacing(spacing['xs'])
        
        # Nom du projet
        project_name = QLabel(self.current_project.name)
        project_name.setFont(ModernDesignSystem.get_font('h3'))
        project_name.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
        project_layout.addWidget(project_name)
        
        # Code et ingénieur
        details_layout = QHBoxLayout()
        details_layout.setSpacing(spacing['md'])
        
        code_label = QLabel(self.current_project.code)
        code_label.setFont(ModernDesignSystem.get_font('caption'))
        code_label.setStyleSheet(f"color: {colors['text_secondary']};")
        details_layout.addWidget(code_label)
        
        engineer_label = QLabel(self.current_project.engineer)
        engineer_label.setFont(ModernDesignSystem.get_font('caption'))
        engineer_label.setStyleSheet(f"color: {colors['text_secondary']};")
        details_layout.addWidget(engineer_label)
        
        project_layout.addLayout(details_layout)
        header_layout.addWidget(project_container)
        
    def _create_default_header_info(self, header_layout):
        """Crée les informations par défaut dans le header"""
        colors = ModernDesignSystem.get_color_palette()
        spacing = ModernDesignSystem.get_spacing_system()
        
        # Container par défaut
        default_container = QFrame()
        default_container.setStyleSheet(f"""
            QFrame {{
                background: {colors['surface_light']};
                border: 1px solid {colors['border']};
                border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
                padding: {spacing['md']}px;
            }}
        """)
        
        default_layout = QVBoxLayout(default_container)
        default_layout.setContentsMargins(0, 0, 0, 0)
        default_layout.setSpacing(spacing['xs'])
        
        # Message par défaut
        default_label = QLabel("Aucun projet sélectionné")
        default_label.setFont(ModernDesignSystem.get_font('body'))
        default_label.setStyleSheet(f"color: {colors['text_muted']}; font-style: italic;")
        default_layout.addWidget(default_label)
        
        header_layout.addWidget(default_container)
        
    def _create_header_actions(self, header_layout):
        """Crée les actions rapides dans le header"""
        from ..components.modern.modern_button import ModernButton
        
        # Container des actions
        actions_container = QWidget()
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)
        
        # Boutons d'action
        settings_btn = ModernButton("Paramètres", "ghost", "sm")
        help_btn = ModernButton("Aide", "ghost", "sm")
        profile_btn = ModernButton("Profil", "ghost", "sm")
        
        actions_layout.addWidget(settings_btn)
        actions_layout.addWidget(help_btn)
        actions_layout.addWidget(profile_btn)
        
        header_layout.addWidget(actions_container)
        
    def setup_modern_splitter(self):
        """Configure le splitter moderne avec animations"""
        # Créer le splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(1)
        
        # Ajouter sidebar et contenu
        self.main_splitter.addWidget(self.modern_sidebar)
        self.main_splitter.addWidget(self.content_area)
        
        # Sidebar compacte
        sidebar_width = 220
        content_width = self.width() - sidebar_width
        
        self.main_splitter.setSizes([sidebar_width, content_width])
        
        # Style moderne pour le splitter
        colors = ModernDesignSystem.get_color_palette()
        self.main_splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background: {colors['border']};
                border: none;
            }}
            QSplitter::handle:hover {{
                background: {colors['primary']};
            }}
        """)
        
        # Ajouter au layout principal
        self.main_layout.addWidget(self.main_splitter)
        
    def _setup_menu_bar(self):
        """Configure la barre de menu moderne"""
        colors = ModernDesignSystem.get_color_palette()
        
        # Style moderne pour la menu bar
        self.menuBar().setStyleSheet(f"""
            QMenuBar {{
                background: {colors['surface']};
                border-bottom: 1px solid {colors['border']};
                color: {colors['text_primary']};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                font-size: 14px;
                padding: 8px 16px;
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 8px 16px;
                border-radius: 6px;
            }}
            QMenuBar::item:selected {{
                background: {colors['surface_hover']};
            }}
            QMenu {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px 0px;
            }}
            QMenu::item {{
                padding: 8px 24px;
                border-radius: 4px;
                margin: 2px 8px;
            }}
            QMenu::item:selected {{
                background: {colors['surface_hover']};
            }}
        """)
        
        # Menus
        file_menu = self.menuBar().addMenu("Fichier")
        project_menu = self.menuBar().addMenu("Projet")
        tools_menu = self.menuBar().addMenu("Outils")
        help_menu = self.menuBar().addMenu("Aide")
        
        # Actions du menu Fichier
        new_project_action = QAction("Nouveau Projet", self)
        open_project_action = QAction("Ouvrir Projet", self)
        save_project_action = QAction("Sauvegarder", self)
        export_action = QAction("Exporter", self)
        exit_action = QAction("Quitter", self)
        
        file_menu.addAction(new_project_action)
        file_menu.addAction(open_project_action)
        file_menu.addAction(save_project_action)
        file_menu.addSeparator()
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Actions du menu Projet
        project_settings_action = QAction("Paramètres", self)
        project_info_action = QAction("Informations", self)
        
        project_menu.addAction(project_settings_action)
        project_menu.addAction(project_info_action)
        
        # Actions du menu Outils
        calibration_tool_action = QAction("Calibration", self)
        acquisition_tool_action = QAction("Acquisition", self)
        analysis_tool_action = QAction("Analyse", self)
        
        tools_menu.addAction(calibration_tool_action)
        tools_menu.addAction(acquisition_tool_action)
        tools_menu.addAction(analysis_tool_action)
        
        # Actions du menu Aide
        user_guide_action = QAction("Guide Utilisateur", self)
        about_action = QAction("À propos", self)
        
        help_menu.addAction(user_guide_action)
        help_menu.addAction(about_action)
        
    def _setup_status_bar(self):
        """Configure la barre de statut moderne"""
        colors = ModernDesignSystem.get_color_palette()
        
        # Style moderne pour la status bar
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background: {colors['surface']};
                border-top: 1px solid {colors['border']};
                color: {colors['text_secondary']};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                font-size: 12px;
                padding: 8px 16px;
            }}
        """)
        
        # Messages de statut
        self.statusBar().showMessage("Prêt - Dashboard moderne initialisé")
        
    def _setup_module_panels(self):
        """Configure les panels des modules (lazy-load)"""
        self._panels = {}
        self._panel_indices = {}

        # Charger uniquement le dashboard au démarrage
        from ..panels.modern.modern_dashboard_panel import ModernDashboardPanel
        self.dashboard_panel = ModernDashboardPanel(self.current_project)
        index = self.module_stack.addWidget(self.dashboard_panel)
        self._panels["dashboard"] = self.dashboard_panel
        self._panel_indices["dashboard"] = index
        self.module_stack.setCurrentIndex(index)

    def _ensure_panel(self, module_id: str):
        """Crée et enregistre le panel demandé s'il n'existe pas encore"""
        if module_id in self._panels:
            return

        if module_id == "calibration":
            from ..panels.modern.modern_calibration_panel import ModernCalibrationPanel
            panel = ModernCalibrationPanel(self.current_project)
        elif module_id == "acquisition":
            from ..panels.modern.modern_acquisition_panel import ModernAcquisitionPanel
            panel = ModernAcquisitionPanel(self.current_project)
        elif module_id == "stats":
            panel = self._create_placeholder_panel("Statistique", "Module d'analyse statistique")
        elif module_id == "advanced":
            panel = self._create_placeholder_panel("Avancée", "Module d'analyse Goda/FFT")
        elif module_id == "export":
            panel = self._create_placeholder_panel("Export", "Module d'export des résultats")
        else:
            panel = self._create_placeholder_panel("Module", f"{module_id}")

        index = self.module_stack.addWidget(panel)
        self._panels[module_id] = panel
        self._panel_indices[module_id] = index

    def _on_module_changed(self, module_id):
        """Gestionnaire de changement de module (lazy-load)"""
        self.current_module = module_id

        # Créer le panel si nécessaire
        self._ensure_panel(module_id)

        # Afficher le panel
        index = self._panel_indices.get(module_id, self._panel_indices.get("dashboard", 0))
        self.module_stack.setCurrentIndex(index)

        # Mettre à jour le statut
        self.statusBar().showMessage(f"Module actuel: {module_id.capitalize()}")
        
    def _on_return_to_projects(self):
        """Gestionnaire de retour aux projets"""
        # Émettre un signal pour retourner au gestionnaire de projets
        # Pour l'instant, on affiche juste un message
        self.statusBar().showMessage("Retour aux projets demandé")
        
    def _update_status(self):
        """Met à jour le statut du dashboard"""
        # Simulation de mise à jour du statut
        status_messages = [
            "Système opérationnel",
            "Vérification des capteurs...",
            "Calibration en cours...",
            "Acquisition active"
        ]
        
        # Rotation des messages
        current_index = (self.status_timer.interval() // 5000) % len(status_messages)
        self.statusBar().showMessage(status_messages[current_index])
        
    def showEvent(self, event):
        """Événement d'affichage"""
        super().showEvent(event)
        
    def resizeEvent(self, event):
        """Gestion du redimensionnement avec proportions φ"""
        super().resizeEvent(event)
        
        # Maintenir les proportions du nombre d'or
        if hasattr(self, 'main_splitter'):
            total_width = self.width()
            sidebar_width = 280  # Largeur fixe de la sidebar
            content_width = total_width - sidebar_width
            
            # Ajuster les proportions
            self.main_splitter.setSizes([sidebar_width, content_width])
            
    def set_project(self, project: ProjectInfo):
        """Change le projet affiché"""
        self.current_project = project
        self.modern_sidebar.set_project(project)
        
        # Mettre à jour le header
        # Note: Pour une implémentation complète, il faudrait recréer le header
        # ou implémenter une méthode de mise à jour dynamique
        
        # Mettre à jour le statut
        self.statusBar().showMessage(f"Projet chargé: {project.name}")

    def _setup_animations(self):
        """Animations désactivées (no-op)"""
        return

    def _setup_timers(self):
        """Initialise un timer simple pour mises à jour de statut (toutes les 5s)."""
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(5000)
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start()

    def _create_placeholder_panel(self, title: str, description: str):
        """Crée un panel placeholder compact pour modules non encore implémentés."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_label.setFont(ModernDesignSystem.get_font('h2'))
        title_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_primary']}; font-weight: 600;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(ModernDesignSystem.get_font('body'))
        desc_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_secondary']};")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        return panel

