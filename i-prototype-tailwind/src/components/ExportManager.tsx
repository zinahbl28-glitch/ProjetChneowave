import React, { useState, useEffect } from 'react';
import {
  ArrowDownTrayIcon,
  DocumentIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  PlayIcon,
  PauseIcon,
  StopIcon,
  TrashIcon,
  EyeIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline';

interface ExportJob {
  id: string;
  name: string;
  type: 'hdf5' | 'tdms' | 'csv';
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  size: number;
  createdAt: string;
  startedAt?: string;
  completedAt?: string;
  sourceData: string[];
  metadata: {
    project?: string;
    channels: number;
    duration: number;
    samplingRate: number;
    description?: string;
  };
  outputPath?: string;
  errorMessage?: string;
}

interface ExportConfig {
  format: 'hdf5' | 'tdms' | 'csv';
  compression: 'none' | 'gzip' | 'lz4';
  includeMetadata: boolean;
  includeCalibration: boolean;
  splitFiles: boolean;
  maxFileSize: number;
  channels: number[];
  timeRange: {
    start: string;
    end: string;
  };
}

const ExportManager: React.FC = () => {
  const [exportJobs, setExportJobs] = useState<ExportJob[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [selectedJob, setSelectedJob] = useState<ExportJob | null>(null);
  const [filterStatus, setFilterStatus] = useState<'all' | 'pending' | 'running' | 'completed' | 'failed'>('all');

  // Données simulées pour le développement
  useEffect(() => {
    const mockJobs: ExportJob[] = [
      {
        id: '1',
        name: 'Export_Houle_2025_01_HDF5',
        type: 'hdf5',
        status: 'completed',
        progress: 100,
        size: 2048000,
        createdAt: '2025-08-15T10:00:00Z',
        startedAt: '2025-08-15T10:01:00Z',
        completedAt: '2025-08-15T10:05:00Z',
        sourceData: ['acquisition_001.hdf5', 'calibration_config.json'],
        metadata: {
          project: 'Test_Houle_2025_01',
          channels: 8,
          duration: 3600,
          samplingRate: 500,
          description: 'Export complet des données de houle'
        },
        outputPath: '/exports/houle_2025_01.hdf5'
      },
      {
        id: '2',
        name: 'Export_Pression_TDMS',
        type: 'tdms',
        status: 'running',
        progress: 65,
        size: 0,
        createdAt: '2025-08-15T15:30:00Z',
        startedAt: '2025-08-15T15:31:00Z',
        sourceData: ['pression_data.tdms'],
        metadata: {
          project: 'Validation_Capteurs_Pression',
          channels: 4,
          duration: 7200,
          samplingRate: 1000,
          description: 'Export des données de pression'
        }
      },
      {
        id: '3',
        name: 'Export_Accel_CSV',
        type: 'csv',
        status: 'pending',
        progress: 0,
        size: 0,
        createdAt: '2025-08-15T16:00:00Z',
        sourceData: ['accel_data.hdf5'],
        metadata: {
          project: 'Essais_Accéléromètres',
          channels: 6,
          duration: 1800,
          samplingRate: 200,
          description: 'Export CSV des accéléromètres'
        }
      },
      {
        id: '4',
        name: 'Export_Validation_HDF5',
        type: 'hdf5',
        status: 'failed',
        progress: 45,
        size: 0,
        createdAt: '2025-08-15T14:00:00Z',
        startedAt: '2025-08-15T14:01:00Z',
        sourceData: ['validation_data.hdf5'],
        metadata: {
          project: 'Validation_Système',
          channels: 8,
          duration: 5400,
          samplingRate: 500,
          description: 'Export de validation'
        },
        errorMessage: 'Espace disque insuffisant'
      }
    ];

    setExportJobs(mockJobs);
  }, []);

  const [exportConfig, setExportConfig] = useState<ExportConfig>({
    format: 'hdf5',
    compression: 'gzip',
    includeMetadata: true,
    includeCalibration: true,
    splitFiles: false,
    maxFileSize: 1000,
    channels: [1, 2, 3, 4, 5, 6, 7, 8],
    timeRange: {
      start: new Date(Date.now() - 3600000).toISOString().slice(0, 16),
      end: new Date().toISOString().slice(0, 16)
    }
  });

  const filteredJobs = exportJobs.filter(job => 
    filterStatus === 'all' || job.status === filterStatus
  );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <ClockIcon className="w-5 h-5 text-gray-500" />;
      case 'running': return <PlayIcon className="w-5 h-5 text-blue-500 animate-pulse" />;
      case 'completed': return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'failed': return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'cancelled': return <StopIcon className="w-5 h-5 text-gray-500" />;
      default: return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
      case 'running': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'failed': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'cancelled': return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending': return 'En attente';
      case 'running': return 'En cours';
      case 'completed': return 'Terminé';
      case 'failed': return 'Échoué';
      case 'cancelled': return 'Annulé';
      default: return 'Inconnu';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleStartExport = () => {
    const newJob: ExportJob = {
      id: Date.now().toString(),
      name: `Export_${exportConfig.format.toUpperCase()}_${new Date().toISOString().slice(0, 10)}`,
      type: exportConfig.format,
      status: 'pending',
      progress: 0,
      size: 0,
      createdAt: new Date().toISOString(),
      sourceData: ['acquisition_data.hdf5', 'calibration.json'],
      metadata: {
        project: 'Projet_Actuel',
        channels: exportConfig.channels.length,
        duration: 3600,
        samplingRate: 500,
        description: 'Export automatique'
      }
    };

    setExportJobs(prev => [newJob, ...prev]);
    setIsCreating(false);

    // Simuler le démarrage de l'export
    setTimeout(() => {
      setExportJobs(prev => prev.map(job => 
        job.id === newJob.id ? { ...job, status: 'running', startedAt: new Date().toISOString() } : job
      ));

      // Simuler la progression
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
          progress = 100;
          clearInterval(interval);
          setExportJobs(prev => prev.map(job => 
            job.id === newJob.id ? { 
              ...job, 
              status: 'completed', 
              progress: 100, 
              completedAt: new Date().toISOString(),
              size: Math.floor(Math.random() * 2000000) + 500000
            } : job
          ));
        } else {
          setExportJobs(prev => prev.map(job => 
            job.id === newJob.id ? { ...job, progress } : job
          ));
        }
      }, 1000);
    }, 1000);
  };

  const handleCancelExport = (jobId: string) => {
    setExportJobs(prev => prev.map(job => 
      job.id === jobId ? { ...job, status: 'cancelled' } : job
    ));
  };

  const handleDeleteJob = (jobId: string) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet export ?')) {
      setExportJobs(prev => prev.filter(job => job.id !== jobId));
      if (selectedJob?.id === jobId) {
        setSelectedJob(null);
      }
    }
  };

  const openJobDetails = (job: ExportJob) => {
    setSelectedJob(job);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Gestionnaire d'Exports
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                Exportez vos données en HDF5, TDMS ou CSV
              </p>
            </div>
            <button
              onClick={() => setIsCreating(true)}
              className="btn btn-primary flex items-center gap-2"
            >
              <ArrowDownTrayIcon className="w-5 h-5" />
              Nouvel Export
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column - Export Jobs */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg">
              
              {/* Filters */}
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-4">
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value as any)}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                  >
                    <option value="all">Tous les statuts</option>
                    <option value="pending">En attente</option>
                    <option value="running">En cours</option>
                    <option value="completed">Terminés</option>
                    <option value="failed">Échoués</option>
                  </select>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {filteredJobs.length} export(s)
                  </span>
                </div>
              </div>

              {/* Jobs List */}
              <div className="p-6">
                <div className="space-y-4">
                  {filteredJobs.map((job) => (
                    <div
                      key={job.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md ${
                        selectedJob?.id === job.id
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                      }`}
                      onClick={() => openJobDetails(job)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <DocumentIcon className="w-5 h-5 text-blue-600" />
                            <h3 className="font-semibold text-gray-900 dark:text-white">
                              {job.name}
                            </h3>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(job.status)}`}>
                              {getStatusText(job.status)}
                            </span>
                          </div>
                          
                          <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-3">
                            <span className="flex items-center gap-1">
                              <span className="capitalize">{job.type}</span>
                            </span>
                            <span className="flex items-center gap-1">
                              <span>{job.metadata.channels} canaux</span>
                            </span>
                            <span className="flex items-center gap-1">
                              <span>{job.metadata.duration}s</span>
                            </span>
                            {job.size > 0 && (
                              <span className="flex items-center gap-1">
                                <span>{formatFileSize(job.size)}</span>
                              </span>
                            )}
                          </div>

                          {/* Progress Bar */}
                          {job.status === 'running' && (
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-3">
                              <div
                                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${job.progress}%` }}
                              ></div>
                            </div>
                          )}

                          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                            <span>Créé: {new Date(job.createdAt).toLocaleString()}</span>
                            {job.startedAt && (
                              <span>Démarré: {new Date(job.startedAt).toLocaleString()}</span>
                            )}
                            {job.completedAt && (
                              <span>Terminé: {new Date(job.completedAt).toLocaleString()}</span>
                            )}
                          </div>

                          {job.errorMessage && (
                            <div className="mt-2 p-2 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-sm rounded">
                              Erreur: {job.errorMessage}
                            </div>
                          )}
                        </div>

                        <div className="flex items-center gap-2">
                          {getStatusIcon(job.status)}
                          {job.status === 'running' && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleCancelExport(job.id);
                              }}
                              className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                            >
                              <StopIcon className="w-4 h-4" />
                            </button>
                          )}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteJob(job.id);
                            }}
                            className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                          >
                            <TrashIcon className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {filteredJobs.length === 0 && (
                  <div className="text-center py-12">
                    <DocumentIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      {filterStatus !== 'all' 
                        ? 'Aucun export ne correspond à ce statut'
                        : 'Aucun export créé pour le moment'
                      }
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Job Details & Export Config */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Job Details */}
            {selectedJob && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Détails de l'Export
                  </h3>
                  <button
                    onClick={() => setSelectedJob(null)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    ×
                  </button>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Nom
                    </label>
                    <p className="text-gray-900 dark:text-white font-medium">
                      {selectedJob.name}
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Format
                    </label>
                    <p className="text-gray-900 dark:text-white text-sm capitalize">
                      {selectedJob.type}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Canaux
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedJob.metadata.channels}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Durée
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedJob.metadata.duration}s
                      </p>
                    </div>
                  </div>

                  {selectedJob.metadata.description && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Description
                      </label>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        {selectedJob.metadata.description}
                      </p>
                    </div>
                  )}

                  <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">Données Sources</h4>
                    <div className="space-y-2">
                      {selectedJob.sourceData.map((source, index) => (
                        <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-lg">
                          <DocumentIcon className="w-4 h-4 text-gray-500" />
                          <span className="text-sm text-gray-900 dark:text-white">{source}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {selectedJob.outputPath && (
                    <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                      <h4 className="font-medium text-gray-900 dark:text-white mb-3">Fichier de Sortie</h4>
                      <div className="flex items-center gap-2 p-2 bg-green-50 dark:bg-green-900 rounded-lg">
                        <CheckCircleIcon className="w-4 h-4 text-green-600" />
                        <span className="text-sm text-gray-900 dark:text-white">{selectedJob.outputPath}</span>
                      </div>
                    </div>
                  )}

                  <div className="flex gap-2 pt-4">
                    <button className="btn btn-secondary flex-1 flex items-center justify-center gap-2">
                      <EyeIcon className="w-4 h-4" />
                      Voir
                    </button>
                    <button className="btn btn-primary flex-1 flex items-center justify-center gap-2">
                      <ArrowDownTrayIcon className="w-4 h-4" />
                      Télécharger
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Export Configuration */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Cog6ToothIcon className="w-5 h-5 text-gray-600" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Configuration Export
                </h3>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Format
                  </label>
                  <select
                    value={exportConfig.format}
                    onChange={(e) => setExportConfig({ ...exportConfig, format: e.target.value as any })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                  >
                    <option value="hdf5">HDF5 (Recommandé)</option>
                    <option value="tdms">TDMS (National Instruments)</option>
                    <option value="csv">CSV (Excel compatible)</option>
                  </select>
                </div>

                {exportConfig.format === 'hdf5' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Compression
                    </label>
                    <select
                      value={exportConfig.compression}
                      onChange={(e) => setExportConfig({ ...exportConfig, compression: e.target.value as any })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    >
                      <option value="none">Aucune</option>
                      <option value="gzip">GZIP (Équilibré)</option>
                      <option value="lz4">LZ4 (Rapide)</option>
                    </select>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={exportConfig.includeMetadata}
                        onChange={(e) => setExportConfig({ ...exportConfig, includeMetadata: e.target.checked })}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">Métadonnées</span>
                    </label>
                  </div>
                  <div>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={exportConfig.includeCalibration}
                        onChange={(e) => setExportConfig({ ...exportConfig, includeCalibration: e.target.checked })}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">Calibration</span>
                    </label>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Plage Temporelle
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="datetime-local"
                      value={exportConfig.timeRange.start}
                      onChange={(e) => setExportConfig({ 
                        ...exportConfig, 
                        timeRange: { ...exportConfig.timeRange, start: e.target.value }
                      })}
                      className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
                    />
                    <input
                      type="datetime-local"
                      value={exportConfig.timeRange.end}
                      onChange={(e) => setExportConfig({ 
                        ...exportConfig, 
                        timeRange: { ...exportConfig.timeRange, end: e.target.value }
                      })}
                      className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
                    />
                  </div>
                </div>

                <button
                  onClick={handleStartExport}
                  className="w-full btn btn-primary flex items-center justify-center gap-2"
                >
                  <ArrowDownTrayIcon className="w-5 h-5" />
                  Démarrer l'Export
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Create Export Modal */}
        {isCreating && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Nouvel Export
                  </h2>
                  <button
                    onClick={() => setIsCreating(false)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    ×
                  </button>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Nom de l'export
                    </label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Ex: Export_Houle_2025_01"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Format de sortie
                    </label>
                    <select
                      value={exportConfig.format}
                      onChange={(e) => setExportConfig({ ...exportConfig, format: e.target.value as any })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    >
                      <option value="hdf5">HDF5 (Recommandé)</option>
                      <option value="tdms">TDMS (National Instruments)</option>
                      <option value="csv">CSV (Excel compatible)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Données à exporter
                    </label>
                    <div className="space-y-2">
                      {['acquisition_data.hdf5', 'calibration.json', 'metadata.json'].map((file, index) => (
                        <label key={index} className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            defaultChecked={index < 2}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700 dark:text-gray-300">{file}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setIsCreating(false)}
                      className="btn btn-secondary flex-1"
                    >
                      Annuler
                    </button>
                    <button
                      type="button"
                      onClick={handleStartExport}
                      className="btn btn-primary flex-1"
                    >
                      Créer l'Export
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExportManager;
