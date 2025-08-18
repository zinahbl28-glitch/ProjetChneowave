import React, { useState, useEffect } from 'react';
import {
  ClockIcon,
  DocumentTextIcon,
  ChartBarIcon,
  ArrowDownTrayIcon,
  EyeIcon,
  TrashIcon,
  CalendarIcon,
  UserIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';

interface HistoryItem {
  id: string;
  type: 'calibration' | 'analysis' | 'export';
  name: string;
  description: string;
  status: 'completed' | 'failed' | 'running';
  createdAt: string;
  completedAt?: string;
  user: string;
  size?: number;
  metadata: {
    project?: string;
    channels?: number;
    duration?: number;
    format?: string;
  };
}

const HistoryComponents: React.FC = () => {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [filterType, setFilterType] = useState<'all' | 'calibration' | 'analysis' | 'export'>('all');
  const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'failed' | 'running'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null);

  // Données simulées pour le développement
  useEffect(() => {
    const mockHistory: HistoryItem[] = [
      {
        id: '1',
        type: 'calibration',
        name: 'Calibration_Capteurs_Pression_2025_01',
        description: 'Calibration des capteurs de pression pour mesure de houle',
        status: 'completed',
        createdAt: '2025-08-15T10:00:00Z',
        completedAt: '2025-08-15T10:30:00Z',
        user: 'Dr. Martin',
        metadata: {
          project: 'Test_Houle_2025_01',
          channels: 4,
          duration: 1800
        }
      },
      {
        id: '2',
        type: 'analysis',
        name: 'Analyse_FFT_Houle_2025_01',
        description: 'Analyse spectrale FFT des données de houle',
        status: 'completed',
        createdAt: '2025-08-15T11:00:00Z',
        completedAt: '2025-08-15T11:15:00Z',
        user: 'Dr. Martin',
        size: 512000,
        metadata: {
          project: 'Test_Houle_2025_01',
          channels: 8,
          duration: 3600
        }
      },
      {
        id: '3',
        type: 'export',
        name: 'Export_HDF5_Houle_2025_01',
        description: 'Export des données de houle en format HDF5',
        status: 'completed',
        createdAt: '2025-08-15T12:00:00Z',
        completedAt: '2025-08-15T12:05:00Z',
        user: 'Dr. Martin',
        size: 2048000,
        metadata: {
          project: 'Test_Houle_2025_01',
          format: 'HDF5'
        }
      },
      {
        id: '4',
        type: 'calibration',
        name: 'Calibration_Accéléromètres_2025_01',
        description: 'Calibration des accéléromètres pour mesure de mouvement',
        status: 'failed',
        createdAt: '2025-08-15T14:00:00Z',
        user: 'Dr. Martin',
        metadata: {
          project: 'Essais_Accéléromètres',
          channels: 6,
          duration: 900
        }
      },
      {
        id: '5',
        type: 'analysis',
        name: 'Analyse_Goda_Validation_2025_01',
        description: 'Analyse Goda des paramètres de houle',
        status: 'running',
        createdAt: '2025-08-15T15:00:00Z',
        user: 'Dr. Martin',
        metadata: {
          project: 'Validation_Système',
          channels: 8,
          duration: 5400
        }
      },
      {
        id: '6',
        type: 'export',
        name: 'Export_TDMS_Pression_2025_01',
        description: 'Export des données de pression en format TDMS',
        status: 'completed',
        createdAt: '2025-08-15T16:00:00Z',
        completedAt: '2025-08-15T16:02:00Z',
        user: 'Dr. Martin',
        size: 1024000,
        metadata: {
          project: 'Validation_Capteurs_Pression',
          format: 'TDMS'
        }
      }
    ];

    setHistoryItems(mockHistory);
  }, []);

  const filteredItems = historyItems.filter(item => {
    const matchesType = filterType === 'all' || item.type === filterType;
    const matchesStatus = filterStatus === 'all' || item.status === filterStatus;
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesType && matchesStatus && matchesSearch;
  });

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'calibration': return <CheckCircleIcon className="w-5 h-5 text-blue-600" />;
      case 'analysis': return <ChartBarIcon className="w-5 h-5 text-green-600" />;
      case 'export': return <ArrowDownTrayIcon className="w-5 h-5 text-purple-600" />;
      default: return <DocumentTextIcon className="w-5 h-5 text-gray-600" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'calibration': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'analysis': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'export': return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'failed': return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'running': return <ClockIcon className="w-5 h-5 text-blue-500 animate-pulse" />;
      default: return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'failed': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'running': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed': return 'Terminé';
      case 'failed': return 'Échoué';
      case 'running': return 'En cours';
      default: return 'Inconnu';
    }
  };

  const getTypeText = (type: string) => {
    switch (type) {
      case 'calibration': return 'Calibration';
      case 'analysis': return 'Analyse';
      case 'export': return 'Export';
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

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  const openItemDetails = (item: HistoryItem) => {
    setSelectedItem(item);
  };

  const deleteHistoryItem = (itemId: string) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet élément de l\'historique ?')) {
      setHistoryItems(prev => prev.filter(item => item.id !== itemId));
      if (selectedItem?.id === itemId) {
        setSelectedItem(null);
      }
    }
  };

  const getStats = () => {
    const total = historyItems.length;
    const completed = historyItems.filter(item => item.status === 'completed').length;
    const failed = historyItems.filter(item => item.status === 'failed').length;
    const running = historyItems.filter(item => item.status === 'running').length;

    return { total, completed, failed, running };
  };

  const stats = getStats();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Historique des Opérations
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                Consultez l'historique des calibrations, analyses et exports
              </p>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
                <DocumentTextIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 dark:bg-green-900">
                <CheckCircleIcon className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Terminés</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.completed}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-red-100 dark:bg-red-900">
                <XCircleIcon className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Échoués</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.failed}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
                <ClockIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">En cours</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.running}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Rechercher dans l'historique..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-2 pl-10 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
                <DocumentTextIcon className="w-5 h-5 text-gray-400 absolute left-3 top-2.5" />
              </div>
            </div>
            
            <div className="flex gap-4">
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value as any)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="all">Tous les types</option>
                <option value="calibration">Calibrations</option>
                <option value="analysis">Analyses</option>
                <option value="export">Exports</option>
              </select>

              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value as any)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="all">Tous les statuts</option>
                <option value="completed">Terminés</option>
                <option value="failed">Échoués</option>
                <option value="running">En cours</option>
              </select>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column - History List */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Historique ({filteredItems.length} éléments)
                </h3>
              </div>

              <div className="p-6">
                <div className="space-y-4">
                  {filteredItems.map((item) => (
                    <div
                      key={item.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md ${
                        selectedItem?.id === item.id
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                      }`}
                      onClick={() => openItemDetails(item)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            {getTypeIcon(item.type)}
                            <div className="flex-1">
                              <h3 className="font-semibold text-gray-900 dark:text-white">
                                {item.name}
                              </h3>
                              <div className="flex items-center gap-2 mt-1">
                                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTypeColor(item.type)}`}>
                                  {getTypeText(item.type)}
                                </span>
                                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(item.status)}`}>
                                  {getStatusText(item.status)}
                                </span>
                              </div>
                            </div>
                          </div>
                          
                          <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                            {item.description}
                          </p>

                          <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-3">
                            {item.metadata.channels && (
                              <span className="flex items-center gap-1">
                                <span>{item.metadata.channels} canaux</span>
                              </span>
                            )}
                            {item.metadata.duration && (
                              <span className="flex items-center gap-1">
                                <span>{formatDuration(item.metadata.duration)}</span>
                              </span>
                            )}
                            {item.size && (
                              <span className="flex items-center gap-1">
                                <span>{formatFileSize(item.size)}</span>
                              </span>
                            )}
                          </div>

                          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                            <span className="flex items-center gap-1">
                              <UserIcon className="w-4 h-4" />
                              {item.user}
                            </span>
                            <span className="flex items-center gap-1">
                              <CalendarIcon className="w-4 h-4" />
                              {new Date(item.createdAt).toLocaleString()}
                            </span>
                            {item.completedAt && (
                              <span className="flex items-center gap-1">
                                <span>Terminé: {new Date(item.completedAt).toLocaleString()}</span>
                              </span>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          {getStatusIcon(item.status)}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteHistoryItem(item.id);
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

                {filteredItems.length === 0 && (
                  <div className="text-center py-12">
                    <DocumentTextIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      {searchTerm || filterType !== 'all' || filterStatus !== 'all'
                        ? 'Aucun élément ne correspond à vos critères'
                        : 'Aucun élément dans l\'historique'
                      }
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Item Details */}
          <div className="lg:col-span-1">
            {selectedItem ? (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Détails
                  </h3>
                  <button
                    onClick={() => setSelectedItem(null)}
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
                      {selectedItem.name}
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Type
                    </label>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTypeColor(selectedItem.type)}`}>
                      {getTypeText(selectedItem.type)}
                    </span>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Statut
                    </label>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(selectedItem.status)}`}>
                      {getStatusText(selectedItem.status)}
                    </span>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {selectedItem.description}
                    </p>
                  </div>

                  {selectedItem.metadata.project && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Projet
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedItem.metadata.project}
                      </p>
                    </div>
                  )}

                  <div className="grid grid-cols-2 gap-4">
                    {selectedItem.metadata.channels && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Canaux
                        </label>
                        <p className="text-gray-900 dark:text-white text-sm">
                          {selectedItem.metadata.channels}
                        </p>
                      </div>
                    )}
                    {selectedItem.metadata.duration && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Durée
                        </label>
                        <p className="text-gray-900 dark:text-white text-sm">
                          {formatDuration(selectedItem.metadata.duration)}
                        </p>
                      </div>
                    )}
                  </div>

                  {selectedItem.size && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Taille
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {formatFileSize(selectedItem.size)}
                      </p>
                    </div>
                  )}

                  <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div className="flex gap-2">
                      <button className="btn btn-secondary flex-1 flex items-center justify-center gap-2">
                        <EyeIcon className="w-4 h-4" />
                        Voir
                      </button>
                      {selectedItem.size && (
                        <button className="btn btn-primary flex-1 flex items-center justify-center gap-2">
                          <ArrowDownTrayIcon className="w-4 h-4" />
                          Télécharger
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 text-center">
                <DocumentTextIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400">
                  Sélectionnez un élément pour voir ses détails
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistoryComponents;
