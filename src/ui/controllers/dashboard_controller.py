from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QMessageBox, QApplication

from ..components.app_state import ProjectInfo
from ..components.base_controller import BaseController
from ..windows.main_dashboard import MainDashboard
from .calibration_controller import CalibrationController


class DashboardController(BaseController):
    """Contrôleur principal du dashboard"""
    
    dashboard_closed = Signal()
    module_switched = Signal(str)  # nom du module
    project_updated = Signal(ProjectInfo)
    
    def __init__(self, project: ProjectInfo, file_path: str = ""):
        super().__init__()
        self.project = project
        self.file_path = file_path
        self.current_module = "dashboard"
        
        self.dashboard_window: MainDashboard = None
        self.calibration_controller: CalibrationController | None = None
        
        # État du système
        self.system_status = {
            "sensors": "disconnected",
            "acquisition": "stopped",
            "calibration": "not_done",
            "analysis": "no_data"
        }
        
    def show_dashboard(self):
        """Afficher le dashboard principal"""
        try:
            if not self.dashboard_window:
                self.dashboard_window = MainDashboard(self.project, self.file_path)
                
                # Connexions des signaux
                self.dashboard_window.module_changed.connect(self.on_module_changed)
                self.dashboard_window.project_updated.connect(self.on_project_updated)
                self.dashboard_window.destroyed.connect(self.on_dashboard_closed)
                
                # Connexion du bouton retour
                self.dashboard_window.navigation_sidebar.return_to_project_manager.connect(
                    self.on_return_to_project_manager
                )
                
            # Afficher la fenêtre
            self.dashboard_window.show()
            self.dashboard_window.raise_()
            self.dashboard_window.activateWindow()
            
            # Mettre à jour l'état système
            self.update_system_status_display()
            
        except Exception as e:
            print(f"[DashboardController] Erreur lors de l'affichage du dashboard: {e}")
            self.show_error_message("Erreur", f"Impossible d'ouvrir le dashboard:\n{str(e)}")
            
    def on_module_changed(self, module_name: str):
        """Gestionnaire de changement de module"""
        self.current_module = module_name
        self.module_switched.emit(module_name)
        
        # Changer le panel selon le module
        if not self.dashboard_window:
            return
        
        if module_name == "calibration":
            # Initialiser le contrôleur de calibration si nécessaire
            if not self.calibration_controller:
                self.calibration_controller = CalibrationController(self.project)
            # Injecter le panel de calibration piloté par le contrôleur
            self.dashboard_window.set_module_panel("calibration", self.calibration_controller.panel)
            # Afficher le panel de calibration
            self.dashboard_window.switch_module_panel("calibration")
        else:
            # Afficher le panel correspondant
            self.dashboard_window.switch_module_panel(module_name)
        
        print(f"[DashboardController] Module changé vers: {module_name}")
        
    def on_project_updated(self, project: ProjectInfo):
        """Gestionnaire de mise à jour du projet"""
        self.project = project
        self.project_updated.emit(project)
        
        # Mettre à jour l'affichage
        if self.dashboard_window:
            self.dashboard_window.update_project_info(project)
            
    def on_dashboard_closed(self):
        """Gestionnaire de fermeture du dashboard"""
        self.dashboard_window = None
        self.dashboard_closed.emit()
        
    def on_return_to_project_manager(self):
        """Gestionnaire de retour au gestionnaire de projets"""
        if self.dashboard_window:
            self.dashboard_window.close()
            
    def switch_module(self, module_name: str):
        """Changement de module avec transition"""
        if not self.dashboard_window:
            return
            
        # Vérifier que le module existe
        valid_modules = ["dashboard", "calibration", "acquisition", "stats", "advanced", "export"]
        if module_name not in valid_modules:
            print(f"[DashboardController] Module invalide: {module_name}")
            return
            
        # Changer le module dans la sidebar
        self.dashboard_window.navigation_sidebar.set_active_module(module_name)
        
        # TODO: Implémenter le changement de panel de contenu
        print(f"[DashboardController] Changement vers module: {module_name}")
        
    def update_project_info(self, project: ProjectInfo):
        """Mise à jour des informations projet"""
        self.project = project
        
        if self.dashboard_window:
            self.dashboard_window.update_project_info(project)
            
    def update_system_status(self, status_updates: dict):
        """Mise à jour de l'état système"""
        # Mettre à jour l'état interne
        for key, value in status_updates.items():
            if key in self.system_status:
                self.system_status[key] = value
                
        # Mettre à jour l'affichage
        self.update_system_status_display()
        
    def update_system_status_display(self):
        """Mise à jour de l'affichage de l'état système"""
        if not self.dashboard_window:
            return
            
        # Mettre à jour la sidebar
        self.dashboard_window.navigation_sidebar.update_system_status(self.system_status)
        
        # TODO: Mettre à jour le panel principal si nécessaire
        
    def get_system_status(self) -> dict:
        """Obtenir l'état actuel du système"""
        return self.system_status.copy()
        
    def simulate_system_activity(self):
        """Simuler l'activité système pour démonstration"""
        import random
        
        # Simulation de changements d'état
        possible_updates = {
            "sensors": ["disconnected", "connected", "warning"],
            "acquisition": ["stopped", "running", "paused"],
            "calibration": ["not_done", "in_progress", "completed"],
            "analysis": ["no_data", "processing", "completed"]
        }
        
        # Choisir un composant à mettre à jour
        component = random.choice(list(possible_updates.keys()))
        new_status = random.choice(possible_updates[component])
        
        # Mettre à jour l'état
        self.update_system_status({component: new_status})
        
        print(f"[DashboardController] Simulation: {component} -> {new_status}")
        
    def start_system_monitoring(self):
        """Démarrer le monitoring du système"""
        # Timer pour la simulation d'activité système
        self.monitoring_timer = QTimer()
        self.monitoring_timer.timeout.connect(self.simulate_system_activity)
        self.monitoring_timer.start(10000)  # Toutes les 10 secondes
        
        print("[DashboardController] Monitoring système démarré")
        
    def stop_system_monitoring(self):
        """Arrêter le monitoring du système"""
        if hasattr(self, 'monitoring_timer'):
            self.monitoring_timer.stop()
            print("[DashboardController] Monitoring système arrêté")
            
    def show_error_message(self, title: str, message: str):
        """Afficher un message d'erreur"""
        QMessageBox.critical(None, title, message)
        
    def show_info_message(self, title: str, message: str):
        """Afficher un message d'information"""
        QMessageBox.information(None, title, message)
        
    def close_dashboard(self):
        """Fermer le dashboard"""
        if self.dashboard_window:
            self.dashboard_window.close()
            
    def is_dashboard_open(self) -> bool:
        """Vérifier si le dashboard est ouvert"""
        return self.dashboard_window is not None and self.dashboard_window.isVisible()
        
    def get_current_module(self) -> str:
        """Obtenir le module actuellement actif"""
        return self.current_module
        
    def get_project_info(self) -> ProjectInfo:
        """Obtenir les informations du projet actuel"""
        return self.project
