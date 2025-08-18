import React, { useState, useEffect } from 'react';
import {
  FolderIcon,
  PlusIcon,
  DocumentIcon,
  ClockIcon,
  UserIcon,
  Cog6ToothIcon,
  TrashIcon,
  PencilIcon,
  EyeIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';

interface Project {
  id: string;
  name: string;
  description: string;
  createdAt: string;
  updatedAt: string;
  status: 'active' | 'archived' | 'completed';
  owner: string;
  metadata: {
    location?: string;
    waterDepth?: number;
    duration?: number;
    channels?: number;
    samplingRate?: number;
    tags?: string[];
  };
  files: {
    id: string;
    name: string;
    type: 'hdf5' | 'tdms' | 'csv' | 'config';
    size: number;
    createdAt: string;
  }[];
}

interface ProjectFormData {
  name: string;
  description: string;
  location: string;
  waterDepth: number;
  duration: number;
  channels: number;
  samplingRate: number;
  tags: string;
}

const ProjectManager: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'active' | 'archived' | 'completed'>('all');

  // Données simulées pour le développement
  useEffect(() => {
    const mockProjects: Project[] = [
      {
        id: '1',
        name: 'Test_Houle_2025_01',
        description: 'Test de validation des capteurs de houle en laboratoire',
        createdAt: '2025-08-15T10:00:00Z',
        updatedAt: '2025-08-15T15:30:00Z',
        status: 'active',
        owner: 'Dr. Martin',
        metadata: {
          location: 'Laboratoire Maritime',
          waterDepth: 2.5,
          duration: 3600,
          channels: 8,
          samplingRate: 500,
          tags: ['validation', 'houle', 'laboratoire']
        },
        files: [
          { id: '1', name: 'acquisition_001.hdf5', type: 'hdf5', size: 1024000, createdAt: '2025-08-15T10:05:00Z' },
          { id: '2', name: 'calibration_config.json', type: 'config', size: 2048, createdAt: '2025-08-15T09:55:00Z' }
        ]
      },
      {
        id: '2',
        name: 'Validation_Capteurs_Pression',
        description: 'Validation des capteurs de pression pour mesure de houle',
        createdAt: '2025-08-14T14:00:00Z',
        updatedAt: '2025-08-14T18:00:00Z',
        status: 'completed',
        owner: 'Dr. Martin',
        metadata: {
          location: 'Bassin d\'Essais',
          waterDepth: 3.0,
          duration: 7200,
          channels: 4,
          samplingRate: 1000,
          tags: ['pression', 'validation', 'bassin']
        },
        files: [
          { id: '3', name: 'pression_data.tdms', type: 'tdms', size: 512000, createdAt: '2025-08-14T14:10:00Z' },
          { id: '4', name: 'analyse_fft.csv', type: 'csv', size: 15360, createdAt: '2025-08-14T17:45:00Z' }
        ]
      },
      {
        id: '3',
        name: 'Essais_Accéléromètres',
        description: 'Tests des accéléromètres pour mesure de mouvement',
        createdAt: '2025-08-13T09:00:00Z',
        updatedAt: '2025-08-13T16:00:00Z',
        status: 'archived',
        owner: 'Dr. Martin',
        metadata: {
          location: 'Plateforme Mobile',
          waterDepth: 1.8,
          duration: 1800,
          channels: 6,
          samplingRate: 200,
          tags: ['accéléromètre', 'mouvement', 'plateforme']
        },
        files: [
          { id: '5', name: 'accel_data.hdf5', type: 'hdf5', size: 256000, createdAt: '2025-08-13T09:05:00Z' }
        ]
      }
    ];

    setProjects(mockProjects);
  }, []);

  const [formData, setFormData] = useState<ProjectFormData>({
    name: '',
    description: '',
    location: '',
    waterDepth: 2.0,
    duration: 3600,
    channels: 8,
    samplingRate: 500,
    tags: ''
  });

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || project.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const handleCreateProject = () => {
    const newProject: Project = {
      id: Date.now().toString(),
      name: formData.name,
      description: formData.description,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      status: 'active',
      owner: 'Dr. Martin',
      metadata: {
        location: formData.location,
        waterDepth: formData.waterDepth,
        duration: formData.duration,
        channels: formData.channels,
        samplingRate: formData.samplingRate,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      },
      files: []
    };

    setProjects(prev => [newProject, ...prev]);
    setIsCreating(false);
    setFormData({
      name: '',
      description: '',
      location: '',
      waterDepth: 2.0,
      duration: 3600,
      channels: 8,
      samplingRate: 500,
      tags: ''
    });
  };

  const handleEditProject = () => {
    if (!selectedProject) return;

    const updatedProject: Project = {
      ...selectedProject,
      name: formData.name,
      description: formData.description,
      updatedAt: new Date().toISOString(),
      metadata: {
        location: formData.location,
        waterDepth: formData.waterDepth,
        duration: formData.duration,
        channels: formData.channels,
        samplingRate: formData.samplingRate,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      }
    };

    setProjects(prev => prev.map(p => p.id === selectedProject.id ? updatedProject : p));
    setSelectedProject(updatedProject);
    setIsEditing(false);
  };

  const handleDeleteProject = (projectId: string) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce projet ?')) {
      setProjects(prev => prev.filter(p => p.id !== projectId));
      if (selectedProject?.id === projectId) {
        setSelectedProject(null);
      }
    }
  };

  const openProject = (project: Project) => {
    setSelectedProject(project);
    setFormData({
      name: project.name,
      description: project.description,
      location: project.metadata.location || '',
      waterDepth: project.metadata.waterDepth || 2.0,
      duration: project.metadata.duration || 3600,
      channels: project.metadata.channels || 8,
      samplingRate: project.metadata.samplingRate || 500,
      tags: project.metadata.tags?.join(', ') || ''
    });
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'completed': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'archived': return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Gestionnaire de Projets
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                Gérez vos projets d'acquisition et d'analyse maritime
              </p>
            </div>
            <button
              onClick={() => setIsCreating(true)}
              className="btn btn-primary flex items-center gap-2"
            >
              <PlusIcon className="w-5 h-5" />
              Nouveau Projet
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column - Project List */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg">
              
              {/* Search and Filters */}
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1">
                    <input
                      type="text"
                      placeholder="Rechercher un projet..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value as any)}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                  >
                    <option value="all">Tous les statuts</option>
                    <option value="active">Actifs</option>
                    <option value="completed">Terminés</option>
                    <option value="archived">Archivés</option>
                  </select>
                </div>
              </div>

              {/* Project List */}
              <div className="p-6">
                <div className="space-y-4">
                  {filteredProjects.map((project) => (
                    <div
                      key={project.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md ${
                        selectedProject?.id === project.id
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                      }`}
                      onClick={() => openProject(project)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <FolderIcon className="w-5 h-5 text-blue-600" />
                            <h3 className="font-semibold text-gray-900 dark:text-white">
                              {project.name}
                            </h3>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(project.status)}`}>
                              {project.status === 'active' ? 'Actif' : 
                               project.status === 'completed' ? 'Terminé' : 'Archivé'}
                            </span>
                          </div>
                          <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                            {project.description}
                          </p>
                          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                            <span className="flex items-center gap-1">
                              <UserIcon className="w-4 h-4" />
                              {project.owner}
                            </span>
                            <span className="flex items-center gap-1">
                              <ClockIcon className="w-4 h-4" />
                              {new Date(project.createdAt).toLocaleDateString()}
                            </span>
                            <span className="flex items-center gap-1">
                              <DocumentIcon className="w-4 h-4" />
                              {project.files.length} fichiers
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              openProject(project);
                              setIsEditing(true);
                            }}
                            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                          >
                            <PencilIcon className="w-4 h-4" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteProject(project.id);
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

                {filteredProjects.length === 0 && (
                  <div className="text-center py-12">
                    <FolderIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      {searchTerm || filterStatus !== 'all' 
                        ? 'Aucun projet ne correspond à vos critères'
                        : 'Aucun projet créé pour le moment'
                      }
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Project Details */}
          <div className="lg:col-span-1">
            {selectedProject ? (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Détails du Projet
                  </h3>
                  <button
                    onClick={() => setSelectedProject(null)}
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
                      {selectedProject.name}
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {selectedProject.description}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Localisation
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedProject.metadata.location || 'Non spécifié'}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Profondeur d'eau
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedProject.metadata.waterDepth ? `${selectedProject.metadata.waterDepth}m` : 'Non spécifié'}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Canaux
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedProject.metadata.channels || 'Non spécifié'}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Fréquence (Hz)
                      </label>
                      <p className="text-gray-900 dark:text-white text-sm">
                        {selectedProject.metadata.samplingRate || 'Non spécifié'}
                      </p>
                    </div>
                  </div>

                  {selectedProject.metadata.tags && selectedProject.metadata.tags.length > 0 && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Tags
                      </label>
                      <div className="flex flex-wrap gap-2">
                        {selectedProject.metadata.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">Fichiers</h4>
                    <div className="space-y-2">
                      {selectedProject.files.map((file) => (
                        <div key={file.id} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded-lg">
                          <div className="flex items-center gap-2">
                            <DocumentIcon className="w-4 h-4 text-gray-500" />
                            <span className="text-sm text-gray-900 dark:text-white">{file.name}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {formatFileSize(file.size)}
                            </span>
                            <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                              <ArrowDownTrayIcon className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex gap-2 pt-4">
                    <button
                      onClick={() => setIsEditing(true)}
                      className="btn btn-secondary flex-1 flex items-center justify-center gap-2"
                    >
                      <PencilIcon className="w-4 h-4" />
                      Modifier
                    </button>
                    <button className="btn btn-primary flex-1 flex items-center justify-center gap-2">
                      <EyeIcon className="w-4 h-4" />
                      Ouvrir
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 text-center">
                <FolderIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400">
                  Sélectionnez un projet pour voir ses détails
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Create/Edit Project Modal */}
        {(isCreating || isEditing) && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {isCreating ? 'Nouveau Projet' : 'Modifier le Projet'}
                  </h2>
                  <button
                    onClick={() => {
                      setIsCreating(false);
                      setIsEditing(false);
                    }}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    ×
                  </button>
                </div>

                <form className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Nom du projet *
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Ex: Test_Houle_2025_01"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Description du projet..."
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Localisation
                      </label>
                      <input
                        type="text"
                        value={formData.location}
                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        placeholder="Ex: Laboratoire Maritime"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Profondeur d'eau (m)
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        value={formData.waterDepth}
                        onChange={(e) => setFormData({ ...formData, waterDepth: parseFloat(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        placeholder="2.5"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Durée (s)
                      </label>
                      <input
                        type="number"
                        value={formData.duration}
                        onChange={(e) => setFormData({ ...formData, duration: parseInt(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        placeholder="3600"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Canaux
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="8"
                        value={formData.channels}
                        onChange={(e) => setFormData({ ...formData, channels: parseInt(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        placeholder="8"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Fréquence (Hz)
                      </label>
                      <input
                        type="number"
                        min="100"
                        max="1000"
                        value={formData.samplingRate}
                        onChange={(e) => setFormData({ ...formData, samplingRate: parseInt(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        placeholder="500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Tags (séparés par des virgules)
                    </label>
                    <input
                      type="text"
                      value={formData.tags}
                      onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Ex: validation, houle, laboratoire"
                    />
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="button"
                      onClick={() => {
                        setIsCreating(false);
                        setIsEditing(false);
                      }}
                      className="btn btn-secondary flex-1"
                    >
                      Annuler
                    </button>
                    <button
                      type="button"
                      onClick={isCreating ? handleCreateProject : handleEditProject}
                      disabled={!formData.name.trim()}
                      className="btn btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isCreating ? 'Créer le Projet' : 'Sauvegarder'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectManager;
