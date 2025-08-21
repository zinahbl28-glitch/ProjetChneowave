from .base_module_panel import BaseModulePanel


class AcquisitionPanel(BaseModulePanel):
    """Panel du module Acquisition"""
    
    def __init__(self, parent=None):
        super().__init__(
            module_name="acquisition",
            module_title="Module Acquisition",
            module_description="Acquisition temps réel des données",
            parent=parent
        )
        
        # Configuration spécifique au module acquisition
        self.setup_acquisition_specific_ui()
        
    def setup_acquisition_specific_ui(self):
        """Configuration spécifique au module acquisition"""
        # TODO: Ajouter des éléments spécifiques à l'acquisition
        # Par exemple: contrôles de démarrage/arrêt, visualisation temps réel, etc.
        pass
