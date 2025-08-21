"""
Sidebar moderne avec blur et gradients - Design 2025
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ...resources.modern_design_system import ModernDesignSystem
from .modern_button import ModernButton, IconButton


class ModernNavigationSidebar(QWidget):
	"""Sidebar moderne avec navigation avancée et design 2025"""
	
	# Signaux
	module_changed = Signal(str)  # Module sélectionné
	return_to_projects = Signal()  # Retour aux projets
	
	def __init__(self, current_project=None, parent=None):
		super().__init__(parent)
		self.current_project = current_project
		self.current_module = "dashboard"
		
		self._setup_modern_style()
		self._setup_layout()
		self._setup_navigation()
		self._setup_project_info()
		self._setup_system_status()
		# Animations supprimées pour interface scientifique compacte
		
	def _setup_modern_style(self):
		"""Style moderne avec glassmorphism et blur"""
		colors = ModernDesignSystem.get_color_palette()
		radius = ModernDesignSystem.get_border_radius()
		
		# Style principal avec effet glassmorphism
		self.setStyleSheet(f"""
			ModernNavigationSidebar {{
				background: {colors['bg_secondary']};
				border-right: 1px solid {colors['border']};
				min-width: 280px;
				max-width: 280px;
			}}
		""")
		
		# Palette moderne
		self.setPalette(ModernDesignSystem.create_modern_palette())
		
	def _setup_layout(self):
		"""Layout moderne avec espacement généreux"""
		spacing = ModernDesignSystem.get_spacing_system()
		
		# Layout principal
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
		self.main_layout.setSpacing(spacing['sm'])
		
		# Scroll area pour le contenu
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
		self.scroll_area.setStyleSheet("""
			QScrollArea {
				border: none;
				background: transparent;
			}
			QScrollBar:vertical {
				background: transparent;
				width: 8px;
				border-radius: 4px;
			}
			QScrollBar::handle:vertical {
				background: rgba(255, 255, 255, 0.2);
				border-radius: 4px;
				min-height: 20px;
			}
			QScrollBar::handle:vertical:hover {
				background: rgba(255, 255, 255, 0.3);
			}
		""")
		
		# Widget de contenu scrollable
		self.content_widget = QWidget()
		self.content_layout = QVBoxLayout(self.content_widget)
		self.content_layout.setContentsMargins(0, 0, 0, 0)
		self.content_layout.setSpacing(spacing['sm'])
		
		self.scroll_area.setWidget(self.content_widget)
		self.main_layout.addWidget(self.scroll_area)
		
	def _setup_navigation(self):
		"""Navigation moderne avec modules"""
		spacing = ModernDesignSystem.get_spacing_system()
		
		# Titre de la navigation
		nav_title = QLabel("Navigation")
		nav_title.setFont(ModernDesignSystem.get_font('h3'))
		nav_title.setStyleSheet(f"color: {ModernDesignSystem.get_color_palette()['text_primary']}; font-weight: 600; margin-bottom: {spacing['sm']}px;")
		self.content_layout.addWidget(nav_title)
		
		# Modules de navigation
		self.modules = [
			("dashboard", "□ Dashboard", "Vue d'ensemble du projet", "success"),
			("calibration", "◐ Calibration", "Calibration des sondes", "warning"),
			("acquisition", "▤ Acquisition", "Acquisition temps réel", "primary"),
			("stats", "△ Statistique", "Analyse des données", "secondary"),
			("advanced", "◈ Avancée", "Analyse Goda/FFT", "warning"),
			("export", "↗ Export", "Export des résultats", "success")
		]
		
		self.module_buttons = {}
		
		for module_id, module_name, module_desc, color in self.modules:
			# Créer le bouton de module
			module_btn = self._create_module_button(module_id, module_name, module_desc, color)
			self.module_buttons[module_id] = module_btn
			self.content_layout.addWidget(module_btn)
			
		# Sélection par défaut
		if "dashboard" in self.module_buttons:
			self._select_module("dashboard")
			
	def _create_module_button(self, module_id, name, description, color):
		"""Crée un bouton de module moderne"""
		colors = ModernDesignSystem.get_color_palette()
		spacing = ModernDesignSystem.get_spacing_system()
		
		# Widget conteneur
		module_widget = QFrame()
		module_widget.setObjectName("module_button")
		module_widget.setStyleSheet(f"""
			QFrame#module_button {{
				background: transparent;
				border: 2px solid transparent;
				border-radius: {ModernDesignSystem.get_border_radius()['md']}px;
				padding: {spacing['xs']}px;
				margin: 1px 0px;
			}}
			QFrame#module_button:hover {{
				background: {colors['surface_hover']};
				border-color: {colors[color]};
			}}
			QFrame#module_button[selected="true"] {{
				background: {colors['surface']};
				border-color: {colors[color]};
			}}
		""")
		module_widget.setFixedHeight(28)
		
		# Layout du module
		module_layout = QVBoxLayout(module_widget)
		module_layout.setContentsMargins(0, 0, 0, 0)
		module_layout.setSpacing(0)
		
		# Nom du module
		name_label = QLabel(name)
		name_label.setFont(ModernDesignSystem.get_font('caption'))
		name_label.setStyleSheet(f"color: {colors['text_primary']}; font-weight: 600;")
		module_layout.addWidget(name_label)
		
		# Description condensée (ou supprimer si trop haut)
		desc_label = QLabel(description)
		desc_label.setFont(ModernDesignSystem.get_font('caption'))
		desc_label.setStyleSheet(f"color: {colors['text_secondary']};")
		desc_label.setWordWrap(False)
		module_layout.addWidget(desc_label)
		
		# Rendre cliquable
		module_widget.mousePressEvent = lambda event, mid=module_id: self._on_module_clicked(mid)
		module_widget.setCursor(Qt.CursorShape.PointingHandCursor)
		
		return module_widget
		
	def _setup_project_info(self):
		"""Informations du projet actuel (condensées)"""
		colors = ModernDesignSystem.get_color_palette()
		
		project_info = QFrame()
		project_info.setStyleSheet(f"""
			QFrame {{
				background: {colors['surface']};
				border: 1px solid {colors['border']};
				border-radius: 8px;
				padding: 6px;
			}}
		""")
		
		project_layout = QVBoxLayout(project_info)
		project_layout.setContentsMargins(0, 0, 0, 0)
		project_layout.setSpacing(2)
		
		name_label = QLabel(self.current_project.name if self.current_project else "Projet: —")
		name_label.setStyleSheet("font-size: 11px;")
		project_layout.addWidget(name_label)
		
		code_label = QLabel(f"Code: {self.current_project.code}" if self.current_project else "Code: —")
		code_label.setStyleSheet("font-size: 10px; color: #94A3B8;")
		project_layout.addWidget(code_label)
		
		self.content_layout.addWidget(project_info)
		
	def _setup_system_status(self):
		"""Statut système compact"""
		colors = ModernDesignSystem.get_color_palette()
		
		status_widget = QFrame()
		status_widget.setStyleSheet(f"""
			QFrame {{
				background: {colors['surface']};
				border: 1px solid {colors['border']};
				border-radius: 8px;
				padding: 6px;
			}}
		""")
		layout = QVBoxLayout(status_widget)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(2)
		for name, desc in [("Capteurs", "●"), ("Acquisition", "●"), ("Calibration", "●"), ("Analyse", "●")]:
			row = QHBoxLayout()
			row.setContentsMargins(0, 0, 0, 0)
			row.setSpacing(4)
			row.addWidget(QLabel(name))
			v = QLabel(desc)
			v.setStyleSheet("font-size: 10px; color: #94A3B8;")
			row.addStretch()
			row.addWidget(v)
			layout.addLayout(row)
		self.content_layout.addWidget(status_widget)
		
	def _on_module_clicked(self, module_id):
		"""Gestionnaire de clic sur un module"""
		self._update_module_selection(module_id)
		self.module_changed.emit(module_id)
		self.current_module = module_id
		
	def _select_module(self, module_id):
		"""Sélectionne un module programmatiquement"""
		if module_id in self.module_buttons:
			self._update_module_selection(module_id)
			self.current_module = module_id
		
	def _update_module_selection(self, selected_module):
		"""Met à jour la sélection visuelle des modules"""
		colors = ModernDesignSystem.get_color_palette()
		for module_id, module_widget in self.module_buttons.items():
			if module_id == selected_module:
				module_widget.setProperty("selected", True)
				current_style = module_widget.styleSheet()
				if "border-color: transparent;" in current_style:
					module_widget.setStyleSheet(current_style.replace("border-color: transparent;", f"border-color: {colors['primary']};"))
			else:
				module_widget.setProperty("selected", False)
				current_style = module_widget.styleSheet()
				if f"border-color: {colors['primary']};" in current_style:
					module_widget.setStyleSheet(current_style.replace(f"border-color: {colors['primary']};", "border-color: transparent;"))
		self.update()
		
	def set_project(self, project):
		self.current_project = project
		self._update_project_info()
		
	def update_system_status(self, status_updates):
		pass
		
	def resizeEvent(self, event):
		super().resizeEvent(event)
		if self.width() != 200:
			self.setFixedWidth(200)

