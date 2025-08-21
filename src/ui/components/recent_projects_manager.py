from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QMessageBox
from typing import List, Optional, Dict, Any
import os
import json
from datetime import datetime

from .app_state import ProjectInfo


class RecentProjectsManager(QObject):
    """Gestionnaire des projets récents avec persistance QSettings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("CHNeoWave", "RecentProjects")
        self.max_recent_projects = 10
        
    def add_recent_project(self, project: ProjectInfo, file_path: str = ""):
        """Ajouter un projet à la liste des projets récents"""
        try:
            recent_projects = self.load_recent_projects()
            
            # Créer l'entrée du projet
            project_entry = {
                'name': project.name,
                'code': project.code,
                'engineer': project.engineer,
                'manager': project.manager,
                'scale': project.scale,
                'basin_type': project.basin_type,
                'file_path': file_path,
                'last_accessed': datetime.now().isoformat(),
                'access_count': 1
            }
            
            # Vérifier si le projet existe déjà
            existing_index = None
            for i, existing in enumerate(recent_projects):
                if (existing.get('code') == project.code and 
                    existing.get('name') == project.name):
                    existing_index = i
                    break
            
            if existing_index is not None:
                # Mettre à jour le projet existant
                existing = recent_projects[existing_index]
                existing['last_accessed'] = project_entry['last_accessed']
                existing['access_count'] = existing.get('access_count', 0) + 1
                if file_path:
                    existing['file_path'] = file_path
                # Déplacer en première position
                recent_projects.pop(existing_index)
                recent_projects.insert(0, existing)
            else:
                # Ajouter le nouveau projet en première position
                recent_projects.insert(0, project_entry)
                
            # Limiter le nombre de projets récents
            if len(recent_projects) > self.max_recent_projects:
                recent_projects = recent_projects[:self.max_recent_projects]
                
            # Sauvegarder
            self.save_recent_projects(recent_projects)
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de l'ajout du projet: {e}")
            
    def load_recent_projects(self) -> List[Dict[str, Any]]:
        """Charger la liste des projets récents depuis QSettings"""
        try:
            projects_data = self.settings.value("recent_projects", "[]")
            if isinstance(projects_data, str):
                return json.loads(projects_data)
            elif isinstance(projects_data, list):
                return projects_data
            else:
                return []
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors du chargement: {e}")
            return []
            
    def save_recent_projects(self, projects: List[Dict[str, Any]]):
        """Sauvegarder la liste des projets récents dans QSettings"""
        try:
            projects_json = json.dumps(projects, ensure_ascii=False, indent=2)
            self.settings.setValue("recent_projects", projects_json)
            self.settings.sync()
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de la sauvegarde: {e}")
            
    def get_recent_projects(self) -> List[ProjectInfo]:
        """Obtenir la liste des projets récents sous forme d'objets ProjectInfo"""
        try:
            projects_data = self.load_recent_projects()
            projects = []
            
            for data in projects_data:
                project = ProjectInfo(
                    name=data.get('name', 'Projet Inconnu'),
                    code=data.get('code', 'CHW-UNK-000'),
                    engineer=data.get('engineer', 'Non spécifié'),
                    manager=data.get('manager', 'Non spécifié'),
                    scale=data.get('scale', 'Non spécifié'),
                    basin_type=data.get('basin_type', 'Non spécifié')
                )
                projects.append(project)
                
            return projects
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de la conversion: {e}")
            return []
            
    def get_project_file_path(self, project: ProjectInfo) -> Optional[str]:
        """Obtenir le chemin du fichier pour un projet donné"""
        try:
            projects_data = self.load_recent_projects()
            
            for data in projects_data:
                if (data.get('code') == project.code and 
                    data.get('name') == project.name):
                    file_path = data.get('file_path', '')
                    if file_path and os.path.exists(file_path):
                        return file_path
                    break
                    
            return None
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de la récupération du chemin: {e}")
            return None
            
    def remove_recent_project(self, project: ProjectInfo):
        """Supprimer un projet de la liste des projets récents"""
        try:
            projects_data = self.load_recent_projects()
            
            # Trouver et supprimer le projet
            projects_data = [
                p for p in projects_data 
                if not (p.get('code') == project.code and p.get('name') == project.name)
            ]
            
            # Sauvegarder la liste mise à jour
            self.save_recent_projects(projects_data)
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de la suppression: {e}")
            
    def clear_recent_projects(self):
        """Vider complètement la liste des projets récents"""
        try:
            self.settings.remove("recent_projects")
            self.settings.sync()
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors du vidage: {e}")
            
    def get_project_stats(self, project: ProjectInfo) -> Dict[str, Any]:
        """Obtenir les statistiques d'utilisation d'un projet"""
        try:
            projects_data = self.load_recent_projects()
            
            for data in projects_data:
                if (data.get('code') == project.code and 
                    data.get('name') == project.name):
                    return {
                        'access_count': data.get('access_count', 0),
                        'last_accessed': data.get('last_accessed', ''),
                        'file_path': data.get('file_path', ''),
                        'file_exists': os.path.exists(data.get('file_path', ''))
                    }
                    
            return {}
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de la récupération des stats: {e}")
            return {}
            
    def validate_project_files(self) -> List[Dict[str, Any]]:
        """Valider l'existence des fichiers de projets et nettoyer les entrées invalides"""
        try:
            projects_data = self.load_recent_projects()
            valid_projects = []
            invalid_projects = []
            
            for data in projects_data:
                file_path = data.get('file_path', '')
                if file_path and os.path.exists(file_path):
                    valid_projects.append(data)
                else:
                    invalid_projects.append(data)
                    
            # Sauvegarder la liste nettoyée
            self.save_recent_projects(valid_projects)
            
            return {
                'valid_count': len(valid_projects),
                'invalid_count': len(invalid_projects),
                'invalid_projects': invalid_projects
            }
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de la validation: {e}")
            return {'valid_count': 0, 'invalid_count': 0, 'invalid_projects': []}
            
    def export_recent_projects(self, export_path: str) -> bool:
        """Exporter la liste des projets récents vers un fichier JSON"""
        try:
            projects_data = self.load_recent_projects()
            
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_projects': len(projects_data),
                'projects': projects_data
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
                
            return True
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de l'export: {e}")
            return False
            
    def import_recent_projects(self, import_path: str, merge: bool = True) -> bool:
        """Importer une liste de projets récents depuis un fichier JSON"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                
            if 'projects' not in import_data:
                print("[RecentProjectsManager] Format de fichier invalide")
                return False
                
            imported_projects = import_data['projects']
            
            if merge:
                # Fusionner avec les projets existants
                existing_projects = self.load_recent_projects()
                
                # Créer un dictionnaire des projets existants par code
                existing_dict = {}
                for p in existing_projects:
                    key = f"{p.get('code')}_{p.get('name')}"
                    existing_dict[key] = p
                    
                # Ajouter les projets importés
                for p in imported_projects:
                    key = f"{p.get('code')}_{p.get('name')}"
                    if key not in existing_dict:
                        existing_dict[key] = p
                        
                # Convertir en liste et trier par date d'accès
                merged_projects = list(existing_dict.values())
                merged_projects.sort(
                    key=lambda x: x.get('last_accessed', ''), 
                    reverse=True
                )
                
                # Limiter le nombre de projets
                if len(merged_projects) > self.max_recent_projects:
                    merged_projects = merged_projects[:self.max_recent_projects]
                    
                self.save_recent_projects(merged_projects)
            else:
                # Remplacer complètement
                self.save_recent_projects(imported_projects)
                
            return True
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors de l'import: {e}")
            return False
            
    def get_recent_projects_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé des projets récents"""
        try:
            projects_data = self.load_recent_projects()
            
            if not projects_data:
                return {
                    'total_projects': 0,
                    'recent_access': 'Aucun projet récent',
                    'most_accessed': 'Aucun projet',
                    'file_validation': {'valid': 0, 'invalid': 0}
                }
                
            # Statistiques de base
            total_projects = len(projects_data)
            
            # Projet le plus récemment accédé
            most_recent = max(projects_data, key=lambda x: x.get('last_accessed', ''))
            recent_access = most_recent.get('last_accessed', '')
            
            # Projet le plus accédé
            most_accessed = max(projects_data, key=lambda x: x.get('access_count', 0))
            most_accessed_name = most_accessed.get('name', 'Inconnu')
            
            # Validation des fichiers
            valid_files = sum(1 for p in projects_data if os.path.exists(p.get('file_path', '')))
            invalid_files = total_projects - valid_files
            
            return {
                'total_projects': total_projects,
                'recent_access': recent_access,
                'most_accessed': most_accessed_name,
                'file_validation': {
                    'valid': valid_files,
                    'invalid': invalid_files
                }
            }
            
        except Exception as e:
            print(f"[RecentProjectsManager] Erreur lors du calcul du résumé: {e}")
            return {}
