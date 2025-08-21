#!/usr/bin/env python3
"""
Démonstration de l'Interface Scientifique ChNeoWave
Test des modules de calibration et d'acquisition
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QTabWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# Ajouter le chemin des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Importer les modules scientifiques
from ui.panels.calibration.scientific_calibration_panel import ScientificCalibrationPanel
from ui.panels.scientific_acquisition_panel import ScientificAcquisitionPanel


class ScientificInterfaceDemo(QMainWindow):
    """Démonstration de l'interface scientifique ChNeoWave"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configuration de l'interface de démonstration"""
        self.setWindowTitle("ChNeoWave - Interface Scientifique - Démonstration")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # En-tête de démonstration
        self.setup_demo_header(main_layout)
        
        # Onglets pour les modules
        self.setup_module_tabs(main_layout)
        
        # Barre de statut
        self.setup_demo_status_bar(main_layout)
        
    def setup_demo_header(self, layout):
        """En-tête de démonstration"""
        header_frame = QWidget()
        header_frame.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1E40AF, stop:1 #3B82F6);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(8)
        
        # Titre principal
        title_label = QLabel("🧪 CHNEOWAVE - INTERFACE SCIENTIFIQUE")
        title_label.setFont(QFont("Inter", 20, QFont.Bold))
        title_label.setStyleSheet("color: white; text-align: center;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Sous-titre
        subtitle_label = QLabel("Démonstration des modules de calibration et d'acquisition")
        subtitle_label.setFont(QFont("Inter", 14))
        subtitle_label.setStyleSheet("color: #E2E8F0; text-align: center;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        # Informations de démonstration
        info_label = QLabel("📊 Modules disponibles: Calibration | Acquisition | Analyse Statistique | Analyse Avancée | Export")
        info_label.setFont(QFont("Inter", 12))
        info_label.setStyleSheet("color: #CBD5E1; text-align: center;")
        info_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(info_label)
        
        layout.addWidget(header_frame)
        
    def setup_module_tabs(self, layout):
        """Configuration des onglets de modules"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Inter", 12, QFont.Bold))
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #F1F5F9;
                border: 1px solid #E2E8F0;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                color: #475569;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #1E40AF;
            }
            QTabBar::tab:hover {
                background: #E2E8F0;
            }
        """)
        
        # Onglet Calibration
        self.calibration_tab = self.create_calibration_tab()
        self.tab_widget.addTab(self.calibration_tab, "⚙️ Calibration Scientifique")
        
        # Onglet Acquisition
        self.acquisition_tab = self.create_acquisition_tab()
        self.tab_widget.addTab(self.acquisition_tab, "📡 Acquisition Temps Réel")
        
        # Onglet Informations
        self.info_tab = self.create_info_tab()
        self.tab_widget.addTab(self.info_tab, "ℹ️ Informations")
        
        layout.addWidget(self.tab_widget)
        
    def create_calibration_tab(self):
        """Création de l'onglet de calibration"""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout(tab_widget)
        tab_layout.setContentsMargins(8, 8, 8, 8)
        tab_layout.setSpacing(8)
        
        # Description du module
        description_label = QLabel("""
        <h3>🧪 Module de Calibration Scientifique</h3>
        <p>Ce module permet de calibrer précisément les sondes d'élévation d'eau et de pression :</p>
        <ul>
            <li><strong>Configuration des sondes :</strong> Sélection du nombre et type de sondes</li>
            <li><strong>Points de calibration :</strong> Définition des points de mesure (0cm, 1cm, 2cm, 3cm, 5cm...)</li>
            <li><strong>Processus de calibration :</strong> Réglage du zéro et validation de la linéarité</li>
            <li><strong>Validation scientifique :</strong> Calcul du coefficient R² et validation de la qualité</li>
            <li><strong>Graphiques temps réel :</strong> Visualisation de la courbe de calibration</li>
        </ul>
        """)
        description_label.setFont(QFont("Inter", 11))
        description_label.setStyleSheet("color: #1E293B; background: #F8FAFC; padding: 12px; border-radius: 8px; border: 1px solid #E2E8F0;")
        description_label.setWordWrap(True)
        tab_layout.addWidget(description_label)
        
        # Module de calibration
        self.calibration_panel = ScientificCalibrationPanel()
        tab_layout.addWidget(self.calibration_panel)
        
        return tab_widget
        
    def create_acquisition_tab(self):
        """Création de l'onglet d'acquisition"""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout(tab_widget)
        tab_layout.setContentsMargins(8, 8, 8, 8)
        tab_layout.setSpacing(8)
        
        # Description du module
        description_label = QLabel("""
        <h3>📡 Module d'Acquisition Temps Réel</h3>
        <p>Ce module permet l'acquisition en temps réel des signaux des sondes :</p>
        <ul>
            <li><strong>Paramètres d'acquisition :</strong> Fréquence d'échantillonnage, cycle de temps, durée</li>
            <li><strong>Sélection des sondes :</strong> Activation/désactivation des sondes à acquérir</li>
            <li><strong>Visualisation temps réel :</strong> Graphiques individuels et multi-sondes</li>
            <li><strong>Métriques statistiques :</strong> Hmax, Hmin, H1/3, Hs, Tp, Tm en temps réel</li>
            <li><strong>Contrôles d'acquisition :</strong> Démarrage, arrêt, pause avec progression</li>
        </ul>
        """)
        description_label.setFont(QFont("Inter", 11))
        description_label.setStyleSheet("color: #1E293B; background: #F8FAFC; padding: 12px; border-radius: 8px; border: 1px solid #E2E8F0;")
        description_label.setWordWrap(True)
        tab_layout.addWidget(description_label)
        
        # Module d'acquisition
        self.acquisition_panel = ScientificAcquisitionPanel()
        tab_layout.addWidget(self.acquisition_panel)
        
        return tab_widget
        
    def create_info_tab(self):
        """Création de l'onglet d'informations"""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout(tab_widget)
        tab_layout.setContentsMargins(16, 16, 16, 16)
        tab_layout.setSpacing(16)
        
        # Informations sur ChNeoWave
        info_content = QLabel("""
        <h2>🚀 ChNeoWave - Logiciel d'Acquisition Scientifique</h2>
        
        <h3>📋 Description</h3>
        <p>ChNeoWave est un logiciel scientifique moderne conçu pour l'acquisition et l'analyse de données de houle. 
        Il offre une interface intuitive et des outils d'analyse avancés pour les chercheurs et ingénieurs en hydrodynamique.</p>
        
        <h3>🎯 Fonctionnalités Principales</h3>
        <ul>
            <li><strong>Calibration Scientifique :</strong> Calibration précise des sondes d'élévation d'eau et de pression</li>
            <li><strong>Acquisition Temps Réel :</strong> Acquisition continue des signaux avec visualisation en temps réel</li>
            <li><strong>Analyse Statistique :</strong> Calcul des paramètres de houle (Hmax, Hmin, H1/3, Hs, Tp, Tm)</li>
            <li><strong>Analyse Avancée :</strong> Méthodes Goda, FFT, moindres carrés pour l'analyse spectrale</li>
            <li><strong>Export Multi-Formats :</strong> Export des données en JSON, CSV, HDF5, PDF</li>
        </ul>
        
        <h3>🔬 Workflow Scientifique</h3>
        <ol>
            <li><strong>Création/Import de Projet :</strong> Configuration des paramètres du projet</li>
            <li><strong>Calibration des Sondes :</strong> Calibration précise de chaque sonde</li>
            <li><strong>Acquisition de Données :</strong> Acquisition temps réel des signaux</li>
            <li><strong>Analyse Statistique :</strong> Traitement et analyse des données</li>
            <li><strong>Analyse Avancée :</strong> Méthodes spécialisées (Goda, FFT, etc.)</li>
            <li><strong>Export des Résultats :</strong> Génération de rapports et export</li>
        </ol>
        
        <h3>🎨 Interface Scientifique</h3>
        <p>L'interface a été conçue selon les meilleures pratiques pour les logiciels scientifiques :</p>
        <ul>
            <li><strong>Design Professionnel :</strong> Interface claire et précise</li>
            <li><strong>Navigation Intuitive :</strong> Workflow logique et efficace</li>
            <li><strong>Visualisation Avancée :</strong> Graphiques temps réel et interactifs</li>
            <li><strong>Validation Scientifique :</strong> Métriques de qualité et validation</li>
            <li><strong>Performance Optimisée :</strong> Gestion mémoire et temps de réponse</li>
        </ul>
        
        <h3>📊 Métriques Scientifiques</h3>
        <ul>
            <li><strong>Hmax :</strong> Hauteur maximale des vagues</li>
            <li><strong>Hmin :</strong> Hauteur minimale des vagues</li>
            <li><strong>H1/3 :</strong> Hauteur significative (1/3 des plus grandes vagues)</li>
            <li><strong>Hs :</strong> Hauteur significative spectrale</li>
            <li><strong>Tp :</strong> Période de pic</li>
            <li><strong>Tm :</strong> Période moyenne</li>
        </ul>
        
        <h3>🔧 Technologies Utilisées</h3>
        <ul>
            <li><strong>Interface :</strong> PySide6 (Qt6) pour l'interface graphique</li>
            <li><strong>Graphiques :</strong> QtCharts pour la visualisation</li>
            <li><strong>Calculs :</strong> NumPy pour les calculs scientifiques</li>
            <li><strong>Données :</strong> JSON, CSV, HDF5 pour le stockage</li>
            <li><strong>Design :</strong> Système de design scientifique personnalisé</li>
        </ul>
        
        <h3>📈 Évolutions Futures</h3>
        <ul>
            <li>Intégration de nouveaux algorithmes d'analyse</li>
            <li>Support de formats de données supplémentaires</li>
            <li>Interface web pour accès distant</li>
            <li>Intégration avec des équipements de laboratoire</li>
            <li>Modules d'analyse spécialisés</li>
        </ul>
        """)
        
        info_content.setFont(QFont("Inter", 11))
        info_content.setStyleSheet("""
            QLabel {
                color: #1E293B;
                background: white;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #E2E8F0;
                line-height: 1.6;
            }
            QLabel h2 {
                color: #1E40AF;
                margin-top: 0;
            }
            QLabel h3 {
                color: #059669;
                margin-top: 20px;
            }
        """)
        info_content.setWordWrap(True)
        
        # Scroll area pour le contenu
        from PySide6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidget(info_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #F1F5F9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }
        """)
        
        tab_layout.addWidget(scroll_area)
        
        return tab_widget
        
    def setup_demo_status_bar(self, layout):
        """Barre de statut de démonstration"""
        status_frame = QWidget()
        status_frame.setStyleSheet("""
            QWidget {
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(12, 6, 12, 6)
        
        # Statut de démonstration
        demo_status = QLabel("🧪 Mode Démonstration - Interface Scientifique ChNeoWave")
        demo_status.setFont(QFont("Inter", 10, QFont.Bold))
        demo_status.setStyleSheet("color: #1E40AF;")
        
        # Informations de version
        version_info = QLabel("Version: 1.0.0 | Développement")
        version_info.setFont(QFont("Inter", 10))
        version_info.setStyleSheet("color: #64748B;")
        
        # Boutons d'action
        help_btn = QPushButton("❓ Aide")
        help_btn.setFont(QFont("Inter", 10))
        help_btn.setStyleSheet("""
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background: #2563EB;
            }
        """)
        help_btn.clicked.connect(self.show_help)
        
        about_btn = QPushButton("ℹ️ À propos")
        about_btn.setFont(QFont("Inter", 10))
        about_btn.setStyleSheet("""
            QPushButton {
                background: #059669;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background: #047857;
            }
        """)
        about_btn.clicked.connect(self.show_about)
        
        status_layout.addWidget(demo_status)
        status_layout.addStretch()
        status_layout.addWidget(version_info)
        status_layout.addWidget(help_btn)
        status_layout.addWidget(about_btn)
        
        layout.addWidget(status_frame)
        
    def setup_connections(self):
        """Configuration des connexions"""
        # Connexions des modules
        if hasattr(self, 'calibration_panel'):
            self.calibration_panel.calibration_completed.connect(self.on_calibration_completed)
            self.calibration_panel.calibration_error.connect(self.on_calibration_error)
            
        if hasattr(self, 'acquisition_panel'):
            self.acquisition_panel.acquisition_started.connect(self.on_acquisition_started)
            self.acquisition_panel.acquisition_stopped.connect(self.on_acquisition_stopped)
            self.acquisition_panel.acquisition_error.connect(self.on_acquisition_error)
            
    def on_calibration_completed(self, data):
        """Callback pour calibration terminée"""
        QMessageBox.information(
            self,
            "Calibration Terminée",
            f"Calibration terminée avec succès !\n\n"
            f"Sondes calibrées : {len(data)}\n"
            f"Sondes validées : {sum(1 for p in data.values() if p.get('status') == 'validated')}"
        )
        
    def on_calibration_error(self, error_msg):
        """Callback pour erreur de calibration"""
        QMessageBox.critical(
            self,
            "Erreur de Calibration",
            f"Erreur lors de la calibration :\n{error_msg}"
        )
        
    def on_acquisition_started(self):
        """Callback pour acquisition démarrée"""
        print("🟢 Acquisition démarrée")
        
    def on_acquisition_stopped(self):
        """Callback pour acquisition arrêtée"""
        print("🔴 Acquisition arrêtée")
        
    def on_acquisition_error(self, error_msg):
        """Callback pour erreur d'acquisition"""
        QMessageBox.critical(
            self,
            "Erreur d'Acquisition",
            f"Erreur lors de l'acquisition :\n{error_msg}"
        )
        
    def show_help(self):
        """Afficher l'aide"""
        QMessageBox.information(
            self,
            "Aide - ChNeoWave",
            """
            <h3>🧪 Aide ChNeoWave</h3>
            
            <h4>Module Calibration :</h4>
            <ul>
                <li>Configurez le nombre de sondes et les paramètres</li>
                <li>Sélectionnez les points de calibration</li>
                <li>Démarrez la calibration et suivez le processus</li>
                <li>Validez les résultats avec les graphiques</li>
            </ul>
            
            <h4>Module Acquisition :</h4>
            <ul>
                <li>Définissez les paramètres d'acquisition</li>
                <li>Sélectionnez les sondes à acquérir</li>
                <li>Démarrez l'acquisition et observez les graphiques</li>
                <li>Surveillez les métriques statistiques</li>
            </ul>
            
            <h4>Navigation :</h4>
            <ul>
                <li>Utilisez les onglets pour naviguer entre les modules</li>
                <li>Consultez les informations dans l'onglet "Informations"</li>
                <li>Les données sont sauvegardées automatiquement</li>
            </ul>
            """
        )
        
    def show_about(self):
        """Afficher les informations à propos"""
        QMessageBox.about(
            self,
            "À propos - ChNeoWave",
            """
            <h3>🚀 ChNeoWave</h3>
            <p><strong>Version :</strong> 1.0.0</p>
            <p><strong>Description :</strong> Logiciel scientifique d'acquisition et d'analyse de données de houle</p>
            <p><strong>Développé avec :</strong> Python, PySide6, NumPy, QtCharts</p>
            <p><strong>Interface :</strong> Design scientifique moderne</p>
            <br>
            <p>© 2024 - Interface Scientifique ChNeoWave</p>
            """
        )


def main():
    """Fonction principale de démonstration"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("ChNeoWave Scientific Interface")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ChNeoWave")
    
    # Style global
    app.setStyleSheet("""
        QApplication {
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
    """)
    
    # Création et affichage de la fenêtre de démonstration
    demo_window = ScientificInterfaceDemo()
    demo_window.show()
    
    # Message de démarrage
    print("🚀 Démarrage de la démonstration ChNeoWave")
    print("📊 Interface scientifique chargée")
    print("🧪 Modules disponibles : Calibration, Acquisition")
    print("ℹ️ Consultez l'onglet 'Informations' pour plus de détails")
    
    # Exécution de l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()