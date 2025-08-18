import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'

// Initialize theme from localStorage or default to light
if (typeof document !== 'undefined') {
  const saved = localStorage.getItem('chneowave-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
