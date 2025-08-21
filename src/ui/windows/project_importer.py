from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFileDialog, QTextEdit, QGroupBox, QFormLayout, QLineEdit,
    QMessageBox, QProgressBar, QCheckBox, QScrollArea, QWidget
)
from PySide6.QtCore import Signal, Qt, QThread
from PySide6.QtGui import QFont, QPixmap, QIcon
from typing import Dict, Any, Optional, List
import os
import h5py
import json
from datetime import datetime

from ..components.app_state import ProjectInfo
from ..resources.styles import COLORS


class ProjectFileValidator(QThread):
    """Thread pour validation des fichiers projet en arrière-plan"""
    
    validation_complete = Signal(dict, bool)  # (metadata, is_valid)
    validation_error = Signal(str)
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        """Validation du fichier projet"""
        try:
            metadata = self.extract_metadata()
            is_valid = self.validate_metadata(metadata)
            self.validation_complete.emit(metadata, is_valid)
        except Exception as e:
            self.validation_error.emit(str(e))
            
    def extract_metadata(self) -> Dict[str, Any]:
        """Extraction des métadonnées du fichier HDF5"""
        metadata = {}
        
        try:
            with h5py.File(self.file_path, 'r') as f:
                # Vérifier la structure du fichier
                if 'metadata' in f:
                    metadata_group = f['metadata']
                    
                    # Informations de base
                    if 'project_info' in metadata_group:
                        project_info = metadata_group['project_info']
                        metadata['name'] = project_info.attrs.get('name', 'Projet Inconnu')
                        metadata['code'] = project_info.attrs.get('code', 'CHW-UNK-000')
                        metadata['engineer'] = project_info.attrs.get('engineer', 'Non spécifié')
                        metadata['manager'] = project_info.attrs.get('manager', 'Non spécifié')
                        metadata['scale'] = project_info.attrs.get('scale', 'Non spécifié')
                        metadata['basin_type'] = project_info.attrs.get('basin_type', 'Non spécifié')
                        metadata['created_date'] = project_info.attrs.get('created_date', 'Date inconnue')
                        
                    # Informations techniques
                    if 'technical_config' in metadata_group:
                        tech_config = metadata_group['technical_config']
                        metadata['sampling_frequency'] = tech_config.attrs.get('sampling_frequency', 'Non spécifié')
                        metadata['probe_count'] = tech_config.attrs.get('probe_count', 'Non spécifié')
                        metadata['duration'] = tech_config.attrs.get('duration', 'Non spécifié')
                        
                    # Informations de données
                    if 'data_info' in metadata_group:
                        data_info = metadata_group['data_info']
                        metadata['data_points'] = data_info.attrs.get('data_points', 'Non spécifié')
                        metadata['channels'] = data_info.attrs.get('channels', 'Non spécifié')
                        
                # Informations fichier
                file_stat = os.stat(self.file_path)
                metadata['file_size'] = f"{file_stat.st_size / (1024*1024):.2f} MB"
                metadata['file_modified'] = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier: {str(e)}")
            
        return metadata
        
    def validate_metadata(self, metadata: Dict[str, Any]) -> bool:
        """Validation des métadonnées extraites"""
        required_fields = ['name', 'code', 'engineer']
        
        for field in required_fields:
            if field not in metadata or not metadata[field] or metadata[field] == 'Non spécifié':
                return False
                
        # Validation du format de code
        if 'code' in metadata:
            code = metadata['code']
            if not code.startswith('CHW-') or len(code.split('-')) != 3:
                return False
                
        return True


class ProjectImporter(QDialog):
    """Fenêtre d'import de projets existants"""
    
    project_imported = Signal(ProjectInfo, str)  # (project, file_path)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file_path = ""
        self.validator_thread = None
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface"""
        self.setWindowTitle("CHNeoWave - Importer Projet Existant")
        self.setModal(True)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # En-tête
        self.setup_header(layout)
        
        # Sélection de fichier
        self.setup_file_selection(layout)
        
        # Aperçu des métadonnées
        self.setup_metadata_preview(layout)
        
        # Options d'import
        self.setup_import_options(layout)
        
        # Boutons d'action
        self.setup_action_buttons(layout)
        
    def setup_header(self, layout):
        """Configuration de l'en-tête"""
        header_label = QLabel("Importer un Projet Existant")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header_label.setStyleSheet(f"color: {COLORS['primary']}; margin-bottom: 10px;")
        layout.addWidget(header_label)
        
        subtitle_label = QLabel("Sélectionnez un fichier projet HDF5 (.h5, .hdf5) pour l'importer dans CHNeoWave")
        subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']}; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
    def setup_file_selection(self, layout):
        """Configuration de la sélection de fichier"""
        file_group = QGroupBox("Sélection du Fichier Projet")
        file_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        file_layout = QVBoxLayout(file_group)
        
        # Bouton de sélection
        select_btn_layout = QHBoxLayout()
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Chemin vers le fichier projet (.h5, .hdf5)")
        self.file_path_edit.setReadOnly(True)
        select_btn_layout.addWidget(self.file_path_edit)
        
        self.select_file_btn = QPushButton("Parcourir...")
        self.select_file_btn.clicked.connect(self.on_select_file_clicked)
        self.select_file_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2C5AA0;
            }}
        """)
        select_btn_layout.addWidget(self.select_file_btn)
        
        file_layout.addLayout(select_btn_layout)
        
        # Filtres de fichiers
        filters_label = QLabel("Formats supportés: .h5, .hdf5")
        filters_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-style: italic;")
        file_layout.addWidget(filters_label)
        
        layout.addWidget(file_group)
        
    def setup_metadata_preview(self, layout):
        """Configuration de l'aperçu des métadonnées"""
        preview_group = QGroupBox("Aperçu des Métadonnées")
        preview_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['secondary']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        preview_layout = QVBoxLayout(preview_group)
        
        # Zone de texte pour l'aperçu
        self.metadata_text = QTextEdit()
        self.metadata_text.setReadOnly(True)
        self.metadata_text.setPlaceholderText("Sélectionnez un fichier pour voir les métadonnées...")
        self.metadata_text.setMaximumHeight(200)
        self.metadata_text.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {COLORS['primary']};
                border-radius: 4px;
                background-color: {COLORS['surface']};
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
            }}
        """)
        preview_layout.addWidget(self.metadata_text)
        
        # Barre de progression pour validation
        self.validation_progress = QProgressBar()
        self.validation_progress.setVisible(False)
        preview_layout.addWidget(self.validation_progress)
        
        # Statut de validation
        self.validation_status = QLabel("")
        self.validation_status.setAlignment(Qt.AlignCenter)
        self.validation_status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        preview_layout.addWidget(self.validation_status)
        
        layout.addWidget(preview_group)
        
    def setup_import_options(self, layout):
        """Configuration des options d'import"""
        options_group = QGroupBox("Options d'Import")
        options_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['warning']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
            }}
        """)
        options_layout = QVBoxLayout(options_group)
        
        # Options
        self.backup_original_check = QCheckBox("Créer une sauvegarde du fichier original")
        self.backup_original_check.setChecked(True)
        options_layout.addWidget(self.backup_original_check)
        
        self.import_calibration_check = QCheckBox("Importer les données de calibration")
        self.import_calibration_check.setChecked(True)
        options_layout.addWidget(self.import_calibration_check)
        
        self.import_analysis_check = QCheckBox("Importer les analyses existantes")
        self.import_analysis_check.setChecked(True)
        options_layout.addWidget(self.import_analysis_check)
        
        layout.addWidget(options_group)
        
    def setup_action_buttons(self, layout):
        """Configuration des boutons d'action"""
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        # Bouton Annuler
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['error']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #C53030;
            }}
        """)
        buttons_layout.addWidget(self.cancel_btn)
        
        # Bouton Importer
        self.import_btn = QPushButton("Importer le Projet")
        self.import_btn.clicked.connect(self.on_import_clicked)
        self.import_btn.setEnabled(False)
        self.import_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2F855A;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['text_secondary']};
            }}
        """)
        buttons_layout.addWidget(self.import_btn)
        
        layout.addLayout(buttons_layout)
        
    def on_select_file_clicked(self):
        """Gestionnaire clic bouton sélection fichier"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un Fichier Projet",
            "",
            "Fichiers HDF5 (*.h5 *.hdf5);;Tous les fichiers (*)"
        )
        
        if file_path:
            self.selected_file_path = file_path
            self.file_path_edit.setText(file_path)
            self.validate_selected_file()
            
    def validate_selected_file(self):
        """Validation du fichier sélectionné"""
        if not self.selected_file_path:
            return
            
        # Démarrer la validation en arrière-plan
        self.validation_progress.setVisible(True)
        self.validation_status.setText("Validation du fichier en cours...")
        self.import_btn.setEnabled(False)
        
        # Créer et démarrer le thread de validation
        self.validator_thread = ProjectFileValidator(self.selected_file_path)
        self.validator_thread.validation_complete.connect(self.on_validation_complete)
        self.validator_thread.validation_error.connect(self.on_validation_error)
        self.validator_thread.start()
        
    def on_validation_complete(self, metadata: Dict[str, Any], is_valid: bool):
        """Gestionnaire de fin de validation"""
        self.validation_progress.setVisible(False)
        
        if is_valid:
            self.validation_status.setText("✓ Fichier valide - Prêt à l'import")
            self.import_btn.setEnabled(True)
            self.display_metadata(metadata)
        else:
            self.validation_status.setText("Fichier invalide - Métadonnées incomplètes")
            self.import_btn.setEnabled(False)
            self.metadata_text.setPlainText("Ce fichier ne contient pas les métadonnées requises pour un projet CHNeoWave valide.")
            
    def on_validation_error(self, error_message: str):
        """Gestionnaire d'erreur de validation"""
        self.validation_progress.setVisible(False)
        self.validation_status.setText(f"Erreur: {error_message}")
        self.import_btn.setEnabled(False)
        self.metadata_text.setPlainText(f"Erreur lors de la validation:\n{error_message}")
        
    def display_metadata(self, metadata: Dict[str, Any]):
        """Affichage des métadonnées extraites"""
        metadata_text = "MÉTADONNÉES DU PROJET\n\n"
        
        # Informations de base
        metadata_text += "INFORMATIONS GÉNÉRALES\n"
        metadata_text += f"• Nom: {metadata.get('name', 'Non spécifié')}\n"
        metadata_text += f"• Code: {metadata.get('code', 'Non spécifié')}\n"
        metadata_text += f"• Ingénieur: {metadata.get('engineer', 'Non spécifié')}\n"
        metadata_text += f"• Chef de projet: {metadata.get('manager', 'Non spécifié')}\n"
        metadata_text += f"• Échelle: {metadata.get('scale', 'Non spécifié')}\n"
        metadata_text += f"• Type: {metadata.get('basin_type', 'Non spécifié')}\n"
        metadata_text += f"• Date création: {metadata.get('created_date', 'Non spécifié')}\n\n"
        
        # Informations techniques
        metadata_text += "CONFIGURATION TECHNIQUE\n"
        metadata_text += f"• Fréquence: {metadata.get('sampling_frequency', 'Non spécifié')}\n"
        metadata_text += f"• Nombre sondes: {metadata.get('probe_count', 'Non spécifié')}\n"
        metadata_text += f"• Durée: {metadata.get('duration', 'Non spécifié')}\n\n"
        
        # Informations données
        metadata_text += "DONNÉES\n"
        metadata_text += f"• Points de données: {metadata.get('data_points', 'Non spécifié')}\n"
        metadata_text += f"• Canaux: {metadata.get('channels', 'Non spécifié')}\n\n"
        
        # Informations fichier
        metadata_text += "INFORMATIONS FICHIER\n"
        metadata_text += f"• Taille: {metadata.get('file_size', 'Non spécifié')}\n"
        metadata_text += f"• Modifié: {metadata.get('file_modified', 'Non spécifié')}\n"
        
        self.metadata_text.setPlainText(metadata_text)
        
    def on_import_clicked(self):
        """Gestionnaire clic bouton importer"""
        if not self.selected_file_path:
            return
            
        try:
            # Créer l'objet ProjectInfo à partir des métadonnées
            # (Pour l'instant, utiliser des valeurs par défaut)
            project = ProjectInfo(
                name="Projet Importé",
                code="CHW-IMP-001",
                engineer="Importé",
                manager="Importé",
                scale="1:100",
                basin_type="Importé"
            )
            
            # Émettre le signal
            self.project_imported.emit(project, self.selected_file_path)
            
            # Message de confirmation
            QMessageBox.information(
                self,
                "Import Réussi",
                f"Le projet a été importé avec succès !\n\n"
                f"Fichier: {os.path.basename(self.selected_file_path)}\n"
                f"Le projet sera maintenant ouvert dans CHNeoWave."
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur d'Import",
                f"Une erreur est survenue lors de l'import:\n{str(e)}"
            )
            
    def apply_styles(self):
        """Application des styles personnalisés"""
        self.setStyleSheet(f"""
            ProjectImporter {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
        
    def closeEvent(self, event):
        """Gestion de la fermeture de la fenêtre"""
        if self.validator_thread and self.validator_thread.isRunning():
            self.validator_thread.quit()
            if not self.validator_thread.wait(1000):
                self.validator_thread.terminate()
        super().closeEvent(event)
