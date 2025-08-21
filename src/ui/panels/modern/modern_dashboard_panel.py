"""
Panneau Dashboard Moderne - Vue d'accueil principale
Interface moderne avec cartes, statistiques et aperçu projet
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QFrame, QScrollArea, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...components.app_state import ProjectInfo
from ...resources.modern_design_system import ModernDesignSystem
from ...components.modern.modern_card import ModernCard, InfoCard, StatusCard, ActionCard
from ...components.modern.modern_button import ModernButton, IconButton


class ModernDashboardPanel(QWidget):
    """Panneau dashboard moderne avec design 2025"""
    
    def __init__(self, project: ProjectInfo = None, parent=None):
        super().__init__(parent)
        self.current_project = project
        
        # Initialisation de l'interface
        self._setup_modern_ui()
        # Supprimé: _setup_project_overview() pour gagner de la hauteur
        self._setup_system_metrics()
        self._setup_quick_actions()
        self._setup_recent_activity()
        # Supprimé: animations pour éviter les warnings QPainter et gagner en réactivité

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
        self.content_layout.setContentsMargins(6, 6, 6, 6)
        self.content_layout.setSpacing(4)
        
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
        
    def _setup_system_metrics(self):
        """Section métriques système compacte"""
        colors = ModernDesignSystem.get_color_palette()
        
        # Container métriques
        metrics_container = QFrame()
        metrics_container.setObjectName("system_metrics")
        metrics_container.setStyleSheet(f"""
            QFrame#system_metrics {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 6px;
            }}
        """)
        
        # Layout
        metrics_layout = QVBoxLayout(metrics_container)
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        metrics_layout.setSpacing(4)
        
        # Grille de métriques compacte (2x2)
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(4)
        
        sensors_card = StatusCard(title="Capteurs", value="● Non connectés", status="error")
        sensors_card.setMinimumHeight(36)
        metrics_grid.addWidget(sensors_card, 0, 0)
        
        acquisition_card = StatusCard(title="Acquisition", value="● Arrêtée", status="error")
        acquisition_card.setMinimumHeight(36)
        metrics_grid.addWidget(acquisition_card, 0, 1)
        
        calibration_card = StatusCard(title="Calibration", value="● Non effectuée", status="error")
        calibration_card.setMinimumHeight(36)
        metrics_grid.addWidget(calibration_card, 1, 0)
        
        analysis_card = StatusCard(title="Analyse", value="● Aucune donnée", status="error")
        analysis_card.setMinimumHeight(36)
        metrics_grid.addWidget(analysis_card, 1, 1)
        
        metrics_layout.addLayout(metrics_grid)
        self.content_layout.addWidget(metrics_container)
        
    def _setup_quick_actions(self):
        """Section actions rapides compacte"""
        colors = ModernDesignSystem.get_color_palette()
        
        actions_container = QFrame()
        actions_container.setObjectName("quick_actions")
        actions_container.setStyleSheet(f"""
            QFrame#quick_actions {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 6px;
            }}
        """)
        
        actions_layout = QVBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(4)
        
        actions_grid = QGridLayout()
        actions_grid.setSpacing(4)
        
        def compact_action(title, desc):
            card = ActionCard(title=title, description=desc, action_text="Démarrer")
            # Forcer le bouton interne à size='sm' via stylesheet minimal
            return card
        
        actions_grid.addWidget(compact_action("Calibration", "Lancer"), 0, 0)
        actions_grid.addWidget(compact_action("Acquisition", "Démarrer"), 0, 1)
        actions_grid.addWidget(compact_action("Analyse", "Exécuter"), 1, 0)
        actions_grid.addWidget(compact_action("Export", "Exporter"), 1, 1)
        
        actions_layout.addLayout(actions_grid)
        self.content_layout.addWidget(actions_container)
        
    def _setup_recent_activity(self):
        """Section activité récente compacte"""
        colors = ModernDesignSystem.get_color_palette()
        
        activity_container = QFrame()
        activity_container.setObjectName("recent_activity")
        activity_container.setStyleSheet(f"""
            QFrame#recent_activity {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 6px;
            }}
        """)
        
        activity_layout = QVBoxLayout(activity_container)
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(4)
        
        # Items d'activité ultra-compacts
        items = [
            ("+", "Nouveau projet créé", "2h"),
            ("Calibration", "Calibration des sondes", "1j"),
            ("Acquisition", "Acquisition de données", "2j"),
            ("Analyse", "Analyse FFT", "3j"),
        ]
        for icon, desc, when in items:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(4)
            row.addWidget(QLabel(icon))
            d = QLabel(desc)
            d.setStyleSheet(f"color: {colors['text_primary']}; font-size: 10px;")
            row.addWidget(d)
            row.addStretch()
            t = QLabel(when)
            t.setStyleSheet(f"color: {colors['text_muted']}; font-size: 9px;")
            row.addWidget(t)
            activity_layout.addLayout(row)
        
        self.content_layout.addWidget(activity_container)
