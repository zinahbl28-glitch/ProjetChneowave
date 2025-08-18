# 🔧 Guide d'Installation des Serveurs MCP pour Qodo Gen

## 📋 Configuration JSON pour Qodo Gen

### Configuration Principale
Copiez cette configuration dans votre fichier de configuration Qodo Gen :

```json
{
  "mcpServers": {
    "everything": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"],
      "env": {"NODE_ENV": "production"}
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"],
      "env": {"NODE_ENV": "production"}
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-filesystem",
        "c:\\Users\\PC\\Desktop\\chneowave\\i-prototype-tailwind"
      ],
      "env": {"NODE_ENV": "production"}
    },
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git", 
        "--repository",
        "c:\\Users\\PC\\Desktop\\chneowave\\i-prototype-tailwind"
      ],
      "env": {"NODE_ENV": "production"}
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {"NODE_ENV": "production"}
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "env": {"NODE_ENV": "production"}
    },
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"],
      "env": {"NODE_ENV": "production"}
    }
  }
}
```

## 🚀 Serveurs MCP Inclus

### 1. **Everything Server**
- **Fonction** : Serveur de référence avec prompts, ressources et outils
- **Capacités** : Tests, prompts, ressources, outils de développement
- **Usage** : Idéal pour tester et développer avec MCP

### 2. **Fetch Server** 
- **Fonction** : Récupération et conversion de contenu web
- **Capacités** : Web scraping, conversion de contenu, récupération d'URLs
- **Usage** : Récupérer du contenu web pour analyse ou intégration

### 3. **Filesystem Server**
- **Fonction** : Opérations de fichiers sécurisées
- **Capacités** : Lecture/écriture de fichiers, listing de répertoires, recherche
- **Sécurité** : Accès limité au répertoire du projet CHNeoWave
- **Usage** : Manipulation sécurisée des fichiers du projet

### 4. **Git Server**
- **Fonction** : Manipulation de dépôts Git
- **Capacités** : git log, diff, status, recherche, informations du dépôt
- **Usage** : Analyse et manipulation du dépôt CHNeoWave

### 5. **Memory Server**
- **Fonction** : Système de mémoire persistante basé sur graphe de connaissances
- **Capacités** : Graphe de connaissances, mémoire persistante, relations d'entités
- **Usage** : Stockage et récupération de connaissances contextuelles

### 6. **Sequential Thinking Server**
- **Fonction** : Résolution de problèmes par séquences de pensée
- **Capacités** : Résolution de problèmes, séquences de pensée, raisonnement dynamique
- **Usage** : Approche structurée pour résoudre des problèmes complexes

### 7. **Time Server**
- **Fonction** : Conversion de temps et fuseaux horaires
- **Capacités** : Conversion de fuseaux, formatage de temps, calculs de dates
- **Usage** : Gestion du temps et des dates dans les projets

## ⚙️ Instructions d'Installation

### Prérequis
- Node.js 18+ installé
- npm ou npx disponible
- Accès internet pour télécharger les packages

### Étapes d'Installation

1. **Ouvrir Qodo Gen**
2. **Accéder aux paramètres MCP**
3. **Copier la configuration JSON** depuis `qodo-gen-mcp-config.json`
4. **Coller dans la section mcpServers**
5. **Sauvegarder et redémarrer Qodo Gen**

### Vérification
Les serveurs MCP seront automatiquement téléchargés et démarrés lors de la première utilisation.

## 🔒 Sécurité

- **Filesystem** : Accès limité au répertoire du projet
- **Git** : Lecture seule du dépôt local  
- **Network** : Requis pour fetch et everything servers
- **Memory** : Stockage local des données de mémoire

## 📁 Fichiers Générés

- `mcp-servers-config.json` - Configuration principale
- `mcp-servers-individual-configs.json` - Configurations détaillées
- `qodo-gen-mcp-config.json` - Configuration optimisée pour Qodo Gen
- `mcp-installation-guide.md` - Ce guide d'installation

## 🎯 Utilisation Recommandée

1. **Développement** : everything, filesystem, git
2. **Recherche Web** : fetch
3. **Mémoire Contextuelle** : memory
4. **Résolution de Problèmes** : sequential-thinking
5. **Gestion du Temps** : time

Tous les serveurs sont configurés pour fonctionner avec votre projet CHNeoWave.