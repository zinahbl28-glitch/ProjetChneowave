"""
Écran de démarrage moderne pour CHNeoWave - Interface scientifique
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QPixmap

from ..resources.modern_design_system import ModernDesignSystem


class ModernSplashWidget(QWidget):
    """Widget de démarrage moderne sans animations complexes"""
    
    # Signaux
    splash_complete = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.loading_steps = [
            "Initialisation du système...",
            "Chargement des composants...",
            "Configuration de l'interface...",
            "Vérification des capteurs...",
            "Interface prête"
        ]
        
        self._setup_modern_style()
        self._setup_layout()
        self._setup_loading_animation()
        
    def _setup_modern_style(self):
        """Style moderne sans effets complexes"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Style de la fenêtre
        colors = ModernDesignSystem.get_color_palette()
        radius = ModernDesignSystem.get_border_radius()
        
        self.setStyleSheet(f"""
            ModernSplashWidget {{
                background: {colors['surface']};
                border: 2px solid {colors['primary']};
                border-radius: {radius['lg']}px;
            }}
        """)
        
        # Taille fixe
        self.setFixedSize(600, 400)
        
    def _setup_layout(self):
        """Layout du splash screen"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(6)
        
        # Logo et titre
        self._setup_header()
        
        # Barre de progression
        self._setup_progress()
        
        # Étapes de chargement
        self._setup_loading_steps()
        
        # Spacer pour centrer
        self.main_layout.addStretch()
        
    def _setup_header(self):
        """En-tête avec logo et titre"""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(6)
        
        # Logo (placeholder)
        logo_label = QLabel("CHNeoWave")
        logo_label.setFont(ModernDesignSystem.get_font('hero'))
        logo_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['primary']}; font-weight: bold;")
        header_layout.addWidget(logo_label)
        
        header_layout.addStretch()
        
        # Titre
        title_label = QLabel("Interface Scientifique")
        title_label.setFont(ModernDesignSystem.get_font('h1'))
        title_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_primary']};")
        header_layout.addWidget(title_label)
        
        self.main_layout.addLayout(header_layout)
        
    def _setup_progress(self):
        """Barre de progression"""
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.loading_steps))
        self.progress_bar.setValue(0)
        
        colors = ModernDesignSystem.get_color_palette()
        radius = ModernDesignSystem.get_border_radius()
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {colors['border']};
                border-radius: {radius['md']}px;
                text-align: center;
                background: {colors['surface_light']};
                height: 20px;
            }}
            QProgressBar::chunk {{
                background: {colors['gradient_primary']};
                border-radius: {radius['sm']}px;
            }}
        """)
        
        self.main_layout.addWidget(self.progress_bar)
        
    def _setup_loading_steps(self):
        """Étapes de chargement"""
        self.step_label = QLabel(self.loading_steps[0])
        self.step_label.setFont(ModernDesignSystem.get_font('body'))
        self.step_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_secondary']};")
        self.step_label.setAlignment(Qt.AlignCenter)
        
        self.main_layout.addWidget(self.step_label)
        
    def _setup_loading_animation(self):
        """Animation de chargement simplifiée"""
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self._next_loading_step)
        self.loading_timer.start(150)  # 150ms par étape (≈0.75s total)
        
    def _next_loading_step(self):
        """Passe à l'étape suivante"""
        self.current_step += 1
        
        if self.current_step < len(self.loading_steps):
            # Mettre à jour l'interface
            self.step_label.setText(self.loading_steps[self.current_step])
            self.progress_bar.setValue(self.current_step)
        else:
            # Chargement terminé
            self.loading_timer.stop()
            self.progress_bar.setValue(len(self.loading_steps))
            self.step_label.setText("Interface prête")
            
            # Délai avant fermeture (rapide)
            QTimer.singleShot(50, self._complete_splash)
            
    def _complete_splash(self):
        """Termine le splash screen"""
        self.splash_complete.emit()
        
    def center_on_screen(self):
        """Centre le splash sur l'écran"""
        from PySide6.QtWidgets import QApplication
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
