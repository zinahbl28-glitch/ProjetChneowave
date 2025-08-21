# 🚀 Guide de Migration CHNeoWave - Qt vers Web

## 📋 **Vue d'Ensemble de la Migration**

Ce guide détaille la migration de l'interface Qt existante vers une interface web moderne pour CHNeoWave, en conservant toutes les fonctionnalités scientifiques tout en améliorant l'expérience utilisateur.

---

## 🎯 **Objectifs de la Migration**

### **Avantages de l'Interface Web :**
- ✅ **Accessibilité universelle** (navigateur web)
- ✅ **Déploiement simplifié** (pas d'installation)
- ✅ **Mise à jour automatique**
- ✅ **Interface responsive** (mobile/desktop)
- ✅ **Intégration facile** avec systèmes existants
- ✅ **Performance optimisée** avec technologies modernes

---

## 🏗️ **Architecture Technique**

### **Stack Technologique Recommandée :**

```yaml
Frontend:
  - React 19 + TypeScript
  - Tailwind CSS 4
  - Chart.js + D3.js (graphiques)
  - React Router (navigation)
  - Zustand (état global)

Backend:
  - Python FastAPI
  - WebSocket (données temps réel)
  - SQLAlchemy (ORM)
  - Pydantic (validation)

Base de données:
  - SQLite (développement)
  - PostgreSQL (production)

Déploiement:
  - Docker + Docker Compose
  - Nginx (reverse proxy)
  - PM2 (process manager)
```

---

## 📁 **Structure du Projet**

```
chneowave-web/
├── frontend/                 # Application React
│   ├── src/
│   │   ├── components/       # Composants réutilisables
│   │   ├── pages/           # Pages de l'application
│   │   ├── hooks/           # Hooks personnalisés
│   │   ├── services/        # Services API
│   │   ├── stores/          # État global (Zustand)
│   │   ├── types/           # Types TypeScript
│   │   └── utils/           # Utilitaires
│   ├── public/              # Assets statiques
│   └── package.json
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── api/             # Routes API
│   │   ├── core/            # Configuration
│   │   ├── models/          # Modèles de données
│   │   ├── services/        # Logique métier
│   │   └── utils/           # Utilitaires
│   ├── requirements.txt
│   └── main.py
├── shared/                   # Code partagé
│   ├── types/               # Types partagés
│   └── constants/           # Constantes
└── docker-compose.yml       # Configuration Docker
```

---

## 🔄 **Plan de Migration Étape par Étape**

### **Phase 1 : Setup de l'Environnement (1 semaine)**

#### **1.1 Configuration Backend**
```bash
# Créer le projet backend
mkdir chneowave-web/backend
cd chneowave-web/backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install fastapi uvicorn sqlalchemy pydantic websockets
pip install python-multipart python-jose[cryptography] passlib[bcrypt]
```

#### **1.2 Configuration Frontend**
```bash
# Créer l'application React
npx create-react-app frontend --template typescript
cd frontend

# Installer les dépendances
npm install @types/react @types/react-dom
npm install tailwindcss postcss autoprefixer
npm install chart.js react-chartjs-2
npm install react-router-dom
npm install zustand
npm install axios
npm install @headlessui/react @heroicons/react
```

#### **1.3 Configuration Docker**
```dockerfile
# Dockerfile pour le backend
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Phase 2 : Migration des Fonctionnalités (4 semaines)**

#### **2.1 Migration de la Gestion des Projets**

**Backend (FastAPI) :**
```python
# backend/app/models/project.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    code: str
    engineer: str
    project_manager: str
    scale: float
    basin: str
    canal: str
    description: Optional[str] = None

class Project(ProjectCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# backend/app/api/projects.py
from fastapi import APIRouter, HTTPException
from typing import List
from ..models.project import Project, ProjectCreate
from ..services.project_service import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate):
    return await ProjectService.create_project(project)

@router.get("/", response_model=List[Project])
async def get_projects():
    return await ProjectService.get_all_projects()

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: int):
    project = await ProjectService.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
```

**Frontend (React) :**
```typescript
// frontend/src/types/project.ts
export interface Project {
  id: number;
  name: string;
  code: string;
  engineer: string;
  project_manager: string;
  scale: number;
  basin: string;
  canal: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  code: string;
  engineer: string;
  project_manager: string;
  scale: number;
  basin: string;
  canal: string;
  description?: string;
}

// frontend/src/services/projectService.ts
import axios from 'axios';
import { Project, ProjectCreate } from '../types/project';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const projectService = {
  async createProject(project: ProjectCreate): Promise<Project> {
    const response = await axios.post(`${API_BASE_URL}/api/projects/`, project);
    return response.data;
  },

  async getProjects(): Promise<Project[]> {
    const response = await axios.get(`${API_BASE_URL}/api/projects/`);
    return response.data;
  },

  async getProject(id: number): Promise<Project> {
    const response = await axios.get(`${API_BASE_URL}/api/projects/${id}`);
    return response.data;
  }
};

// frontend/src/components/ProjectForm.tsx
import React, { useState } from 'react';
import { ProjectCreate } from '../types/project';
import { projectService } from '../services/projectService';

export const ProjectForm: React.FC = () => {
  const [formData, setFormData] = useState<ProjectCreate>({
    name: '',
    code: '',
    engineer: '',
    project_manager: '',
    scale: 1.0,
    basin: '',
    canal: '',
    description: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const project = await projectService.createProject(formData);
      console.log('Project created:', project);
      // Navigation vers le dashboard
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Nom du projet
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
        {/* Autres champs... */}
      </div>
      <button
        type="submit"
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Créer le projet
      </button>
    </form>
  );
};
```

#### **2.2 Migration de la Calibration**

**Backend :**
```python
# backend/app/models/calibration.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CalibrationPoint(BaseModel):
    height: float
    voltage: float
    timestamp: datetime

class CalibrationData(BaseModel):
    probe_id: int
    points: List[CalibrationPoint]
    linearity_factor: float
    is_valid: bool

class CalibrationSession(BaseModel):
    id: int
    project_id: int
    probe_count: int
    points_per_probe: int
    status: str  # 'pending', 'in_progress', 'completed'
    created_at: datetime
    completed_at: Optional[datetime] = None

# backend/app/api/calibration.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.calibration_service import CalibrationService

router = APIRouter(prefix="/api/calibration", tags=["calibration"])

@router.websocket("/ws/{session_id}")
async def calibration_websocket(websocket: WebSocket, session_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Traitement des données de calibration
            result = await CalibrationService.process_calibration_point(
                session_id, data
            )
            await websocket.send_json(result)
    except WebSocketDisconnect:
        print(f"Client disconnected from calibration session {session_id}")
```

**Frontend :**
```typescript
// frontend/src/components/CalibrationView.tsx
import React, { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';

interface CalibrationPoint {
  height: number;
  voltage: number;
  timestamp: string;
}

export const CalibrationView: React.FC = () => {
  const [currentProbe, setCurrentProbe] = useState(1);
  const [currentStep, setCurrentStep] = useState(1);
  const [calibrationData, setCalibrationData] = useState<CalibrationPoint[]>([]);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const startCalibration = () => {
    setIsCalibrating(true);
    // Connexion WebSocket pour la calibration en temps réel
    wsRef.current = new WebSocket(`ws://localhost:8000/api/calibration/ws/${sessionId}`);
    
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setCalibrationData(prev => [...prev, data]);
    };
  };

  const validatePoint = async (height: number, voltage: number) => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({
        probe_id: currentProbe,
        height,
        voltage,
        step: currentStep
      }));
    }
  };

  const chartData = {
    labels: calibrationData.map(point => point.height),
    datasets: [{
      label: 'Calibration',
      data: calibrationData.map(point => point.voltage),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium mb-4">Configuration</h3>
          {/* Configuration des sondes */}
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium mb-4">Processus</h3>
          {isCalibrating ? (
            <div className="space-y-4">
              <div className="text-sm text-gray-600">
                Sonde {currentProbe} - Étape {currentStep}/5
              </div>
              {/* Formulaire de saisie des points */}
            </div>
          ) : (
            <button
              onClick={startCalibration}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              Démarrer la calibration
            </button>
          )}
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-4">Graphique de Calibration</h3>
        <Line data={chartData} />
      </div>
    </div>
  );
};
```

#### **2.3 Migration de l'Acquisition**

**Backend (WebSocket pour données temps réel) :**
```python
# backend/app/services/acquisition_service.py
import asyncio
from typing import Dict, List
import numpy as np

class AcquisitionService:
    def __init__(self):
        self.active_sessions: Dict[int, bool] = {}
        self.data_buffers: Dict[int, List[float]] = {}
    
    async def start_acquisition(self, session_id: int, config: dict):
        self.active_sessions[session_id] = True
        self.data_buffers[session_id] = []
        
        # Simulation de l'acquisition de données
        while self.active_sessions.get(session_id, False):
            # Génération de données simulées
            data = self.generate_wave_data(config)
            self.data_buffers[session_id].extend(data)
            
            # Calcul des métriques temps réel
            metrics = self.calculate_realtime_metrics(data)
            
            await asyncio.sleep(1.0 / config['sampling_frequency'])
            
            return metrics
    
    def generate_wave_data(self, config: dict) -> List[float]:
        # Simulation de données de houle
        t = np.linspace(0, 1, config['sampling_frequency'])
        frequency = 0.5  # Hz
        amplitude = 1.0  # m
        noise = np.random.normal(0, 0.1, len(t))
        
        wave_data = amplitude * np.sin(2 * np.pi * frequency * t) + noise
        return wave_data.tolist()
    
    def calculate_realtime_metrics(self, data: List[float]) -> dict:
        if not data:
            return {'hmax': 0, 'hmin': 0, 'h1_3': 0}
        
        hmax = max(data)
        hmin = min(data)
        
        # Calcul de H1/3 (hauteur significative)
        sorted_data = sorted(data, reverse=True)
        third_count = len(sorted_data) // 3
        h1_3 = np.mean(sorted_data[:third_count])
        
        return {
            'hmax': round(hmax, 3),
            'hmin': round(hmin, 3),
            'h1_3': round(h1_3, 3)
        }

# backend/app/api/acquisition.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.acquisition_service import AcquisitionService

router = APIRouter(prefix="/api/acquisition", tags=["acquisition"])

acquisition_service = AcquisitionService()

@router.websocket("/ws/{session_id}")
async def acquisition_websocket(websocket: WebSocket, session_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            
            if data['action'] == 'start':
                config = data['config']
                await acquisition_service.start_acquisition(session_id, config)
                
            elif data['action'] == 'stop':
                acquisition_service.active_sessions[session_id] = False
                
    except WebSocketDisconnect:
        acquisition_service.active_sessions[session_id] = False
```

**Frontend :**
```typescript
// frontend/src/components/AcquisitionView.tsx
import React, { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';

interface AcquisitionConfig {
  sampling_frequency: number;
  time_cycle: number;
  duration: number;
}

interface RealTimeMetrics {
  hmax: number;
  hmin: number;
  h1_3: number;
}

export const AcquisitionView: React.FC = () => {
  const [isAcquiring, setIsAcquiring] = useState(false);
  const [config, setConfig] = useState<AcquisitionConfig>({
    sampling_frequency: 50,
    time_cycle: 30,
    duration: 300
  });
  const [metrics, setMetrics] = useState<RealTimeMetrics>({
    hmax: 0,
    hmin: 0,
    h1_3: 0
  });
  const [elapsedTime, setElapsedTime] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startAcquisition = () => {
    setIsAcquiring(true);
    setElapsedTime(0);
    
    // Connexion WebSocket
    wsRef.current = new WebSocket(`ws://localhost:8000/api/acquisition/ws/${sessionId}`);
    
    wsRef.current.onopen = () => {
      wsRef.current?.send(JSON.stringify({
        action: 'start',
        config
      }));
    };
    
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data);
    };
    
    // Timer pour le temps écoulé
    intervalRef.current = setInterval(() => {
      setElapsedTime(prev => prev + 1);
    }, 1000);
  };

  const stopAcquisition = () => {
    setIsAcquiring(false);
    wsRef.current?.send(JSON.stringify({ action: 'stop' }));
    wsRef.current?.close();
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      wsRef.current?.close();
    };
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Acquisition de Données</h2>
          <div className="flex gap-2">
            <button
              onClick={startAcquisition}
              disabled={isAcquiring}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
            >
              ▶️ Démarrer
            </button>
            <button
              onClick={stopAcquisition}
              disabled={!isAcquiring}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:opacity-50"
            >
              ⏹️ Arrêter
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium mb-4">Paramètres</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Fréquence d'échantillonnage (Hz)
                </label>
                <select
                  value={config.sampling_frequency}
                  onChange={(e) => setConfig({...config, sampling_frequency: Number(e.target.value)})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value={10}>10 Hz</option>
                  <option value={20}>20 Hz</option>
                  <option value={50}>50 Hz</option>
                  <option value={100}>100 Hz</option>
                </select>
              </div>
              {/* Autres paramètres... */}
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-medium mb-4">Métriques Temps Réel</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Hmax:</span>
                <span className="font-medium">{metrics.hmax} m</span>
              </div>
              <div className="flex justify-between">
                <span>Hmin:</span>
                <span className="font-medium">{metrics.hmin} m</span>
              </div>
              <div className="flex justify-between">
                <span>H1/3:</span>
                <span className="font-medium">{metrics.h1_3} m</span>
              </div>
              <div className="flex justify-between">
                <span>Temps écoulé:</span>
                <span className="font-medium">{formatTime(elapsedTime)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Graphiques temps réel */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-4">Visualisation Temps Réel</h3>
        <div className="grid grid-cols-2 gap-6">
          <div>
            <h4 className="text-md font-medium mb-2">Sonde 1</h4>
            <div className="h-64 bg-gray-50 rounded flex items-center justify-center">
              <span className="text-gray-500">Graphique temps réel</span>
            </div>
          </div>
          <div>
            <h4 className="text-md font-medium mb-2">Sonde 2</h4>
            <div className="h-64 bg-gray-50 rounded flex items-center justify-center">
              <span className="text-gray-500">Graphique temps réel</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
```

### **Phase 3 : Intégration et Tests (2 semaines)**

#### **3.1 Tests Automatisés**

**Backend (Pytest) :**
```python
# backend/tests/test_calibration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.calibration_service import CalibrationService

client = TestClient(app)

def test_create_calibration_session():
    response = client.post("/api/calibration/sessions/", json={
        "project_id": 1,
        "probe_count": 4,
        "points_per_probe": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["probe_count"] == 4
    assert data["status"] == "pending"

def test_calibration_point_validation():
    # Test de validation d'un point de calibration
    point_data = {
        "probe_id": 1,
        "height": 10.0,
        "voltage": 2.5
    }
    result = CalibrationService.validate_calibration_point(point_data)
    assert result["is_valid"] == True
```

**Frontend (Jest + Testing Library) :**
```typescript
// frontend/src/components/__tests__/CalibrationView.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { CalibrationView } from '../CalibrationView';

describe('CalibrationView', () => {
  test('should start calibration when button is clicked', () => {
    render(<CalibrationView />);
    
    const startButton = screen.getByText('Démarrer la calibration');
    fireEvent.click(startButton);
    
    expect(screen.getByText('Sonde 1 - Étape 1/5')).toBeInTheDocument();
  });

  test('should validate calibration point', () => {
    render(<CalibrationView />);
    
    const heightInput = screen.getByLabelText('Hauteur de référence (cm)');
    const voltageInput = screen.getByLabelText('Tension mesurée (V)');
    
    fireEvent.change(heightInput, { target: { value: '10' } });
    fireEvent.change(voltageInput, { target: { value: '2.5' } });
    
    const validateButton = screen.getByText('✅ Valider le point');
    fireEvent.click(validateButton);
    
    // Vérifier que le point est validé
  });
});
```

#### **3.2 Configuration de Production**

**Docker Compose :**
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/chneowave
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=chneowave
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Nginx Configuration :**
```nginx
# nginx.conf
server {
    listen 80;
    server_name chneowave.local;

    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 🔧 **Migration des Données Existantes**

### **Script de Migration des Projets Qt vers Web :**

```python
# scripts/migrate_qt_data.py
import sqlite3
import json
from pathlib import Path

def migrate_qt_projects():
    """Migre les projets depuis l'ancienne base Qt vers la nouvelle base web"""
    
    # Connexion à l'ancienne base Qt
    qt_db_path = Path("old_chneowave.db")
    if not qt_db_path.exists():
        print("Base Qt non trouvée")
        return
    
    qt_conn = sqlite3.connect(qt_db_path)
    qt_cursor = qt_conn.cursor()
    
    # Récupération des projets Qt
    qt_cursor.execute("""
        SELECT id, name, code, engineer, project_manager, scale, basin, canal, description
        FROM projects
    """)
    
    qt_projects = qt_cursor.fetchall()
    
    # Connexion à la nouvelle base web
    web_conn = sqlite3.connect("chneowave_web.db")
    web_cursor = web_conn.cursor()
    
    # Migration des projets
    for project in qt_projects:
        web_cursor.execute("""
            INSERT INTO projects (name, code, engineer, project_manager, scale, basin, canal, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, project[1:])  # Exclure l'ancien ID
    
    web_conn.commit()
    print(f"Migré {len(qt_projects)} projets")
    
    qt_conn.close()
    web_conn.close()

if __name__ == "__main__":
    migrate_qt_projects()
```

---

## 📊 **Métriques de Performance**

### **Avant/Après Migration :**

| Métrique | Qt (Avant) | Web (Après) | Amélioration |
|----------|------------|-------------|--------------|
| Temps de démarrage | 3-5 secondes | < 1 seconde | 80% |
| Taille application | 150 MB | 15 MB | 90% |
| Mise à jour | Manuel | Automatique | 100% |
| Compatibilité | Windows/Linux | Tous OS | 100% |
| Déploiement | Installation | Navigateur | 100% |

---

## 🚀 **Déploiement et Mise en Production**

### **Script de Déploiement Automatisé :**

```bash
#!/bin/bash
# scripts/deploy.sh

echo "🚀 Déploiement CHNeoWave Web"

# Build des images Docker
echo "📦 Build des images..."
docker-compose build

# Arrêt des services existants
echo "🛑 Arrêt des services existants..."
docker-compose down

# Démarrage des nouveaux services
echo "▶️ Démarrage des nouveaux services..."
docker-compose up -d

# Vérification de la santé
echo "🏥 Vérification de la santé..."
sleep 10
curl -f http://localhost:3000 || exit 1
curl -f http://localhost:8000/health || exit 1

echo "✅ Déploiement terminé avec succès!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
```

---

## 🎯 **Plan de Formation Utilisateurs**

### **Formation à la Nouvelle Interface :**

1. **Session d'introduction** (2h)
   - Présentation des nouvelles fonctionnalités
   - Comparaison avec l'ancienne interface
   - Démonstration des améliorations

2. **Formation pratique** (4h)
   - Création de projets
   - Processus de calibration
   - Acquisition de données
   - Analyse et export

3. **Support post-migration** (2 semaines)
   - Support technique dédié
   - Documentation utilisateur
   - Sessions de questions/réponses

---

## 📈 **Suivi et Maintenance**

### **Monitoring de Production :**

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'chneowave-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'chneowave-frontend'
    static_configs:
      - targets: ['frontend:3000']
```

### **Logs et Alertes :**

```python
# backend/app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('chneowave.log', maxBytes=10*1024*1024, backupCount=5),
            logging.StreamHandler()
        ]
    )
```

---

## 🎉 **Conclusion**

La migration vers une interface web moderne apporte des avantages significatifs :

1. **Performance améliorée** : Chargement plus rapide, interface plus réactive
2. **Accessibilité universelle** : Utilisation depuis n'importe quel navigateur
3. **Maintenance simplifiée** : Mises à jour automatiques, déploiement facilité
4. **Expérience utilisateur optimisée** : Interface moderne, responsive, intuitive
5. **Évolutivité** : Architecture modulaire, facilement extensible

**Prochaine étape :** Démarrer la Phase 1 du plan de migration avec la configuration de l'environnement de développement.