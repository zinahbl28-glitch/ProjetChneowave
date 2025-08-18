# Système de Design Maritime - CHNeoWave

## Palette de Couleurs

### Couleurs Primaires
- **Bleu Océan Profond** : `#1e3a8a` (bg-ocean-blue)
- **Bleu Océan Clair** : `#1e40af` (bg-ocean-blue-light)
- **Turquoise Scientifique** : `#0891b2` (bg-turquoise)
- **Turquoise Clair** : `#06b6d4` (bg-turquoise-light)

### Couleurs Secondaires
- **Orange Maritime** : `#ea580c` (bg-maritime-orange)
- **Orange Clair** : `#f97316` (bg-maritime-orange-light)
- **Vert Validation** : `#059669` (bg-validation-green)
- **Vert Clair** : `#10b981` (bg-validation-green-light)

### Couleurs Neutres
- **Gris Foncé** : `#64748b` (text-gray-dark)
- **Gris Moyen** : `#94a3b8` (text-gray-medium)
- **Gris Clair** : `#e2e8f0` (text-gray-light)
- **Blanc** : `#ffffff` (text-white)

## Typographie

### En-têtes
- **Font Family** : Inter, Roboto, sans-serif
- **Font Weight** : Bold (700)
- **Sizes** :
  - H1 : 2.25rem (36px)
  - H2 : 1.875rem (30px)
  - H3 : 1.5rem (24px)
  - H4 : 1.25rem (20px)

### Texte Courant
- **Font Family** : Source Sans Pro, sans-serif
- **Font Weight** : Regular (400)
- **Sizes** :
  - Body Large : 1.125rem (18px)
  - Body Medium : 1rem (16px)
  - Body Small : 0.875rem (14px)

### Données Numériques
- **Font Family** : JetBrains Mono, monospace
- **Font Weight** : Regular (400)
- **Sizes** :
  - Data Large : 1.5rem (24px)
  - Data Medium : 1.25rem (20px)
  - Data Small : 1rem (16px)

## Composants UI

### Boutons
- **Primary Button** :
  ```html
  <button className="px-6 py-3 bg-ocean-blue text-white rounded-lg hover:bg-ocean-blue-light transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ocean-blue">
    Action principale
  </button>
  ```

- **Secondary Button** :
  ```html
  <button className="px-6 py-3 bg-turquoise text-white rounded-lg hover:bg-turquoise-light transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-turquoise">
    Action secondaire
  </button>
  ```

- **Alert Button** :
  ```html
  <button className="px-6 py-3 bg-maritime-orange text-white rounded-lg hover:bg-maritime-orange-light transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-maritime-orange">
    Alerte/Action critique
  </button>
  ```

### Cards
- **Data Card** :
  ```html
  <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-turquoise">
    <h3 className="text-lg font-bold text-gray-dark mb-2">Titre de la Card</h3>
    <p className="text-gray-medium">Contenu de la card avec données scientifiques</p>
  </div>
  ```

- **Metric Card** :
  ```html
  <div className="bg-gradient-to-br from-ocean-blue to-ocean-blue-light rounded-xl shadow-lg p-6 text-white">
    <h4 className="text-sm font-medium opacity-80">Nom de la Métrique</h4>
    <p className="text-3xl font-bold mt-2">12.45 m</p>
    <div className="mt-4 h-2 bg-white bg-opacity-20 rounded-full overflow-hidden">
      <div className="h-full bg-validation-green" style={{ width: '65%' }}></div>
    </div>
  </div>
  ```

### Graphiques
- **Chart Container** :
  ```html
  <div className="bg-white rounded-xl shadow-lg p-4 md:p-6">
    <div className="flex justify-between items-center mb-4">
      <h3 className="text-lg font-bold text-gray-dark">Nom du Graphique</h3>
      <button className="text-turquoise hover:text-turquoise-light">
        <SignalIcon className="h-5 w-5" />
      </button>
    </div>
    <div className="h-80">
      {/* Graphique ici */}
    </div>
  </div>
  ```

## Animations et Transitions

### Transitions Standards
- **Duration** : 200ms
- **Timing Function** : ease-in-out
- **Properties** : color, background-color, opacity, transform

### Animations Spécifiques
- **Maritime Wave** :
  ```css
  @keyframes maritime-wave {
    0% { transform: translateY(0) translateX(0); }
    25% { transform: translateY(-10px) translateX(5px); }
    50% { transform: translateY(0) translateX(10px); }
    75% { transform: translateY(10px) translateX(5px); }
    100% { transform: translateY(0) translateX(0); }
  }
  ```

- **Maritime Glow** :
  ```css
  @keyframes maritime-glow {
    0% { box-shadow: 0 0 5px rgba(8, 145, 178, 0.3); }
    50% { box-shadow: 0 0 20px rgba(8, 145, 178, 0.6); }
    100% { box-shadow: 0 0 5px rgba(8, 145, 178, 0.3); }
  }
  ```

- **Maritime Pulse** :
  ```css
  @keyframes maritime-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }
  ```

## Responsive Design

### Breakpoints Tailwind
- **Mobile** : < 768px
- **Tablet** : 768px - 1024px
- **Desktop** : > 1024px

### Grille d'Acquisition (3 colonnes)
- **Desktop** : Grid 3 colonnes avec ratios d'or
- **Tablet** : Grid 2 colonnes, réorganisation contenu
- **Mobile** : Stack vertical, visualisations prioritaires

### Tailles d'Éléments Interactifs
- **Minimum Touch Target** : 44px
- **Boutons Principaux** : 48px hauteur
- **Navigation Items** : 44px hauteur
- **Form Inputs** : 44px hauteur minimum

## Accessibilité

### Contraste des Couleurs
- **Texte Normal** : Ratio minimum 7:1
- **Texte Large** : Ratio minimum 4.5:1
- **Éléments Interactifs** : Contraste élevé

### Navigation Clavier
- **Focus Visible** : Outline 2px solid turquoise
- **Skip Links** : Navigation rapide
- **ARIA Labels** : Description des éléments

### Typographie Accessible
- **Line Height** : 1.5 pour body text
- **Font Size** : Minimum 16px pour texte principal
- **Font Weight** : Sufficient contrast between weights
