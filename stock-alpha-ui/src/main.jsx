import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import BackendStatusLoader from './components/backendStatusLoader/BackendStatusLoader.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BackendStatusLoader />
  </StrictMode>,
)
