"""
Système de Design Moderne 2025 pour CHNeoWave
Typographie massive, morphisme, couleurs vibrantes et animations fluides
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtGui import QFont, QColor, QPalette
import math


class ModernDesignSystem:
    """Système de design moderne 2025 - Transformation complète de l'interface"""
    
    # ===== TYPOGRAPHIE MODERNE - IMPACT VISUEL =====
    @classmethod
    def get_typography_scale(cls):
        """Échelle typographique moderne avec tailles massives"""
        return {
            'hero': {'size': 20, 'weight': 'bold', 'line_height': 1.1, 'family': 'Inter Display'},
            'h1': {'size': 16, 'weight': 'semibold', 'line_height': 1.2, 'family': 'Inter'},
            'h2': {'size': 14, 'weight': 'medium', 'line_height': 1.3, 'family': 'Inter'},
            'h3': {'size': 13, 'weight': 'medium', 'line_height': 1.4, 'family': 'Inter'},
            'body': {'size': 12, 'weight': 'normal', 'line_height': 1.5, 'family': 'Inter'},
            'body_small': {'size': 10, 'weight': 'normal', 'line_height': 1.4, 'family': 'Inter'},
            'caption': {'size': 10, 'weight': 'normal', 'line_height': 1.3, 'family': 'Inter'},
            'button': {'size': 12, 'weight': '600', 'line_height': 1.2, 'family': 'Inter'},
            'nav': {'size': 12, 'weight': '500', 'line_height': 1.2, 'family': 'Inter'}
        }
    
    @classmethod
    def get_font(cls, style='body'):
        """Retourne un QFont configuré selon le style moderne"""
        typo = cls.get_typography_scale().get(style, cls.get_typography_scale()['body'])
        
        font = QFont(typo['family'], typo['size'])
        font.setWeight(cls._get_font_weight(typo['weight']))
        return font
    
    @staticmethod
    def _get_font_weight(weight_str):
        """Convertit string weight en QFont.Weight"""
        weights = {
            'normal': QFont.Weight.Normal,
            'medium': QFont.Weight.Medium,
            'semibold': QFont.Weight.DemiBold,
            'bold': QFont.Weight.Bold,
            '600': QFont.Weight.DemiBold
        }
        return weights.get(weight_str, QFont.Weight.Normal)
    
    # ===== PALETTE DE COULEURS MODERNES 2025 =====
    @classmethod
    def get_color_palette(cls):
        """Palette moderne avec contrastes forts et couleurs vibrantes"""
        return {
            # Couleurs principales vibrantes
            'primary': '#6366F1',      # Indigo moderne
            'primary_dark': '#4F46E5', # Indigo sombre
            'secondary': '#EC4899',    # Pink vibrant
            'secondary_dark': '#DB2777', # Pink sombre
            'accent': '#10B981',       # Emerald
            'accent_dark': '#059669',  # Emerald sombre
            
            # Backgrounds sombres et profonds
            'bg_primary': '#0F0F23',   # Dark deep
            'bg_secondary': '#1A1B3A', # Purple dark
            'bg_tertiary': '#0D1117',  # GitHub dark
            'surface': '#252641',      # Cards/containers
            'surface_light': '#2D2E4A',
            'surface_hover': '#3A3B5A',
            
            # Textes avec contrastes élevés
            'text_primary': '#F8FAFC',   # White clean
            'text_secondary': '#94A3B8', # Gray medium
            'text_muted': '#64748B',     # Gray light
            'text_inverse': '#0F0F23',   # Dark sur light
            
            # Status colors vibrants
            'success': '#22C55E',
            'success_dark': '#16A34A',
            'warning': '#F59E0B', 
            'warning_dark': '#D97706',
            'error': '#EF4444',
            'error_dark': '#DC2626',
            'info': '#3B82F6',
            'info_dark': '#2563EB',
            
            # Gradients modernes
            'gradient_primary': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366F1, stop:1 #EC4899)',
            'gradient_dark': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0F0F23, stop:1 #1A1B3A)',
            'gradient_surface': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #252641, stop:1 #2D2E4A)',
            'gradient_accent': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #3B82F6)',
            
            # Couleurs spéciales
            'border': '#374151',
            'border_light': '#4B5563',
            'shadow': 'rgba(0, 0, 0, 0.25)',
            'overlay': 'rgba(15, 15, 35, 0.8)'
        }
    
    # ===== SYSTÈME D'ESPACEMENT MODERNE =====
    @classmethod
    def get_spacing_system(cls):
        """Système d'espacement moderne avec espacement généreux"""
        return {
            'xs': 2,
            'sm': 4,
            'md': 6,
            'lg': 8,
            'xl': 12,
            'xxl': 18,
            'container': 16,
            'section': 24,
            'hero': 36
        }
    
    @classmethod
    def get_border_radius(cls):
        """Système de bordures arrondies modernes"""
        return {
            'xs': 4,     # Petits éléments
            'sm': 8,     # Boutons
            'md': 12,    # Cartes
            'lg': 16,    # Conteneurs
            'xl': 20,    # Sections
            'xxl': 24,   # Hero sections
            'full': 9999 # Pills/badges
        }
    
    # ===== STYLES DE COMPOSANTS MODERNES =====
    @classmethod
    def get_button_styles(cls):
        """Styles de boutons modernes avec morphisme"""
        colors = cls.get_color_palette()
        radius = cls.get_border_radius()
        
        return {
            'primary': f"""
                QPushButton {{
                    background: {colors['gradient_primary']};
                    border: none;
                    border-radius: {radius['md']}px;
                    color: {colors['text_primary']};
                    font-size: 12px;
                    font-weight: 600;
                    padding: 6px 12px;
                    min-height: 26px;
                }}
                QPushButton:hover {{
                    background: {colors['gradient_accent']};
                    transform: translateY(-2px);
                }}
                QPushButton:pressed {{
                    transform: translateY(0px);
                }}
            """,
            
            'secondary': f"""
                QPushButton {{
                    background: {colors['surface']};
                    border: 2px solid {colors['primary']};
                    border-radius: {radius['md']}px;
                    color: {colors['primary']};
                    font-size: 12px;
                    font-weight: 600;
                    padding: 6px 12px;
                    min-height: 26px;
                }}
                QPushButton:hover {{
                    background: {colors['primary']};
                    color: {colors['text_primary']};
                }}
            """,
            
            'ghost': f"""
                QPushButton {{
                    background: transparent;
                    border: 1px solid {colors['border']};
                    border-radius: {radius['sm']}px;
                    color: {colors['text_secondary']};
                    font-size: 12px;
                    font-weight: 500;
                    padding: 4px 8px;
                    min-height: 22px;
                }}
                QPushButton:hover {{
                    background: {colors['surface_hover']};
                    border-color: {colors['primary']};
                    color: {colors['text_primary']};
                }}
            """,
            
            'danger': f"""
                QPushButton {{
                    background: {colors['error']};
                    border: none;
                    border-radius: {radius['md']}px;
                    color: {colors['text_primary']};
                    font-size: 12px;
                    font-weight: 600;
                    padding: 6px 12px;
                    min-height: 26px;
                }}
                QPushButton:hover {{
                    background: {colors['error_dark']};
                }}
            """
        }
    
    @classmethod
    def get_card_styles(cls):
        """Styles de cartes modernes avec glassmorphism"""
        colors = cls.get_color_palette()
        radius = cls.get_border_radius()
        
        return f"""
            QFrame {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {radius['lg']}px;
                padding: 8px;
            }}
            QFrame:hover {{
                border-color: {colors['primary']};
                background: {colors['surface_hover']};
            }}
        """
    
    @classmethod
    def get_sidebar_styles(cls):
        """Styles de sidebar moderne avec blur"""
        colors = cls.get_color_palette()
        
        return f"""
            QWidget {{
                background: {colors['bg_secondary']};
                border-right: 1px solid {colors['border']};
            }}
        """
    
    # ===== SYSTÈME D'ANIMATIONS MODERNES =====
    @classmethod
    def create_hover_animation(cls, widget, scale=1.05, duration=200):
        """Crée animation hover moderne avec scale up"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        return animation
    
    @classmethod
    def create_fade_in_animation(cls, widget, duration=300):
        """Animation fade in progressif"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        return animation
    
    @classmethod
    def create_slide_in_animation(cls, widget, direction='left', distance=100, duration=400):
        """Animation slide in depuis une direction"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Position initiale selon direction
        if direction == 'left':
            animation.setStartValue(widget.geometry().adjusted(-distance, 0, -distance, 0))
        elif direction == 'right':
            animation.setStartValue(widget.geometry().adjusted(distance, 0, distance, 0))
        elif direction == 'top':
            animation.setStartValue(widget.geometry().adjusted(0, -distance, 0, -distance))
        elif direction == 'bottom':
            animation.setStartValue(widget.geometry().adjusted(0, distance, 0, distance))
        
        animation.setEndValue(widget.geometry())
        return animation
    
    @classmethod
    def create_pulse_animation(cls, widget, scale_range=(1.0, 1.1), duration=1000):
        """Animation pulse continue"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setLoopCount(-1)  # Infini
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Scale up puis down
        original_geo = widget.geometry()
        center = original_geo.center()
        
        # Calculer les nouvelles dimensions
        scale_min, scale_max = scale_range
        width_min = int(original_geo.width() * scale_min)
        height_min = int(original_geo.height() * scale_min)
        width_max = int(original_geo.width() * scale_max)
        height_max = int(original_geo.height() * scale_max)
        
        # Positions centrées
        x_min = center.x() - width_min // 2
        y_min = center.y() - height_min // 2
        x_max = center.x() - width_max // 2
        y_max = center.y() - height_max // 2
        
        # Keyframes
        animation.setKeyValueAt(0.0, original_geo)
        animation.setKeyValueAt(0.5, widget.geometry().adjusted(x_max, y_max, x_max + width_max, y_max + height_max))
        animation.setKeyValueAt(1.0, original_geo)
        
        return animation
    
    # ===== UTILITAIRES DE STYLE =====
    @classmethod
    def apply_modern_stylesheet(cls, widget, style_type='default'):
        """Applique un stylesheet moderne au widget"""
        if style_type == 'card':
            widget.setStyleSheet(cls.get_card_styles())
        elif style_type == 'sidebar':
            widget.setStyleSheet(cls.get_sidebar_styles())
        elif style_type == 'modern_window':
            colors = cls.get_color_palette()
            widget.setStyleSheet(f"""
                QMainWindow {{
                    background: {colors['gradient_dark']};
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                    color: {colors['text_primary']};
                }}
            """)
    
    @classmethod
    def create_modern_palette(cls):
        """Crée une palette moderne pour l'application"""
        colors = cls.get_color_palette()
        palette = QPalette()
        
        # Backgrounds
        palette.setColor(QPalette.ColorRole.Window, QColor(colors['bg_primary']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors['surface']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors['surface_light']))
        
        # Textes
        palette.setColor(QPalette.ColorRole.Text, QColor(colors['text_primary']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors['text_primary']))
        
        # Boutons
        palette.setColor(QPalette.ColorRole.Button, QColor(colors['surface']))
        palette.setColor(QPalette.ColorRole.Light, QColor(colors['surface_light']))
        palette.setColor(QPalette.ColorRole.Mid, QColor(colors['border']))
        palette.setColor(QPalette.ColorRole.Dark, QColor(colors['border_light']))
        
        # Liens et highlights
        palette.setColor(QPalette.ColorRole.Link, QColor(colors['primary']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors['text_primary']))
        
        return palette


# ===== CONSTANTES GLOBALES MODERNES =====
MODERN_FONTS = ModernDesignSystem.get_typography_scale()
MODERN_COLORS = ModernDesignSystem.get_color_palette()
MODERN_SPACING = ModernDesignSystem.get_spacing_system()
MODERN_BORDERS = ModernDesignSystem.get_border_radius()
MODERN_BUTTON_STYLES = ModernDesignSystem.get_button_styles()

