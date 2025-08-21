"""
Test simple des composants modernes
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

def test_modern_components():
    """Test simple des composants modernes"""
    app = QApplication(sys.argv)
    
    # Fenêtre de test
    window = QMainWindow()
    window.setWindowTitle("Test Composants Modernes")
    window.resize(800, 600)
    
    # Widget central
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Layout
    layout = QVBoxLayout(central_widget)
    
    try:
        # Test 1: Design System
        print("Tests Test 1: Design System")
        from src.ui.resources.modern_design_system import ModernDesignSystem
        colors = ModernDesignSystem.get_color_palette()
        print(f"✓ Couleurs chargées: {len(colors)} couleurs")
        
        # Test 2: Composants
        print("Tests Test 2: Composants Modernes")
        from src.ui.components.modern.modern_card import ModernCard, StatusCard, ActionCard
        print("✓ Cartes modernes chargées")
        
        from src.ui.components.modern.modern_button import ModernButton
        print("✓ Boutons modernes chargés")
        
        from src.ui.components.modern.modern_sidebar import ModernNavigationSidebar
        print("✓ Sidebar moderne chargée")
        
        # Test 3: Création d'instances
        print("Tests Test 3: Création d'instances")
        
        # Créer une carte de test
        test_card = ModernCard(title="Test", style="glassmorphism")
        layout.addWidget(test_card)
        
        # Créer un bouton de test
        test_button = ModernButton("Test Bouton", "primary", "md")
        layout.addWidget(test_button)
        
        print("✓ Instances créées avec succès")
        
        # Afficher la fenêtre
        window.show()
        print("✓ Fenêtre affichée")
        
        return app.exec()
        
    except Exception as e:
        print(f"Erreur Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_modern_components())
