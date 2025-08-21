from .base_module_panel import BaseModulePanel


class ExportPanel(BaseModulePanel):
    """Panel du module Export"""
    
    def __init__(self, parent=None):
        super().__init__(
            module_name="export",
            module_title="Module Export",
            module_description="Export des résultats et données",
            parent=parent
        )
        
        # Configuration spécifique au module export
        self.setup_export_specific_ui()
        
    def setup_export_specific_ui(self):
        """Configuration spécifique au module export"""
        # TODO: Ajouter des éléments spécifiques à l'export
        # Par exemple: sélecteur de formats, options d'export, etc.
        pass
