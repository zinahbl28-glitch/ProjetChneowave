import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ui.components.ui_config_manager import UIConfigManager
from src.ui.components.signal_adapter import UISignalAdapter
from src.ui.controllers.dashboard_controller import DashboardController
from src.ui.components.app_state import ProjectInfo
from src.ui.windows.splash_screen import SplashScreen

# Références globales pour empêcher la collecte et fermeture immédiate
PHASE4_WINDOW = None
PHASE4_SPLASH = None


class CHNeoWavePhase4Demo(QMainWindow):
    """Démonstration Phase 4 - Dashboard Principal"""
    
    def __init__(self):
        super().__init__()
        self.dashboard_controller = None
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configuration de l'interface de démonstration"""
        self.setWindowTitle("CHNeoWave - Phase 4 Demo - Dashboard Principal")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        
        # En-tête
        self.setup_header(main_layout)
        
        # Informations Phase 4
        self.setup_phase4_info(main_layout)
        
        # Contrôles de démonstration
        self.setup_demo_controls(main_layout)
        
        # Statut et informations
        self.setup_status_info(main_layout)
        
        # Espace flexible
        main_layout.addStretch()
        
    def setup_header(self, layout):
        """Configuration de l'en-tête"""
        header_label = QLabel("PHASE 4 - DASHBOARD PRINCIPAL")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #2C5282; margin-bottom: 10px;")
        layout.addWidget(header_label)
        
        subtitle_label = QLabel("Interface principale avec navigation 5 modules")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #718096; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
    def setup_phase4_info(self, layout):
        """Configuration des informations Phase 4"""
        info_group = QWidget()
        info_group.setStyleSheet("""
            QWidget {
                background-color: #F7FAFC;
                border: 2px solid #2C5282;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        info_layout = QVBoxLayout(info_group)
        info_layout.setSpacing(15)
        
        # Titre de la section
        info_title = QLabel("Fonctionnalités Phase 4")
        info_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info_title.setStyleSheet("color: #2C5282;")
        info_layout.addWidget(info_title)
        
        # Liste des fonctionnalités
        features = [
            "- Dashboard principal avec interface moderne",
            "- Navigation latérale avec 5 modules",
            "- Sidebar avec informations projet et état système",
            "- Panels modulaires pour chaque module",
            "- Transition fluide entre modules",
            "- Interface maritime cohérente (OpenBridge)",
            "- Architecture MVC respectée",
            "- Intégration transparente avec Phase 3"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("color: #2D3748; font-size: 12px;")
            info_layout.addWidget(feature_label)
            
        layout.addWidget(info_group)
        
    def setup_demo_controls(self, layout):
        """Configuration des contrôles de démonstration"""
        controls_group = QWidget()
        controls_group.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 2px solid #38A169;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setSpacing(15)
        
        # Titre de la section
        controls_title = QLabel("Contrôles de Démonstration")
        controls_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        controls_title.setStyleSheet("color: #38A169;")
        controls_layout.addWidget(controls_title)
        
        # Boutons de contrôle
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Bouton ouvrir dashboard
        self.open_dashboard_btn = QPushButton("Ouvrir Dashboard")
        self.open_dashboard_btn.setMinimumHeight(30)
        self.open_dashboard_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C5282;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2B6CB0;
            }
        """)
        self.open_dashboard_btn.clicked.connect(self.on_open_dashboard)
        buttons_layout.addWidget(self.open_dashboard_btn)
        
        # Bouton simuler activité
        self.simulate_btn = QPushButton("Simuler Activité Système")
        self.simulate_btn.setMinimumHeight(30)
        self.simulate_btn.setStyleSheet("""
            QPushButton {
                background-color: #ED8936;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #DD6B20;
            }
        """)
        self.simulate_btn.clicked.connect(self.on_simulate_activity)
        buttons_layout.addWidget(self.simulate_btn)
        
        # Bouton informations
        self.info_btn = QPushButton("Informations Phase 4")
        self.info_btn.setMinimumHeight(30)
        self.info_btn.setStyleSheet("""
            QPushButton {
                background-color: #38A169;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2F855A;
            }
        """)
        self.info_btn.clicked.connect(self.on_show_info)
        buttons_layout.addWidget(self.info_btn)
        
        controls_layout.addLayout(buttons_layout)
        layout.addWidget(controls_group)
        
    def setup_status_info(self, layout):
        """Configuration des informations de statut"""
        status_group = QWidget()
        status_group.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 2px solid #718096;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(15)
        
        # Titre de la section
        status_title = QLabel("Statut et Informations")
        status_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        status_title.setStyleSheet("color: #718096;")
        status_layout.addWidget(status_title)
        
        # Informations de statut
        self.status_label = QLabel("Phase 4 prête - Dashboard disponible")
        self.status_label.setStyleSheet("color: #2D3748; font-size: 12px;")
        status_layout.addWidget(self.status_label)
        
        # Informations techniques
        tech_info = QLabel(
            "Architecture: MVC avec panels modulaires\n"
            "Design: Maritime OpenBridge cohérent\n"
            "Performance: < 300ms startup, < 100ms module switching\n"
            "Tests: Framework pytest-qt configuré\n"
            "Intégration: Phase 3 Project Manager connecté"
        )
        tech_info.setStyleSheet("color: #4A5568; font-size: 11px;")
        tech_info.setWordWrap(True)
        status_layout.addWidget(tech_info)
        
        layout.addWidget(status_group)
        
    def setup_connections(self):
        """Configuration des connexions de signaux"""
        # TODO: Connexions avec le dashboard controller
        pass
        
    def on_open_dashboard(self):
        """Gestionnaire d'ouverture du dashboard"""
        try:
            # Créer un projet de démonstration
            demo_project = ProjectInfo(
                name="Projet Démo Phase 4",
                code="CHW-2024-DEMO",
                engineer="Ing. Démonstration",
                manager="Chef Démo",
                scale="1:100",
                basin_type="Bassin de Test"
            )
            
            # Créer et afficher le dashboard
            self.dashboard_controller = DashboardController(demo_project)
            self.dashboard_controller.dashboard_closed.connect(self.on_dashboard_closed)
            self.dashboard_controller.show_dashboard()
            
            # Mettre à jour le statut
            self.status_label.setText("Dashboard ouvert - Module Dashboard actif")
            self.open_dashboard_btn.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible d'ouvrir le dashboard:\n{str(e)}"
            )
            
    def on_simulate_activity(self):
        """Gestionnaire de simulation d'activité"""
        if self.dashboard_controller and self.dashboard_controller.is_dashboard_open():
            # Démarrer la simulation
            self.dashboard_controller.start_system_monitoring()
            self.status_label.setText("Simulation d'activité système démarrée")
            self.simulate_btn.setText("Arrêter la Simulation")
            self.simulate_btn.clicked.disconnect()
            self.simulate_btn.clicked.connect(self.on_stop_simulation)
        else:
            QMessageBox.information(
                self,
                "Information",
                "Ouvrez d'abord le dashboard pour simuler l'activité système."
            )
            
    def on_stop_simulation(self):
        """Gestionnaire d'arrêt de simulation"""
        if self.dashboard_controller:
            self.dashboard_controller.stop_system_monitoring()
            self.status_label.setText("Simulation arrêtée")
            self.simulate_btn.setText("Simuler Activité Système")
            self.simulate_btn.clicked.disconnect()
            self.simulate_btn.clicked.connect(self.on_simulate_activity)
            
    def on_show_info(self):
        """Gestionnaire d'affichage des informations"""
        QMessageBox.information(
            self,
            "Phase 4 - Dashboard Principal",
            "PHASE 4 COMPLÉTÉE AVEC SUCCÈS !\n\n"
            "- Dashboard principal opérationnel\n"
            "- Navigation 5 modules fonctionnelle\n"
            "- Interface maritime cohérente\n"
            "- Architecture MVC respectée\n"
            "- Intégration Phase 3 parfaite\n\n"
            "Prêt pour Phase 5 (Calibration) !"
        )
        
    def on_dashboard_closed(self):
        """Gestionnaire de fermeture du dashboard"""
        self.dashboard_controller = None
        self.status_label.setText("✓ Phase 4 prête - Dashboard disponible")
        self.open_dashboard_btn.setEnabled(True)
        
    def closeEvent(self, event):
        """Gestion de la fermeture de la fenêtre"""
        if self.dashboard_controller:
            self.dashboard_controller.close_dashboard()
        event.accept()


def main():
    """Point d'entrée principal"""
    app = QApplication(sys.argv)
    
    # Afficher le splash screen
    global PHASE4_SPLASH
    splash = SplashScreen()
    PHASE4_SPLASH = splash
    splash.show()
    
    def on_splash_finished():
        # Créer et afficher la fenêtre de démonstration
        global PHASE4_WINDOW
        PHASE4_WINDOW = CHNeoWavePhase4Demo()
        PHASE4_WINDOW.show()
        
        # Mettre à jour le statut après un délai
        QTimer.singleShot(1000, lambda: PHASE4_WINDOW.status_label.setText("Phase 4 prête - Dashboard disponible"))
        
    splash.finished.connect(on_splash_finished)
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
