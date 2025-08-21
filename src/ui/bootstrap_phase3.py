import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# Add src directory to Python path for hrneowave imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ui.components.ui_config_manager import UIConfigManager
from src.ui.components.signal_adapter import UISignalAdapter
from src.ui.controllers.project_manager_controller import ProjectManagerController
from src.ui.windows.splash_screen import SplashScreen


class CHNeoWavePhase3Demo(QMainWindow):
    """Démonstration de la Phase 3 - Project Manager complet"""
    
    def __init__(self):
        super().__init__()
        self.project_controller = ProjectManagerController()
        self.setup_ui()
        self.setup_connections()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface de démonstration"""
        self.setWindowTitle("CHNeoWave - Phase 3 Demo - Project Manager")
        self.resize(1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # En-tête
        self.setup_header(main_layout)
        
        # Boutons de démonstration
        self.setup_demo_buttons(main_layout)
        
        # Zone de statut
        self.setup_status_section(main_layout)
        
        # Zone d'informations
        self.setup_info_section(main_layout)
        
    def setup_header(self, layout):
        """Configuration de l'en-tête"""
        header_label = QLabel("CHNeoWave - Phase 3 - Project Manager")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header_label.setStyleSheet("color: #2C5282; margin-bottom: 20px;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        subtitle_label = QLabel("Démonstration complète du système de gestion de projets")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("color: #718096; margin-bottom: 30px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
    def setup_demo_buttons(self, layout):
        """Configuration des boutons de démonstration"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)
        
        # Bouton Project Manager
        self.project_manager_btn = QPushButton("Ouvrir Project Manager")
        self.project_manager_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.project_manager_btn.setMinimumHeight(36)
        self.project_manager_btn.clicked.connect(self.on_open_project_manager)
        self.project_manager_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C5282;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2B6CB0;
            }
        """)
        buttons_layout.addWidget(self.project_manager_btn)
        
        # Bouton Project Wizard
        self.project_wizard_btn = QPushButton("Créer Nouveau Projet")
        self.project_wizard_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.project_wizard_btn.setMinimumHeight(36)
        self.project_wizard_btn.clicked.connect(self.on_open_project_wizard)
        self.project_wizard_btn.setStyleSheet("""
            QPushButton {
                background-color: #38A169;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2F855A;
            }
        """)
        buttons_layout.addWidget(self.project_wizard_btn)
        
        # Bouton Project Importer
        self.project_importer_btn = QPushButton("Importer Projet")
        self.project_importer_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.project_importer_btn.setMinimumHeight(36)
        self.project_importer_btn.clicked.connect(self.on_open_project_importer)
        self.project_importer_btn.setStyleSheet("""
            QPushButton {
                background-color: #ED8936;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #DD6B20;
            }
        """)
        buttons_layout.addWidget(self.project_importer_btn)
        
        layout.addLayout(buttons_layout)
        
    def setup_status_section(self, layout):
        """Configuration de la section de statut"""
        status_group = QWidget()
        status_group.setStyleSheet("""
            QWidget {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                background-color: #F7FAFC;
                padding: 8px;
            }
        """)
        
        status_layout = QVBoxLayout(status_group)
        
        status_title = QLabel("Statut du Système")
        status_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        status_title.setStyleSheet("color: #2D3748; margin-bottom: 15px;")
        status_layout.addWidget(status_title)
        
        self.status_label = QLabel("Système prêt - Project Manager initialisé")
        self.status_label.setStyleSheet("color: #38A169; font-size: 14px;")
        status_layout.addWidget(self.status_label)
        
        self.projects_summary_label = QLabel("Aucun projet récent")
        self.projects_summary_label.setStyleSheet("color: #718096; font-size: 12px;")
        status_layout.addWidget(self.projects_summary_label)
        
        layout.addWidget(status_group)
        
    def setup_info_section(self, layout):
        """Configuration de la section d'informations"""
        info_group = QWidget()
        info_group.setStyleSheet("""
            QWidget {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                background-color: #FFFFFF;
                padding: 8px;
            }
        """)
        
        info_layout = QVBoxLayout(info_group)
        
        info_title = QLabel("Informations Phase 3")
        info_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info_title.setStyleSheet("color: #2D3748; margin-bottom: 15px;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel("""
        <b>Fonctionnalités Implémentées:</b>
        • ProjectManager - Interface d'accueil avec projets récents
        • ProjectWizard - Assistant 3 étapes pour création de projet
        • ProjectImporter - Import de projets HDF5 avec validation
        • RecentProjectsManager - Gestion persistance QSettings
        • ProjectManagerController - Orchestration complète
        
        <b>Architecture:</b>
        • Pattern MVC strict respecté
        • Séparation UI/logique métier
        • Communication par signaux/slots
        • Gestion d'erreurs robuste
        
        <b>Tests:</b>
        • Tests unitaires complets
        • Tests d'intégration
        • Tests de performance
        • Tests d'accessibilité
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #4A5568; font-size: 12px; line-height: 1.5;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
    def setup_connections(self):
        """Configuration des connexions de signaux"""
        # Connexions du contrôleur de projets
        self.project_controller.project_loaded.connect(self.on_project_loaded)
        self.project_controller.project_created.connect(self.on_project_created)
        self.project_controller.project_imported.connect(self.on_project_imported)
        self.project_controller.project_manager_closed.connect(self.on_project_manager_closed)
        
    def on_open_project_manager(self):
        """Gestionnaire d'ouverture du Project Manager"""
        try:
            self.project_controller.show_project_manager()
            self.status_label.setText("Project Manager ouvert")
            self.update_projects_summary()
        except Exception as e:
            self.show_error_message("Erreur", f"Impossible d'ouvrir le Project Manager:\n{str(e)}")
            
    def on_open_project_wizard(self):
        """Gestionnaire d'ouverture du Project Wizard"""
        try:
            self.project_controller.on_new_project_requested()
            self.status_label.setText("Project Wizard ouvert")
        except Exception as e:
            self.show_error_message("Erreur", f"Impossible d'ouvrir le Project Wizard:\n{str(e)}")
            
    def on_open_project_importer(self):
        """Gestionnaire d'ouverture du Project Importer"""
        try:
            self.project_controller.on_import_project_requested()
            self.status_label.setText("Project Importer ouvert")
        except Exception as e:
            self.show_error_message("Erreur", f"Impossible d'ouvrir le Project Importer:\n{str(e)}")
            
    def on_project_loaded(self, project, file_path):
        """Gestionnaire de chargement de projet"""
        self.status_label.setText(f"✓ Projet chargé: {project.name}")
        self.update_projects_summary()
        
        QMessageBox.information(
            self,
            "Projet Chargé",
            f"Le projet '{project.name}' a été chargé avec succès !\n\n"
            f"Code: {project.code}\n"
            f"Fichier: {file_path if file_path else 'Aucun fichier'}"
        )
        
    def on_project_created(self, project):
        """Gestionnaire de création de projet"""
        self.status_label.setText(f"Projet créé: {project.name}")
        self.update_projects_summary()
        
    def on_project_imported(self, project, file_path):
        """Gestionnaire d'import de projet"""
        self.status_label.setText(f"Projet importé: {project.name}")
        self.update_projects_summary()
        
    def on_project_manager_closed(self):
        """Gestionnaire de fermeture du Project Manager"""
        self.status_label.setText(" Project Manager fermé")
        
    def update_projects_summary(self):
        """Mise à jour du résumé des projets"""
        try:
            summary = self.project_controller.get_recent_projects_summary()
            total = summary.get('total_projects', 0)
            
            if total > 0:
                most_recent = summary.get('recent_access', 'Inconnue')
                most_accessed = summary.get('most_accessed', 'Inconnu')
                
                self.projects_summary_label.setText(
                    f"{total} projet(s) récent(s) | "
                    f"Plus récent: {most_recent[:10]}... | "
                    f"Plus accédé: {most_accessed}"
                )
            else:
                self.projects_summary_label.setText("Aucun projet récent")
                
        except Exception as e:
            self.projects_summary_label.setText(f"Erreur: {str(e)}")
            
    def show_error_message(self, title: str, message: str):
        """Afficher un message d'erreur"""
        QMessageBox.critical(self, title, message)
        
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet("""
            CHNeoWavePhase3Demo {
                background-color: #F7FAFC;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
    def closeEvent(self, event):
        """Gestion de la fermeture de la fenêtre"""
        try:
            # Nettoyer le contrôleur
            self.project_controller.cleanup()
        except Exception as e:
            print(f"Erreur lors du nettoyage: {e}")
            
        super().closeEvent(event)


def main():
    """Point d'entrée principal avec splash screen"""
    app = QApplication(sys.argv)
    
    # Afficher le splash screen
    splash = SplashScreen()
    splash.show()
    
    def on_splash_finished():
        # Créer et afficher la fenêtre de démonstration
        window = CHNeoWavePhase3Demo()
        window.show()
        
        # Mettre à jour le statut après un délai
        QTimer.singleShot(1000, window.update_projects_summary)
        
    splash.finished.connect(on_splash_finished)
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
