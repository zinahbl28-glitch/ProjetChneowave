# 🚀 CHNeoWave - Interface Moderne React/Tailwind

## 📋 Vue d'Ensemble

**CHNeoWave** est une application maritime moderne construite avec **React 19** et **Tailwind CSS 4**, offrant une interface professionnelle pour l'analyse et l'acquisition de données de houle.

## 🎯 Technologies Utilisées

- **Frontend** : React 19 + TypeScript
- **Styling** : Tailwind CSS 4 + PostCSS
- **Build Tool** : Vite 7
- **Navigation** : React Router DOM 7
- **Icons** : Heroicons React
- **Linting** : ESLint 9 + TypeScript ESLint

## 🚀 Démarrage Rapide

### 1. **Installation des Dépendances**
```bash
cd i-prototype-tailwind
npm install
```

### 2. **Lancement en Mode Développement**
```bash
npm run dev
```

### 3. **Build de Production**
```bash
npm run build
npm run preview
```

## 🌐 Accès à l'Application

- **Développement** : `http://localhost:5173`
- **Production** : `http://localhost:4173` (après build)

## 🎨 Architecture de l'Interface

### **Pages Principales**
- **🏠 Dashboard** : Vue d'ensemble avec métriques temps réel
- **📡 Acquisition** : Contrôle des capteurs et acquisition de données
- **⚙️ Calibration** : Configuration et calibration des instruments
- **📊 Analyse** : Traitement et visualisation des données
- **📈 Analyse Avancée** : Outils d'analyse spécialisés

### **Composants Réutilisables**
- **Navigation Minimaliste** : Sidebar élégante et responsive
- **Sélecteur de Thème** : Basculement clair/sombre
- **Logo de Lancement** : Animation d'accueil professionnelle

### **Design System**
- **Palette Maritime** : Couleurs océaniques et professionnelles
- **Golden Ratio** : Proportions harmonieuses et équilibrées
- **Responsive Design** : Adaptation mobile et desktop
- **Accessibilité** : Support complet des standards A11y

## 🔧 Fonctionnalités Clés

### **Acquisition de Données**
- Contrôle en temps réel des capteurs
- Configuration multi-canaux
- Surveillance des métriques de performance
- Gestion des erreurs et alertes

### **Analyse Maritime**
- Traitement FFT pour analyse spectrale
- Analyse Goda pour paramètres de houle
- Visualisations interactives
- Export de données (HDF5, CSV, PDF)

### **Interface Utilisateur**
- Navigation intuitive et rapide
- Thèmes adaptatifs (jour/nuit)
- Animations fluides et professionnelles
- Support multi-résolutions

## 📱 Compatibilité

- **Navigateurs** : Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Systèmes** : Windows 10/11, macOS 10.15+, Linux Ubuntu 20.04+
- **Résolutions** : 1024x768 (min) → 4K (recommandé)

## 🚨 Dépannage

### **Problèmes Courants**

#### **Dépendances non installées**
```bash
npm install
# ou
yarn install
```

#### **Port déjà utilisé**
```bash
# Changer le port dans vite.config.ts
export default defineConfig({
  server: { port: 3000 }
})
```

#### **Erreurs TypeScript**
```bash
npm run lint
# Vérifier les erreurs dans la console
```

### **Debug et Logs**
- **Console navigateur** : F12 → Console
- **Logs Vite** : Terminal de développement
- **TypeScript** : Vérification des types en temps réel

## 🔄 Développement

### **Structure des Fichiers**
```
src/
├── components/          # Composants réutilisables
├── pages/              # Pages de l'application
├── layouts/            # Layouts et templates
├── contexts/           # Contextes React
├── styles/             # Styles globaux
└── assets/             # Images et ressources
```

### **Ajout de Nouvelles Pages**
1. Créer le composant dans `src/pages/`
2. Ajouter la route dans `src/App.tsx`
3. Mettre à jour la navigation si nécessaire

### **Personnalisation des Thèmes**
- Modifier `src/styles/` pour les variables CSS
- Ajuster `tailwind.config.js` pour la configuration
- Utiliser le composant `ThemeSelector` pour les thèmes

## 📦 Scripts Disponibles

```json
{
  "dev": "vite",                    // Développement
  "build": "tsc -b && vite build",  // Build production
  "preview": "vite preview",        // Prévisualisation
  "lint": "eslint ."                // Vérification code
}
```

## 🌟 Fonctionnalités Avancées

### **Performance**
- Lazy loading des composants
- Optimisation des bundles
- Code splitting automatique
- Cache intelligent des ressources

### **Accessibilité**
- Navigation au clavier
- Support des lecteurs d'écran
- Contraste et lisibilité optimisés
- Labels et descriptions appropriés

### **Internationalisation**
- Support multi-langues (préparé)
- Formatage des dates et nombres
- Traductions contextuelles

## 🔗 Intégration Backend

L'interface est conçue pour s'intégrer avec :
- **API REST** : Endpoints d'acquisition et d'analyse
- **WebSocket** : Données temps réel et métriques
- **Base de données** : Stockage et récupération des données
- **Systèmes externes** : Intégration avec équipements de laboratoire

## 📞 Support et Contribution

### **Documentation**
- **Guide utilisateur** : Ce README
- **Documentation technique** : Dossier `docs/`
- **Design system** : Fichiers de spécification

### **Développement**
- **Issues** : Via le système de tickets
- **Pull Requests** : Contributions bienvenues
- **Code Review** : Processus de validation

---

## 🎉 Prêt à Utiliser !

L'interface CHNeoWave moderne est maintenant prête pour l'analyse maritime professionnelle. 

**🚀 Lancez l'application et explorez ses fonctionnalités !**

**Bon travail avec CHNeoWave ! 🌊📊**
