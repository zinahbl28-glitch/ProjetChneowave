# CHNeoWave UI Architecture

## Vue d'ensemble

L'architecture UI de CHNeoWave suit le pattern Model-View-Controller (MVC) strict, avec une séparation claire entre l'interface utilisateur et la logique métier. L'interface est construite avec PySide6 et respecte les standards maritimes OpenBridge.

## Structure des Packages

```
src/ui/
├── components/          # Composants de base réutilisables
│   ├── base_controller.py      # Contrôleur MVC abstrait
│   ├── app_state.py           # État global de l'application
│   ├── signal_adapter.py      # Adaptateur UI ↔ Core SignalBus
│   ├── ui_config_manager.py   # Configuration et styles
│   ├── navigation_sidebar.py  # Sidebar de navigation
│   └── recent_projects_manager.py # Gestion projets récents
├── windows/            # Fenêtres principales
│   ├── splash_screen.py       # Écran de démarrage
│   ├── project_manager.py     # Gestionnaire de projets
│   ├── project_wizard.py      # Assistant création projet
│   ├── project_importer.py    # Import de projets
│   └── main_dashboard.py      # Dashboard principal
├── panels/             # Panels modulaires
│   ├── base_module_panel.py   # Panel de base pour modules
│   ├── project_dashboard_panel.py # Panel dashboard projet
│   ├── calibration_panel.py   # Panel calibration
│   ├── acquisition_panel.py   # Panel acquisition
│   ├── stats_panel.py         # Panel analyse statistique
│   ├── advanced_panel.py      # Panel analyses avancées
│   └── export_panel.py        # Panel export
├── controllers/        # Contrôleurs MVC
│   ├── project_manager_controller.py # Contrôleur gestion projets
│   └── dashboard_controller.py       # Contrôleur dashboard
├── resources/          # Assets et styles
│   ├── styles.py              # Constantes couleurs/styles
│   └── styles.qss             # Feuilles de style Qt
└── bootstrap.py        # Point d'entrée principal
```

## Composants Principaux

### 1. BaseController

Classe de base pour tous les contrôleurs UI, fournissant les signaux de base et la structure MVC.

```python
class BaseController(QObject):
    data_changed = Signal(dict)
    error_occurred = Signal(str)
    
    def initialize(self):
        pass
```

### 2. AppState

Gestionnaire de l'état global de l'application, incluant les informations du projet actuel et les données partagées.

```python
@dataclass
class ProjectInfo:
    name: str = ""
    code: str = ""
    engineer: str = ""
    manager: str = ""
    scale: str = ""
    basin_type: str = ""

class AppState(QObject):
    project_changed = Signal(ProjectInfo)
```

### 3. UISignalAdapter

Pont de communication entre l'interface utilisateur et le core SignalBus existant, permettant l'échange de données sans modification du core.

```python
class UISignalAdapter(QObject):
    calibration_data_received = Signal(dict)
    acquisition_data_received = Signal(dict)
    analysis_completed = Signal(dict)
    core_error_occurred = Signal(str)
    session_state_changed = Signal(object)
```

### 4. UIConfigManager

Gestionnaire de configuration UI, incluant le chargement et l'application des styles QSS et la persistance des préférences utilisateur.

```python
class UIConfigManager:
    def load_styles(self) -> str
    def apply_styles(self, app: QApplication)
    def save_window_geometry(self, window_name: str, geometry)
```

## Fenêtres Principales

### 1. SplashScreen (Phase 2)

Écran de démarrage animé avec barre de progression et chargement des modules en arrière-plan.

**Fonctionnalités :**
- Animation de démarrage 2.5 secondes
- 5 étapes de chargement progressif
- Threading pour chargement non-bloquant
- Transition fluide vers fenêtre principale

**Architecture :**
```python
class SplashScreen(QSplashScreen):
    def __init__(self):
        self.setup_ui()
        self.setup_loading()
    
class LoadingWorker(QThread):
    step_completed = pyqtSignal(str, float)
    loading_finished = pyqtSignal()
```

### 2. ProjectManager (Phase 3)

Fenêtre d'accueil principale permettant la création, l'import et la sélection de projets.

**Fonctionnalités :**
- Création de nouveaux projets
- Import de projets existants
- Liste des projets récents
- Navigation vers ProjectWizard et ProjectImporter

**Architecture :**
```python
class ProjectManager(QDialog):
    project_selected = Signal(ProjectInfo)
    new_project_requested = Signal()
    import_project_requested = Signal()
```

### 3. ProjectWizard (Phase 3)

Assistant en 3 étapes pour la création de nouveaux projets avec validation en temps réel.

**Pages :**
1. **Informations Générales** : Nom, code, ingénieur, chef de projet
2. **Configuration Technique** : Échelle, type de bassin, configuration capteurs
3. **Validation et Création** : Récapitulatif et création finale

**Architecture :**
```python
class ProjectWizard(QWizard):
    def __init__(self):
        self.addPage(GeneralInfoPage())
        self.addPage(TechnicalConfigPage())
        self.addPage(ValidationPage())
```

### 4. ProjectImporter (Phase 3)

Interface d'import de projets existants avec validation et aperçu des métadonnées.

**Fonctionnalités :**
- Sélecteur de fichiers HDF5
- Validation en arrière-plan
- Aperçu des métadonnées
- Gestion des erreurs de format

**Architecture :**
```python
class ProjectImporter(QDialog):
    project_imported = Signal(ProjectInfo, str)

class ProjectFileValidator(QThread):
    validation_complete = Signal(dict, bool)
    validation_error = Signal(str)
```

### 5. MainDashboard (Phase 4)

Interface principale après sélection de projet, avec navigation entre 5 modules et sidebar informative.

**Fonctionnalités :**
- Navigation latérale avec 5 modules
- Sidebar avec informations projet et état système
- Panels modulaires pour chaque module
- Transition fluide entre modules

**Architecture :**
```python
class MainDashboard(QMainWindow):
    module_changed = Signal(str)
    project_updated = Signal(ProjectInfo)
    
    def __init__(self, project: ProjectInfo, file_path: str = ""):
        self.setup_ui()
        self.setup_sidebar()
        self.setup_main_content()
        self.setup_menu()
        self.setup_status_bar()
```

## Panels Modulaires

### 1. BaseModulePanel

Classe de base pour tous les panels de modules, fournissant une structure commune et des fonctionnalités de base.

**Fonctionnalités :**
- En-tête de module standardisé
- Zone de contenu avec message "Coming Soon"
- Barre de progression de développement
- Boutons d'action de démonstration

**Architecture :**
```python
class BaseModulePanel(QWidget):
    def __init__(self, module_name: str, module_title: str, module_description: str):
        self.setup_ui()
        self.setup_module_header()
        self.setup_content_area()
        self.setup_status_area()
```

### 2. ProjectDashboardPanel

Panel par défaut affiché dans le dashboard principal, fournissant une vue d'ensemble du projet et des métriques système.

**Fonctionnalités :**
- Informations détaillées du projet
- Métriques système en temps réel
- Activité récente
- Accès rapide aux autres modules

### 3. Panels Spécialisés

Chaque module a son panel spécialisé héritant de BaseModulePanel :

- **CalibrationPanel** : Calibration des sondes et capteurs
- **AcquisitionPanel** : Acquisition temps réel des données
- **StatsPanel** : Analyse statistique des données
- **AdvancedPanel** : Analyses avancées (Goda, FFT)
- **ExportPanel** : Export des résultats et données

## Contrôleurs

### 1. ProjectManagerController

Contrôleur central pour la gestion des projets, orchestrant l'interaction entre ProjectManager, ProjectWizard et ProjectImporter.

**Responsabilités :**
- Gestion du cycle de vie des fenêtres
- Traitement des requêtes utilisateur
- Communication avec RecentProjectsManager
- Gestion des erreurs et validation

**Architecture :**
```python
class ProjectManagerController(QObject):
    project_loaded = Signal(ProjectInfo, str)
    project_created = Signal(ProjectInfo)
    project_imported = Signal(ProjectInfo, str)
    project_manager_closed = Signal()
```

### 2. DashboardController

Contrôleur central pour le dashboard principal, gérant la navigation entre modules et l'état du système.

**Responsabilités :**
- Gestion du cycle de vie du dashboard
- Changement de modules
- Mise à jour des informations projet
- Simulation et monitoring du système

**Architecture :**
```python
class DashboardController(BaseController):
    dashboard_closed = Signal()
    module_switched = Signal(str)
    project_updated = Signal(ProjectInfo)
```

## Navigation et Sidebar

### NavigationSidebar

Sidebar de navigation latérale du dashboard principal, fournissant :

**Fonctionnalités :**
- En-tête avec informations projet
- Navigation entre 5 modules
- Indicateurs d'état système
- Bouton de retour au gestionnaire de projets

**Architecture :**
```python
class NavigationSidebar(QWidget):
    module_changed = Signal(str)
    return_to_project_manager = Signal()
    
    def setup_module_navigation(self):
        self.modules = [
            ("dashboard", "📋 Dashboard", "Vue d'ensemble du projet"),
            ("calibration", "⚙️ Calibration", "Calibration des sondes"),
            ("acquisition", "📊 Acquisition", "Acquisition temps réel"),
            ("stats", "📈 Statistique", "Analyse statistique"),
            ("advanced", "🔬 Avancée", "Analyses avancées"),
            ("export", "📤 Export", "Export des résultats")
        ]
```

## Gestion des Projets Récents

### RecentProjectsManager

Gestionnaire des projets récemment accessibles, utilisant QSettings pour la persistance.

**Fonctionnalités :**
- Sauvegarde automatique des projets récents
- Limite configurable (défaut : 10 projets)
- Suivi des compteurs d'accès
- Export/import de la liste des projets récents

**Architecture :**
```python
class RecentProjectsManager(QObject):
    def add_recent_project(self, project: ProjectInfo, file_path: str = "")
    def load_recent_projects(self) -> List[Dict[str, Any]]
    def save_recent_projects(self, projects: List[Dict[str, Any]])
    def get_recent_projects(self) -> List[Dict[str, Any]]
```

## Flux de Données

### 1. Core → UI

```
SignalBus → UISignalAdapter → Signaux UI → Contrôleurs → Vues
```

### 2. UI → Core

```
Actions UI → Contrôleurs → UISignalAdapter → SignalBus → Core
```

### 3. Communication Inter-UI

```
Fenêtres ↔ Contrôleurs ↔ Composants via signaux/slots Qt
```

## Styles et Thème

### Palette de Couleurs Maritime

```python
COLORS = {
    'primary': '#2C5282',      # Bleu maritime principal
    'secondary': '#2B6CB0',    # Bleu secondaire
    'success': '#38A169',      # Vert validation
    'warning': '#ED8936',      # Orange attention
    'error': '#E53E3E',        # Rouge critique
    'background': '#F7FAFC',   # Fond principal
    'surface': '#FFFFFF',      # Surface cartes
    'text_primary': '#2D3748', # Texte principal
    'text_secondary': '#718096' # Texte secondaire
}
```

### Styles QSS

Les styles sont appliqués via Qt Style Sheets (QSS) pour maintenir la cohérence visuelle et respecter les standards maritimes OpenBridge.

## Tests

### Structure des Tests

```
tests/ui/
├── test_controllers.py         # Tests des contrôleurs
├── test_app_state.py          # Tests de l'état global
├── test_signal_integration.py # Tests d'intégration signal
├── test_robustness.py         # Tests de robustesse
├── test_splash_screen.py      # Tests du splash screen
├── test_project_manager.py    # Tests du gestionnaire de projets
└── test_dashboard.py          # Tests du dashboard
```

### Types de Tests

- **Tests Unitaires** : Composants individuels
- **Tests d'Intégration** : Communication entre composants
- **Tests de Robustesse** : Gestion d'erreurs et edge cases
- **Tests de Performance** : Temps de réponse et réactivité
- **Tests d'Accessibilité** : Navigation clavier et lecteurs d'écran

## Performance et Métriques

### Objectifs de Performance

- **Démarrage UI** : < 300ms
- **Changement de module** : < 100ms
- **Temps de réponse UI** : < 200ms
- **Rendu graphiques temps réel** : < 100ms

### Métriques de Qualité

- **Coverage des tests** : >80%
- **Lint score** : 0 erreur/warning
- **Architecture** : MVC strict respecté
- **Intégration** : 0 modification du core

## Évolutions Futures

### Phase 5 : Module Calibration
- Interface de calibration des sondes
- Validation en temps réel
- Gestion des certificats de calibration

### Phase 6 : Module Acquisition
- Interface d'acquisition temps réel
- Visualisation des données
- Gestion des sessions d'acquisition

### Phase 7 : Modules d'Analyse
- Analyse statistique avancée
- Traitement FFT optimisé
- Analyse Goda et moindres carrés

### Phase 8 : Module Export
- Export multi-format
- Gestion des métadonnées
- Validation des données exportées

## Conformité et Standards

### Standards Maritimes
- **OpenBridge** : Interface cohérente avec les standards maritimes
- **ITTC** : Conformité aux recommandations de l'ITTC
- **ISO 17025** : Standards de qualité pour laboratoires

### Accessibilité
- **WCAG 2.1 AA** : Conformité niveau AA
- **Navigation clavier** : Support complet
- **Contraste** : Ratios de contraste appropriés
- **Tailles de police** : Lisibilité optimisée

### Architecture Logicielle
- **SOLID** : Principes SOLID respectés
- **MVC** : Pattern Model-View-Controller strict
- **Dependency Injection** : Injection de dépendances
- **Observer Pattern** : Communication via signaux/slots
