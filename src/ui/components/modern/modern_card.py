"""
Cartes modernes pour interface scientifique CHNeoWave
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...resources.modern_design_system import ModernDesignSystem


class ModernCard(QFrame):
    """Carte moderne de base sans animations"""
    
    def __init__(self, title="", description="", parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        
        self._setup_modern_style()
        self._setup_layout()
        self._setup_content()
        
    def _setup_modern_style(self):
        """Style moderne sans effets d'opacité"""
        colors = ModernDesignSystem.get_color_palette()
        radius = ModernDesignSystem.get_border_radius()
        
        self.setStyleSheet(f"""
            ModernCard {{
                background: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: {radius['md']}px;
                padding: 8px;
            }}
            ModernCard:hover {{
                border-color: {colors['primary']};
                background: {colors['surface_hover']};
            }}
        """)
        
        # Hauteur minimale fixe pour éviter les conflits
        self.setMinimumHeight(36)
        
    def _setup_layout(self):
        """Layout simple sans animations"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)
        
    def _setup_content(self):
        """Contenu de base"""
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(ModernDesignSystem.get_font('h3'))
            title_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_primary']}; font-weight: 600;")
            self.main_layout.addWidget(title_label)
            
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setFont(ModernDesignSystem.get_font('body'))
            desc_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_secondary']};")
            desc_label.setWordWrap(True)
            self.main_layout.addWidget(desc_label)


class InfoCard(ModernCard):
    """Carte d'information simple"""
    
    def __init__(self, title="", value="", icon="", parent=None):
        super().__init__(title, "", parent)
        self.value = value
        self.icon = icon
        self._setup_info_content()
        
    def _setup_info_content(self):
        """Contenu d'information"""
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setFont(ModernDesignSystem.get_font('h2'))
            icon_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['accent']};")
            self.main_layout.addWidget(icon_label)
            
        if self.value:
            value_label = QLabel(str(self.value))
            value_label.setFont(ModernDesignSystem.get_font('h1'))
            value_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_primary']}; font-weight: 600;")
            self.main_layout.addWidget(value_label)


class StatusCard(ModernCard):
    """Carte de statut sans animations"""
    
    def __init__(self, title="", value="", status="info", description="", parent=None):
        super().__init__(title, description, parent)
        self.value = value
        self.status = status
        self._setup_status_content()
        
    def _setup_status_content(self):
        """Contenu de statut"""
        colors = ModernDesignSystem.get_color_palette()
        
        # Valeur du statut
        if self.value:
            value_label = QLabel(str(self.value))
            value_label.setFont(ModernDesignSystem.get_font('body'))
            
            # Couleur selon le statut
            status_colors = {
                'success': colors['success'],
                'warning': colors['warning'],
                'error': colors['error'],
                'info': colors['primary']
            }
            status_color = status_colors.get(self.status, colors['primary'])
            
            value_label.setStyleSheet(f"color: {status_color}; font-weight: 600;")
            self.main_layout.addWidget(value_label)


class ActionCard(ModernCard):
    """Carte d'action sans animations"""
    
    def __init__(self, title="", description="", action_text="", icon="", parent=None):
        super().__init__(title, description, parent)
        self.action_text = action_text
        self.icon = icon
        self._setup_action_content()
        
    def _setup_action_content(self):
        """Contenu d'action"""
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setFont(ModernDesignSystem.get_font('h2'))
            icon_label.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['accent']};")
            self.main_layout.addWidget(icon_label)
            
        if self.action_text:
            action_btn = QPushButton(self.action_text)
            action_btn.setFont(ModernDesignSystem.get_font('body'))
            action_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {ModernDesignSystem.get_color_palette()['primary']};
                    border: none;
                    border-radius: 4px;
                    color: white;
                    padding: 4px 8px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: {ModernDesignSystem.get_color_palette()['primary_dark']};
                }}
            """)
            self.main_layout.addWidget(action_btn)

