import React, { useState, useEffect } from 'react';

type Theme = 'light' | 'dark' | 'beige';

interface ThemeSelectorProps {
  className?: string;
}

const ThemeSelector: React.FC<ThemeSelectorProps> = ({ className = '' }) => {
  const [currentTheme, setCurrentTheme] = useState<Theme>('light');

  // Charger le thème sauvegardé au démarrage
  useEffect(() => {
    const savedTheme = localStorage.getItem('chneowave-theme') as Theme;
    if (savedTheme && ['light', 'dark', 'beige'].includes(savedTheme)) {
      setCurrentTheme(savedTheme);
      applyTheme(savedTheme);
    }
  }, []);

  const applyTheme = (theme: Theme) => {
    // Supprimer les anciens thèmes
    document.documentElement.removeAttribute('data-theme');
    document.body.classList.remove('theme-light', 'theme-dark', 'theme-beige');
    
    // Appliquer le nouveau thème
    document.documentElement.setAttribute('data-theme', theme);
    document.body.classList.add(`theme-${theme}`);
    
    // Sauvegarder dans localStorage
    localStorage.setItem('chneowave-theme', theme);
  };

  const handleThemeChange = (theme: Theme) => {
    setCurrentTheme(theme);
    applyTheme(theme);
  };

  const themes = [
    { 
      id: 'light' as Theme, 
      name: 'Clair', 
      icon: '☀️',
      gradient: 'from-white to-gray-100',
      textColor: 'text-gray-800'
    },
    { 
      id: 'dark' as Theme, 
      name: 'Sombre', 
      icon: '🌙',
      gradient: 'from-gray-900 to-gray-700',
      textColor: 'text-white'
    },
    { 
      id: 'beige' as Theme, 
      name: 'Beige', 
      icon: '🏛️',
      gradient: 'from-amber-50 to-yellow-100',
      textColor: 'text-amber-900'
    }
  ];

  return (
    <div className={`theme-selector ${className}`}>
      {themes.map((theme) => (
        <button
          key={theme.id}
          onClick={() => handleThemeChange(theme.id)}
          className={`theme-option theme-${theme.id} ${currentTheme === theme.id ? 'active' : ''}`}
          title={`Thème ${theme.name}`}
          aria-label={`Basculer vers le thème ${theme.name}`}
        >
          <span className="text-xs">{theme.icon}</span>
        </button>
      ))}
    </div>
  );
};

export default ThemeSelector;