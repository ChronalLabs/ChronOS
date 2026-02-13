import { useState, useEffect } from 'react'
// Simple DJB2 hash for string
function hashPolicyText(text: string): string {
  let hash = 5381;
  for (let i = 0; i < text.length; i++) {
    hash = ((hash << 5) + hash) + text.charCodeAt(i);
  }
  return 'ml_analysis_' + (hash >>> 0); // unsigned
}
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Home, Play, RotateCcw, Settings, Building2, Brain, BarChart3, ArrowRight, Sparkles, FileText, X, CheckCircle2 } from 'lucide-react'
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

function SimulationEnginePage() {
  const navigate = useNavigate()
  const [config, setConfig] = useState<SimulationConfig>(initialConfig)
  const [results, setResults] = useState<SimulationResults | null>(null)
  const [loading, setLoading] = useState(false)
  const [errorBanner, setErrorBanner] = useState<string | null>(null)
  const [activeApiBase, setActiveApiBase] = useState<string | null>(API_ENDPOINTS[0] ?? null)
  const [mlParams, setMlParams] = useState<any>(null)
  const [mlParamsApplied, setMlParamsApplied] = useState(false)
  // Special flow state: hide sidebar until first simulation completes
  // This only applies when entering via Policy Config -> ML Analysis flow
  const [specialFlowActive, setSpecialFlowActive] = useState(false)

  // Load ML parameters from localStorage on mount
  useEffect(() => {
    // Check for special flow flag (set when coming from Policy Config after ML Analysis)
    const specialFlag = localStorage.getItem('first_simulation_special_flow') === 'true'
    setSpecialFlowActive(specialFlag)

    // Try to get the last used ML analysis key
    const lastKey = localStorage.getItem('ml_analysis_last_key');
    let mlStored = null;
    if (lastKey) {
      mlStored = localStorage.getItem(lastKey);
    }
    if (mlStored) {
      try {
        const params = JSON.parse(mlStored);
        setMlParams(params);
        // Auto-configure simulation based on ML analysis
        const newConfig: SimulationConfig = { ...initialConfig };
        // Map safety profile to simulation config
        if (params.safetyProfile) {
          if (params.safetyProfile.mandatory_training || params.safetyProfile.ppe_required) {
            newConfig.safety_level = 'high';
          } else if (params.safetyProfile.safety_score !== undefined) {
            newConfig.safety_level = params.safetyProfile.safety_score > 70 ? 'high' : params.safetyProfile.safety_score > 40 ? 'standard' : 'low';
          }
        }
        // Map speed profile to urgency and labor
        if (params.speedProfile) {
          if (params.speedProfile.night_work_allowed) {
            newConfig.night_shifts = true;
          }
          if (params.speedProfile.priority === 'high' || params.speedProfile.expedited) {
            newConfig.urgency = 'high';
            newConfig.labor = 'increased';
          }
        }
        // Map zone constraints to traffic management
        if (params.zoneConstraints) {
          if (params.zoneConstraints.traffic_restrictions || params.zoneConstraints.lane_closures) {
            newConfig.traffic = 'advanced';
          }
        }
        // Map risk level
        if (params.riskLevel) {
          if (params.riskLevel.toLowerCase() === 'high' || params.riskLevel.toLowerCase() === 'critical') {
            newConfig.safety_level = 'high';
          }
        }
        setConfig(newConfig);
        setMlParamsApplied(true);
        return; // Don't load policy config if ML params exist
      } catch (e) {
        console.error('Failed to parse ML params:', e);
      }
    }
    
    // Then check for policy preset config (from Policy Configuration page)
    const policyConfig = localStorage.getItem('active_simulation_config')
    if (policyConfig) {
      try {
        const parsedConfig = JSON.parse(policyConfig)
        setConfig(parsedConfig)
        // Clear after loading to avoid stale configs
        localStorage.removeItem('active_simulation_config')
      } catch (e) {
        console.error('Failed to parse policy config:', e)
      }
    }
  }, [])

  const clearMlParams = () => {
    localStorage.removeItem('ml_analysis_params')
    setMlParams(null)
    setMlParamsApplied(false)
    setConfig(initialConfig)
  }

  const runSimulation = async () => {
    setLoading(true)
    setErrorBanner(null)
    let lastError: unknown = null

    for (const baseUrl of API_ENDPOINTS) {
      try {
        const response = await axios.post(`${baseUrl}/simulate`, config)
        const result = { ...response.data, timestamp: new Date().toISOString(), config: { ...config } }
        setResults(result)
        setActiveApiBase(baseUrl)
        
        const stored = localStorage.getItem('simulation_results')
        const existingResults = stored ? JSON.parse(stored) : []
        existingResults.unshift(result)
        const trimmed = existingResults.slice(0, 10)
        localStorage.setItem('simulation_results', JSON.stringify(trimmed))
        
        // Dispatch custom event to notify other components about the update
        window.dispatchEvent(new CustomEvent('simulation_results_updated'))
        
        // If special flow is active, clear it after first simulation completes
        if (specialFlowActive) {
          setSpecialFlowActive(false)
          localStorage.removeItem('first_simulation_special_flow')
        }
        
        setLoading(false)
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

  const resetSimulation = () => {
    setConfig(initialConfig)
    setResults(null)
    setErrorBanner(null)
  }

  return (
    <div className="app" style={{ background: 'linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)' }}>
      {/* Premium Header */}
      <header className="app-header" style={{ minHeight: 'auto', padding: '0', position: 'relative', overflow: 'hidden' }}>
        <div className="app-header__bg" style={{ background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 30%, #ede9fe 70%, #e0e7ff 100%)' }} />
        <div className="app-header__glow app-header__glow--right" style={{ background: 'rgba(139, 92, 246, 0.15)', width: '20rem', height: '20rem' }} />
        <div className="app-header__glow app-header__glow--left" style={{ background: 'rgba(99, 102, 241, 0.12)', width: '24rem', height: '24rem' }} />
        
        <div className="app-header__content" style={{ padding: '1.5rem 2rem', position: 'relative', zIndex: 1 }}>
          <nav className="navbar" style={{ borderBottom: 'none', maxWidth: '1400px', margin: '0 auto' }}>
            <div className="navbar__brand">
              <div className="brand-icon" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', color: 'white', fontSize: '1.25rem' }}>⚡</div>
              <div className="brand-meta">
                <p className="brand-tagline" style={{ color: '#8b5cf6', fontWeight: '600' }}>SIMULATION LAB</p>
                <h1 className="brand-title" style={{ fontSize: '1.25rem', background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>CIVISIM</h1>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button onClick={() => navigate('/')} className="secondary-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Home size={16} />
                Home
              </button>
              <button 
                onClick={() => navigate('/policy-config')} 
                className="secondary-button"
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <Settings size={16} />
                Policy Config
              </button>
              <button 
                onClick={() => navigate('/ml-analysis')} 
                className="primary-button"
                style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', padding: '0.5rem 1rem', fontSize: '0.875rem', boxShadow: '0 8px 24px rgba(139,92,246,0.25)' }}
              >
                <Brain size={16} />
                ML Analysis
              </button>
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section with Premium Styling */}
      <section style={{ padding: '3rem 2rem', textAlign: 'center', background: 'linear-gradient(135deg, #faf5ff 0%, #ede9fe 50%, #e0e7ff 100%)', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: '10%', right: '15%', width: '200px', height: '200px', background: 'radial-gradient(circle, rgba(139,92,246,0.08) 0%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }} />
        <div style={{ maxWidth: '1400px', margin: '0 auto', position: 'relative', zIndex: 1 }}>
          <div className="hero-badge" style={{ marginBottom: '1.5rem', background: 'linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%)', color: '#7c3aed', border: '1px solid rgba(139,92,246,0.2)' }}>
            <Play size={16} />
            Real-time Simulation
          </div>
          <h2 style={{ fontSize: '2.5rem', fontWeight: '700', marginBottom: '1rem', background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Simulation Engine
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#64748b', maxWidth: '700px', margin: '0 auto' }}>
            Run real-time construction scenarios and see the immediate impact on safety, schedule, and civic disruption
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="app-main" style={{ padding: '2rem' }}>
        <div className="layout-container" style={{ maxWidth: '1400px', margin: '0 auto' }}>
          {errorBanner && (
            <div style={{ marginBottom: '1.5rem', padding: '1rem 1.5rem', background: 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: '14px', color: '#dc2626', fontWeight: '500' }}>
              {errorBanner}
            </div>
          )}

          {/* ML Analysis Parameters Banner */}
          {mlParams && mlParamsApplied && (
            <div style={{ 
              marginBottom: '1.5rem', 
              padding: '1.25rem 1.5rem', 
              background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
              border: '2px solid #86efac', 
              borderRadius: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '1rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ 
                  width: '48px', 
                  height: '48px', 
                  borderRadius: '12px', 
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Brain size={24} style={{ color: 'white' }} />
                </div>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <CheckCircle2 size={16} style={{ color: '#16a34a' }} />
                    <span style={{ fontWeight: '700', color: '#166534', fontSize: '1rem' }}>ML Parameters Applied</span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.875rem', color: '#047857' }}>
                    Policy: <span style={{ fontWeight: '600' }}>{mlParams.policyName}</span>
                    {mlParams.classification && <> • Classification: <span style={{ fontWeight: '600' }}>{mlParams.classification}</span></>}
                    {mlParams.confidence && <> • Confidence: <span style={{ fontWeight: '600' }}>{Math.round(mlParams.confidence * 100)}%</span></>}
                  </p>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                <button
                  onClick={() => navigate('/ml-analysis')}
                  style={{
                    padding: '0.625rem 1rem',
                    background: 'white',
                    border: '2px solid #86efac',
                    borderRadius: '10px',
                    color: '#166534',
                    fontWeight: '600',
                    fontSize: '0.875rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <FileText size={16} />
                  View Analysis
                </button>
                <button
                  onClick={clearMlParams}
                  style={{
                    padding: '0.625rem 1rem',
                    background: 'transparent',
                    border: '2px solid #fca5a5',
                    borderRadius: '10px',
                    color: '#dc2626',
                    fontWeight: '600',
                    fontSize: '0.875rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <X size={16} />
                  Clear & Reset
                </button>
              </div>
            </div>
          )}

          {/* Special Flow Mode: Hide sidebar, show only action button and output */}
          {specialFlowActive ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              {/* Single Action Button for Special Flow */}
              <div style={{ 
                background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                borderRadius: '24px', 
                padding: '1.5rem 2rem', 
                boxShadow: '0 25px 60px rgba(139,92,246,0.08)', 
                border: '2px solid #86efac',
                backdropFilter: 'blur(20px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '1rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div style={{ 
                    width: '48px', 
                    height: '48px', 
                    borderRadius: '12px', 
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Play size={24} style={{ color: 'white' }} />
                  </div>
                  <div>
                    <h3 style={{ margin: 0, fontSize: '1.125rem', fontWeight: '700', color: '#166534' }}>Policy Configuration Applied</h3>
                    <p style={{ margin: '0.25rem 0 0', fontSize: '0.875rem', color: '#047857' }}>
                      Ready to run your first simulation with the selected preset
                    </p>
                  </div>
                </div>
                <button
                  onClick={runSimulation}
                  disabled={loading}
                  className="primary-button"
                  style={{
                    padding: '1rem 2rem',
                    opacity: loading ? 0.7 : 1,
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    boxShadow: '0 8px 24px rgba(16,185,129,0.3)',
                    fontSize: '1rem'
                  }}
                >
                  <Play size={20} />
                  {loading ? 'Running Simulation...' : 'Run First Simulation'}
                </button>
              </div>

              {/* Results/Output Panel - Full Width in Special Flow */}
              <div>
                {!results ? (
                  <div style={{ 
                    background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                    borderRadius: '24px', 
                    padding: '3rem 2rem', 
                    border: '2px dashed rgba(16,185,129,0.3)', 
                    textAlign: 'center',
                    backdropFilter: 'blur(20px)',
                    boxShadow: '0 25px 60px rgba(16,185,129,0.08)'
                  }}>
                    <div style={{ 
                      width: '72px', 
                      height: '72px', 
                      margin: '0 auto 1.5rem',
                      borderRadius: '18px',
                      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <BarChart3 size={36} style={{ color: 'white' }} />
                    </div>
                    <h3 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#166534', marginBottom: '0.5rem' }}>Awaiting First Simulation</h3>
                    <p style={{ color: '#047857', fontSize: '1rem', marginBottom: '1rem' }}>
                      Click "Run First Simulation" above to analyze the policy impact
                    </p>
                    <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
                      After the simulation completes, you'll have access to the full configuration panel
                    </p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {/* Policy Config Applied Badge */}
                    <div style={{ 
                      padding: '0.75rem 1rem', 
                      background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
                      borderRadius: '10px', 
                      border: '1px solid #86efac',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}>
                      <Settings size={16} style={{ color: '#16a34a' }} />
                      <span style={{ fontSize: '0.875rem', color: '#166534', fontWeight: '600' }}>
                        First simulation completed - Full configuration panel now available
                      </span>
                    </div>
                    
                    {/* Quick Stats */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)', 
                        borderRadius: '16px', 
                        padding: '1.25rem', 
                        boxShadow: '0 8px 24px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)' 
                      }}>
                        <p style={{ fontSize: '0.875rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Baseline Duration</p>
                        <p style={{ fontSize: '2rem', fontWeight: '700', color: '#1e1b4b', margin: 0 }}>{results.baseline.metrics.duration}<span style={{ fontSize: '1rem', color: '#64748b' }}> days</span></p>
                      </div>
                      <div style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', borderRadius: '16px', padding: '1.25rem', boxShadow: '0 8px 24px rgba(139,92,246,0.25)' }}>
                        <p style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.8)', marginBottom: '0.5rem', fontWeight: '600' }}>Policy Duration</p>
                        <p style={{ fontSize: '2rem', fontWeight: '700', color: 'white', margin: 0 }}>{results.policy.metrics.duration}<span style={{ fontSize: '1rem', color: 'rgba(255,255,255,0.7)' }}> days</span></p>
                      </div>
                      <div style={{ 
                        background: results.policy.metrics.risk_score > 50 
                          ? 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)' 
                          : 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
                        borderRadius: '16px', 
                        padding: '1.25rem', 
                        border: `1px solid ${results.policy.metrics.risk_score > 50 ? 'rgba(239,68,68,0.2)' : 'rgba(34,197,94,0.2)'}` 
                      }}>
                        <p style={{ fontSize: '0.875rem', color: results.policy.metrics.risk_score > 50 ? '#dc2626' : '#16a34a', marginBottom: '0.5rem', fontWeight: '600' }}>Risk Score</p>
                        <p style={{ fontSize: '2rem', fontWeight: '700', color: results.policy.metrics.risk_score > 50 ? '#dc2626' : '#16a34a', margin: 0 }}>{results.policy.metrics.risk_score}<span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span></p>
                      </div>
                      <div style={{ background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)', borderRadius: '16px', padding: '1.25rem', border: '1px solid rgba(217,119,6,0.2)' }}>
                        <p style={{ fontSize: '0.875rem', color: '#d97706', marginBottom: '0.5rem', fontWeight: '600' }}>Disruption Index</p>
                        <p style={{ fontSize: '2rem', fontWeight: '700', color: '#d97706', margin: 0 }}>{results.policy.metrics.disruption_index}<span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span></p>
                      </div>
                    </div>

                    {/* Analysis Summary */}
                    <div style={{ 
                      background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                      borderRadius: '20px', 
                      padding: '1.5rem', 
                      boxShadow: '0 15px 40px rgba(139,92,246,0.08)', 
                      border: '1px solid rgba(139,92,246,0.1)' 
                    }}>
                      <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '28px', height: '28px', borderRadius: '8px', background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          <BarChart3 size={16} style={{ color: 'white' }} />
                        </div>
                        Quick Analysis
                      </h4>
                      <p style={{ color: '#64748b', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                        {results.analysis?.summary || 'Simulation completed successfully. View detailed analysis in the Impact Analysis page.'}
                      </p>
                      <button
                        onClick={() => navigate('/impact-analysis')}
                        className="primary-button"
                        style={{ width: '100%', background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)', boxShadow: '0 8px 24px rgba(139,92,246,0.25)' }}
                      >
                        View Detailed Analysis
                        <ArrowRight size={18} />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            /* Normal Mode: Show sidebar and results panel */
            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(320px, 400px) 1fr', gap: '2rem' }}>
              {/* Config Panel */}
              <div style={{ 
                background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                borderRadius: '24px', 
                padding: '1.5rem', 
                boxShadow: '0 25px 60px rgba(139,92,246,0.08)', 
                border: '1px solid rgba(139,92,246,0.1)',
                backdropFilter: 'blur(20px)',
                height: 'fit-content'
              }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: '32px', height: '32px', borderRadius: '10px', background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Settings size={18} style={{ color: 'white' }} />
                  </div>
                  {mlParamsApplied ? 'ML-Configured' : 'Quick Configuration'}
                  {mlParamsApplied && (
                    <span style={{ 
                      marginLeft: 'auto', 
                      padding: '0.25rem 0.75rem', 
                      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', 
                      color: 'white', 
                      fontSize: '0.7rem', 
                      fontWeight: '700', 
                      borderRadius: '999px',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em'
                    }}>
                      <Sparkles size={12} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle' }} />
                      Auto
                    </span>
                  )}
                </h3>

              {/* Night Shifts */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#8b5cf6', marginBottom: '0.75rem' }}>Night Shifts</label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => setConfig({ ...config, night_shifts: false })}
                    style={{
                      flex: 1,
                      padding: '0.75rem',
                      borderRadius: '12px',
                      border: '2px solid',
                      fontWeight: '600',
                      fontSize: '0.875rem',
                      cursor: 'pointer',
                      background: !config.night_shifts ? 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)' : 'white',
                      color: !config.night_shifts ? 'white' : '#64748b',
                      borderColor: !config.night_shifts ? '#8b5cf6' : 'rgba(139,92,246,0.2)',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    Daylight Only
                  </button>
                  <button
                    onClick={() => setConfig({ ...config, night_shifts: true })}
                    style={{
                      flex: 1,
                      padding: '0.75rem',
                      borderRadius: '12px',
                      border: '2px solid',
                      fontWeight: '600',
                      fontSize: '0.875rem',
                      cursor: 'pointer',
                      background: config.night_shifts ? 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)' : 'white',
                      color: config.night_shifts ? 'white' : '#64748b',
                      borderColor: config.night_shifts ? '#8b5cf6' : 'rgba(139,92,246,0.2)',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    24/7 Operations
                  </button>
                </div>
              </div>

              {/* Safety Level */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#8b5cf6', marginBottom: '0.75rem' }}>Safety Level</label>
                <select
                  value={config.safety_level}
                  onChange={(e) => setConfig({ ...config, safety_level: e.target.value as any })}
                  style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '12px', color: '#1e1b4b', fontSize: '0.875rem', outline: 'none' }}
                >
                  <option value="low">Low - Cost Cutting</option>
                  <option value="standard">Standard - BIS Baseline</option>
                  <option value="high">High - International</option>
                </select>
              </div>

              {/* Urgency */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#8b5cf6', marginBottom: '0.75rem' }}>Urgency</label>
                <select
                  value={config.urgency}
                  onChange={(e) => setConfig({ ...config, urgency: e.target.value as any })}
                  style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '12px', color: '#1e1b4b', fontSize: '0.875rem', outline: 'none' }}
                >
                  <option value="standard">Standard Timeline</option>
                  <option value="high">Election Deadline</option>
                </select>
              </div>

              {/* Labor */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#8b5cf6', marginBottom: '0.75rem' }}>Labor Force</label>
                <select
                  value={config.labor}
                  onChange={(e) => setConfig({ ...config, labor: e.target.value as any })}
                  style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '12px', color: '#1e1b4b', fontSize: '0.875rem', outline: 'none' }}
                >
                  <option value="standard">Standard</option>
                  <option value="increased">Increased</option>
                </select>
              </div>

              {/* Traffic */}
              <div style={{ marginBottom: '2rem' }}>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#8b5cf6', marginBottom: '0.75rem' }}>Traffic Management</label>
                <select
                  value={config.traffic}
                  onChange={(e) => setConfig({ ...config, traffic: e.target.value as any })}
                  style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '12px', color: '#1e1b4b', fontSize: '0.875rem', outline: 'none' }}
                >
                  <option value="basic">Basic</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>

              {/* Actions */}
              <div style={{ display: 'flex', gap: '12px' }}>
                <button
                  onClick={runSimulation}
                  disabled={loading}
                  className="primary-button"
                  style={{
                    flex: 1,
                    padding: '0.875rem',
                    opacity: loading ? 0.7 : 1,
                    background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                    boxShadow: '0 8px 24px rgba(139,92,246,0.25)'
                  }}
                >
                  <Play size={18} />
                  {loading ? 'Running...' : 'Run Simulation'}
                </button>
                <button
                  onClick={resetSimulation}
                  className="secondary-button"
                  style={{ padding: '0.875rem' }}
                >
                  <RotateCcw size={18} />
                </button>
              </div>

              {/* Status */}
              <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)', borderRadius: '10px', border: '1px solid rgba(139,92,246,0.1)' }}>
                <p style={{ fontSize: '0.75rem', color: '#8b5cf6', margin: 0, fontWeight: '500' }}>
                  Status: {activeApiBase ? `Connected to ${activeApiBase}` : 'Not connected'}
                </p>
              </div>
            </div>

            {/* Results Panel */}
            <div>
              {!results ? (
                <div style={{ 
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                  borderRadius: '24px', 
                  padding: '3rem 2rem', 
                  border: mlParamsApplied ? '2px solid #86efac' : '2px dashed rgba(139,92,246,0.3)', 
                  textAlign: 'center',
                  backdropFilter: 'blur(20px)',
                  boxShadow: mlParamsApplied ? '0 25px 60px rgba(16,185,129,0.12)' : '0 25px 60px rgba(139,92,246,0.08)'
                }}>
                  {mlParamsApplied && mlParams ? (
                    <>
                      <div style={{ 
                        width: '72px', 
                        height: '72px', 
                        margin: '0 auto 1.5rem',
                        borderRadius: '18px',
                        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        <Brain size={36} style={{ color: 'white' }} />
                      </div>
                      <h3 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#166534', marginBottom: '0.5rem' }}>ML Analysis Ready</h3>
                      <p style={{ color: '#047857', fontSize: '1rem', marginBottom: '1.5rem' }}>
                        Parameters from "<strong>{mlParams.policyName}</strong>" have been applied
                      </p>
                      
                      {/* ML Summary Cards */}
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.75rem', marginBottom: '1.5rem', textAlign: 'left' }}>
                        {mlParams.trustLevel && (
                          <div style={{ 
                            padding: '1rem', 
                            background: mlParams.trustLevel.toLowerCase() === 'high' ? '#ecfdf5' : mlParams.trustLevel.toLowerCase() === 'medium' ? '#fffbeb' : '#fef2f2',
                            borderRadius: '12px',
                            border: `1px solid ${mlParams.trustLevel.toLowerCase() === 'high' ? '#a7f3d0' : mlParams.trustLevel.toLowerCase() === 'medium' ? '#fcd34d' : '#fca5a5'}`
                          }}>
                            <p style={{ margin: 0, fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Trust Level</p>
                            <p style={{ margin: '0.25rem 0 0', fontSize: '1.1rem', fontWeight: '700', textTransform: 'capitalize',
                              color: mlParams.trustLevel.toLowerCase() === 'high' ? '#059669' : mlParams.trustLevel.toLowerCase() === 'medium' ? '#d97706' : '#dc2626'
                            }}>{mlParams.trustLevel}</p>
                          </div>
                        )}
                        {mlParams.riskLevel && (
                          <div style={{ 
                            padding: '1rem', 
                            background: mlParams.riskLevel.toLowerCase() === 'low' ? '#ecfdf5' : mlParams.riskLevel.toLowerCase() === 'medium' ? '#fffbeb' : '#fef2f2',
                            borderRadius: '12px',
                            border: `1px solid ${mlParams.riskLevel.toLowerCase() === 'low' ? '#a7f3d0' : mlParams.riskLevel.toLowerCase() === 'medium' ? '#fcd34d' : '#fca5a5'}`
                          }}>
                            <p style={{ margin: 0, fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Risk Level</p>
                            <p style={{ margin: '0.25rem 0 0', fontSize: '1.1rem', fontWeight: '700', textTransform: 'capitalize',
                              color: mlParams.riskLevel.toLowerCase() === 'low' ? '#059669' : mlParams.riskLevel.toLowerCase() === 'medium' ? '#d97706' : '#dc2626'
                            }}>{mlParams.riskLevel}</p>
                          </div>
                        )}
                        {mlParams.confidence && (
                          <div style={{ padding: '1rem', background: '#eef2ff', borderRadius: '12px', border: '1px solid #c7d2fe' }}>
                            <p style={{ margin: 0, fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Confidence</p>
                            <p style={{ margin: '0.25rem 0 0', fontSize: '1.1rem', fontWeight: '700', color: '#4f46e5' }}>{Math.round(mlParams.confidence * 100)}%</p>
                          </div>
                        )}
                        {mlParams.classification && (
                          <div style={{ padding: '1rem', background: '#faf5ff', borderRadius: '12px', border: '1px solid #e9d5ff' }}>
                            <p style={{ margin: 0, fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Type</p>
                            <p style={{ margin: '0.25rem 0 0', fontSize: '0.95rem', fontWeight: '700', color: '#7c3aed' }}>{mlParams.classification}</p>
                          </div>
                        )}
                      </div>
                      
                      <p style={{ color: '#64748b', fontSize: '0.9rem' }}>
                        Click "Run Simulation" to analyze policy impact
                      </p>
                    </>
                  ) : (
                    <>
                      <div style={{ 
                        width: '72px', 
                        height: '72px', 
                        margin: '0 auto 1.5rem',
                        borderRadius: '18px',
                        background: 'linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        <Play size={36} style={{ color: '#8b5cf6' }} />
                      </div>
                      <h3 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e1b4b', marginBottom: '0.5rem' }}>Ready to Run</h3>
                      <p style={{ color: '#64748b', fontSize: '1rem', marginBottom: '1.5rem' }}>
                        Configure your parameters and click "Run Simulation" to see results
                      </p>
                      <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                        💡 Tip: Use <button onClick={() => navigate('/ml-analysis')} style={{ color: '#8b5cf6', fontWeight: '600', background: 'none', border: 'none', cursor: 'pointer', padding: 0, textDecoration: 'underline' }}>ML Analysis</button> to auto-configure from policy documents
                      </p>
                    </>
                  )}
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                  {/* ML Analysis Badge if applicable */}
                  {mlParamsApplied && mlParams && (
                    <div style={{ 
                      padding: '0.75rem 1rem', 
                      background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
                      borderRadius: '10px', 
                      border: '1px solid #86efac',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}>
                      <Brain size={16} style={{ color: '#16a34a' }} />
                      <span style={{ fontSize: '0.875rem', color: '#166534', fontWeight: '600' }}>
                        Results based on ML analysis of "{mlParams.policyName}"
                      </span>
                    </div>
                  )}
                  
                  {/* Quick Stats */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
                    <div style={{ 
                      background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)', 
                      borderRadius: '16px', 
                      padding: '1.25rem', 
                      boxShadow: '0 8px 24px rgba(139,92,246,0.08)', 
                      border: '1px solid rgba(139,92,246,0.1)' 
                    }}>
                      <p style={{ fontSize: '0.875rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Baseline Duration</p>
                      <p style={{ fontSize: '2rem', fontWeight: '700', color: '#1e1b4b', margin: 0 }}>{results.baseline.metrics.duration}<span style={{ fontSize: '1rem', color: '#64748b' }}> days</span></p>
                    </div>
                    <div style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', borderRadius: '16px', padding: '1.25rem', boxShadow: '0 8px 24px rgba(139,92,246,0.25)' }}>
                      <p style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.8)', marginBottom: '0.5rem', fontWeight: '600' }}>Policy Duration</p>
                      <p style={{ fontSize: '2rem', fontWeight: '700', color: 'white', margin: 0 }}>{results.policy.metrics.duration}<span style={{ fontSize: '1rem', color: 'rgba(255,255,255,0.7)' }}> days</span></p>
                    </div>
                    <div style={{ 
                      background: results.policy.metrics.risk_score > 50 
                        ? 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)' 
                        : 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
                      borderRadius: '16px', 
                      padding: '1.25rem', 
                      border: `1px solid ${results.policy.metrics.risk_score > 50 ? 'rgba(239,68,68,0.2)' : 'rgba(34,197,94,0.2)'}` 
                    }}>
                      <p style={{ fontSize: '0.875rem', color: results.policy.metrics.risk_score > 50 ? '#dc2626' : '#16a34a', marginBottom: '0.5rem', fontWeight: '600' }}>Risk Score</p>
                      <p style={{ fontSize: '2rem', fontWeight: '700', color: results.policy.metrics.risk_score > 50 ? '#dc2626' : '#16a34a', margin: 0 }}>{results.policy.metrics.risk_score}<span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span></p>
                    </div>
                    <div style={{ background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)', borderRadius: '16px', padding: '1.25rem', border: '1px solid rgba(217,119,6,0.2)' }}>
                      <p style={{ fontSize: '0.875rem', color: '#d97706', marginBottom: '0.5rem', fontWeight: '600' }}>Disruption Index</p>
                      <p style={{ fontSize: '2rem', fontWeight: '700', color: '#d97706', margin: 0 }}>{results.policy.metrics.disruption_index}<span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span></p>
                    </div>
                  </div>

                  {/* Analysis Summary */}
                  <div style={{ 
                    background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                    borderRadius: '20px', 
                    padding: '1.5rem', 
                    boxShadow: '0 15px 40px rgba(139,92,246,0.08)', 
                    border: '1px solid rgba(139,92,246,0.1)' 
                  }}>
                    <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '28px', height: '28px', borderRadius: '8px', background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <BarChart3 size={16} style={{ color: 'white' }} />
                      </div>
                      Quick Analysis
                    </h4>
                    <p style={{ color: '#64748b', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                      {results.analysis?.summary || 'Simulation completed successfully. View detailed analysis in the Impact Analysis page.'}
                    </p>
                    <button
                      onClick={() => navigate('/impact-analysis')}
                      className="primary-button"
                      style={{ width: '100%', background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)', boxShadow: '0 8px 24px rgba(139,92,246,0.25)' }}
                    >
                      View Detailed Analysis
                      <ArrowRight size={18} />
                    </button>
                  </div>

                  {/* Time Savings */}
                  {results.baseline.metrics.duration !== results.policy.metrics.duration && (
                    <div style={{
                      background: results.policy.metrics.duration < results.baseline.metrics.duration 
                        ? 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)' 
                        : 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
                      borderRadius: '16px',
                      padding: '1.5rem',
                      border: `1px solid ${results.policy.metrics.duration < results.baseline.metrics.duration ? 'rgba(34,197,94,0.2)' : 'rgba(239,68,68,0.2)'}`
                    }}>
                      <p style={{ fontSize: '1.125rem', color: '#1e1b4b', margin: 0 }}>
                        {results.policy.metrics.duration < results.baseline.metrics.duration ? '🎉' : '⚠️'} 
                        {' '}Policy {results.policy.metrics.duration < results.baseline.metrics.duration ? 'saves' : 'adds'}{' '}
                        <span style={{ fontWeight: '700', fontSize: '1.5rem', color: results.policy.metrics.duration < results.baseline.metrics.duration ? '#16a34a' : '#dc2626' }}>
                          {Math.abs(results.baseline.metrics.duration - results.policy.metrics.duration)}
                        </span>{' '}
                        days compared to baseline
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer style={{ background: 'linear-gradient(135deg, #faf5ff 0%, #ede9fe 100%)', borderTop: '1px solid rgba(139,92,246,0.1)', padding: '1.5rem' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', textAlign: 'center' }}>
          <p style={{ color: '#7c3aed', fontSize: '0.875rem', margin: 0, fontWeight: '500' }}>
            🏛️ CIVISIM - Civic Intelligence Platform • Simulation Engine
          </p>
        </div>
      </footer>
    </div>
  )
}

export default SimulationEnginePage
