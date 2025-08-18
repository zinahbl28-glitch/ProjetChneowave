# Architecture de Navigation Unifiée - Interface Maritime CHNeoWave

## Structure de Navigation Principale

### Sidebar Navigation (Navigation Maritime Professionnelle)
- **Position** : Fixe à gauche, pleine hauteur
- **Largeur** : 280px (desktop), réduit en mode mobile
- **Style** : Thème maritime (bleu foncé, éléments cyan/turquoise)
- **Accessibilité** : Navigation clavier, contraste élevé, taille minimum 44px

### Éléments de Navigation
1. **🏠 Dashboard Général**
   - Vue d'ensemble système
   - Statistiques temps réel
   - Projets récents
   - Quick actions

2. **📊 Acquisition Temps Réel**
   - Visualisations houle
   - Statistiques essentielles
   - Contrôles acquisition
   - Mode masquage stats avancées

3. **🔬 Calibration Matérielle**
   - Assistant calibration
   - Validation matérielle
   - Paramètres capteurs
   - Historique calibrations

4. **📈 Analyse Spectrale**
   - Outils scientifiques
   - Visualisations avancées
   - Comparaison données
   - Export résultats

5. **📋 Rapports & Export**
   - Génération rapports
   - Export multi-format
   - Historique exports
   - Templates rapports

6. **⚙️ Configuration Système**
   - Gestion profils
   - Thèmes (clair/sombre/maritime)
   - Notifications
   - Paramètres avancés

## Hiérarchie des Pages

### Page Principale - Dashboard
- **Route** : /
- **Contenu** :
  - Statut système global
  - Alertes critiques
  - Sélection projet
  - Navigation rapide

### Page Acquisition
- **Route** : /acquisition
- **Contenu** :
  - 3 graphiques professionnels
  - Barre statistiques temps réel
  - Bouton sauvegarder
  - Design maritime épuré

### Page Calibration
- **Route** : /calibration
- **Contenu** :
  - Assistant step-by-step
  - Validation matérielle
  - Paramètres capteurs

### Page Analyse
- **Route** : /analysis
- **Contenu** :
  - Analyse statistique
  - Visualisations interactives
  - Outils scientifiques

### Page Export
- **Route** : /export
- **Contenu** :
  - Gestion exports
  - Multi-format (HDF5, CSV, PDF, MATLAB)
  - Historique

### Page Configuration
- **Route** : /settings
- **Contenu** :
  - Gestion profils utilisateurs
  - Sélection thèmes
  - Paramètres système

## Design Responsive

### Desktop (>1024px)
- Sidebar fixe complète
- Grid 3 colonnes pour acquisition
- Visualisations pleine taille

### Tablet (768px - 1024px)
- Sidebar rétractable
- Grid 2 colonnes pour acquisition
- Contrôles adaptés touch

### Mobile (<768px)
- Navigation bottom bar
- Sidebar en overlay
- Visualisations simplifiées
- Focus sur données essentielles

## Accessibilité et Ergonomie

### Navigation Clavier
- Tabulation entre éléments
- Raccourcis clavier
- Focus visible

### Contraste et Lisibilité
- Ratio ≥7:1 pour texte
- Taille minimum 44px
- Typographie claire

### Feedback Utilisateur
- Indication pages actives
- Animations de transition
- Confirmation actions
