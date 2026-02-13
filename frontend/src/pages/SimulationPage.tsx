import { useMemo, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Sparkles, Shield, Presentation, ArrowRight, Home } from 'lucide-react'
import PolicyForm from '../components/PolicyForm'
import Dashboard from '../components/Dashboard'
import ExplanationCard from '../components/ExplanationCard'
import GoogleMap from '../components/GoogleMap'
import { SimulationConfig, SimulationResults } from '../types/simulation'

const configuredApi = import.meta.env.VITE_API_URL as string | undefined
const API_ENDPOINTS = [
  configuredApi,
  'http://localhost:8000',
  'http://localhost:8001',
  'http://localhost:8002',
]
  .filter((value): value is string => Boolean(value))
  .map((url) => (url.endsWith('/') ? url.slice(0, -1) : url))

const initialConfig: SimulationConfig = {
  night_shifts: false,
  safety_level: 'standard',
  urgency: 'standard',
  labor: 'standard',
  traffic: 'basic',
}

function SimulationPage() {
  const navigate = useNavigate()
  const [config, setConfig] = useState<SimulationConfig>(initialConfig)
  const [results, setResults] = useState<SimulationResults | null>(null)
  const [loading, setLoading] = useState(false)
  const [errorBanner, setErrorBanner] = useState<string | null>(null)
  const [activeApiBase, setActiveApiBase] = useState<string | null>(API_ENDPOINTS[0] ?? null)
  // Special flow state for hiding sidebar and showing only action button/output
  const [specialFlowActive, setSpecialFlowActive] = useState(false)
  const [firstSimulationDone, setFirstSimulationDone] = useState(false)

  // On mount, check for special flow flag
  useEffect(() => {
    const specialFlag = localStorage.getItem('first_simulation_special_flow') === 'true'
    setSpecialFlowActive(specialFlag)
  }, [])

  const runSimulation = async () => {
    setLoading(true)
    setErrorBanner(null)
    let lastError: unknown = null

    for (const baseUrl of API_ENDPOINTS) {
      try {
        const response = await axios.post(`${baseUrl}/simulate`, config)
        setResults(response.data)
        setActiveApiBase(baseUrl)
        setLoading(false)
        // If special flow is active, mark first simulation as done and clear flag
        if (specialFlowActive && !firstSimulationDone) {
          setFirstSimulationDone(true)
          setSpecialFlowActive(false)
          localStorage.removeItem('first_simulation_special_flow')
        }
        return
      } catch (error) {
        lastError = error
      }
    }

    console.error('Simulation failed', lastError)
    setErrorBanner(
      `Backend not reachable. Tried: ${API_ENDPOINTS.join(', ')}. ` +
        'Ensure the FastAPI server is running.',
    )
    setLoading(false)
  }

  const scrollToControls = () => {
    document.getElementById('policy-panel')?.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }

  const summaryTiles = useMemo(() => {
    if (!results) {
      return [
        { label: 'Schedule Delta', value: '—', helper: 'Awaiting simulation' },
        { label: 'Safety Shift', value: '—', helper: 'Awaiting simulation' },
        { label: 'Disruption Impact', value: '—', helper: 'Awaiting simulation' },
      ]
    }

    const durationDelta =
      results.baseline.metrics.duration - results.policy.metrics.duration
    const safetyDelta =
      results.baseline.metrics.risk_score - results.policy.metrics.risk_score
    const disruptionDelta =
      results.baseline.metrics.disruption_index -
      results.policy.metrics.disruption_index

    const toSigned = (value: number, unit = '') => {
      const prefix = value > 0 ? '-' : value < 0 ? '+' : '+/-'
      return `${prefix}${Math.abs(value).toFixed(1)}${unit}`
    }

    return [
      {
        label: 'Schedule Delta',
        value: toSigned(durationDelta, ' d'),
        helper: 'vs. baseline delivery window',
      },
      {
        label: 'Safety Shift',
        value: toSigned(safetyDelta, ' pts'),
        helper: 'risk score change',
      },
      {
        label: 'Disruption Impact',
        value: toSigned(disruptionDelta, ' pts'),
        helper: 'civic disruption index',
      },
    ]
  }, [results])

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header__bg" />
        <div className="app-header__glow app-header__glow--right" />
        <div className="app-header__glow app-header__glow--left" />

        <div className="app-header__content">
          <nav className="navbar">
            <div className="navbar__brand">
              <div className="brand-icon">🏗️</div>
              <div className="brand-meta">
                <p className="brand-tagline">CIVIC OPS LAB</p>
                <h1 className="brand-title">CIVISIM</h1>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button onClick={() => navigate('/')} className="secondary-button">
                <Home size={16} />
                Home
              </button>
              {!specialFlowActive && (
                <button onClick={scrollToControls} className="nav-button">
                  Configure Policy
                  <ArrowRight size={16} />
                </button>
              )}
            </div>
          </nav>

          <div className="hero-grid">
            <div>
              <p className="hero-badge">
                <Sparkles size={14} />
                Policy Intelligence Preview
              </p>
              <h2 className="hero-title">
                Prototype the ripple effects of construction policy before a single barricade is placed.
              </h2>
              <p className="hero-text">
                CIVISIM blends risk, disruption, and delivery models into a unified simulation cockpit. Iterate on guardrails, communicate trade-offs, and keep public trust intact.
              </p>
              <div className="hero-actions">
                {/* Special flow: Only show the main action button before first simulation */}
                {specialFlowActive ? (
                  <button onClick={runSimulation} disabled={loading} className="primary-button">
                    <Presentation size={18} />
                    {loading ? 'Simulating...' : 'Apply & Run Simulation'}
                  </button>
                ) : (
                  <>
                    <button onClick={runSimulation} disabled={loading} className="primary-button">
                      <Presentation size={18} />
                      {loading ? 'Simulating...' : 'Run Latest Scenario'}
                    </button>
                    <button onClick={scrollToControls} className="secondary-button">
                      <Shield size={18} />
                      Tune Safety Levers
                    </button>
                  </>
                )}
              </div>
              <p className="connection-label">
                {activeApiBase ? `Connected to ${activeApiBase}` : 'Not connected to backend'}
              </p>
            </div>

            <div className="summary-card">
              <div className="summary-card__header">
                <span>Executive Snapshot</span>
                <span>{results ? 'Live scenario' : 'Awaiting input'}</span>
              </div>
              <div className="summary-grid">
                {summaryTiles.map((tile) => (
                  <div key={tile.label} className="summary-tile">
                    <p className="summary-tile__label">{tile.label}</p>
                    <p className="summary-tile__value">{tile.value}</p>
                    <p className="summary-tile__helper">{tile.helper}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="layout-container">
          {errorBanner && <div className="error-banner">{errorBanner}</div>}

          <section className="policy-layout">
            {/* Special flow: Hide sidebar (policy panel) until first simulation is run */}
            {specialFlowActive ? (
              <div className="panel-stack">
                <Dashboard data={results} />
                <ExplanationCard analysis={results?.analysis} />
              </div>
            ) : (
              <>
                <div id="policy-panel">
                  <PolicyForm
                    config={config}
                    setConfig={setConfig}
                    onSimulate={runSimulation}
                    isLoading={loading}
                  />
                </div>
                <div className="panel-stack">
                  <Dashboard data={results} />
                  <ExplanationCard analysis={results?.analysis} />
                  <div style={{ marginTop: '1.5rem' }}>
                    <GoogleMap 
                      simulationActive={!!results}
                      impactLevel={results ? 'medium' : 'low'}
                      height="600px"
                    />
                  </div>
                </div>
              </>
            )}
          </section>
        </div>
      </main>
    </div>
  )
}

export default SimulationPage
