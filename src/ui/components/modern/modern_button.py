"""
Bouton moderne sans animations - Interface scientifique CHNeoWave
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...resources.modern_design_system import ModernDesignSystem


class ModernButton(QPushButton):
    """Bouton moderne sans animations pour interface scientifique"""
    
    def __init__(self, text="", style="primary", size="md", parent=None):
        super().__init__(text, parent)
        self.style_type = style
        self.size_type = size
        self._setup_modern_style()
        
    def _setup_modern_style(self):
        """Style moderne sans animations"""
        colors = ModernDesignSystem.get_color_palette()
        radius = ModernDesignSystem.get_border_radius()
        
        # Tailles selon le type
        size_config = {
            'sm': {'padding': '2px 6px', 'min_height': 18, 'font_size': 10},
            'md': {'padding': '3px 8px', 'min_height': 22, 'font_size': 11},
            'lg': {'padding': '4px 10px', 'min_height': 26, 'font_size': 12}
        }
        
        config = size_config.get(self.size_type, size_config['md'])
        
        # Styles selon le type
        if self.style_type == 'primary':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {colors['gradient_primary']};
                    border: none;
                    border-radius: {radius['md']}px;
                    color: {colors['text_primary']};
                    font-size: {config['font_size']}px;
                    font-weight: 600;
                    padding: {config['padding']};
                    min-height: {config['min_height']}px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                }}
                QPushButton:hover {{
                    background: {colors['gradient_accent']};
                }}
                QPushButton:pressed {{
                    background: {colors['primary_dark']};
                }}
                QPushButton:disabled {{
                    background: {colors['border']};
                    color: {colors['text_muted']};
                }}
            """)
            
        elif self.style_type == 'secondary':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {colors['surface']};
                    border: 2px solid {colors['primary']};
                    border-radius: {radius['md']}px;
                    color: {colors['primary']};
                    font-size: {config['font_size']}px;
                    font-weight: 600;
                    padding: {config['padding']};
                    min-height: {config['min_height']}px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                }}
                QPushButton:hover {{
                    background: {colors['primary']};
                    color: {colors['text_primary']};
                }}
                QPushButton:pressed {{
                    background: {colors['primary_dark']};
                    border-color: {colors['primary_dark']};
                }}
            """)
            
        elif self.style_type == 'ghost':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: 1px solid {colors['border']};
                    border-radius: {radius['sm']}px;
                    color: {colors['text_secondary']};
                    font-size: {config['font_size']}px;
                    font-weight: 500;
                    padding: {config['padding']};
                    min-height: {config['min_height']}px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                }}
                QPushButton:hover {{
                    background: {colors['surface_hover']};
                    border-color: {colors['primary']};
                    color: {colors['text_primary']};
                }}
                QPushButton:pressed {{
                    background: {colors['surface']};
                }}
            """)
            
        elif self.style_type == 'danger':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {colors['error']};
                    border: none;
                    border-radius: {radius['md']}px;
                    color: {colors['text_primary']};
                    font-size: {config['font_size']}px;
                    font-weight: 600;
                    padding: {config['padding']};
                    min-height: {config['min_height']}px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                }}
                QPushButton:hover {{
                    background: {colors['error_dark']};
                }}
                QPushButton:pressed {{
                    background: {colors['error_dark']};
                }}
            """)
            
        elif self.style_type == 'success':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {colors['success']};
                    border: none;
                    border-radius: {radius['md']}px;
                    color: {colors['text_primary']};
                    font-size: {config['font_size']}px;
                    font-weight: 600;
                    padding: {config['padding']};
                    min-height: {config['min_height']}px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont;
                }}
                QPushButton:hover {{
                    background: {colors['success_dark']};
                }}
                QPushButton:pressed {{
                    background: {colors['success_dark']};
                }}
            """)
    
    def set_loading_state(self, loading=True):
        """Change l'état du bouton (loading/disabled)"""
        if loading:
            self.setEnabled(False)
            self.setText("Chargement...")
        else:
            self.setEnabled(True)
            self.setText(self._original_text if hasattr(self, '_original_text') else "")
            
    def set_text(self, text):
        """Change le texte du bouton"""
        if not hasattr(self, '_original_text'):
            self._original_text = self.text()
        self.setText(text)
        
    def set_icon(self, icon_path, size=24):
        """Ajoute une icône au bouton"""
        from PySide6.QtGui import QIcon
        from PySide6.QtCore import QSize
        
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(QSize(size, size))


class IconButton(ModernButton):
    """Bouton moderne avec icône uniquement"""
    
    def __init__(self, icon_path="", style="ghost", size="md", parent=None):
        super().__init__("", style, size, parent)
        if icon_path:
            self.set_icon(icon_path, size=24 if size == 'md' else 20 if size == 'sm' else 28)
            
        # Ajuster le style pour les boutons icône
        if size == 'md':
            self.setFixedSize(48, 48)
        elif size == 'sm':
            self.setFixedSize(40, 40)
        else:
            self.setFixedSize(56, 56)


class FloatingActionButton(ModernButton):
    """Bouton d'action flottant moderne"""
    
    def __init__(self, icon_path="", parent=None):
        super().__init__("", "primary", "lg", parent)
        if icon_path:
            self.set_icon(icon_path, size=32)
            
        # Style flottant
        self.setFixedSize(64, 64)
        self.setStyleSheet(self.styleSheet() + """
            QPushButton {
                border-radius: 32px;
                box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
            }
            QPushButton:hover {
                box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4);
            }
        """)

