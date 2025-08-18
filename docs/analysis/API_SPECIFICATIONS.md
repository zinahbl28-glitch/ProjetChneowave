# 🔌 Spécifications API et Modèles de Données

## 📋 Vue d'Ensemble des APIs

CHNeoWave expose deux interfaces principales pour la communication avec l'interface React :

1. **🌐 REST API** : Contrôle et configuration
2. **📡 WebSocket** : Données temps réel et événements

---

## 🌐 REST API - Spécifications

### **Base URL**
```
http://localhost:8766
```

### **Headers Communs**
```http
Content-Type: application/json
Accept: application/json
```

---

## 🎯 ACQUISITION API

### **POST /acq/start**
Démarre l'acquisition de données

**Request Body:**
```typescript
interface StartAcquisitionRequest {
  samplingRate: number;        // Hz (100-1000)
  channels: number[];          // Canaux à activer [1,2,3,4,5,6,7,8]
  duration?: number;           // Durée en secondes (optionnel)
  projectName?: string;        // Nom du projet (optionnel)
  metadata?: Record<string, any>; // Métadonnées additionnelles
}
```

**Response:**
```typescript
interface StartAcquisitionResponse {
  success: boolean;
  sessionId: string;
  message: string;
  estimatedDuration?: number;
  startTime: string;           // ISO 8601
}
```

**Example:**
```bash
curl -X POST http://localhost:8766/acq/start \
  -H "Content-Type: application/json" \
  -d '{
    "samplingRate": 500,
    "channels": [1,2,3,4],
    "duration": 3600,
    "projectName": "Test_Houle_2025"
  }'
```

### **POST /acq/stop**
Arrête l'acquisition en cours

**Response:**
```typescript
interface StopAcquisitionResponse {
  success: boolean;
  sessionId: string;
  totalSamples: number;
  endTime: string;
  dataFilePath?: string;
  message: string;
}
```

### **POST /acq/pause**
Met en pause l'acquisition

**Response:**
```typescript
interface PauseAcquisitionResponse {
  success: boolean;
  sessionId: string;
  status: 'paused' | 'resumed';
  message: string;
}
```

### **GET /acq/status**
Récupère le statut actuel de l'acquisition

**Response:**
```typescript
interface AcquisitionStatus {
  isAcquiring: boolean;
  isPaused: boolean;
  sessionId?: string;
  samplingRate: number;
  activeChannels: number[];
  elapsedTime: number;         // Secondes
  totalSamples: number;
  bufferFillRatio: number;     // 0-100%
  overruns: number;
  underruns: number;
  errors: number;
  startTime?: string;
  estimatedEndTime?: string;
}
```

### **GET /acq/boards**
Liste les cartes d'acquisition disponibles

**Response:**
```typescript
interface BoardInfo {
  id: string;
  name: string;
  type: 'mcc' | 'ni' | 'iotech' | 'demo';
  status: 'ok' | 'error' | 'unknown';
  channels: number;
  maxSamplingRate: number;
  supportedRanges: string[];
  firmware?: string;
  serialNumber?: string;
}

interface BoardsResponse {
  boards: BoardInfo[];
  defaultBoard?: string;
}
```

### **POST /acq/configure-channels**
Configure les paramètres des canaux

**Request Body:**
```typescript
interface ChannelConfig {
  channel: number;
  sensorType: 'pressure' | 'accelerometer' | 'wave_height' | 'temperature';
  label: string;
  units: string;
  rangeType: 'bipolar_10v' | 'bipolar_5v' | 'bipolar_2v' | 'unipolar_10v';
  calibrationOffset: number;
  calibrationScale: number;
  physicalUnits: string;
  sensorSensitivity: number;
  enabled: boolean;
}

interface ConfigureChannelsRequest {
  channels: ChannelConfig[];
}
```

---

## 📊 ANALYSE API

### **POST /analysis/fft/benchmark**
Lance un benchmark de performance FFT

**Request Body:**
```typescript
interface FFTBenchmarkRequest {
  signalLength: number;        // Longueur du signal (1024, 2048, 4096, etc.)
  iterations: number;          // Nombre d'itérations pour le benchmark
  useOptimized: boolean;       // Utiliser pyFFTW si disponible
}
```

**Response:**
```typescript
interface FFTBenchmarkResponse {
  success: boolean;
  results: {
    numpyTime: number;         // Temps numpy.fft (ms)
    optimizedTime?: number;    // Temps pyFFTW (ms)
    speedup?: number;          // Facteur d'accélération
    memoryUsage: number;       // Utilisation mémoire (MB)
    cpuUsage: number;          // Utilisation CPU (%)
  };
  recommendations: string[];
}
```

### **POST /analysis/goda/analyze**
Lance l'analyse Goda pour séparation des ondes

**Request Body:**
```typescript
interface GodaAnalysisRequest {
  data: number[][];            // Données des sondes [n_sondes, n_échantillons]
  samplingRate: number;        // Fréquence d'échantillonnage
  probePositions: number[];    // Positions des sondes [m]
  waterDepth: number;          // Profondeur d'eau [m]
  frequencyRange: [number, number]; // Plage de fréquences [Hz]
  useCache: boolean;           // Utiliser le cache des matrices
}
```

**Response:**
```typescript
interface GodaAnalysisResponse {
  success: boolean;
  results: {
    incidentAmplitude: number;     // Amplitude incidente [m]
    reflectedAmplitude: number;    // Amplitude réfléchie [m]
    reflectionCoefficient: number; // Coefficient de réflexion
    phaseIncident: number;         // Phase incidente [rad]
    phaseReflected: number;        // Phase réfléchie [rad]
    frequency: number;             // Fréquence [Hz]
    wavelength: number;            // Longueur d'onde [m]
    waveNumber: number;            // Nombre d'onde [rad/m]
  };
  processingTime: number;          // Temps de traitement [ms]
  cacheHit: boolean;               // Cache utilisé ?
}
```

### **POST /analysis/process-file**
Traite un fichier de données existant

**Request Body:**
```typescript
interface ProcessFileRequest {
  filePath: string;            // Chemin vers le fichier
  analysisType: 'fft' | 'goda' | 'both';
  parameters: Record<string, any>; // Paramètres spécifiques à l'analyse
}
```

---

## 💾 EXPORT API

### **POST /export/start**
Démarre l'export des données

**Request Body:**
```typescript
interface ExportRequest {
  format: 'hdf5' | 'tdms' | 'csv';
  data: number[][];            // Données à exporter
  filename: string;            // Nom du fichier
  compression: boolean;        // Activer la compression
  metadata: Record<string, any>; // Métadonnées
  sessionInfo?: Record<string, any>; // Informations de session
  calibrationInfo?: Record<string, any>; // Informations de calibration
}
```

**Response:**
```typescript
interface ExportResponse {
  success: boolean;
  exportId: string;
  filePath: string;
  estimatedTime: number;       // Temps estimé [s]
  message: string;
}
```

### **GET /export/progress**
Récupère la progression de l'export

**Response:**
```typescript
interface ExportProgress {
  exportId: string;
  status: 'running' | 'completed' | 'error' | 'cancelled';
  progress: number;            // 0-100%
  currentStep: string;
  estimatedTimeRemaining: number; // Secondes
  errorMessage?: string;
}
```

### **GET /export/recent**
Liste les exports récents

**Response:**
```typescript
interface ExportHistory {
  exports: {
    id: string;
    filename: string;
    format: string;
    size: number;              // Taille en bytes
    createdAt: string;         // ISO 8601
    status: 'completed' | 'error';
    filePath: string;
  }[];
}
```

---

## 📈 MONITORING API

### **GET /monitoring/metrics**
Récupère les métriques de performance système

**Response:**
```typescript
interface SystemMetrics {
  cpu: {
    usage: number;             // Utilisation CPU (%)
    temperature?: number;       // Température CPU (°C)
    frequency: number;          // Fréquence CPU (MHz)
    cores: number;             // Nombre de cœurs
  };
  memory: {
    total: number;             // Mémoire totale (MB)
    used: number;              // Mémoire utilisée (MB)
    available: number;         // Mémoire disponible (MB)
    swap: {
      total: number;
      used: number;
    };
  };
  disk: {
    total: number;             // Espace total (GB)
    used: number;              // Espace utilisé (GB)
    free: number;              // Espace libre (GB)
    readSpeed: number;         // Vitesse lecture (MB/s)
    writeSpeed: number;        // Vitesse écriture (MB/s)
  };
  network: {
    bytesSent: number;         // Octets envoyés
    bytesReceived: number;     // Octets reçus
    packetsSent: number;       // Paquets envoyés
    packetsReceived: number;   // Paquets reçus
  };
  processes: {
    total: number;             // Nombre total de processus
    threads: number;           // Nombre total de threads
    chneowaveThreads: number;  // Threads CHNeoWave
  };
  timestamp: string;           // ISO 8601
}
```

---

## 🚨 ERREURS API

### **Codes d'Erreur HTTP**
- **200** : Succès
- **400** : Erreur de requête (paramètres invalides)
- **404** : Ressource non trouvée
- **500** : Erreur interne du serveur
- **503** : Service indisponible

### **Format d'Erreur Standard**
```typescript
interface APIError {
  error: {
    code: string;              // Code d'erreur unique
    message: string;           // Message d'erreur lisible
    details?: any;             // Détails additionnels
    timestamp: string;         // ISO 8601
    requestId?: string;        // ID de requête pour traçabilité
  };
}
```

**Exemples de Codes d'Erreur:**
- `ACQ_ALREADY_RUNNING` : Acquisition déjà en cours
- `INVALID_CHANNEL_CONFIG` : Configuration de canal invalide
- `HARDWARE_NOT_FOUND` : Matériel non détecté
- `INSUFFICIENT_MEMORY` : Mémoire insuffisante
- `FILE_ACCESS_ERROR` : Erreur d'accès au fichier

---

## 📡 WEBSOCKET API

### **Endpoint**
```
ws://localhost:8765/signals
```

### **Types de Messages**

#### **Buffer Status**
```typescript
interface BufferStatusMessage {
  type: 'buffer_status';
  data: {
    fillRatio: number;         // 0-100%
    overruns: number;
    underruns: number;
    maxLatency: number;        // ms
    samplesAcquired: number;
    acquisitionRate: number;   // Hz
  };
  timestamp: string;
}
```

#### **Session Event**
```typescript
interface SessionEventMessage {
  type: 'session_event';
  data: {
    eventType: 'started' | 'stopped' | 'paused' | 'resumed' | 'error';
    sessionId: string;
    message: string;
    details?: any;
  };
  timestamp: string;
}
```

#### **Error Occurred**
```typescript
interface ErrorMessage {
  type: 'error_occurred';
  data: {
    errorId: string;
    category: 'hardware' | 'software' | 'data' | 'system';
    severity: 'low' | 'medium' | 'high' | 'critical';
    message: string;
    details?: any;
    stackTrace?: string;
  };
  timestamp: string;
}
```

#### **Performance Metrics**
```typescript
interface PerformanceMessage {
  type: 'perf_metrics';
  data: {
    cpu: number;               // %
    memory: number;            // %
    disk: number;              // %
    network: number;           // %
    activeThreads: number;
    bufferEfficiency: number;  // %
  };
  timestamp: string;
}
```

---

## 🔧 ZOD SCHEMAS (Frontend)

### **Validation des Requêtes**
```typescript
import { z } from 'zod';

// Schéma de validation pour StartAcquisition
export const StartAcquisitionSchema = z.object({
  samplingRate: z.number().min(100).max(1000),
  channels: z.array(z.number().min(1).max(8)).min(1).max(8),
  duration: z.number().positive().optional(),
  projectName: z.string().min(1).max(100).optional(),
  metadata: z.record(z.any()).optional(),
});

// Schéma de validation pour ChannelConfig
export const ChannelConfigSchema = z.object({
  channel: z.number().min(1).max(8),
  sensorType: z.enum(['pressure', 'accelerometer', 'wave_height', 'temperature']),
  label: z.string().min(1).max(50),
  units: z.string().min(1).max(20),
  rangeType: z.enum(['bipolar_10v', 'bipolar_5v', 'bipolar_2v', 'unipolar_10v']),
  calibrationOffset: z.number(),
  calibrationScale: z.number().positive(),
  physicalUnits: z.string().min(1).max(20),
  sensorSensitivity: z.number().positive(),
  enabled: z.boolean(),
});

// Schéma de validation pour ExportRequest
export const ExportRequestSchema = z.object({
  format: z.enum(['hdf5', 'tdms', 'csv']),
  data: z.array(z.array(z.number())),
  filename: z.string().min(1).max(255),
  compression: z.boolean(),
  metadata: z.record(z.any()),
  sessionInfo: z.record(z.any()).optional(),
  calibrationInfo: z.record(z.any()).optional(),
});
```

---

## 📊 MÉTRIQUES DE PERFORMANCE

### **Temps de Réponse Cibles**
- **GET requests** : < 100ms
- **POST requests** : < 500ms
- **WebSocket messages** : < 50ms
- **File uploads** : < 1s par MB

### **Débit Cible**
- **Acquisition** : 1000 Hz × 8 canaux = 8000 échantillons/s
- **WebSocket** : 20 messages/s maximum
- **REST API** : 1000 requests/minute

### **Disponibilité**
- **Uptime cible** : 99.9%
- **Recovery time** : < 5 secondes
- **Graceful degradation** : Mode dégradé en cas d'erreur

---

## 🔒 SÉCURITÉ ET VALIDATION

### **Validation des Données**
- **Type checking** : Validation TypeScript stricte
- **Range validation** : Vérification des limites
- **Sanitization** : Nettoyage des entrées utilisateur
- **Rate limiting** : Limitation du nombre de requêtes

### **Gestion des Erreurs**
- **Logging** : Traçabilité complète des erreurs
- **User feedback** : Messages d'erreur clairs
- **Recovery** : Récupération automatique quand possible
- **Fallback** : Modes de fonctionnement dégradés

---

## 📚 RÉFÉRENCES

- **OpenAPI 3.0** : Spécification standard des APIs REST
- **Zod** : Validation TypeScript runtime
- **WebSocket RFC 6455** : Protocole WebSocket
- **HTTP/1.1 RFC 7231** : Protocole HTTP
- **ISO 8601** : Format des dates et heures
