import React, { useState, useEffect } from 'react';
import {
  CpuChipIcon,
  MemoryIcon,
  HardDriveIcon,
  SignalIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';

interface SystemMetrics {
  cpu: {
    usage: number;
    temperature?: number;
    frequency: number;
    cores: number;
  };
  memory: {
    total: number;
    used: number;
    available: number;
    swap: {
      total: number;
      used: number;
    };
  };
  disk: {
    total: number;
    used: number;
    free: number;
    readSpeed: number;
    writeSpeed: number;
  };
  network: {
    bytesSent: number;
    bytesReceived: number;
    packetsSent: number;
    packetsReceived: number;
  };
  processes: {
    total: number;
    threads: number;
    chneowaveThreads: number;
  };
  timestamp: string;
}

interface PerformanceAlert {
  id: string;
  type: 'warning' | 'error' | 'info';
  message: string;
  timestamp: string;
  metric: string;
  value: number;
  threshold: number;
}

const PerformanceWidget: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [alerts, setAlerts] = useState<PerformanceAlert[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  // Configuration des seuils d'alerte
  const thresholds = {
    cpu: { warning: 70, error: 90 },
    memory: { warning: 80, error: 95 },
    disk: { warning: 85, error: 95 },
    network: { warning: 80, error: 95 }
  };

  // Simulation des métriques (remplacé par l'API réelle)
  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        // TODO: Remplacer par l'appel API réel
        // const response = await fetch('http://localhost:8766/monitoring/metrics');
        // const data = await response.json();
        
        // Simulation des métriques
        const mockMetrics: SystemMetrics = {
          cpu: {
            usage: Math.random() * 100,
            temperature: 45 + Math.random() * 20,
            frequency: 2400 + Math.random() * 800,
            cores: 8
          },
          memory: {
            total: 16384,
            used: 8192 + Math.random() * 4096,
            available: 8192 - Math.random() * 4096,
            swap: {
              total: 8192,
              used: Math.random() * 2048
            }
          },
          disk: {
            total: 1000,
            used: 600 + Math.random() * 200,
            free: 400 - Math.random() * 200,
            readSpeed: Math.random() * 100,
            writeSpeed: Math.random() * 50
          },
          network: {
            bytesSent: Math.random() * 1000000,
            bytesReceived: Math.random() * 2000000,
            packetsSent: Math.random() * 10000,
            packetsReceived: Math.random() * 15000
          },
          processes: {
            total: 150 + Math.random() * 50,
            threads: 300 + Math.random() * 100,
            chneowaveThreads: 8 + Math.random() * 4
          },
          timestamp: new Date().toISOString()
        };

        setMetrics(mockMetrics);
        setLastUpdate(new Date());
        setIsConnected(true);

        // Vérifier les alertes
        checkAlerts(mockMetrics);

      } catch (error) {
        console.error('Erreur lors de la récupération des métriques:', error);
        setIsConnected(false);
      }
    };

    // Mise à jour toutes les 2 secondes
    const interval = setInterval(fetchMetrics, 2000);
    fetchMetrics(); // Première récupération

    return () => clearInterval(interval);
  }, []);

  const checkAlerts = (currentMetrics: SystemMetrics) => {
    const newAlerts: PerformanceAlert[] = [];
    const now = new Date().toISOString();

    // Vérification CPU
    if (currentMetrics.cpu.usage > thresholds.cpu.error) {
      newAlerts.push({
        id: `cpu-${Date.now()}`,
        type: 'error',
        message: `CPU usage critique: ${currentMetrics.cpu.usage.toFixed(1)}%`,
        timestamp: now,
        metric: 'cpu',
        value: currentMetrics.cpu.usage,
        threshold: thresholds.cpu.error
      });
    } else if (currentMetrics.cpu.usage > thresholds.cpu.warning) {
      newAlerts.push({
        id: `cpu-${Date.now()}`,
        type: 'warning',
        message: `CPU usage élevé: ${currentMetrics.cpu.usage.toFixed(1)}%`,
        timestamp: now,
        metric: 'cpu',
        value: currentMetrics.cpu.usage,
        threshold: thresholds.cpu.warning
      });
    }

    // Vérification mémoire
    const memoryUsage = (currentMetrics.memory.used / currentMetrics.memory.total) * 100;
    if (memoryUsage > thresholds.memory.error) {
      newAlerts.push({
        id: `memory-${Date.now()}`,
        type: 'error',
        message: `Mémoire critique: ${memoryUsage.toFixed(1)}%`,
        timestamp: now,
        metric: 'memory',
        value: memoryUsage,
        threshold: thresholds.memory.error
      });
    } else if (memoryUsage > thresholds.memory.warning) {
      newAlerts.push({
        id: `memory-${Date.now()}`,
        type: 'warning',
        message: `Mémoire élevée: ${memoryUsage.toFixed(1)}%`,
        timestamp: now,
        metric: 'memory',
        value: memoryUsage,
        threshold: thresholds.memory.warning
      });
    }

    // Vérification disque
    const diskUsage = (currentMetrics.disk.used / currentMetrics.disk.total) * 100;
    if (diskUsage > thresholds.disk.error) {
      newAlerts.push({
        id: `disk-${Date.now()}`,
        type: 'error',
        message: `Espace disque critique: ${diskUsage.toFixed(1)}%`,
        timestamp: now,
        metric: 'disk',
        value: diskUsage,
        threshold: thresholds.disk.error
      });
    } else if (diskUsage > thresholds.disk.warning) {
      newAlerts.push({
        id: `disk-${Date.now()}`,
        type: 'warning',
        message: `Espace disque faible: ${diskUsage.toFixed(1)}%`,
        timestamp: now,
        metric: 'disk',
        value: diskUsage,
        threshold: thresholds.disk.warning
      });
    }

    // Ajouter les nouvelles alertes
    if (newAlerts.length > 0) {
      setAlerts(prev => [...prev, ...newAlerts].slice(-10)); // Garder les 10 dernières
    }
  };

  const clearAlert = (alertId: string) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const getStatusColor = (value: number, warning: number, error: number) => {
    if (value >= error) return 'text-red-500';
    if (value >= warning) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getStatusIcon = (value: number, warning: number, error: number) => {
    if (value >= error) return <XCircleIcon className="w-5 h-5 text-red-500" />;
    if (value >= warning) return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
    return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
  };

  if (!metrics) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  const memoryUsage = (metrics.memory.used / metrics.memory.total) * 100;
  const diskUsage = (metrics.disk.used / metrics.disk.total) * 100;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      {/* En-tête avec statut de connexion */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Monitoring Système
        </h2>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className={`text-sm ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
            {isConnected ? 'Connecté' : 'Déconnecté'}
          </span>
          {lastUpdate && (
            <span className="text-xs text-gray-500">
              Dernière mise à jour: {lastUpdate.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {/* CPU */}
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <CpuChipIcon className="w-5 h-5 text-blue-600" />
              <span className="font-medium text-gray-900 dark:text-white">CPU</span>
            </div>
            {getStatusIcon(metrics.cpu.usage, thresholds.cpu.warning, thresholds.cpu.error)}
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {metrics.cpu.usage.toFixed(1)}%
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {metrics.cpu.cores} cœurs • {metrics.cpu.frequency.toFixed(0)} MHz
          </div>
          {metrics.cpu.temperature && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Temp: {metrics.cpu.temperature.toFixed(1)}°C
            </div>
          )}
        </div>

        {/* Mémoire */}
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <MemoryIcon className="w-5 h-5 text-green-600" />
              <span className="font-medium text-gray-900 dark:text-white">Mémoire</span>
            </div>
            {getStatusIcon(memoryUsage, thresholds.memory.warning, thresholds.memory.error)}
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {memoryUsage.toFixed(1)}%
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {(metrics.memory.used / 1024).toFixed(1)} GB / {(metrics.memory.total / 1024).toFixed(1)} GB
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Swap: {(metrics.memory.swap.used / 1024).toFixed(1)} GB
          </div>
        </div>

        {/* Disque */}
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <HardDriveIcon className="w-5 h-5 text-purple-600" />
              <span className="font-medium text-gray-900 dark:text-white">Disque</span>
            </div>
            {getStatusIcon(diskUsage, thresholds.disk.warning, thresholds.disk.error)}
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {diskUsage.toFixed(1)}%
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {(metrics.disk.used / 1024).toFixed(1)} GB / {(metrics.disk.total / 1024).toFixed(1)} GB
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            R: {(metrics.disk.readSpeed).toFixed(1)} MB/s • W: {(metrics.disk.writeSpeed).toFixed(1)} MB/s
          </div>
        </div>

        {/* Réseau */}
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <SignalIcon className="w-5 h-5 text-orange-600" />
              <span className="font-medium text-gray-900 dark:text-white">Réseau</span>
            </div>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            ↓ {(metrics.network.bytesReceived / 1024 / 1024).toFixed(2)} MB
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            ↑ {(metrics.network.bytesSent / 1024 / 1024).toFixed(2)} MB
          </div>
          <div className="text-xs text-gray-500">
            {metrics.network.packetsReceived.toLocaleString()} pkt
          </div>
        </div>
      </div>

      {/* Processus et Threads */}
      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
        <h3 className="font-medium text-gray-900 dark:text-white mb-3">Processus</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-lg font-semibold text-gray-900 dark:text-white">
              {metrics.processes.total}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Total</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-gray-900 dark:text-white">
              {metrics.processes.threads}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Threads</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-blue-600">
              {metrics.processes.chneowaveThreads}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">CHNeoWave</div>
          </div>
        </div>
      </div>

      {/* Alertes de performance */}
      {alerts.length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 dark:text-white mb-3">
            Alertes ({alerts.length})
          </h3>
          <div className="space-y-2">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`flex items-center justify-between p-3 rounded-lg ${
                  alert.type === 'error' ? 'bg-red-100 dark:bg-red-900' :
                  alert.type === 'warning' ? 'bg-yellow-100 dark:bg-yellow-900' :
                  'bg-blue-100 dark:bg-blue-900'
                }`}
              >
                <div className="flex items-center space-x-2">
                  {alert.type === 'error' && <XCircleIcon className="w-5 h-5 text-red-600" />}
                  {alert.type === 'warning' && <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600" />}
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {alert.message}
                  </span>
                </div>
                <button
                  onClick={() => clearAlert(alert.id)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Barres de progression détaillées */}
      <div className="space-y-4">
        {/* CPU Progress */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600 dark:text-gray-400">CPU Usage</span>
            <span className={getStatusColor(metrics.cpu.usage, thresholds.cpu.warning, thresholds.cpu.error)}>
              {metrics.cpu.usage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${
                metrics.cpu.usage >= thresholds.cpu.error ? 'bg-red-500' :
                metrics.cpu.usage >= thresholds.cpu.warning ? 'bg-yellow-500' :
                'bg-green-500'
              }`}
              style={{ width: `${Math.min(metrics.cpu.usage, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Memory Progress */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600 dark:text-gray-400">Mémoire</span>
            <span className={getStatusColor(memoryUsage, thresholds.memory.warning, thresholds.memory.error)}>
              {memoryUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${
                memoryUsage >= thresholds.memory.error ? 'bg-red-500' :
                memoryUsage >= thresholds.memory.warning ? 'bg-yellow-500' :
                'bg-green-500'
              }`}
              style={{ width: `${Math.min(memoryUsage, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Disk Progress */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600 dark:text-gray-400">Disque</span>
            <span className={getStatusColor(diskUsage, thresholds.disk.warning, thresholds.disk.error)}>
              {diskUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${
                diskUsage >= thresholds.disk.error ? 'bg-red-500' :
                diskUsage >= thresholds.disk.warning ? 'bg-yellow-500' :
                'bg-green-500'
              }`}
              style={{ width: `${Math.min(diskUsage, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceWidget;
