import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Home, TrendingUp, AlertTriangle, Shield, Clock, Building2, Brain, BarChart3, Layers, RefreshCw, Trash2 } from 'lucide-react'
import { SimulationResults } from '../types/simulation'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts'

function ImpactAnalysisPage() {
  const navigate = useNavigate()
  const [results, setResults] = useState<SimulationResults[]>([])
  const [selectedResult, setSelectedResult] = useState<SimulationResults | null>(null)

  // Load results from localStorage
  const loadResults = () => {
    const stored = localStorage.getItem('simulation_results')
    if (stored) {
      try {
        const parsed = JSON.parse(stored)
        setResults(parsed)
        if (parsed.length > 0) {
          setSelectedResult(parsed[parsed.length - 1]) // Select the latest result
        }
      } catch (e) {
        console.error('Failed to parse simulation results:', e)
      }
    }
  }

  useEffect(() => {
    // Initial load
    loadResults()

    // Listen for storage changes (when other tabs/windows update localStorage)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'simulation_results') {
        loadResults()
      }
    }

    // Listen for custom event (when same tab updates localStorage)
    const handleCustomStorageChange = () => {
      loadResults()
    }

    window.addEventListener('storage', handleStorageChange)
    window.addEventListener('simulation_results_updated', handleCustomStorageChange)

    return () => {
      window.removeEventListener('storage', handleStorageChange)
      window.removeEventListener('simulation_results_updated', handleCustomStorageChange)
    }
  }, [])

  const formatDate = (timestamp?: string) => {
    if (!timestamp) return 'Unknown date'
    return new Date(timestamp).toLocaleString()
  }

  // Memoize comparison data based on selectedResult
  const comparisonData = selectedResult ? [
    { 
      name: 'Duration', 
      Baseline: Number(selectedResult.baseline.metrics.duration.toFixed(1)), 
      Policy: Number(selectedResult.policy.metrics.duration.toFixed(1)) 
    },
    { 
      name: 'Risk Score', 
      Baseline: Number(selectedResult.baseline.metrics.risk_score.toFixed(1)), 
      Policy: Number(selectedResult.policy.metrics.risk_score.toFixed(1)) 
    },
    { 
      name: 'Disruption', 
      Baseline: Number(selectedResult.baseline.metrics.disruption_index.toFixed(1)), 
      Policy: Number(selectedResult.policy.metrics.disruption_index.toFixed(1)) 
    },
  ] : []

  // Memoize radar data based on selectedResult
  const radarData = selectedResult ? (() => {
    const maxDuration = Math.max(selectedResult.baseline.metrics.duration, selectedResult.policy.metrics.duration)
    const config = (selectedResult as any).config || {}
    
    // Calculate efficiency based on actual config
    const efficiencyBonus = config.night_shifts ? 15 : 0
    const urgencyBonus = config.urgency === 'high' ? 10 : config.urgency === 'low' ? -10 : 0
    const laborBonus = config.labor === 'increased' ? 10 : config.labor === 'reduced' ? -10 : 0
    
    // Calculate compliance based on safety level
    const complianceScore = config.safety_level === 'high' ? 95 : config.safety_level === 'standard' ? 80 : 65
    
    return [
      { 
        metric: 'Timeline', 
        baseline: Number(((selectedResult.baseline.metrics.duration / maxDuration) * 100).toFixed(1)), 
        policy: Number(((selectedResult.policy.metrics.duration / maxDuration) * 100).toFixed(1)) 
      },
      { 
        metric: 'Safety', 
        baseline: Number((100 - selectedResult.baseline.metrics.risk_score).toFixed(1)), 
        policy: Number((100 - selectedResult.policy.metrics.risk_score).toFixed(1)) 
      },
      { 
        metric: 'Community', 
        baseline: Number((100 - selectedResult.baseline.metrics.disruption_index).toFixed(1)), 
        policy: Number((100 - selectedResult.policy.metrics.disruption_index).toFixed(1)) 
      },
      { 
        metric: 'Efficiency', 
        baseline: 70, 
        policy: Math.min(100, 70 + efficiencyBonus + urgencyBonus + laborBonus) 
      },
      { 
        metric: 'Compliance', 
        baseline: 75, 
        policy: complianceScore 
      },
    ]
  })() : []

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
              <div className="brand-icon" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', color: 'white', fontSize: '1.25rem' }}>📊</div>
              <div className="brand-meta">
                <p className="brand-tagline" style={{ color: '#8b5cf6', fontWeight: '600' }}>ANALYTICS LAB</p>
                <h1 className="brand-title" style={{ fontSize: '1.25rem', background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>CIVISIM</h1>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button onClick={() => navigate('/')} className="secondary-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Home size={16} />
                Home
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
            <TrendingUp size={16} />
            Impact & Analytics
          </div>
          <h2 style={{ fontSize: '2.5rem', fontWeight: '700', marginBottom: '1rem', background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Impact Analysis
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#64748b', maxWidth: '700px', margin: '0 auto' }}>
            Compare simulation results and understand the trade-offs between policy configurations
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="app-main" style={{ padding: '2rem' }}>
        <div className="layout-container" style={{ maxWidth: '1400px', margin: '0 auto' }}>
          {results.length === 0 ? (
            <div style={{ 
              background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
              borderRadius: '24px', 
              padding: '4rem 2rem', 
              border: '2px dashed rgba(139,92,246,0.3)', 
              textAlign: 'center',
              backdropFilter: 'blur(20px)',
              boxShadow: '0 25px 60px rgba(139,92,246,0.08)'
            }}>
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
                <BarChart3 size={36} style={{ color: '#8b5cf6' }} />
              </div>
              <h3 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e1b4b', marginBottom: '0.5rem' }}>No Simulation Results</h3>
              <p style={{ color: '#64748b', marginBottom: '2rem', fontSize: '1rem' }}>
                Run a simulation first to see impact analysis
              </p>
              <button
                onClick={() => navigate('/simulation-engine')}
                className="primary-button"
                style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', padding: '1rem 2rem', boxShadow: '0 20px 40px rgba(139,92,246,0.3)' }}
              >
                Go to Simulation Engine
              </button>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '2rem' }}>
              {/* History Panel */}
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '0.75rem',
                background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)',
                borderRadius: '20px',
                padding: '1.5rem',
                border: '1px solid rgba(139,92,246,0.1)',
                backdropFilter: 'blur(20px)',
                boxShadow: '0 20px 50px rgba(139,92,246,0.08)',
                height: 'fit-content'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Layers size={20} style={{ color: '#8b5cf6' }} />
                    Recent Simulations
                  </h3>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      onClick={loadResults}
                      style={{
                        padding: '8px',
                        background: 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)',
                        border: '1px solid rgba(139,92,246,0.2)',
                        borderRadius: '10px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        transition: 'all 0.2s ease'
                      }}
                      title="Refresh"
                    >
                      <RefreshCw size={14} color="#8b5cf6" />
                    </button>
                    <button
                      onClick={() => {
                        if (confirm('Clear all simulation history?')) {
                          localStorage.removeItem('simulation_results')
                          setResults([])
                          setSelectedResult(null)
                        }
                      }}
                      style={{
                        padding: '8px',
                        background: 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
                        border: '1px solid rgba(239,68,68,0.2)',
                        borderRadius: '10px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        transition: 'all 0.2s ease'
                      }}
                      title="Clear History"
                    >
                      <Trash2 size={14} color="#ef4444" />
                    </button>
                  </div>
                </div>
                <p style={{ fontSize: '0.75rem', color: '#8b5cf6', margin: '0 0 0.5rem', fontWeight: '500' }}>{results.length} simulation(s) recorded</p>
                {results.map((result, index) => (
                  <div
                    key={`${result.timestamp}-${index}`}
                    onClick={() => setSelectedResult(result)}
                    style={{
                      padding: '1rem',
                      background: selectedResult === result 
                        ? 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)' 
                        : 'white',
                      borderRadius: '14px',
                      border: selectedResult === result 
                        ? '2px solid #8b5cf6' 
                        : '1px solid rgba(139,92,246,0.1)',
                      cursor: 'pointer',
                      boxShadow: selectedResult === result 
                        ? '0 8px 24px rgba(139,92,246,0.15)' 
                        : '0 2px 8px rgba(0,0,0,0.03)',
                      transition: 'all 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                      if (selectedResult !== result) {
                        e.currentTarget.style.background = 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)';
                        e.currentTarget.style.borderColor = 'rgba(139,92,246,0.3)';
                        e.currentTarget.style.transform = 'translateY(-2px)';
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (selectedResult !== result) {
                        e.currentTarget.style.background = 'white';
                        e.currentTarget.style.borderColor = 'rgba(139,92,246,0.1)';
                        e.currentTarget.style.transform = 'translateY(0)';
                      }
                    }}
                  >
                    <p style={{ fontSize: '0.75rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '500' }}>{formatDate(result.timestamp)}</p>
                    <p style={{ fontSize: '0.9375rem', color: '#1e1b4b', fontWeight: '600', margin: '0 0 0.5rem' }}>
                      Risk: {result.policy.metrics.risk_score.toFixed(1)} | {result.policy.metrics.duration.toFixed(0)} days
                    </p>
                    {(result as any).config && (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginTop: '0.5rem' }}>
                        {(result as any).config.night_shifts && (
                          <span style={{ fontSize: '0.65rem', background: '#fef3c7', color: '#92400e', padding: '2px 6px', borderRadius: '4px' }}>Night</span>
                        )}
                        <span style={{ fontSize: '0.65rem', background: '#e0f2fe', color: '#0369a1', padding: '2px 6px', borderRadius: '4px' }}>
                          {(result as any).config.safety_level}
                        </span>
                        <span style={{ fontSize: '0.65rem', background: '#f3e8ff', color: '#7c3aed', padding: '2px 6px', borderRadius: '4px' }}>
                          {(result as any).config.urgency}
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Analysis Panel */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {selectedResult && (
                  <>
                    {/* Quick Stats */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)', 
                        borderRadius: '16px', 
                        padding: '1.25rem', 
                        boxShadow: '0 8px 24px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)',
                        backdropFilter: 'blur(10px)'
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem' }}>
                          <div style={{ width: '32px', height: '32px', borderRadius: '10px', background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Clock size={16} style={{ color: 'white' }} />
                          </div>
                          <p style={{ fontSize: '0.8125rem', color: '#64748b', margin: 0, fontWeight: '500' }}>Time Saved</p>
                        </div>
                        <p style={{ fontSize: '1.75rem', fontWeight: '700', color: selectedResult.baseline.metrics.duration - selectedResult.policy.metrics.duration > 0 ? '#16a34a' : '#f59e0b', margin: 0 }}>
                          {selectedResult.baseline.metrics.duration - selectedResult.policy.metrics.duration}
                          <span style={{ fontSize: '1rem', color: '#64748b' }}> days</span>
                        </p>
                      </div>
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)', 
                        borderRadius: '16px', 
                        padding: '1.25rem', 
                        boxShadow: '0 8px 24px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)',
                        backdropFilter: 'blur(10px)'
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem' }}>
                          <div style={{ width: '32px', height: '32px', borderRadius: '10px', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Shield size={16} style={{ color: 'white' }} />
                          </div>
                          <p style={{ fontSize: '0.8125rem', color: '#64748b', margin: 0, fontWeight: '500' }}>Risk Delta</p>
                        </div>
                        <p style={{ fontSize: '1.75rem', fontWeight: '700', color: selectedResult.policy.metrics.risk_score - selectedResult.baseline.metrics.risk_score < 0 ? '#16a34a' : '#dc2626', margin: 0 }}>
                          {selectedResult.policy.metrics.risk_score - selectedResult.baseline.metrics.risk_score > 0 ? '+' : ''}
                          {selectedResult.policy.metrics.risk_score - selectedResult.baseline.metrics.risk_score}
                          <span style={{ fontSize: '1rem', color: '#64748b' }}> pts</span>
                        </p>
                      </div>
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)', 
                        borderRadius: '16px', 
                        padding: '1.25rem', 
                        boxShadow: '0 8px 24px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)',
                        backdropFilter: 'blur(10px)'
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem' }}>
                          <div style={{ width: '32px', height: '32px', borderRadius: '10px', background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <TrendingUp size={16} style={{ color: 'white' }} />
                          </div>
                          <p style={{ fontSize: '0.8125rem', color: '#64748b', margin: 0, fontWeight: '500' }}>Disruption</p>
                        </div>
                        <p style={{ fontSize: '1.75rem', fontWeight: '700', color: '#1e1b4b', margin: 0 }}>
                          {selectedResult.policy.metrics.disruption_index}
                          <span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span>
                        </p>
                      </div>
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)', 
                        borderRadius: '16px', 
                        padding: '1.25rem', 
                        boxShadow: '0 8px 24px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)',
                        backdropFilter: 'blur(10px)'
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem' }}>
                          <div style={{ width: '32px', height: '32px', borderRadius: '10px', background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <AlertTriangle size={16} style={{ color: 'white' }} />
                          </div>
                          <p style={{ fontSize: '0.8125rem', color: '#64748b', margin: 0, fontWeight: '500' }}>Policy Risk</p>
                        </div>
                        <p style={{ fontSize: '1.75rem', fontWeight: '700', color: selectedResult.policy.metrics.risk_score > 50 ? '#dc2626' : '#16a34a', margin: 0 }}>
                          {selectedResult.policy.metrics.risk_score}
                          <span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span>
                        </p>
                      </div>
                    </div>

                    {/* Charts */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem' }}>
                      {/* Comparison Bar Chart */}
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                        borderRadius: '20px', 
                        padding: '1.5rem', 
                        boxShadow: '0 15px 40px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)',
                        backdropFilter: 'blur(20px)'
                      }}>
                        <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1.25rem' }}>Baseline vs Policy Comparison</h4>
                        <ResponsiveContainer width="100%" height={280}>
                          <BarChart data={comparisonData} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                            <XAxis dataKey="name" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={{ stroke: '#e2e8f0' }} />
                            <YAxis tick={{ fill: '#64748b', fontSize: 12 }} axisLine={{ stroke: '#e2e8f0' }} />
                            <Tooltip contentStyle={{ background: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', color: '#0f172a' }} />
                            <Legend />
                            <Bar dataKey="Baseline" fill="#94a3b8" radius={[4, 4, 0, 0]} />
                            <Bar dataKey="Policy" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>

                      {/* Radar Chart */}
                      <div style={{ 
                        background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                        borderRadius: '20px', 
                        padding: '1.5rem', 
                        boxShadow: '0 15px 40px rgba(139,92,246,0.08)', 
                        border: '1px solid rgba(139,92,246,0.1)',
                        backdropFilter: 'blur(20px)'
                      }}>
                        <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1.25rem' }}>Multi-dimensional Analysis</h4>
                        <ResponsiveContainer width="100%" height={280}>
                          <RadarChart data={radarData}>
                            <PolarGrid stroke="#e2e8f0" />
                            <PolarAngleAxis dataKey="metric" tick={{ fill: '#64748b', fontSize: 12 }} />
                            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 10 }} />
                            <Radar name="Baseline" dataKey="baseline" stroke="#94a3b8" fill="#94a3b8" fillOpacity={0.3} />
                            <Radar name="Policy" dataKey="policy" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.4} />
                            <Legend />
                          </RadarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* Analysis Summary */}
                    <div style={{ 
                      background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                      borderRadius: '20px', 
                      padding: '1.5rem', 
                      boxShadow: '0 15px 40px rgba(139,92,246,0.08)', 
                      border: '1px solid rgba(139,92,246,0.1)',
                      backdropFilter: 'blur(20px)'
                    }}>
                      <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1rem' }}>Analysis Summary</h4>
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
                        <div>
                          <p style={{ fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Timeline Impact</p>
                          <p style={{ fontSize: '1rem', color: '#1e1b4b', lineHeight: '1.5', margin: 0 }}>
                            {selectedResult.policy.metrics.duration < selectedResult.baseline.metrics.duration
                              ? `Project completion accelerated by ${selectedResult.baseline.metrics.duration - selectedResult.policy.metrics.duration} days through policy optimizations.`
                              : selectedResult.policy.metrics.duration > selectedResult.baseline.metrics.duration
                              ? `Project duration increased by ${selectedResult.policy.metrics.duration - selectedResult.baseline.metrics.duration} days due to additional requirements.`
                              : 'No significant change in project timeline.'}
                          </p>
                        </div>
                        <div>
                          <p style={{ fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Safety Assessment</p>
                          <p style={{ fontSize: '1rem', color: '#1e1b4b', lineHeight: '1.5', margin: 0 }}>
                            {selectedResult.policy.metrics.risk_score < 30
                              ? 'Low risk configuration with strong safety protocols in place.'
                              : selectedResult.policy.metrics.risk_score < 60
                              ? 'Moderate risk level - standard safety measures recommended.'
                              : 'High risk detected - enhanced safety protocols required.'}
                          </p>
                        </div>
                        <div>
                          <p style={{ fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Community Impact</p>
                          <p style={{ fontSize: '1rem', color: '#1e1b4b', lineHeight: '1.5', margin: 0 }}>
                            {selectedResult.policy.metrics.disruption_index < 30
                              ? 'Minimal community disruption expected during construction.'
                              : selectedResult.policy.metrics.disruption_index < 60
                              ? 'Moderate disruption - community engagement recommended.'
                              : 'Significant community impact - mitigation strategies needed.'}
                          </p>
                        </div>
                      </div>
                    </div>
                  </>
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
            🏛️ CIVISIM - Civic Intelligence Platform • Analytics & Impact Assessment
          </p>
        </div>
      </footer>
    </div>
  )
}

export default ImpactAnalysisPage
