import React from 'react';
import {
  HomeIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  PlayIcon,
  ChartBarIcon,
  BeakerIcon,
  ArrowDownTrayIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';
import ThemeSelector from './ThemeSelector';

interface MinimalistNavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
  projectName: string;
}

const MinimalistNavigation: React.FC<MinimalistNavigationProps> = ({
  currentPage,
  onPageChange,
  projectName
}) => {
  const navigationItems = [
    { id: 'dashboard', label: 'Tableau de Bord', icon: HomeIcon },
    { id: 'projects', label: 'Projets', icon: DocumentTextIcon },
    { id: 'metadata', label: 'Métadonnées', icon: DocumentTextIcon },
    { id: 'history', label: 'Historique', icon: ClockIcon },
    { id: 'calibration', label: 'Calibration', icon: Cog6ToothIcon },
    { id: 'acquisition', label: 'Acquisition', icon: PlayIcon },
    { id: 'analysis', label: 'Analyse', icon: ChartBarIcon },
    { id: 'advanced-analysis', label: 'Analyse Avancée', icon: BeakerIcon },
    { id: 'export', label: 'Export', icon: ArrowDownTrayIcon },
    { id: 'settings', label: 'Paramètres', icon: AdjustmentsHorizontalIcon }
  ];

  return (
    <nav className="themed-nav">
      <div className="golden-container">
        <div className="flex items-center justify-between">
          
          {/* Logo & Project */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-sm">CHN</span>
              </div>
              <div>
                <div className="text-body font-semibold" style={{color: 'var(--text-primary)'}}>CHNeoWave</div>
                <div className="text-meta truncate max-w-xs" style={{color: 'var(--text-muted)'}}>
                  {projectName}
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center gap-1">
            {navigationItems.map((item) => {
              const IconComponent = item.icon;
              const isActive = currentPage === item.id;
              
              return (
                <button
                  key={item.id}
                  onClick={() => onPageChange(item.id)}
                  className={`themed-nav-item px-3 py-2 rounded-lg flex items-center gap-2 transition-all duration-200 ${isActive ? 'active' : ''}`}
                  title={item.label}
                >
                  <IconComponent className="w-4 h-4" />
                  <span className="hidden md:inline text-sm font-medium">{item.label}</span>
                </button>
              );
            })}
          </div>

          {/* Status & Theme Selector */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-small hidden sm:inline" style={{color: 'var(--text-secondary)'}}>
                Système actif
              </span>
            </div>
            <div className="text-meta font-mono" style={{color: 'var(--text-muted)'}}>
              {new Date().toLocaleTimeString('fr-FR', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
            <ThemeSelector />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default MinimalistNavigation;
