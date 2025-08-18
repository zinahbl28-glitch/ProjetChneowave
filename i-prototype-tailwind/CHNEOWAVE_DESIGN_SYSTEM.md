# CHNeoWave Visual Identity & Design System

## Brand Identity: "Scientific Maritime Precision"

### Core Brand Values
- **🎯 Precision**: Accurate, reliable data acquisition and analysis
- **🌊 Maritime Heritage**: Deep connection to ocean science and naval engineering
- **🔬 Scientific Excellence**: Laboratory-grade quality and methodology
- **⚡ Innovation**: Cutting-edge technology for maritime research
- **🤝 Professional Trust**: Dependable partner for critical research

## Visual Identity System

### 1. Color Palette

#### Primary Colors
```css
--ocean-deep: #0f172a;      /* Deep ocean blue - primary backgrounds */
--maritime-blue: #1e40af;   /* Maritime blue - primary actions */
--wave-teal: #0891b2;       /* Scientific teal - secondary actions */
--precision-slate: #475569; /* Professional gray - text and borders */
```

#### Accent Colors
```css
--success-emerald: #059669; /* Success states, active connections */
--warning-amber: #d97706;   /* Warnings, calibration alerts */
--danger-red: #dc2626;      /* Errors, critical alerts */
--info-cyan: #0891b2;       /* Information, data highlights */
--gold-accent: #f59e0b;     /* Premium features, achievements */
```

#### Neutral Palette
```css
--white: #ffffff;
--gray-50: #f8fafc;
--gray-100: #f1f5f9;
--gray-200: #e2e8f0;
--gray-300: #cbd5e1;
--gray-400: #94a3b8;
--gray-500: #64748b;
--gray-600: #475569;
--gray-700: #334155;
--gray-800: #1e293b;
--gray-900: #0f172a;
```

### 2. Typography System

#### Font Families
- **Primary**: Inter (Clean, technical, excellent readability)
- **Monospace**: JetBrains Mono (Data display, technical values)
- **Display**: Inter (Consistent brand experience)

#### Type Scale (Golden Ratio Based)
```css
--text-xs: 0.75rem;    /* 12px - Small labels, captions */
--text-sm: 0.875rem;   /* 14px - Secondary text */
--text-base: 1rem;     /* 16px - Body text baseline */
--text-lg: 1.125rem;   /* 18px - Emphasized text */
--text-xl: 1.25rem;    /* 20px - Small headings */
--text-2xl: 1.625rem;  /* 26px - Section headings (16 × 1.618) */
--text-3xl: 2.625rem;  /* 42px - Page headings (26 × 1.618) */
--text-4xl: 4.25rem;   /* 68px - Display text (42 × 1.618) */
```

#### Line Heights
```css
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.618; /* Golden ratio for optimal readability */
--leading-loose: 2;
```

### 3. Spacing System (Golden Ratio)

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px - Base unit */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
--space-32: 8rem;     /* 128px */
```

### 4. Component Design Tokens

#### Border Radius
```css
--radius-sm: 0.25rem;   /* 4px - Small elements */
--radius-md: 0.5rem;    /* 8px - Standard components */
--radius-lg: 0.75rem;   /* 12px - Cards, panels */
--radius-xl: 1rem;      /* 16px - Large containers */
--radius-2xl: 1.5rem;   /* 24px - Hero elements */
--radius-full: 9999px;  /* Circular elements */
```

#### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```

## Component Library

### 1. Data Cards
```tsx
// Metric Display Card
<div className="bg-white dark:bg-slate-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-slate-700">
  <div className="flex items-center justify-between mb-4">
    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Wave Height</h3>
    <span className="text-2xl">🌊</span>
  </div>
  <div className="text-3xl font-bold text-maritime-blue dark:text-wave-teal mb-2">2.4 m</div>
  <div className="text-sm text-gray-600 dark:text-gray-400">Hs - ITTC Standard</div>
</div>
```

### 2. Status Indicators
```tsx
// Connection Status
<div className="flex items-center gap-2">
  <div className="w-3 h-3 rounded-full bg-success-emerald animate-pulse"></div>
  <span className="text-sm font-medium text-success-emerald">Connecté</span>
</div>

// System Status
<div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm bg-success-emerald/10 text-success-emerald border border-success-emerald/20">
  <div className="w-2 h-2 rounded-full bg-success-emerald"></div>
  Acquisition Active
</div>
```

### 3. Technical Controls
```tsx
// Parameter Input
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
    Fréquence d'Échantillonnage
  </label>
  <select className="w-full px-4 py-3 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-maritime-blue focus:border-maritime-blue transition-colors">
    <option value="100">100 Hz</option>
    <option value="250">250 Hz</option>
    <option value="500">500 Hz</option>
  </select>
</div>
```

### 4. Data Visualization
```tsx
// Chart Container
<div className="bg-white dark:bg-slate-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-slate-700">
  <div className="flex items-center justify-between mb-6">
    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Simulation de Houle</h3>
    <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
      <span>Temps Réel</span>
      <div className="w-2 h-2 rounded-full bg-success-emerald animate-pulse"></div>
    </div>
  </div>
  <div className="h-64 bg-gradient-to-r from-maritime-blue/10 to-wave-teal/10 rounded-lg flex items-center justify-center">
    <span className="text-gray-500 dark:text-gray-400">Graphique de Simulation</span>
  </div>
</div>
```

## Interface Patterns

### 1. Navigation Hierarchy
- **Primary Navigation**: Core workflow steps (Dashboard, Project, Calibration, Acquisition, Analysis, Export)
- **Secondary Navigation**: Settings, Help, User management
- **Contextual Navigation**: Within-page tabs, filters, view controls

### 2. Information Architecture
- **Dashboard**: System overview, quick actions, recent projects
- **Project Management**: Project creation, configuration, history
- **Calibration**: Sensor setup, validation, quality control
- **Acquisition**: Real-time data collection, monitoring
- **Analysis**: Signal processing, spectral analysis, reporting
- **Export**: Data formatting, report generation, sharing

### 3. Responsive Behavior
- **Desktop (≥1024px)**: Full sidebar, multi-column layouts, detailed views
- **Tablet (768-1023px)**: Collapsible sidebar, adaptive grids, touch-optimized
- **Mobile (<768px)**: Overlay navigation, single-column, gesture-friendly

## Brand Applications

### 1. Logo & Branding
- **Primary Logo**: CHNeoWave with wave-inspired typography
- **Icon**: Stylized wave with data points, representing precision measurement
- **Tagline**: "Suite de Laboratoire Maritime" or "Maritime Laboratory Suite"

### 2. Iconography Style
- **Technical**: Precise, line-based icons for instruments and controls
- **Maritime**: Wave patterns, ship silhouettes, ocean elements
- **Scientific**: Charts, graphs, measurement tools
- **System**: Standard UI icons with maritime color treatment

### 3. Data Visualization Style
- **Wave Patterns**: Smooth, flowing lines representing ocean data
- **Color Coding**: Consistent color mapping for different data types
- **Grid Systems**: Technical, precise grid layouts for charts
- **Typography**: Monospace fonts for numerical data, clear labels

## Implementation Guidelines

### 1. Dark Mode Support
- All components must support both light and dark themes
- Use CSS custom properties for easy theme switching
- Maintain contrast ratios for accessibility (WCAG AA)

### 2. Accessibility Standards
- Minimum 4.5:1 contrast ratio for normal text
- Minimum 3:1 contrast ratio for large text
- Keyboard navigation support for all interactive elements
- Screen reader compatibility with proper ARIA labels

### 3. Performance Considerations
- Optimize for real-time data updates
- Efficient rendering for large datasets
- Smooth animations and transitions
- Responsive image loading

## Unique Differentiators

### 1. Maritime-Specific Design Language
- **Ocean-Inspired Aesthetics**: Deep blues, wave patterns, fluid animations
- **Technical Precision**: Clean lines, exact measurements, professional typography
- **Laboratory Quality**: High contrast, clear visibility, scientific accuracy

### 2. Workflow-Optimized Interface
- **Task-Oriented Layout**: Logical progression through testing procedures
- **Context-Aware Tools**: Relevant controls and data for each workflow stage
- **Expert-Friendly**: Advanced features accessible without overwhelming novices

### 3. Professional Brand Identity
- **Scientific Credibility**: Visual language that conveys expertise and reliability
- **Maritime Heritage**: Design elements that connect to naval and ocean engineering
- **Modern Innovation**: Contemporary interface patterns with cutting-edge functionality

---

*This design system establishes CHNeoWave as a distinctive, professional maritime data acquisition platform with a unique visual identity that reflects its scientific precision and maritime focus.*
