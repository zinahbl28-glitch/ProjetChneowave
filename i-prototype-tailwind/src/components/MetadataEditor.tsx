import React, { useState, useEffect } from 'react';
import {
  DocumentTextIcon,
  PencilIcon,
  SaveIcon,
  XMarkIcon,
  PlusIcon,
  TrashIcon,
  EyeIcon,
  Cog6ToothIcon,
  CalendarIcon,
  MapPinIcon,
  UserIcon,
  TagIcon
} from '@heroicons/react/24/outline';

interface MetadataField {
  id: string;
  key: string;
  value: string;
  type: 'text' | 'number' | 'date' | 'select' | 'textarea';
  required: boolean;
  description: string;
  options?: string[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
  };
}

interface MetadataSection {
  id: string;
  name: string;
  description: string;
  fields: MetadataField[];
  collapsed: boolean;
}

interface ProjectMetadata {
  id: string;
  name: string;
  description: string;
  sections: MetadataSection[];
  lastModified: string;
  version: string;
}

const MetadataEditor: React.FC = () => {
  const [metadata, setMetadata] = useState<ProjectMetadata | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [selectedSection, setSelectedSection] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Métadonnées simulées pour le développement
  useEffect(() => {
    const mockMetadata: ProjectMetadata = {
      id: '1',
      name: 'Test_Houle_2025_01',
      description: 'Métadonnées du projet de test de houle en laboratoire',
      version: '1.0.0',
      lastModified: new Date().toISOString(),
      sections: [
        {
          id: 'general',
          name: 'Informations Générales',
          description: 'Informations de base sur le projet',
          collapsed: false,
          fields: [
            {
              id: 'project_name',
              key: 'Nom du Projet',
              value: 'Test_Houle_2025_01',
              type: 'text',
              required: true,
              description: 'Nom unique du projet'
            },
            {
              id: 'project_description',
              key: 'Description',
              value: 'Test de validation des capteurs de houle en laboratoire',
              type: 'textarea',
              required: true,
              description: 'Description détaillée du projet'
            },
            {
              id: 'investigator',
              key: 'Investigateur Principal',
              value: 'Dr. Martin',
              type: 'text',
              required: true,
              description: 'Nom de l\'investigateur principal'
            },
            {
              id: 'start_date',
              key: 'Date de Début',
              value: '2025-08-15',
              type: 'date',
              required: true,
              description: 'Date de début du projet'
            },
            {
              id: 'end_date',
              key: 'Date de Fin',
              value: '2025-08-20',
              type: 'date',
              required: false,
              description: 'Date de fin prévue du projet'
            }
          ]
        },
        {
          id: 'location',
          name: 'Localisation',
          description: 'Informations sur le site d\'expérimentation',
          collapsed: false,
          fields: [
            {
              id: 'site_name',
              key: 'Nom du Site',
              value: 'Laboratoire Maritime',
              type: 'text',
              required: true,
              description: 'Nom du site d\'expérimentation'
            },
            {
              id: 'site_type',
              key: 'Type de Site',
              value: 'Laboratoire',
              type: 'select',
              required: true,
              description: 'Type de site d\'expérimentation',
              options: ['Laboratoire', 'Bassin d\'Essais', 'Tunnel Hydrodynamique', 'Site Naturel']
            },
            {
              id: 'water_depth',
              key: 'Profondeur d\'Eau (m)',
              value: '2.5',
              type: 'number',
              required: true,
              description: 'Profondeur d\'eau en mètres',
              validation: { min: 0.1, max: 100 }
            },
            {
              id: 'coordinates',
              key: 'Coordonnées GPS',
              value: '48.8566°N, 2.3522°E',
              type: 'text',
              required: false,
              description: 'Coordonnées GPS du site'
            }
          ]
        },
        {
          id: 'technical',
          name: 'Paramètres Techniques',
          description: 'Paramètres techniques de l\'acquisition',
          collapsed: false,
          fields: [
            {
              id: 'sampling_rate',
              key: 'Fréquence d\'Échantillonnage (Hz)',
              value: '500',
              type: 'number',
              required: true,
              description: 'Fréquence d\'échantillonnage en Hz',
              validation: { min: 1, max: 10000 }
            },
            {
              id: 'channels',
              key: 'Nombre de Canaux',
              value: '8',
              type: 'number',
              required: true,
              description: 'Nombre de canaux d\'acquisition',
              validation: { min: 1, max: 64 }
            },
            {
              id: 'duration',
              key: 'Durée d\'Acquisition (s)',
              value: '3600',
              type: 'number',
              required: true,
              description: 'Durée totale d\'acquisition en secondes',
              validation: { min: 1, max: 86400 }
            },
            {
              id: 'data_format',
              key: 'Format des Données',
              value: 'HDF5',
              type: 'select',
              required: true,
              description: 'Format de stockage des données',
              options: ['HDF5', 'TDMS', 'CSV', 'MAT']
            }
          ]
        },
        {
          id: 'sensors',
          name: 'Capteurs',
          description: 'Informations sur les capteurs utilisés',
          collapsed: false,
          fields: [
            {
              id: 'sensor_types',
              key: 'Types de Capteurs',
              value: 'Pression, Accéléromètre, Température',
              type: 'textarea',
              required: true,
              description: 'Types de capteurs utilisés'
            },
            {
              id: 'calibration_date',
              key: 'Date de Calibration',
              value: '2025-08-10',
              type: 'date',
              required: true,
              description: 'Date de la dernière calibration'
            },
            {
              id: 'calibration_standard',
              key: 'Standard de Calibration',
              value: 'ISO 17025',
              type: 'select',
              required: true,
              description: 'Standard de calibration utilisé',
              options: ['ISO 17025', 'NIST', 'Autre']
            }
          ]
        },
        {
          id: 'environmental',
          name: 'Conditions Environnementales',
          description: 'Conditions environnementales pendant l\'expérimentation',
          collapsed: false,
          fields: [
            {
              id: 'water_temperature',
              key: 'Température de l\'Eau (°C)',
              value: '18.5',
              type: 'number',
              required: false,
              description: 'Température de l\'eau en degrés Celsius',
              validation: { min: -5, max: 40 }
            },
            {
              id: 'air_temperature',
              key: 'Température de l\'Air (°C)',
              value: '22.0',
              type: 'number',
              required: false,
              description: 'Température de l\'air en degrés Celsius',
              validation: { min: -20, max: 50 }
            },
            {
              id: 'humidity',
              key: 'Humidité Relative (%)',
              value: '65',
              type: 'number',
              required: false,
              description: 'Humidité relative en pourcentage',
              validation: { min: 0, max: 100 }
            },
            {
              id: 'weather_conditions',
              key: 'Conditions Météorologiques',
              value: 'Ciel dégagé, vent faible',
              type: 'textarea',
              required: false,
              description: 'Description des conditions météorologiques'
            }
          ]
        }
      ]
    };

    setMetadata(mockMetadata);
  }, []);

  const handleFieldChange = (sectionId: string, fieldId: string, value: string) => {
    if (!metadata) return;

    setMetadata(prev => {
      if (!prev) return prev;

      return {
        ...prev,
        sections: prev.sections.map(section => {
          if (section.id === sectionId) {
            return {
              ...section,
              fields: section.fields.map(field => {
                if (field.id === fieldId) {
                  return { ...field, value };
                }
                return field;
              })
            };
          }
          return section;
        })
      };
    });
  };

  const toggleSection = (sectionId: string) => {
    if (!metadata) return;

    setMetadata(prev => {
      if (!prev) return prev;

      return {
        ...prev,
        sections: prev.sections.map(section => {
          if (section.id === sectionId) {
            return { ...section, collapsed: !section.collapsed };
          }
          return section;
        })
      };
    });
  };

  const addField = (sectionId: string) => {
    if (!metadata) return;

    const newField: MetadataField = {
      id: `field_${Date.now()}`,
      key: 'Nouveau Champ',
      value: '',
      type: 'text',
      required: false,
      description: 'Description du nouveau champ'
    };

    setMetadata(prev => {
      if (!prev) return prev;

      return {
        ...prev,
        sections: prev.sections.map(section => {
          if (section.id === sectionId) {
            return {
              ...section,
              fields: [...section.fields, newField]
            };
          }
          return section;
        })
      };
    });
  };

  const removeField = (sectionId: string, fieldId: string) => {
    if (!metadata) return;

    setMetadata(prev => {
      if (!prev) return prev;

      return {
        ...prev,
        sections: prev.sections.map(section => {
          if (section.id === sectionId) {
            return {
              ...section,
              fields: section.fields.filter(field => field.id !== fieldId)
            };
          }
          return section;
        })
      };
    });
  };

  const saveMetadata = () => {
    if (!metadata) return;

    // Simuler la sauvegarde
    const updatedMetadata = {
      ...metadata,
      lastModified: new Date().toISOString(),
      version: (parseFloat(metadata.version) + 0.1).toFixed(1)
    };

    setMetadata(updatedMetadata);
    setIsEditing(false);

    // Afficher une confirmation
    alert('Métadonnées sauvegardées avec succès !');
  };

  const renderField = (field: MetadataField, sectionId: string) => {
    const commonProps = {
      value: field.value,
      onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
        handleFieldChange(sectionId, field.id, e.target.value),
      className: "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white",
      disabled: !isEditing
    };

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            {...commonProps}
            rows={3}
            placeholder={field.description}
          />
        );
      case 'select':
        return (
          <select {...commonProps}>
            {field.options?.map((option, index) => (
              <option key={index} value={option}>{option}</option>
            ))}
          </select>
        );
      case 'date':
        return (
          <input
            {...commonProps}
            type="date"
          />
        );
      case 'number':
        return (
          <input
            {...commonProps}
            type="number"
            min={field.validation?.min}
            max={field.validation?.max}
            step="any"
          />
        );
      default:
        return (
          <input
            {...commonProps}
            type="text"
            placeholder={field.description}
          />
        );
    }
  };

  const filteredSections = metadata?.sections.filter(section =>
    section.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    section.fields.some(field =>
      field.key.toLowerCase().includes(searchTerm.toLowerCase()) ||
      field.value.toLowerCase().includes(searchTerm.toLowerCase())
    )
  ) || [];

  if (!metadata) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Éditeur de Métadonnées
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                Gérez les métadonnées du projet : {metadata.name}
              </p>
              <div className="flex items-center gap-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                <span>Version: {metadata.version}</span>
                <span>Dernière modification: {new Date(metadata.lastModified).toLocaleString()}</span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {isEditing ? (
                <>
                  <button
                    onClick={() => setIsEditing(false)}
                    className="btn btn-secondary flex items-center gap-2"
                  >
                    <XMarkIcon className="w-4 h-4" />
                    Annuler
                  </button>
                  <button
                    onClick={saveMetadata}
                    className="btn btn-primary flex items-center gap-2"
                  >
                    <SaveIcon className="w-4 h-4" />
                    Sauvegarder
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="btn btn-primary flex items-center gap-2"
                >
                  <PencilIcon className="w-4 h-4" />
                  Modifier
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative">
            <input
              type="text"
              placeholder="Rechercher dans les métadonnées..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 pl-10 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            />
            <DocumentTextIcon className="w-5 h-5 text-gray-400 absolute left-3 top-2.5" />
          </div>
        </div>

        {/* Metadata Sections */}
        <div className="space-y-6">
          {filteredSections.map((section) => (
            <div key={section.id} className="bg-white dark:bg-gray-800 rounded-lg shadow-lg">
              <div
                className="p-6 border-b border-gray-200 dark:border-gray-700 cursor-pointer"
                onClick={() => toggleSection(section.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Cog6ToothIcon className="w-5 h-5 text-blue-600" />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {section.name}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {section.description}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {section.fields.length} champ(s)
                    </span>
                    <button
                      className={`transform transition-transform ${section.collapsed ? 'rotate-0' : 'rotate-180'}`}
                    >
                      ▼
                    </button>
                  </div>
                </div>
              </div>

              {!section.collapsed && (
                <div className="p-6">
                  <div className="space-y-4">
                    {section.fields.map((field) => (
                      <div key={field.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                {field.key}
                                {field.required && <span className="text-red-500 ml-1">*</span>}
                              </label>
                              {field.validation && (
                                <span className="text-xs text-gray-500 dark:text-gray-400">
                                  {field.validation.min !== undefined && `Min: ${field.validation.min}`}
                                  {field.validation.max !== undefined && `Max: ${field.validation.max}`}
                                </span>
                              )}
                            </div>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">
                              {field.description}
                            </p>
                          </div>
                          {isEditing && (
                            <button
                              onClick={() => removeField(section.id, field.id)}
                              className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                            >
                              <TrashIcon className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                        {renderField(field, section.id)}
                      </div>
                    ))}

                    {isEditing && (
                      <button
                        onClick={() => addField(section.id)}
                        className="w-full p-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-gray-500 dark:text-gray-400 hover:border-blue-500 hover:text-blue-500 dark:hover:border-blue-400 dark:hover:text-blue-400 transition-colors"
                      >
                        <PlusIcon className="w-5 h-5 mx-auto mb-1" />
                        Ajouter un champ
                      </button>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Export Options */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Options d'Export
          </h3>
          <div className="flex items-center gap-4">
            <button className="btn btn-secondary flex items-center gap-2">
              <DocumentTextIcon className="w-4 h-4" />
              Exporter en JSON
            </button>
            <button className="btn btn-secondary flex items-center gap-2">
              <DocumentTextIcon className="w-4 h-4" />
              Exporter en XML
            </button>
            <button className="btn btn-secondary flex items-center gap-2">
              <DocumentTextIcon className="w-4 h-4" />
              Exporter en CSV
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetadataEditor;
