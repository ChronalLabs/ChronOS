import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import LandingPage from './pages/LandingPage'
import SimulationEnginePage from './pages/SimulationEnginePage'
import PolicyConfigurationPage from './pages/PolicyConfigurationPage'
import ImpactAnalysisPage from './pages/ImpactAnalysisPage'
import MLAnalysisPage from './pages/MLAnalysisPage'
import ImpactMapPage from './pages/ImpactMapPage'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={
          <ProtectedRoute>
            <LandingPage />
          </ProtectedRoute>
        } />
        <Route path="/simulation-engine" element={
          <ProtectedRoute requireAdmin>
            <SimulationEnginePage />
          </ProtectedRoute>
        } />
        <Route path="/policy-config" element={
          <ProtectedRoute requireAdmin>
            <PolicyConfigurationPage />
          </ProtectedRoute>
        } />
        <Route path="/impact-analysis" element={
          <ProtectedRoute>
            <ImpactAnalysisPage />
          </ProtectedRoute>
        } />
        <Route path="/ml-analysis" element={
          <ProtectedRoute requireAdmin>
            <MLAnalysisPage />
          </ProtectedRoute>
        } />
        <Route path="/impact-map" element={
          <ProtectedRoute>
            <ImpactMapPage />
          </ProtectedRoute>
        } />
      </Routes>
    </AuthProvider>
  )
}

export default App