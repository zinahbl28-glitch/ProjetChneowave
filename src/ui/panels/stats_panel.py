from .base_module_panel import BaseModulePanel


class StatsPanel(BaseModulePanel):
    """Panel du module Statistiques"""
    
    def __init__(self, parent=None):
        super().__init__(
            module_name="stats",
            module_title="Statistique Module Analyse Statistique",
            module_description="Analyse statistique des données acquises",
            parent=parent
        )
        
        # Configuration spécifique au module statistiques
        self.setup_stats_specific_ui()
        
    def setup_stats_specific_ui(self):
        """Configuration spécifique au module statistiques"""
        # TODO: Ajouter des éléments spécifiques aux statistiques
        # Par exemple: graphiques, tableaux de données, etc.
        pass
