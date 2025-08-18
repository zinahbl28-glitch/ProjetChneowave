# 🏗️ Architecture CHNeoWave - Vue d'Ensemble

## 📊 Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CHNeoWave - Architecture Maritime                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              🖥️ INTERFACE UTILISATEUR                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   Dashboard     │  │   Acquisition   │  │    Analyse      │                │
│  │   Maritime      │  │   Temps Réel    │  │   Spectrale     │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   Calibration   │  │   Export        │  │   Monitoring    │                │
│  │   Capteurs      │  │   HDF5/TDMS     │  │   Performance   │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔌 COUCHE D'INTÉGRATION                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   WebSocket     │  │   REST API      │  │   Event Bus     │                │
│  │   Temps Réel    │  │   Contrôle      │  │   Signaux       │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🧠 CORE LOGICIEL PYTHON                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    🎯 ACQUISITION & HARDWARE                           │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │    │
│  │  │ Acquisition     │  │ MCC DAQ         │  │ Hardware        │        │    │
│  │  │ Controller      │  │ USB-1608FS      │  │ Manager         │        │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    🔬 TRAITEMENT & ANALYSE                             │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │    │
│  │  │ FFT Optimisé    │  │ Goda Analyzer   │  │ Post-Processor  │        │    │
│  │  │ pyFFTW          │  │ SVD + Cache     │  │ Validation      │        │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    💾 DONNÉES & EXPORT                                 │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │    │
│  │  │ Circular Buffer │  │ Export Manager  │  │ Metadata        │        │    │
│  │  │ Temps Réel      │  │ HDF5/TDMS       │  │ Manager         │        │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    ⚙️ INFRASTRUCTURE                                   │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │    │
│  │  │ Signal Bus      │  │ Error Handler   │  │ Performance     │        │    │
│  │  │ Event System    │  │ Logging         │  │ Monitor         │        │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔌 PILOTES MATÉRIEL                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   MCC DAQ       │  │   NI-DAQmx      │  │   IOtech        │                │
│  │   USB-1608FS    │  │   National      │  │   Legacy        │                │
│  │   Principal     │  │   Instruments   │  │   Support       │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🌊 CAPTEURS MARITIMES                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   Capteurs      │  │   Accéléro-     │  │   Sonde de      │                │
│  │   de Pression   │  │   mètres        │  │   Température   │                │
│  │   (Houle)       │  │   (Mouvement)   │  │   (Eau)        │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Flux de Données Principal

### 1. **Acquisition Temps Réel**
```
Capteurs → Pilotes → AcquisitionController → CircularBuffer → SignalBus → Interface
```

### 2. **Traitement et Analyse**
```
CircularBuffer → FFT Processor → Goda Analyzer → Post-Processor → Export
```

### 3. **Communication Interface**
```
Interface React → WebSocket/REST → Core Python → Hardware → Capteurs
```

## 🏛️ Composants Architecturaux

### **🎯 Couche Interface (React + TypeScript)**
- **Navigation** : Sidebar minimaliste avec routing
- **Pages** : Dashboard, Acquisition, Calibration, Analyse, Export
- **Composants** : Thèmes, Navigation, Logo de lancement
- **État** : Gestion centralisée avec hooks React

### **🔌 Couche d'Intégration**
- **WebSocket** : Communication temps réel (métriques, événements)
- **REST API** : Contrôle et configuration
- **Event Bus** : Gestion des signaux et erreurs

### **🧠 Core Logiciel (Python)**
- **Acquisition** : Contrôle des capteurs et acquisition de données
- **Traitement** : FFT optimisé, analyse Goda, validation
- **Données** : Buffer circulaire, export HDF5/TDMS, métadonnées
- **Infrastructure** : Gestion d'erreurs, monitoring, logging

### **🔌 Pilotes Matériel**
- **MCC DAQ** : Carte principale USB-1608FS
- **NI-DAQmx** : Support National Instruments
- **IOtech** : Support legacy

## 📊 Métriques de Performance

### **Acquisition**
- **Fréquence** : 100-1000 Hz configurable
- **Latence** : < 2ms (objectif)
- **Buffer** : 10,000 échantillons circulaire
- **Canaux** : 8 canaux simultanés

### **Traitement**
- **FFT** : +80% performance avec pyFFTW
- **Goda** : +1000% avec cache SVD
- **Mémoire** : Gestion optimisée des buffers

### **Interface**
- **Rendu** : 60 FPS cible
- **Mise à jour** : ≤ 20 Hz pour les métriques
- **Responsive** : Support mobile et desktop

## 🔒 Sécurité et Robustesse

### **Gestion d'Erreurs**
- **Validation** : Données d'entrée et paramètres
- **Recovery** : Récupération automatique des erreurs
- **Logging** : Traçabilité complète des opérations

### **Performance**
- **Monitoring** : Métriques CPU, mémoire, disque
- **Throttling** : Limitation des mises à jour UI
- **Cache** : Optimisation des calculs répétitifs

## 🚀 Évolutivité

### **Modularité**
- **Plugins** : Architecture extensible pour nouveaux capteurs
- **APIs** : Interfaces standardisées pour intégration
- **Formats** : Support extensible des formats d'export

### **Scalabilité**
- **Multi-threading** : Traitement parallèle des canaux
- **Async** : Opérations non-bloquantes
- **Distribué** : Support multi-nœuds (futur)

---

## 📋 Résumé Architecture

**CHNeoWave** suit une architecture **modulaire en couches** avec :

1. **Interface React moderne** pour l'expérience utilisateur
2. **Couche d'intégration** pour la communication temps réel
3. **Core Python optimisé** pour le traitement maritime
4. **Pilotes matériel** pour l'acquisition de données
5. **Capteurs spécialisés** pour l'analyse de houle

Cette architecture garantit **performance**, **maintenabilité** et **évolutivité** pour les applications maritimes professionnelles.
