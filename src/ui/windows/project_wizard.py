from PySide6.QtWidgets import (
    QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QLabel, QTextEdit, QCheckBox,
    QGroupBox, QPushButton, QMessageBox, QProgressBar
)
from PySide6.QtCore import Signal, Qt, QTimer, QRegularExpression
from PySide6.QtGui import QFont, QValidator, QRegularExpressionValidator
from typing import Dict, Any, Optional
import re

from ..components.app_state import ProjectInfo
from ..resources.styles import COLORS


class ProjectCodeValidator(QValidator):
    """Validateur pour le format de code projet CHW-YYYY-XXX"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pattern = QRegularExpression(r"^CHW-\d{4}-\d{3}$")
        
    def validate(self, input_str: str, pos: int):
        match = self.pattern.match(input_str)
        if match.hasMatch() and match.capturedLength() == len(input_str):
            return QValidator.Acceptable, input_str, pos
        elif input_str == "" or input_str.startswith("CHW-"):
            return QValidator.Intermediate, input_str, pos
        else:
            return QValidator.Invalid, input_str, pos


class GeneralInfoPage(QWizardPage):
    """Page 1: Informations générales du projet"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Informations Générales")
        self.setSubTitle("Définissez les informations de base de votre projet")
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface de la page"""
        layout = QVBoxLayout(self)
        
        # Groupe informations projet
        project_group = QGroupBox("Informations du Projet")
        project_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        project_layout = QFormLayout(project_group)
        
        # Nom du projet
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ex: Étude Port de Marseille")
        self.name_edit.setMinimumWidth(300)
        project_layout.addRow("Nom du Projet *:", self.name_edit)
        
        # Code projet
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("CHW-2024-001")
        self.code_edit.setValidator(ProjectCodeValidator())
        project_layout.addRow("Code Projet *:", self.code_edit)
        
        # Groupe équipe
        team_group = QGroupBox("Équipe du Projet")
        team_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['secondary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        team_layout = QFormLayout(team_group)
        
        # Ingénieur
        self.engineer_edit = QLineEdit()
        self.engineer_edit.setPlaceholderText("Ex: Dr. Ahmed Hassan")
        team_layout.addRow("Ingénieur Principal *:", self.engineer_edit)
        
        # Chef de projet
        self.manager_edit = QLineEdit()
        self.manager_edit.setPlaceholderText("Ex: Prof. Marie Dubois")
        team_layout.addRow("Chef de Projet:", self.manager_edit)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Description détaillée du projet...")
        self.description_edit.setMaximumHeight(100)
        project_layout.addRow("Description:", self.description_edit)
        
        layout.addWidget(project_group)
        layout.addWidget(team_group)
        layout.addStretch()
        
        # Validation en temps réel
        self.name_edit.textChanged.connect(self.validate_page)
        self.code_edit.textChanged.connect(self.validate_page)
        self.engineer_edit.textChanged.connect(self.validate_page)
        
    def validate_page(self):
        """Validation en temps réel de la page"""
        is_valid = (
            self.name_edit.text().strip() != "" and
            self.code_edit.text().strip() != "" and
            self.engineer_edit.text().strip() != ""
        )
        
        # Mise à jour visuelle
        self.name_edit.setStyleSheet(
            f"border: 2px solid {'#E53E3E' if not self.name_edit.text().strip() else COLORS['success']};"
        )
        self.code_edit.setStyleSheet(
            f"border: 2px solid {'#E53E3E' if not self.code_edit.text().strip() else COLORS['success']};"
        )
        self.engineer_edit.setStyleSheet(
            f"border: 2px solid {'#E53E3E' if not self.engineer_edit.text().strip() else COLORS['success']};"
        )
        
        self.completeChanged.emit()
        
    def isComplete(self):
        """Vérification si la page est complète"""
        return (
            self.name_edit.text().strip() != "" and
            self.code_edit.text().strip() != "" and
            self.engineer_edit.text().strip() != ""
        )


class TechnicalConfigPage(QWizardPage):
    """Page 2: Configuration technique du projet"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Configuration Technique")
        self.setSubTitle("Définissez les paramètres techniques de votre projet")
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface de la page"""
        layout = QVBoxLayout(self)
        
        # Groupe échelle et type
        scale_group = QGroupBox("Échelle et Type de Projet")
        scale_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        scale_layout = QFormLayout(scale_group)
        
        # Échelle du projet
        self.scale_combo = QComboBox()
        self.scale_combo.addItems([
            "1:25", "1:50", "1:75", "1:100", "1:150", "1:200", "1:500"
        ])
        self.scale_combo.setCurrentText("1:100")
        scale_layout.addRow("Échelle du Projet:", self.scale_combo)
        
        # Type de bassin/canal
        self.basin_type_combo = QComboBox()
        self.basin_type_combo.addItems([
            "Bassin de Carène",
            "Canal à Houle",
            "Port",
            "Canal de Navigation",
            "Zone Côtière",
            "Autre"
        ])
        scale_layout.addRow("Type de Bassin/Canal:", self.basin_type_combo)
        
        # Groupe configuration capteurs
        sensors_group = QGroupBox("Configuration des Capteurs")
        sensors_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['secondary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        sensors_layout = QFormLayout(sensors_group)
        
        # Nombre de sondes
        self.probes_spin = QSpinBox()
        self.probes_spin.setRange(1, 50)
        self.probes_spin.setValue(8)
        self.probes_spin.setSuffix(" sondes")
        sensors_layout.addRow("Nombre de Sondes:", self.probes_spin)
        
        # Fréquence d'échantillonnage
        self.sampling_combo = QComboBox()
        self.sampling_combo.addItems([
            "16 Hz", "32 Hz", "64 Hz", "128 Hz", "256 Hz"
        ])
        self.sampling_combo.setCurrentText("32 Hz")
        sensors_layout.addRow("Fréquence d'Échantillonnage:", self.sampling_combo)
        
        # Groupe options avancées
        advanced_group = QGroupBox("Options Avancées")
        advanced_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['warning']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        advanced_layout = QVBoxLayout(advanced_group)
        
        # Options
        self.auto_calibration_check = QCheckBox("Calibration automatique des capteurs")
        self.auto_calibration_check.setChecked(True)
        advanced_layout.addWidget(self.auto_calibration_check)
        
        self.real_time_analysis_check = QCheckBox("Analyse en temps réel")
        self.real_time_analysis_check.setChecked(True)
        advanced_layout.addWidget(self.real_time_analysis_check)
        
        self.export_raw_data_check = QCheckBox("Export des données brutes")
        self.export_raw_data_check.setChecked(False)
        advanced_layout.addWidget(self.export_raw_data_check)
        
        layout.addWidget(scale_group)
        layout.addWidget(sensors_group)
        layout.addWidget(advanced_group)
        layout.addStretch()
        
    def isComplete(self):
        """Vérification si la page est complète"""
        return True  # Cette page n'a pas de validation stricte


class ValidationPage(QWizardPage):
    """Page 3: Validation et création du projet"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Validation et Création")
        self.setSubTitle("Vérifiez les informations et créez votre projet")
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface de la page"""
        layout = QVBoxLayout(self)
        
        # Récapitulatif
        self.summary_label = QLabel("Récapitulatif du projet:")
        self.summary_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.summary_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(self.summary_label)
        
        # Zone de récapitulatif
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(200)
        self.summary_text.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {COLORS['primary']};
                border-radius: 4px;
                background-color: {COLORS['surface']};
                padding: 8px;
            }}
        """)
        layout.addWidget(self.summary_text)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Message de statut
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Note importante
        note_label = QLabel("⚠ Note: Une fois créé, le projet sera automatiquement ouvert dans CHNeoWave.")
        note_label.setStyleSheet(f"""
            color: {COLORS['warning']};
            font-style: italic;
            padding: 10px;
            border: 1px solid {COLORS['warning']};
            border-radius: 4px;
            background-color: {COLORS['background']};
        """)
        layout.addWidget(note_label)
        
    def initializePage(self):
        """Initialisation de la page avec les données collectées"""
        wizard = self.wizard()
        
        # Collecter toutes les données
        general_page = wizard.page(0)
        tech_page = wizard.page(1)
        
        summary = f""" INFORMATIONS GÉNÉRALES
• Nom: {general_page.name_edit.text()}
• Code: {general_page.code_edit.text()}
• Ingénieur: {general_page.engineer_edit.text()}
• Chef de projet: {general_page.manager_edit.text()}

Calibration CONFIGURATION TECHNIQUE
• Échelle: {tech_page.scale_combo.currentText()}
• Type: {tech_page.basin_type_combo.currentText()}
• Sondes: {tech_page.probes_spin.value()}
• Fréquence: {tech_page.sampling_combo.currentText()}

Options OPTIONS AVANCÉES
• Calibration auto: {'Oui' if tech_page.auto_calibration_check.isChecked() else 'Non'}
• Analyse temps réel: {'Oui' if tech_page.real_time_analysis_check.isChecked() else 'Non'}
• Export données brutes: {'Oui' if tech_page.export_raw_data_check.isChecked() else 'Non'}"""
        
        self.summary_text.setPlainText(summary)
        
    def isComplete(self):
        """Vérification si la page est complète"""
        return True


class ProjectWizard(QWizard):
    """Wizard de création de projet - 3 étapes avec validation"""
    
    project_created = Signal(ProjectInfo)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CHNeoWave - Assistant Création de Projet")
        self.setModal(True)
        self.resize(700, 600)
        self.setup_wizard()
        
    def setup_wizard(self):
        """Configuration du wizard"""
        # Pages
        self.addPage(GeneralInfoPage())
        self.addPage(TechnicalConfigPage())
        self.addPage(ValidationPage())
        
        # Configuration des boutons
        self.setButtonText(QWizard.FinishButton, "Créer le Projet")
        self.setButtonText(QWizard.CancelButton, "Annuler")
        self.setButtonText(QWizard.BackButton, "Précédent")
        self.setButtonText(QWizard.NextButton, "Suivant")
        
        # Connexions
        self.finished.connect(self.on_wizard_finished)
        
        # Styles
        self.setStyleSheet(f"""
            QWizard {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QWizardPage {{
                background-color: {COLORS['background']};
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['text_secondary']};
            }}
        """)
        
    def on_wizard_finished(self, result):
        """Gestionnaire de fin du wizard"""
        if result == QWizard.Accepted:
            self.create_project()
            
    def create_project(self):
        """Création du projet à partir des données du wizard"""
        # Collecter les données
        general_page = self.page(0)
        tech_page = self.page(1)
        
        # Créer l'objet ProjectInfo
        project = ProjectInfo(
            name=general_page.name_edit.text().strip(),
            code=general_page.code_edit.text().strip(),
            engineer=general_page.engineer_edit.text().strip(),
            manager=general_page.manager_edit.text().strip(),
            scale=tech_page.scale_combo.currentText(),
            basin_type=tech_page.basin_type_combo.currentText()
        )
        
        # Simuler la création (avec barre de progression)
        validation_page = self.page(2)
        validation_page.progress_bar.setVisible(True)
        validation_page.status_label.setText("Création du projet en cours...")
        
        # Simulation de progression
        for i in range(101):
            validation_page.progress_bar.setValue(i)
            QTimer.singleShot(i * 20, lambda: None)  # Délai artificiel
            
        validation_page.status_label.setText("✓ Projet créé avec succès !")
        
        # Émettre le signal
        self.project_created.emit(project)
        
        # Message de confirmation
        QMessageBox.information(
            self,
            "Projet Créé",
            f"Le projet '{project.name}' a été créé avec succès !\n\n"
            f"Code: {project.code}\n"
            f"Échelle: {project.scale}\n"
            f"Type: {project.basin_type}"
        )
