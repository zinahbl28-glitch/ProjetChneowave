import React, { useEffect, useRef, useState } from 'react';
import {
  HomeIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  PlayIcon,
  ChartBarIcon,
  BeakerIcon,
  ArrowDownTrayIcon,
  AdjustmentsHorizontalIcon,
  ExclamationCircleIcon,
  CheckCircleIcon,
  XMarkIcon,
  ArrowUpTrayIcon
} from '@heroicons/react/24/outline';
import { NavLink, Routes, Route, Navigate } from 'react-router-dom';

// Styles: ensure theme-system overrides any conflicting base styles
import './index.css';
import './styles/theme-system.css';
import ThemeSelector from './components/ThemeSelector';
import ProjectManager from './components/ProjectManager';
import ExportManager from './components/ExportManager';
import MetadataEditor from './components/MetadataEditor';
import HistoryComponents from './components/HistoryComponents';

// =============================
// Signal Bus Bridge (stubbed)
// =============================
export type BufferStatus = {
  fillRatio: number;
  overruns: number;
  underruns: number;
  maxLatency: number;
};

export type BusError = { id: string; category: string; message: string };
export type SessionEvent = { id: string; message: string };

export const useSignalBus = () => {
  const [bufferStatus, setBufferStatus] = useState<BufferStatus>({
    fillRatio: 23,
    overruns: 0,
    underruns: 0,
    maxLatency: 1.2,
  });
  const [errors, setErrors] = useState<BusError[]>([]);
  const [sessionEvents, setSessionEvents] = useState<SessionEvent[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setBufferStatus(prev => {
        const drift = Math.max(0, Math.min(100, prev.fillRatio + (Math.random() - 0.5) * 5));
        const over = drift > 90 ? prev.overruns + 1 : prev.overruns;
        const under = drift < 5 ? prev.underruns + 1 : prev.underruns;
        const latency = Math.max(0.2, Math.min(25, prev.maxLatency + (Math.random() - 0.5) * 0.8));
        return { fillRatio: drift, overruns: over, underruns: under, maxLatency: latency };
      });
    }, 1000);

    const eventInterval = setInterval(() => {
      if (Math.random() < 0.1) {
        setSessionEvents(prev => [...prev.slice(-19), { id: `${Date.now()}`, message: 'Session mise à jour' }]);
      }
    }, 3000);

    return () => {
      clearInterval(interval);
      clearInterval(eventInterval);
    };
  }, []);

  const clearError = (errorId: string) => {
    setErrors(prev => prev.filter(e => e.id !== errorId));
  };

  return { bufferStatus, errors, sessionEvents, clearError, isConnected: true };
};

// =============================
// Phase 1 Components (Acquisition)
// =============================

interface BoardItem {
  id: string;
  name: string;
  type: string;
  status: 'ok' | 'error' | 'unknown';
}

const HardwarePanel: React.FC = () => {
  const [boards, setBoards] = useState<BoardItem[]>([
    { id: '0', name: 'MCC USB-1608FS', type: 'DAQ', status: 'ok' },
  ]);
  const [testing, setTesting] = useState(false);

  const testChannel = async (boardId: string) => {
    setTesting(true);
    await new Promise(res => setTimeout(res, 1200));
    setBoards(prev => prev.map(b => (b.id === boardId ? { ...b, status: Math.random() < 0.9 ? 'ok' : 'error' } : b)));
    setTesting(false);
  };

  return (
    <div className="chn-card p-4">
      <h3 className="text-lg font-semibold mb-4">Matériel Détecté</h3>
      <div className="space-y-2">
        {boards.map(board => (
          <div key={board.id} className="flex items-center justify-between p-3 border rounded">
            <div>
              <span className="font-medium">{board.name}</span>
              <span className="text-sm text-gray-600 ml-2">({board.type})</span>
            </div>
            <div className="flex items-center gap-3">
              <button
                className="chn-btn-secondary text-sm"
                onClick={() => testChannel(board.id)}
                disabled={testing}
                aria-busy={testing}
              >
                {testing ? 'Test...' : 'Test Canal'}
              </button>
              <div
                className={`w-3 h-3 rounded-full ${board.status === 'ok' ? 'bg-green-500' : board.status === 'error' ? 'bg-red-500' : 'bg-gray-400'}`}
                aria-label={`Statut: ${board.status}`}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

type Channel = {
  id: string;
  enabled: boolean;
  label: string;
  range: number;
  sensitivity: number;
  unit: string;
};

const defaultChannel = (n: number): Channel => ({
  id: `${Date.now()}_${n}`,
  enabled: true,
  label: `Canal ${n}`,
  range: 10,
  sensitivity: 1,
  unit: 'V',
});

const ChannelRow: React.FC<{
  channel: Channel;
  onUpdate: (ch: Channel) => void;
  onDelete: (id: string) => void;
}> = ({ channel, onUpdate, onDelete }) => {
  return (
    <tr className="border-b">
      <td className="p-2 align-middle">
        <input
          type="checkbox"
          checked={channel.enabled}
          onChange={e => onUpdate({ ...channel, enabled: e.target.checked })}
        />
      </td>
      <td className="p-2">
        <input className="chn-input w-full" value={channel.label} onChange={e => onUpdate({ ...channel, label: e.target.value })} />
      </td>
      <td className="p-2">
        <select className="chn-input w-full" value={channel.range} onChange={e => onUpdate({ ...channel, range: Number(e.target.value) })}>
          {[10, 5, 2, 1].map(r => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </td>
      <td className="p-2">
        <input type="number" step="0.01" className="chn-input w-full" value={channel.sensitivity} onChange={e => onUpdate({ ...channel, sensitivity: Number(e.target.value) })} />
      </td>
      <td className="p-2">
        <select className="chn-input w-full" value={channel.unit} onChange={e => onUpdate({ ...channel, unit: e.target.value })}>
          {['V', 'm', 'hPa', 'm/s²', '°C'].map(u => (
            <option key={u} value={u}>{u}</option>
          ))}
        </select>
      </td>
      <td className="p-2">
        <button className="chn-btn-secondary text-sm" onClick={() => onDelete(channel.id)}>Supprimer</button>
      </td>
    </tr>
  );
};

const ChannelEditor: React.FC = () => {
  const [channels, setChannels] = useState<Channel[]>([defaultChannel(1), defaultChannel(2), defaultChannel(3)]);

  const addChannel = () => setChannels(prev => [...prev, defaultChannel(prev.length + 1)]);
  const updateChannel = (ch: Channel) => setChannels(prev => prev.map(c => (c.id === ch.id ? ch : c)));
  const deleteChannel = (id: string) => setChannels(prev => prev.filter(c => c.id !== id));

  return (
    <div className="chn-card p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Configuration Canaux</h3>
        <button className="chn-btn-secondary" onClick={addChannel}>+ Ajouter Canal</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b">
              <th className="text-left p-2">Activé</th>
              <th className="text-left p-2">Label</th>
              <th className="text-left p-2">Range (V)</th>
              <th className="text-left p-2">Sensibilité</th>
              <th className="text-left p-2">Unité</th>
              <th className="text-left p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {channels.map(ch => (
              <ChannelRow key={ch.id} channel={ch} onUpdate={updateChannel} onDelete={deleteChannel} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const LiveAcquisition: React.FC = () => {
  const { bufferStatus } = useSignalBus();
  const [isAcquiring, setIsAcquiring] = useState(false);
  const [sampleRate] = useState(1000);
  const [duration, setDuration] = useState(0);
  const [activeChannels] = useState<number[]>([1, 2, 3]);

  useEffect(() => {
    let t: number | undefined;
    if (isAcquiring) {
      const start = Date.now();
      const tick = () => {
        setDuration(Math.floor((Date.now() - start) / 1000));
        t = window.setTimeout(tick, 1000);
      };
      tick();
    }
    return () => t && clearTimeout(t);
  }, [isAcquiring]);

  const { fillRatio, overruns, underruns, maxLatency } = bufferStatus;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="chn-card p-4">
        <h3 className="text-lg font-semibold mb-4">Signaux Temps Réel</h3>
        <div className="h-64 border rounded bg-gray-50 flex items-center justify-center">
          {isAcquiring ? (
            <div className="text-center">
              <div className="animate-pulse text-green-600 mb-2">● REC</div>
              <div className="text-sm text-gray-600">
                {sampleRate} Hz | {duration}s | {activeChannels.length} canaux
              </div>
            </div>
          ) : (
            <div className="text-gray-400">Graphique temps réel (prêt)</div>
          )}
        </div>
        <div className="mt-3 flex gap-2">
          <button className="chn-btn-primary" onClick={() => setIsAcquiring(true)}>Démarrer</button>
          <button className="chn-btn-secondary" onClick={() => setIsAcquiring(false)}>Arrêter</button>
        </div>
      </div>

      <div className="chn-card p-4">
        <h3 className="text-lg font-semibold mb-4">État Buffer</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span>Remplissage</span>
              <span className={fillRatio > 80 ? 'text-red-600 font-bold' : 'text-green-600'}>
                {fillRatio.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all duration-300 ${fillRatio > 80 ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`}
                style={{ width: `${fillRatio}%` }}
              />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="text-center p-2 bg-gray-50 rounded">
              <div className="text-xs text-gray-600">Overruns</div>
              <div className={`font-mono text-lg ${overruns > 0 ? 'text-red-600' : 'text-green-600'}`}>{overruns}</div>
            </div>
            <div className="text-center p-2 bg-gray-50 rounded">
              <div className="text-xs text-gray-600">Underruns</div>
              <div className={`font-mono text-lg ${underruns > 0 ? 'text-red-600' : 'text-green-600'}`}>{underruns}</div>
            </div>
            <div className="text-center p-2 bg-gray-50 rounded">
              <div className="text-xs text-gray-600">Latence (ms)</div>
              <div className="font-mono text-lg text-blue-600">{maxLatency.toFixed(1)}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const NotificationCenter: React.FC = () => {
  const { errors, sessionEvents, clearError } = useSignalBus();
  return (
    <div className="fixed top-4 right-4 space-y-2 z-50 max-w-sm">
      {errors.slice(-3).map(error => (
        <div key={error.id} className="chn-card bg-red-50 border-red-200 p-4 shadow-lg" role="alert">
          <div className="flex items-start gap-3">
            <ExclamationCircleIcon className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="font-medium text-red-900">{error.category}</p>
              <p className="text-sm text-red-700 mt-1 break-words">{error.message}</p>
              <p className="text-xs text-red-600 mt-2 font-mono">ID: {error.id}</p>
            </div>
            <button className="text-red-400 hover:text-red-600 flex-shrink-0" onClick={() => clearError(error.id)} aria-label="Fermer notification">
              <XMarkIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
      {sessionEvents.slice(-2).map(event => (
        <div key={event.id} className="chn-card bg-green-50 border-green-200 p-3 shadow-lg" role="status" aria-live="polite">
          <div className="flex items-center gap-2">
            <CheckCircleIcon className="w-4 h-4 text-green-600" />
            <span className="text-sm text-green-800">{event.message}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

// =============================
// Phase 2 Components (Analysis)
// =============================

type RecentFile = { path: string; name: string; size: string };

const FileImportPanel: React.FC = () => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [recentFiles, setRecentFiles] = useState<RecentFile[]>([
    { path: '/data/session_2025_01_01.h5', name: 'session_2025_01_01.h5', size: '24.3 MB' },
    { path: '/data/run_15.csv', name: 'run_15.csv', size: '8.7 MB' },
  ]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileDrop: React.DragEventHandler<HTMLDivElement> = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (!files?.length) return;
    const next: RecentFile[] = [];
    for (let i = 0; i < files.length; i++) {
      const f = files[i];
      next.push({ path: f.name, name: f.name, size: `${(f.size / (1024 * 1024)).toFixed(1)} MB` });
    }
    setRecentFiles(prev => [...next, ...prev].slice(0, 10));
  };
  const handleDragOver: React.DragEventHandler<HTMLDivElement> = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };
  const handleDragLeave: React.DragEventHandler<HTMLDivElement> = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };
  const handleFileSelect: React.ChangeEventHandler<HTMLInputElement> = (e) => {
    const files = e.target.files;
    if (!files?.length) return;
    const next: RecentFile[] = [];
    for (let i = 0; i < files.length; i++) {
      const f = files[i];
      next.push({ path: f.name, name: f.name, size: `${(f.size / (1024 * 1024)).toFixed(1)} MB` });
    }
    setRecentFiles(prev => [...next, ...prev].slice(0, 10));
    if (fileInputRef.current) fileInputRef.current.value = '';
  };
  const loadFile = (file: RecentFile) => {
    console.log('Load file', file);
  };

  return (
    <div className="chn-card p-4">
      <h3 className="text-lg font-semibold mb-4">Import de Données</h3>
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${isDragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
        onDrop={handleFileDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <ArrowUpTrayIcon className="w-8 h-8 text-gray-400 mx-auto mb-2" />
        <p className="text-sm text-gray-600 mb-2">Glissez vos fichiers ici ou cliquez pour parcourir</p>
        <p className="text-xs text-gray-500">Formats supportés: CSV, HDF5, JSON, TDMS</p>
        <input type="file" multiple accept=".csv,.h5,.hdf5,.json,.tdms" className="hidden" ref={fileInputRef} onChange={handleFileSelect} />
        <button className="chn-btn-secondary mt-3" onClick={() => fileInputRef.current?.click()}>Parcourir Fichiers</button>
      </div>
      <div className="mt-4">
        <h4 className="text-sm font-medium mb-2">Fichiers Récents</h4>
        <div className="space-y-1">
          {recentFiles.map(file => (
            <div key={file.path} className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
              <div className="flex items-center gap-2">
                <DocumentTextIcon className="w-4 h-4 text-gray-400" />
                <span className="text-sm">{file.name}</span>
                <span className="text-xs text-gray-500">({file.size})</span>
              </div>
              <button className="text-blue-600 hover:text-blue-800 text-sm" onClick={() => loadFile(file)}>Charger</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

type BenchResults = { speedup: number; time: number; memory: number; efficiency: number } | null;

const FFTEngineControl: React.FC = () => {
  const [useOptimized, setUseOptimized] = useState(true);
  const [benchmarking, setBenchmarking] = useState(false);
  const [benchmarkResults, setBenchmarkResults] = useState<BenchResults>(null);

  const runBenchmark = async () => {
    setBenchmarking(true);
    await new Promise(res => setTimeout(res, 1200));
    setBenchmarkResults({ speedup: 3.7, time: 12.4, memory: 48.2, efficiency: 86 });
    setBenchmarking(false);
  };

  return (
    <div className="chn-card p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Moteur FFT</h3>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm">Moteur:</span>
            <button
              className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${useOptimized ? 'bg-green-100 text-green-800 ring-2 ring-green-200' : 'bg-gray-100 text-gray-600'}`}
              onClick={() => setUseOptimized(!useOptimized)}
            >
              {useOptimized ? '⚡ pyFFTW (Optimisé)' : '📊 NumPy (Standard)'}
            </button>
          </div>
          <button className="chn-btn-secondary text-sm" onClick={runBenchmark} disabled={benchmarking}>
            {benchmarking ? 'Benchmark...' : 'Tester Performance'}
          </button>
        </div>
      </div>
      {benchmarkResults && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
            <div className="text-xs text-blue-600 uppercase tracking-wide">Gain</div>
            <div className="text-2xl font-bold text-blue-800">{benchmarkResults.speedup.toFixed(1)}x</div>
          </div>
          <div className="text-center p-3 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
            <div className="text-xs text-green-600 uppercase tracking-wide">Temps (ms)</div>
            <div className="text-2xl font-bold text-green-800">{benchmarkResults.time.toFixed(1)}</div>
          </div>
          <div className="text-center p-3 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
            <div className="text-xs text-purple-600 uppercase tracking-wide">Mémoire (MB)</div>
            <div className="text-2xl font-bold text-purple-800">{benchmarkResults.memory.toFixed(1)}</div>
          </div>
          <div className="text-center p-3 bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg">
            <div className="text-xs text-amber-600 uppercase tracking-wide">Efficacité</div>
            <div className="text-2xl font-bold text-amber-800">{benchmarkResults.efficiency.toFixed(0)}%</div>
          </div>
        </div>
      )}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Taille FFT</label>
          <select className="chn-input text-sm" defaultValue="1024">
            <option value="256">256</option>
            <option value="512">512</option>
            <option value="1024">1024</option>
            <option value="2048">2048</option>
            <option value="4096">4096</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Fenêtre</label>
          <select className="chn-input text-sm" defaultValue="hann">
            <option value="hann">Hann</option>
            <option value="hamming">Hamming</option>
            <option value="blackman">Blackman</option>
            <option value="bartlett">Bartlett</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Overlap (%)</label>
          <input type="number" className="chn-input text-sm" defaultValue={50} min={0} max={90} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Detrend</label>
          <select className="chn-input text-sm" defaultValue="linear">
            <option value="linear">Linéaire</option>
            <option value="constant">Constante</option>
            <option value="none">Aucun</option>
          </select>
        </div>
      </div>
    </div>
  );
};

type Probe = { id: number; position: number; depth: number; label: string };

type GodaFrequencyResult = {
  frequency: number;
  k: number;
  wavelength: number;
  ai: number;
  ar: number;
  kr: number;
};

type GodaResults = {
  ai_mean: number;
  ar_mean: number;
  reflection_coefficient: number;
  dominant_wavelength: number;
  frequency_results: GodaFrequencyResult[];
} | null;

const GodaGeometryEditor: React.FC = () => {
  const [probes, setProbes] = useState<Probe[]>([
    { id: 1, position: 0, depth: 2.5, label: 'Sonde 1' },
    { id: 2, position: 10, depth: 2.5, label: 'Sonde 2' },
    { id: 3, position: 20, depth: 2.5, label: 'Sonde 3' },
  ]);
  const [godaResults, setGodaResults] = useState<GodaResults>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const updateProbe = (id: number, key: keyof Probe, value: any) => {
    setProbes(prev => prev.map(p => (p.id === id ? { ...p, [key]: value } : p)));
  };
  const deleteProbe = (id: number) => {
    setProbes(prev => prev.length > 2 ? prev.filter(p => p.id !== id) : prev);
  };

  const runGodaAnalysis = async () => {
    setIsAnalyzing(true);
    await new Promise(res => setTimeout(res, 1500));
    const freq = Array.from({ length: 16 }, (_, i) => 0.1 + i * 0.12);
    const fr: GodaFrequencyResult[] = freq.map(f => ({
      frequency: f,
      k: 2 * Math.PI * f / 1.5,
      wavelength: (2 * Math.PI) / Math.max(0.001, (2 * Math.PI * f / 1.5)),
      ai: Math.abs(Math.sin(f)) * 0.5 + 0.1,
      ar: Math.abs(Math.cos(f)) * 0.3 + 0.05,
      kr: Math.abs(Math.cos(f)) * 0.6
    }));
    setGodaResults({
      ai_mean: fr.reduce((a, b) => a + b.ai, 0) / fr.length,
      ar_mean: fr.reduce((a, b) => a + b.ar, 0) / fr.length,
      reflection_coefficient: fr.reduce((a, b) => a + b.kr, 0) / fr.length,
      dominant_wavelength: fr.reduce((a, b) => a + b.wavelength, 0) / fr.length,
      frequency_results: fr
    });
    setIsAnalyzing(false);
  };

  const maxPos = Math.max(20, ...probes.map(p => p.position));

  return (
    <div className="space-y-6">
      <div className="chn-card p-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Géométrie des Sondes</h3>
          <div className="flex gap-2">
            <button
              className="chn-btn-secondary"
              onClick={() => setProbes([...probes, { id: Date.now(), position: Math.max(...probes.map(p => p.position)) + 10, depth: 2.5, label: `Sonde ${probes.length + 1}` }])}
            >
              + Ajouter Sonde
            </button>
            <button className="chn-btn-primary" onClick={runGodaAnalysis} disabled={isAnalyzing || probes.length < 2}>
              {isAnalyzing ? 'Analyse...' : '⚡ Analyser Goda'}
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium mb-3">Configuration Sondes</h4>
            <div className="space-y-2">
              {probes.map((probe) => (
                <div key={probe.id} className="flex items-center gap-3 p-3 border rounded-lg">
                  <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  <input className="chn-input flex-1" value={probe.label} onChange={(e) => updateProbe(probe.id, 'label', e.target.value)} placeholder="Label sonde" />
                  <div className="flex gap-2">
                    <div>
                      <label className="text-xs text-gray-500">Position (m)</label>
                      <input type="number" className="chn-input w-20 text-sm" value={probe.position} onChange={(e) => updateProbe(probe.id, 'position', parseFloat(e.target.value))} step="0.1" />
                    </div>
                    <div>
                      <label className="text-xs text-gray-500">Profondeur (m)</label>
                      <input type="number" className="chn-input w-20 text-sm" value={probe.depth} onChange={(e) => updateProbe(probe.id, 'depth', parseFloat(e.target.value))} step="0.1" />
                    </div>
                    <button className="text-red-500 hover:text-red-700 mt-4" onClick={() => deleteProbe(probe.id)} disabled={probes.length <= 2}>
                      <XMarkIcon className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3">Visualisation Géométrie</h4>
            <div className="border rounded-lg bg-gray-50 p-4 h-64">
              <svg width="100%" height="100%" viewBox="0 0 300 200">
                <line x1="0" y1="150" x2="300" y2="150" stroke="#8B4513" strokeWidth="2" />
                <text x="10" y="145" fontSize="10" fill="#8B4513">Fond marin</text>
                <line x1="0" y1="50" x2="300" y2="50" stroke="#4A90E2" strokeWidth="2" strokeDasharray="5,5" />
                <text x="10" y="45" fontSize="10" fill="#4A90E2">Surface libre</text>
                {probes.map((probe) => {
                  const x = 50 + (probe.position / maxPos) * 200;
                  const y = 50 + probe.depth * 20;
                  return (
                    <g key={probe.id}>
                      <circle cx={x} cy={y} r="4" fill="#E53E3E" stroke="#FFF" strokeWidth="1" />
                      <text x={x + 8} y={y + 3} fontSize="8" fill="#333">{probe.label}</text>
                      <line x1={x} y1={50} x2={x} y2={y} stroke="#E53E3E" strokeWidth="1" strokeDasharray="2,2" />
                    </g>
                  );
                })}
              </svg>
            </div>
          </div>
        </div>
      </div>
      {godaResults && (
        <div className="chn-card p-4">
          <h3 className="text-lg font-semibold mb-4">Résultats Analyse Goda</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-xs text-blue-600 uppercase">Ai Moyen</div>
              <div className="text-xl font-bold text-blue-800">{godaResults.ai_mean.toFixed(3)}</div>
            </div>
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="text-xs text-green-600 uppercase">Ar Moyen</div>
              <div className="text-xl font-bold text-green-800">{godaResults.ar_mean.toFixed(3)}</div>
            </div>
            <div className="text-center p-3 bg-purple-50 rounded-lg">
              <div className="text-xs text-purple-600 uppercase">Coeff. Réflexion</div>
              <div className="text-xl font-bold text-purple-800">{godaResults.reflection_coefficient.toFixed(3)}</div>
            </div>
            <div className="text-center p-3 bg-amber-50 rounded-lg">
              <div className="text-xs text-amber-600 uppercase">λ Dominant (m)</div>
              <div className="text-xl font-bold text-amber-800">{godaResults.dominant_wavelength.toFixed(1)}</div>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Fréquence (Hz)</th>
                  <th className="text-left p-2">k (rad/m)</th>
                  <th className="text-left p-2">λ (m)</th>
                  <th className="text-left p-2">Ai</th>
                  <th className="text-left p-2">Ar</th>
                  <th className="text-left p-2">Kr</th>
                </tr>
              </thead>
              <tbody>
                {godaResults.frequency_results.map((result, index) => (
                  <tr key={index} className="border-b">
                    <td className="p-2 font-mono">{result.frequency.toFixed(3)}</td>
                    <td className="p-2 font-mono">{result.k.toFixed(4)}</td>
                    <td className="p-2 font-mono">{result.wavelength.toFixed(2)}</td>
                    <td className="p-2 font-mono">{result.ai.toFixed(4)}</td>
                    <td className="p-2 font-mono">{result.ar.toFixed(4)}</td>
                    <td className="p-2 font-mono">{result.kr.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

const SpectralAnalysisDashboard: React.FC = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="chn-card p-4">
        <h3 className="text-lg font-semibold mb-4">Densité Spectrale de Puissance</h3>
        <div className="h-64 border rounded bg-gray-50 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <ChartBarIcon className="w-8 h-8 mx-auto mb-2" />
            <p className="text-sm">Graphique PSD (prêt pour chart lib)</p>
          </div>
        </div>
        <div className="mt-4 flex gap-4 text-sm">
          <label className="flex items-center gap-2">
            <input type="radio" name="psd-scale" value="linear" defaultChecked />
            <span>Échelle Linéaire</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" name="psd-scale" value="log" />
            <span>Échelle Log</span>
          </label>
        </div>
      </div>
      <div className="chn-card p-4">
        <h3 className="text-lg font-semibold mb-4">Spectrogramme</h3>
        <div className="h-64 border rounded bg-gray-50 flex itemscenter justify-center">
          <div className="text-center text-gray-500">
            <BeakerIcon className="w-8 h-8 mx-auto mb-2" />
            <p className="text-sm">Spectrogramme temps-fréquence</p>
          </div>
        </div>
      </div>
      <div className="chn-card p-4 lg:col-span-2">
        <h3 className="text-lg font-semibold mb-4">Détection de Pics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Seuil Minimum</label>
            <input type="number" className="chn-input" step="0.001" placeholder="0.01" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Distance Minimale</label>
            <input type="number" className="chn-input" step={1} placeholder="10" />
          </div>
          <div className="flex items-end">
            <button className="chn-btn-secondary w-full">Détecter Pics</button>
          </div>
        </div>
      </div>
    </div>
  );
};

// =============================
// App Layout & Routing
// =============================

const navItems: Array<{ id: string; label: string; icon: React.FC<React.SVGProps<SVGSVGElement>>; to: string }> = [
  { id: 'dashboard', label: 'Tableau de Bord', icon: HomeIcon, to: '/dashboard' },
  { id: 'project', label: 'Projet', icon: DocumentTextIcon, to: '/project' },
  { id: 'calibration', label: 'Calibration', icon: Cog6ToothIcon, to: '/calibration' },
  { id: 'acquisition', label: 'Acquisition', icon: PlayIcon, to: '/acquisition' },
  { id: 'analysis', label: 'Analyse', icon: ChartBarIcon, to: '/analysis' },
  { id: 'advanced', label: 'Analyse Avancée', icon: BeakerIcon, to: '/advanced' },
  { id: 'export', label: 'Export', icon: ArrowDownTrayIcon, to: '/export' },
  { id: 'settings', label: 'Paramètres', icon: AdjustmentsHorizontalIcon, to: '/settings' },
];

function App() {
  const projectName = 'Projet Houle Atlantique 2024';

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 bg-white text-black px-3 py-2 rounded">Aller au contenu principal</a>

      <NotificationCenter />

      {/* Top App Bar */}
      <header className="themed-nav h-16">
        <div className="golden-container h-full">
          <div className="flex items-center justify-between h-full">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-sm">CHN</span>
              </div>
              <div>
                <div className="text-body font-semibold text-[var(--text-primary)]">CHNeoWave</div>
                <div className="text-meta truncate max-w-xs text-[var(--text-muted)]">{projectName}</div>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-small hidden sm:inline text-[var(--text-secondary)]">Système actif</span>
              </div>
              <div className="text-meta font-mono text-[var(--text-muted)]">
                {new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
              </div>
              <ThemeSelector />
            </div>
          </div>
        </div>
      </header>

      {/* Main with Side Nav */}
      <div className="golden-container pt-4">
        <div className="grid gap-5" style={{ gridTemplateColumns: '220px 1fr' }}>
          {/* Side Navigation */}
          <aside className="chn-card p-3">
            <nav role="navigation" aria-label="Navigation principale" className="flex flex-col gap-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.id}
                    to={item.to}
                    className={({ isActive }) => `themed-nav-item w-full px-3 py-2 rounded-lg flex items-center gap-2 transition-all ${isActive ? 'active' : ''}`}
                    title={item.label}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-medium">{item.label}</span>
                  </NavLink>
                );
              })}
            </nav>
          </aside>

          {/* Content Area */}
          <main id="main-content">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<><PageHeader page="dashboard" /><div className="space-y-6"><DashboardPage /></div></>} />
              <Route path="/projects" element={<><PageHeader page="projects" /><div className="space-y-6"><ProjectManager /></div></>} />
        <Route path="/metadata" element={<><PageHeader page="metadata" /><div className="space-y-6"><MetadataEditor /></div></>} />
        <Route path="/history" element={<><PageHeader page="history" /><div className="space-y-6"><HistoryComponents /></div></>} />
              <Route path="/calibration" element={<><PageHeader page="calibration" /><div className="space-y-6"><CalibrationPage /></div></>} />
              <Route path="/acquisition" element={<><PageHeader page="acquisition" /><div className="space-y-6"><AcquisitionPage /></div></>} />
              <Route path="/analysis" element={<><PageHeader page="analysis" /><div className="space-y-6"><AnalysisPage /></div></>} />
              <Route path="/advanced" element={<><PageHeader page="advanced" /><div className="space-y-6"><AdvancedPage /></div></>} />
              <Route path="/export" element={<><PageHeader page="export" /><div className="space-y-6"><ExportManager /></div></>} />
              <Route path="/settings" element={<><PageHeader page="settings" /><div className="space-y-6"><SettingsPage /></div></>} />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  );
}

function PageHeader({ page }: { page: string }) {
  const titles: Record<string, { title: string; subtitle: string }> = {
    dashboard: { title: 'Tableau de Bord', subtitle: "Vue d'ensemble du système d'acquisition" },
    project: { title: 'Projet', subtitle: 'Gestion des projets et métadonnées' },
    calibration: { title: 'Calibration des Sondes', subtitle: 'Étalonnage et vérification' },
    acquisition: { title: 'Acquisition de Données', subtitle: 'Mesure temps réel des élévations de surface' },
    analysis: { title: 'Analyse Statistique', subtitle: 'Statistiques descriptives et qualité' },
    advanced: { title: 'Analyse Avancée', subtitle: 'Spectres, cohérence, non-linéaire' },
    export: { title: 'Centre d’Export', subtitle: 'Formats scientifiques et rapports' },
    settings: { title: 'Paramètres', subtitle: 'Configuration du système' },
  };
  const { title, subtitle } = titles[page];
  return (
    <div className="mb-4">
      <h1 className="text-title text-[var(--text-primary)]">{title}</h1>
      <p className="text-small text-[var(--text-tertiary)]">{subtitle}</p>
    </div>
  );
}

function DashboardCard({ title, value, unit, accent }: { title: string; value: string; unit?: string; accent?: string }) {
  return (
    <div className="chn-card p-4">
      <div className="text-small text-[var(--text-muted)]">{title}</div>
      <div className="flex items-baseline gap-2 mt-1">
        <div className={`text-2xl font-mono font-bold ${accent ? '' : 'text-[var(--text-primary)]'}`} style={accent ? { color: accent } : undefined}>{value}</div>
        {unit && <div className="text-small text-[var(--text-tertiary)]">{unit}</div>}
      </div>
    </div>
  );
}

function DashboardPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <DashboardCard title="Canaux Actifs" value="8" />
      <DashboardCard title="Fréquence" value="1000" unit="Hz" />
      <DashboardCard title="Durée" value="02:45:33" />
      <DashboardCard title="CPU" value="34" unit="%" accent="#3b82f6" />
      <DashboardCard title="Mémoire" value="67" unit="%" accent="#06b6d4" />
      <DashboardCard title="Stockage" value="23" unit="%" accent="#10b981" />
    </div>
  );
}

function AcquisitionPage() {
  const { bufferStatus } = useSignalBus();
  const [isRunning, setIsRunning] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Acquisition de Données</h2>
        <div className="flex gap-3">
          <button className="chn-btn-primary" onClick={() => setIsRunning(true)}>Démarrer</button>
          <button className="chn-btn-secondary" onClick={() => setIsRunning(false)}>Pause</button>
          <button className="chn-btn-secondary" onClick={() => setIsRunning(false)}>Arrêter</button>
        </div>
      </div>

      <HardwarePanel />
      <ChannelEditor />
      <LiveAcquisition />
    </div>
  );
}

function CalibrationPage() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="chn-card p-4">
        <h3 className="text-heading">Configuration</h3>
        <div className="mt-2">
          <label className="text-small text-[var(--text-secondary)]">Nombre de sondes</label>
          <select className="chn-input w-full" defaultValue={8}>
            {[4,8,12,16].map(v => <option key={v} value={v}>{v}</option>)}
          </select>
        </div>
        <div className="mt-2">
          <label className="text-small text-[var(--text-secondary)]">Points de calibration</label>
          <select className="chn-input w-full" defaultValue={3}>
            {[3,5,7].map(v => <option key={v} value={v}>{v}</option>)}
          </select>
        </div>
        <div className="flex gap-2 mt-3">
          <button className="chn-btn-primary">Démarrer</button>
          <button className="chn-btn-secondary">Arrêter</button>
        </div>
      </div>
      <div className="chn-card p-4">
        <h3 className="text-heading">Sonde Active</h3>
        <div className="mt-3 grid grid-cols-4 gap-2">
          {Array.from({ length: 8 }, (_, i) => i + 1).map(id => (
            <button key={id} className="chn-btn-secondary px-2 py-2">#{id}</button>
          ))}
        </div>
      </div>
      <div className="chn-card p-4">
        <h3 className="text-heading">Résultats</h3>
        <div className="mt-2 h-40 rounded bg-[var(--bg-secondary)]" />
      </div>
    </div>
  );
}

function AnalysisPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Analyse Scientifique</h2>
        <div className="flex gap-2">
          <button className="chn-btn-secondary">Exporter CSV</button>
          <button className="chn-btn-secondary">Exporter JSON</button>
          <button className="chn-btn-primary">Exporter HDF5</button>
        </div>
      </div>
      <FileImportPanel />
      <FFTEngineControl />
      <GodaGeometryEditor />
      <SpectralAnalysisDashboard />
    </div>
  );
}

function AdvancedPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="chn-card p-4">
        <h3 className="text-heading">Analyse Spectrale</h3>
        <div className="mt-2 h-52 rounded bg-[var(--bg-secondary)]" />
      </div>
      <div className="chn-card p-4">
        <h3 className="text-heading">Cohérence Spatiale</h3>
        <div className="mt-2 h-52 rounded bg-[var(--bg-secondary)]" />
      </div>
    </div>
  );
}

function ExportPage() {
  const formats = [
    { name: 'HDF5', desc: 'Format scientifique' },
    { name: 'CSV', desc: 'Données tabulaires' },
    { name: 'MATLAB', desc: 'Fichiers .mat' },
    { name: 'PDF', desc: 'Rapports' },
  ];
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {formats.map((f) => (
        <div key={f.name} className="chn-card p-4">
          <div className="text-body font-medium text-[var(--text-primary)]">{f.name}</div>
          <div className="text-small text-[var(--text-tertiary)]">{f.desc}</div>
          <button className="chn-btn-primary mt-3 px-3 py-2">Exporter</button>
        </div>
      ))}
    </div>
  );
}

function SettingsPage() {
  return (
    <div className="chn-card p-4">
      <h3 className="text-heading">Préférences</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
        <div>
          <label className="text-small text-[var(--text-secondary)]">Thème</label>
          <select
            className="chn-input w-full"
            onChange={(e) => {
              const theme = e.target.value;
              document.documentElement.removeAttribute('data-theme');
              document.documentElement.setAttribute('data-theme', theme);
              localStorage.setItem('chneowave-theme', theme);
            }}
            defaultValue={localStorage.getItem('chneowave-theme') || 'light'}
          >
            <option value="light">Clair</option>
            <option value="dark">Sombre</option>
            <option value="beige">Beige</option>
          </select>
        </div>
        <div>
          <label className="text-small text-[var(--text-secondary)]">Unité hauteur</label>
          <select className="chn-input w-full" defaultValue={'m'}>
            <option value="m">m</option>
            <option value="cm">cm</option>
          </select>
        </div>
      </div>
    </div>
  );
}

function ProjectPage() {
  return <ProjectManager />;
}

export default App;
