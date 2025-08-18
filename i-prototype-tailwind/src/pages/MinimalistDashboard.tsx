import React, { useState, useEffect } from 'react';
import {
  PlayIcon,
  PauseIcon,
  CpuChipIcon,
  SignalIcon,
  ClockIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import PerformanceWidget from '../components/PerformanceWidget';

interface DashboardMetrics {
  acquisition: {
    status: 'active' | 'inactive' | 'error';
    duration: string;
    sampleRate: number;
    channels: number;
  };
  system: {
    cpu: number;
    memory: number;
    storage: number;
  };
  sensors: Array<{
    id: string;
    name: string;
    value: number;
    unit: string;
    status: 'ok' | 'warning' | 'error';
  }>;
}

const MinimalistDashboard: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    acquisition: {
      status: 'active',
      duration: '02:45:33',
      sampleRate: 1000,
      channels: 8
    },
    system: {
      cpu: 34,
      memory: 67,
      storage: 23
    },
    sensors: [
      { id: '1', name: 'Houle #1', value: 2.34, unit: 'm', status: 'ok' },
      { id: '2', name: 'Houle #2', value: 1.87, unit: 'm', status: 'ok' },
      { id: '3', name: 'Pression', value: 1013.4, unit: 'hPa', status: 'ok' },
      { id: '4', name: 'Accél. X', value: 0.15, unit: 'm/s²', status: 'warning' },
      { id: '5', name: 'Accél. Y', value: -0.08, unit: 'm/s²', status: 'ok' },
      { id: '6', name: 'Accél. Z', value: 9.81, unit: 'm/s²', status: 'ok' },
      { id: '7', name: 'Temp. Eau', value: 18.7, unit: '°C', status: 'ok' },
      { id: '8', name: 'Force', value: 0, unit: 'N', status: 'error' }
    ]
  });

  // Mise à jour temps réel
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      
      // Simulation légère des métriques
      setMetrics(prev => ({
        ...prev,
        system: {
          ...prev.system,
          cpu: Math.max(20, Math.min(80, prev.system.cpu + (Math.random() - 0.5) * 5))
        }
      }));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ok': case 'active':
        return <CheckCircleIcon className="w-5 h-5 text-green-600" />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5 text-orange-600" />;
      case 'error': case 'inactive':
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-600" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  const activeChannels = metrics.sensors.filter(s => s.status === 'ok').length;
  const warningChannels = metrics.sensors.filter(s => s.status === 'warning').length;
  const errorChannels = metrics.sensors.filter(s => s.status === 'error').length;

  return (
    <div className="min-h-screen" style={{backgroundColor: 'var(--bg-primary)'}}>
      <div className="golden-container py-8">
        
        {/* Header */}
        <header className="flex items-center justify-between mb-8 themed-fade-in">
          <div>
            <h1 className="text-title" style={{color: 'var(--text-primary)'}}>Tableau de Bord</h1>
            <p className="text-small mt-1" style={{color: 'var(--text-tertiary)'}}>
              Vue d'ensemble du système d'acquisition
            </p>
          </div>
          
          <div className="text-right">
            <div className="text-heading font-mono" style={{color: 'var(--accent-primary)'}}>
              {currentTime.toLocaleTimeString('fr-FR')}
            </div>
            <div className="text-small" style={{color: 'var(--text-muted)'}}>
              {currentTime.toLocaleDateString('fr-FR', { 
                weekday: 'long',
                day: 'numeric',
                month: 'long'
              })}
            </div>
          </div>
        </header>

        {/* Main Grid (Golden Ratio) */}
        <div className="golden-grid golden-grid-2 mb-8">
          
          {/* Left Column - Primary Metrics */}
          <div className="space-y-6 slide-up">
            
            {/* Acquisition Status */}
            <div className="themed-card golden-card">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    metrics.acquisition.status === 'active' ? 'bg-green-100' : 'bg-gray-100'
                  }`}>
                    {metrics.acquisition.status === 'active' ? (
                      <PlayIcon className="w-5 h-5 text-green-600" />
                    ) : (
                      <PauseIcon className="w-5 h-5 text-gray-600" />
                    )}
                  </div>
                  <div>
                    <h3 className="text-heading text-gray-900">Acquisition</h3>
                    <p className="text-small text-gray-500">Collecte de données</p>
                  </div>
                </div>
                <span className={`status ${
                  metrics.acquisition.status === 'active' ? 'status-success' : 'status-neutral'
                }`}>
                  {metrics.acquisition.status === 'active' ? 'Active' : 'Inactive'}
                </span>
              </div>

              <div className="golden-grid golden-grid-2">
                <div className="metric">
                  <div className="metric-value">{metrics.acquisition.channels}</div>
                  <div className="metric-label">Canaux</div>
                </div>
                <div className="metric">
                  <div className="metric-value">
                    {metrics.acquisition.sampleRate}
                    <span className="metric-unit">Hz</span>
                  </div>
                  <div className="metric-label">Fréquence</div>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="flex items-center justify-between">
                  <span className="text-small text-gray-600">Durée d'acquisition</span>
                  <span className="text-body font-mono text-gray-900">
                    {metrics.acquisition.duration}
                  </span>
                </div>
              </div>
            </div>

            {/* System Performance */}
            <div className="themed-card golden-card">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <CpuChipIcon className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-heading text-gray-900">Système</h3>
                  <p className="text-small text-gray-500">Performance en temps réel</p>
                </div>
              </div>

              <div className="space-y-4">
                {[
                  { label: 'Processeur', value: metrics.system.cpu, unit: '%' },
                  { label: 'Mémoire', value: metrics.system.memory, unit: '%' },
                  { label: 'Stockage', value: metrics.system.storage, unit: '%' }
                ].map((item, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-small text-gray-600">{item.label}</span>
                      <span className="text-small font-mono text-gray-900">
                        {Math.round(item.value)}{item.unit}
                      </span>
                    </div>
                    <div className="progress">
                      <div 
                        className="progress-bar"
                        style={{ width: `${item.value}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Sensors */}
          <div className="slide-up" style={{ animationDelay: '150ms' }}>
            <div className="themed-card golden-card h-full">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <SignalIcon className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <h3 className="text-heading text-gray-900">Capteurs</h3>
                    <p className="text-small text-gray-500">État du réseau</p>
                  </div>
                </div>
              </div>

              {/* Summary */}
              <div className="golden-grid golden-grid-3 mb-6">
                <div className="metric">
                  <div className="metric-value text-green-600">{activeChannels}</div>
                  <div className="metric-label">Actifs</div>
                </div>
                <div className="metric">
                  <div className="metric-value text-orange-600">{warningChannels}</div>
                  <div className="metric-label">Alertes</div>
                </div>
                <div className="metric">
                  <div className="metric-value text-red-600">{errorChannels}</div>
                  <div className="metric-label">Erreurs</div>
                </div>
              </div>

              {/* Sensor List */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {metrics.sensors.map((sensor, index) => (
                  <div key={sensor.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(sensor.status)}
                      <div>
                        <div className="text-body text-gray-900">{sensor.name}</div>
                        <div className="text-meta">Canal {index + 1}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-body font-mono text-gray-900">
                        {sensor.value.toFixed(sensor.unit === 'm/s²' ? 2 : 1)}
                        <span className="metric-unit ml-1">{sensor.unit}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Performance Widget */}
        <div className="slide-up" style={{ animationDelay: '300ms' }}>
          <PerformanceWidget />
        </div>

        {/* Quick Actions */}
        <div className="themed-card golden-card slide-up" style={{ animationDelay: '400ms' }}>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-heading text-gray-900 mb-1">Actions Rapides</h3>
              <p className="text-small text-gray-500">Contrôles du système</p>
            </div>
            
            <div className="flex items-center gap-3">
              <button className="btn btn-secondary">
                <Cog6ToothIcon className="w-4 h-4" />
                Calibration
              </button>
              <button className="btn btn-secondary">
                <ChartBarIcon className="w-4 h-4" />
                Analyse
              </button>
              <button className="btn btn-primary">
                {metrics.acquisition.status === 'active' ? (
                  <>
                    <PauseIcon className="w-4 h-4" />
                    Arrêter
                  </>
                ) : (
                  <>
                    <PlayIcon className="w-4 h-4" />
                    Démarrer
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MinimalistDashboard;
