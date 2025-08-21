"""
Bootstrap de l'Interface Moderne 2025 - CHNeoWave
Script de démonstration de la transformation moderne de l'interface
"""

import sys
import os
import time

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette

# Imports absolus pour permettre l'exécution directe
from src.ui.windows.modern_main_dashboard import ModernMainDashboard
from src.ui.windows.modern_splash_screen import ModernSplashWidget
from src.ui.components.app_state import ProjectInfo
from src.ui.resources.modern_design_system import ModernDesignSystem


# Variables globales pour maintenir les références
splash_screen = None
main_dashboard = None
_start_time = time.perf_counter()
_splash_start_time = None
_splash_complete_time = None
_dashboard_shown_time = None


def create_demo_project():
    """Crée un projet de démonstration"""
    return ProjectInfo(
        name="Projet Démo - Interface Moderne 2025",
        code="CHW-2025-001",
        engineer="Ingénieur Démo",
        manager="Manager Démo",
        scale="1:100",
        basin_type="Canal de Test"
    )


def main():
    """Point d'entrée principal"""
    global splash_screen, main_dashboard, _splash_start_time
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave - Interface Moderne 2025")
    app.setApplicationVersion("2.0.0")
    
    # Appliquer la palette moderne globale
    modern_palette = ModernDesignSystem.create_modern_palette()
    app.setPalette(modern_palette)
    
    # Créer le projet de démonstration
    demo_project = create_demo_project()
    
    # Créer et afficher le splash screen moderne
    splash_screen = ModernSplashWidget()
    splash_screen.splash_complete.connect(lambda: _on_splash_complete(app, demo_project))
    
    # Centrer le splash sur l'écran
    splash_screen.center_on_screen()
    splash_screen.show()
    _splash_start_time = time.perf_counter()
    
    print("Interface Moderne 2025 - CHNeoWave")
    print("Splash screen initialisé")
    print("Design system moderne appliqué")
    print("Composants modernes chargés")
    print("Prêt pour la démonstration")
    
    # Lancer la boucle d'événements principale
    return app.exec()


def _on_splash_complete(app, demo_project):
    """Callback appelé quand le splash est terminé"""
    global main_dashboard, splash_screen, _splash_complete_time, _dashboard_shown_time
    
    _splash_complete_time = time.perf_counter()
    print(f"[Perf] Splash duration: {(_splash_complete_time - _splash_start_time)*1000:.1f} ms")
    
    # Fermer le splash screen
    splash_screen.close()
    
    # Créer le dashboard moderne
    main_dashboard = ModernMainDashboard(demo_project)
    main_dashboard.show()
    _dashboard_shown_time = time.perf_counter()
    
    # Centrer la fenêtre
    screen = app.primaryScreen().geometry()
    main_dashboard.move(
        (screen.width() - main_dashboard.width()) // 2,
        (screen.height() - main_dashboard.height()) // 2
    )
    
    print(f"[Perf] Dashboard after splash: {(_dashboard_shown_time - _splash_complete_time)*1000:.1f} ms")
    print(f"[Perf] Total to dashboard: {(_dashboard_shown_time - _start_time)*1000:.1f} ms")
    
    print("Dashboard moderne initialisé avec succès")
    print("Interface prête à l'utilisation !")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Erreur lors du démarrage: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

