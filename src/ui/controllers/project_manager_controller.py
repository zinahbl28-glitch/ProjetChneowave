from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QMessageBox, QApplication
from typing import Optional, Dict, Any
import os

from ..components.app_state import ProjectInfo
from ..components.recent_projects_manager import RecentProjectsManager
from ..windows.project_manager import ProjectManager
from ..windows.project_wizard import ProjectWizard
from ..windows.project_importer import ProjectImporter


class ProjectManagerController(QObject):
    """Contrôleur principal pour la gestion des projets CHNeoWave"""
    
    # Signaux pour communication avec l'interface principale
    project_loaded = Signal(ProjectInfo, str)  # (project, file_path)
    project_created = Signal(ProjectInfo)
    project_imported = Signal(ProjectInfo, str)  # (project, file_path)
    project_manager_closed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recent_projects_manager = RecentProjectsManager()
        self.current_project: Optional[ProjectInfo] = None
        self.current_file_path: str = ""
        
        # Fenêtres
        self.project_manager_window: Optional[ProjectManager] = None
        self.project_wizard_window: Optional[ProjectWizard] = None
        self.project_importer_window: Optional[ProjectImporter] = None
        
    def show_project_manager(self):
        """Afficher la fenêtre principale de gestion des projets"""
        try:
            if not self.project_manager_window:
                self.project_manager_window = ProjectManager()
                
                # Connexion des signaux
                self.project_manager_window.project_selected.connect(self.on_project_selected)
                self.project_manager_window.new_project_requested.connect(self.on_new_project_requested)
                self.project_manager_window.import_project_requested.connect(self.on_import_project_requested)
                self.project_manager_window.finished.connect(self.on_project_manager_closed)
                
            self.project_manager_window.show()
            self.project_manager_window.raise_()
            self.project_manager_window.activateWindow()
            
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de l'affichage du ProjectManager: {e}")
            self.show_error_message("Erreur", f"Impossible d'ouvrir le gestionnaire de projets:\n{str(e)}")
            
    def on_project_selected(self, project: ProjectInfo):
        """Gestionnaire de sélection d'un projet existant"""
        try:
            # Obtenir le chemin du fichier si disponible
            file_path = self.recent_projects_manager.get_project_file_path(project)
            
            if file_path and os.path.exists(file_path):
                # Projet avec fichier valide
                self.load_project(project, file_path)
            else:
                # Projet sans fichier - demander à l'utilisateur
                self.handle_project_without_file(project)
                
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de la sélection du projet: {e}")
            self.show_error_message("Erreur", f"Impossible de charger le projet:\n{str(e)}")
            
    def on_new_project_requested(self):
        """Gestionnaire de demande de création de nouveau projet"""
        try:
            if not self.project_wizard_window:
                self.project_wizard_window = ProjectWizard()
                self.project_wizard_window.project_created.connect(self.on_project_wizard_completed)
                
            self.project_wizard_window.show()
            self.project_wizard_window.raise_()
            self.project_wizard_window.activateWindow()
            
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de l'ouverture du wizard: {e}")
            self.show_error_message("Erreur", f"Impossible d'ouvrir l'assistant de création:\n{str(e)}")
            
    def on_import_project_requested(self):
        """Gestionnaire de demande d'import de projet"""
        try:
            if not self.project_importer_window:
                self.project_importer_window = ProjectImporter()
                self.project_importer_window.project_imported.connect(self.on_project_imported)
                
            self.project_importer_window.show()
            self.project_importer_window.raise_()
            self.project_importer_window.activateWindow()
            
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de l'ouverture de l'importateur: {e}")
            self.show_error_message("Erreur", f"Impossible d'ouvrir l'importateur:\n{str(e)}")
            
    def on_project_wizard_completed(self, project: ProjectInfo):
        """Gestionnaire de fin du wizard de création"""
        try:
            # Ajouter aux projets récents
            self.recent_projects_manager.add_recent_project(project)
            
            # Créer la structure du projet (simulation)
            self.create_project_structure(project)
            
            # Émettre le signal de création
            self.project_created.emit(project)
            
            # Fermer le wizard
            if self.project_wizard_window:
                self.project_wizard_window.close()
                self.project_wizard_window = None
                
            # Fermer le gestionnaire de projets
            if self.project_manager_window:
                self.project_manager_window.close()
                self.project_manager_window = None
                
            # Message de confirmation
            self.show_success_message(
                "Projet Créé",
                f"Le projet '{project.name}' a été créé avec succès !\n\n"
                f"Code: {project.code}\n"
                f"Échelle: {project.scale}\n"
                f"Type: {project.basin_type}\n\n"
                f"Le projet sera maintenant ouvert dans CHNeoWave."
            )
            
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de la création du projet: {e}")
            self.show_error_message("Erreur", f"Erreur lors de la création du projet:\n{str(e)}")
            
    def on_project_imported(self, project: ProjectInfo, file_path: str):
        """Gestionnaire de fin d'import de projet"""
        try:
            # Ajouter aux projets récents
            self.recent_projects_manager.add_recent_project(project, file_path)
            
            # Émettre le signal d'import
            self.project_imported.emit(project, file_path)
            
            # Fermer l'importateur
            if self.project_importer_window:
                self.project_importer_window.close()
                self.project_importer_window = None
                
            # Fermer le gestionnaire de projets
            if self.project_manager_window:
                self.project_manager_window.close()
                self.project_manager_window = None
                
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de l'import du projet: {e}")
            self.show_error_message("Erreur", f"Erreur lors de l'import du projet:\n{str(e)}")
            
    def on_project_manager_closed(self, result):
        """Gestionnaire de fermeture du gestionnaire de projets"""
        try:
            # Nettoyer les références
            if self.project_manager_window:
                self.project_manager_window = None
                
            # Émettre le signal de fermeture
            self.project_manager_closed.emit()
            
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de la fermeture: {e}")
            
    def load_project(self, project: ProjectInfo, file_path: str):
        """Charger un projet existant"""
        try:
            # Mettre à jour l'état courant
            self.current_project = project
            self.current_file_path = file_path
            
            # Ajouter aux projets récents (mise à jour de la date d'accès)
            self.recent_projects_manager.add_recent_project(project, file_path)
            
            # Émettre le signal de chargement
            self.project_loaded.emit(project, file_path)
            
            # Fermer le gestionnaire de projets
            if self.project_manager_window:
                self.project_manager_window.close()
                self.project_manager_window = None
                
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors du chargement du projet: {e}")
            self.show_error_message("Erreur", f"Impossible de charger le projet:\n{str(e)}")
            
    def handle_project_without_file(self, project: ProjectInfo):
        """Gérer un projet sans fichier associé"""
        try:
            reply = QMessageBox.question(
                None,
                "Projet Sans Fichier",
                f"Le projet '{project.name}' n'a pas de fichier associé.\n\n"
                f"Voulez-vous le supprimer de la liste des projets récents ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Supprimer le projet de la liste
                self.recent_projects_manager.remove_recent_project(project)
                
                # Recharger la liste
                if self.project_manager_window:
                    self.project_manager_window.load_recent_projects()
                    
                QMessageBox.information(
                    None,
                    "Projet Supprimé",
                    f"Le projet '{project.name}' a été supprimé de la liste des projets récents."
                )
            else:
                # L'utilisateur veut garder le projet
                # Créer un projet vide
                self.load_project(project, "")
                
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de la gestion du projet sans fichier: {e}")
            self.show_error_message("Erreur", f"Erreur lors de la gestion du projet:\n{str(e)}")
            
    def create_project_structure(self, project: ProjectInfo):
        """Créer la structure de base d'un nouveau projet"""
        try:
            # TODO: Implémenter la création de la structure de projet
            # Pour l'instant, simulation
            print(f"[ProjectManagerController] Création de la structure pour le projet: {project.name}")
            
            # Simuler la création de dossiers et fichiers
            project_dir = f"projects/{project.code}"
            os.makedirs(project_dir, exist_ok=True)
            
            # Créer le fichier de métadonnées
            metadata_file = os.path.join(project_dir, "project_metadata.json")
            metadata = {
                'name': project.name,
                'code': project.code,
                'engineer': project.engineer,
                'manager': project.manager,
                'scale': project.scale,
                'basin_type': project.basin_type,
                'created_date': project.created_date if hasattr(project, 'created_date') else '2024-01-01',
                'version': '1.0.0'
            }
            
            import json
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
                
            print(f"[ProjectManagerController] Structure créée dans: {project_dir}")
            
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors de la création de la structure: {e}")
            # Ne pas bloquer le processus principal
            
    def get_current_project(self) -> Optional[ProjectInfo]:
        """Obtenir le projet actuellement chargé"""
        return self.current_project
        
    def get_current_file_path(self) -> str:
        """Obtenir le chemin du fichier du projet actuel"""
        return self.current_file_path
        
    def get_recent_projects_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé des projets récents"""
        return self.recent_projects_manager.get_recent_projects_summary()
        
    def validate_project_files(self) -> Dict[str, Any]:
        """Valider l'existence des fichiers de projets"""
        return self.recent_projects_manager.validate_project_files()
        
    def export_recent_projects(self, export_path: str) -> bool:
        """Exporter la liste des projets récents"""
        return self.recent_projects_manager.export_recent_projects(export_path)
        
    def import_recent_projects(self, import_path: str, merge: bool = True) -> bool:
        """Importer une liste de projets récents"""
        return self.recent_projects_manager.import_recent_projects(import_path, merge)
        
    def clear_recent_projects(self):
        """Vider la liste des projets récents"""
        try:
            reply = QMessageBox.question(
                None,
                "Confirmation",
                "Êtes-vous sûr de vouloir vider complètement la liste des projets récents ?\n\n"
                "Cette action ne peut pas être annulée.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.recent_projects_manager.clear_recent_projects()
                
                # Recharger la liste si la fenêtre est ouverte
                if self.project_manager_window:
                    self.project_manager_window.load_recent_projects()
                    
                QMessageBox.information(
                    None,
                    "Liste Vidée",
                    "La liste des projets récents a été vidée avec succès."
                )
                
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors du vidage: {e}")
            self.show_error_message("Erreur", f"Impossible de vider la liste:\n{str(e)}")
            
    def show_error_message(self, title: str, message: str):
        """Afficher un message d'erreur"""
        QMessageBox.critical(None, title, message)
        
    def show_success_message(self, title: str, message: str):
        """Afficher un message de succès"""
        QMessageBox.information(None, title, message)
        
    def cleanup(self):
        """Nettoyage des ressources"""
        try:
            # Fermer toutes les fenêtres ouvertes
            if self.project_manager_window:
                self.project_manager_window.close()
                self.project_manager_window = None
                
            if self.project_wizard_window:
                self.project_wizard_window.close()
                self.project_wizard_window = None
                
            if self.project_importer_window:
                self.project_importer_window.close()
                self.project_importer_window = None
                
        except Exception as e:
            print(f"[ProjectManagerController] Erreur lors du nettoyage: {e}")
