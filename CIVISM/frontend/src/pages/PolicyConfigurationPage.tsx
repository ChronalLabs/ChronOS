import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Home, Save, Trash2, FileText, Plus, Building2, Brain, Settings, Edit2, CheckCircle, AlertTriangle, Sparkles, ArrowRight, Play } from 'lucide-react'
import { SimulationConfig } from '../types/simulation'

interface ConfigPreset {
  id: string
  name: string
  description: string
  config: SimulationConfig
  createdAt: string
}

const defaultPresets: ConfigPreset[] = [
  {
    id: 'fast-track',
    name: 'Fast Track Development',
    description: 'Aggressive timeline with 24/7 operations for election deadlines',
    config: {
      night_shifts: true,
      safety_level: 'standard',
      urgency: 'high',
      labor: 'increased',
      traffic: 'advanced',
    },
    createdAt: new Date().toISOString(),
  },
  {
    id: 'safety-first',
    name: 'Safety First Protocol',
    description: 'International safety standards with standard timeline',
    config: {
      night_shifts: false,
      safety_level: 'high',
      urgency: 'standard',
      labor: 'standard',
      traffic: 'basic',
    },
    createdAt: new Date().toISOString(),
  },
  {
    id: 'budget-conscious',
    name: 'Budget Conscious',
    description: 'Balanced approach optimizing cost without compromising safety',
    config: {
      night_shifts: false,
      safety_level: 'standard',
      urgency: 'standard',
      labor: 'standard',
      traffic: 'basic',
    },
    createdAt: new Date().toISOString(),
  },
]

function PolicyConfigurationPage() {
  const navigate = useNavigate()
  const [presets, setPresets] = useState<ConfigPreset[]>([])
  const [selectedPreset, setSelectedPreset] = useState<ConfigPreset | null>(null)
  const [isEditing, setIsEditing] = useState(false)
  const [editedConfig, setEditedConfig] = useState<SimulationConfig | null>(null)
  const [newPresetName, setNewPresetName] = useState('')
  const [newPresetDescription, setNewPresetDescription] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [savedNotification, setSavedNotification] = useState(false)
  const [mlParams, setMlParams] = useState<any>(null)
  const [showMlBanner, setShowMlBanner] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('policy_presets')
    if (stored) {
      setPresets(JSON.parse(stored))
    } else {
      setPresets(defaultPresets)
      localStorage.setItem('policy_presets', JSON.stringify(defaultPresets))
    }
    
    // Check for ML analysis params
    const mlStored = localStorage.getItem('ml_analysis_params')
    if (mlStored) {
      try {
        const params = JSON.parse(mlStored)
        setMlParams(params)
        setShowMlBanner(true)
      } catch (e) {
        console.error('Failed to parse ML params:', e)
      }
    }
  }, [])
  
  const createPresetFromML = () => {
    if (!mlParams) return
    
    // Convert ML params to SimulationConfig
    const mlConfig: SimulationConfig = {
      night_shifts: mlParams.speedProfile?.night_work_allowed || false,
      safety_level: mlParams.safetyProfile?.mandatory_training ? 'high' : 
                    mlParams.riskLevel?.toLowerCase() === 'high' ? 'high' : 'standard',
      urgency: mlParams.speedProfile?.priority === 'high' ? 'high' : 'standard',
      labor: mlParams.speedProfile?.expedited ? 'increased' : 'standard',
      traffic: mlParams.zoneConstraints?.traffic_restrictions ? 'advanced' : 'basic',
    }
    
    const newPreset: ConfigPreset = {
      id: `ml-${Date.now()}`,
      name: mlParams.policyName || 'ML Generated Config',
      description: `Auto-generated from ML analysis. Classification: ${mlParams.classification || 'N/A'}. Confidence: ${mlParams.confidence ? Math.round(mlParams.confidence * 100) + '%' : 'N/A'}`,
      config: mlConfig,
      createdAt: new Date().toISOString(),
    }
    
    const updated = [...presets, newPreset]
    savePresets(updated)
    handleSelectPreset(newPreset)
    setShowMlBanner(false)
    showSavedNotification()
  }

  const savePresets = (updated: ConfigPreset[]) => {
    setPresets(updated)
    localStorage.setItem('policy_presets', JSON.stringify(updated))
  }

  const handleSelectPreset = (preset: ConfigPreset) => {
    setSelectedPreset(preset)
    setEditedConfig(preset.config)
    setIsEditing(false)
    setShowCreateForm(false)
  }

  const handleSaveEdit = () => {
    if (!selectedPreset || !editedConfig) return
    const updated = presets.map((p) =>
      p.id === selectedPreset.id ? { ...p, config: editedConfig } : p
    )
    savePresets(updated)
    setSelectedPreset({ ...selectedPreset, config: editedConfig })
    setIsEditing(false)
    showSavedNotification()
  }

  const handleCreatePreset = () => {
    if (!newPresetName.trim()) return
    const newPreset: ConfigPreset = {
      id: `custom-${Date.now()}`,
      name: newPresetName,
      description: newPresetDescription || 'Custom configuration preset',
      config: {
        night_shifts: false,
        safety_level: 'standard',
        urgency: 'standard',
        labor: 'standard',
        traffic: 'basic',
      },
      createdAt: new Date().toISOString(),
    }
    const updated = [...presets, newPreset]
    savePresets(updated)
    setNewPresetName('')
    setNewPresetDescription('')
    setShowCreateForm(false)
    handleSelectPreset(newPreset)
    showSavedNotification()
  }

  const handleDeletePreset = (presetId: string) => {
    const updated = presets.filter((p) => p.id !== presetId)
    savePresets(updated)
    if (selectedPreset?.id === presetId) {
      setSelectedPreset(null)
      setEditedConfig(null)
    }
  }

  const handleApplyToSimulation = () => {
    if (selectedPreset) {
      localStorage.setItem('active_simulation_config', JSON.stringify(selectedPreset.config))
      // Only set special flow flag if user came from ML Analysis (mlParams exists)
      // This ensures the sidebar is hidden only when navigating via ML Analysis -> Policy Config -> Simulation
      if (mlParams) {
        localStorage.setItem('first_simulation_special_flow', 'true')
      }
      navigate('/simulation-engine')
    }
  }

  const showSavedNotification = () => {
    setSavedNotification(true)
    setTimeout(() => setSavedNotification(false), 2000)
  }

  return (
    <div className="app" style={{ background: 'linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)' }}>
      {/* Saved Notification */}
      {savedNotification && (
        <div style={{ position: 'fixed', top: '20px', right: '20px', display: 'flex', alignItems: 'center', gap: '8px', padding: '1rem 1.5rem', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', borderRadius: '14px', color: 'white', fontWeight: '600', zIndex: 100, boxShadow: '0 15px 40px rgba(16,185,129,0.3)' }}>
          <CheckCircle size={20} />
          Saved successfully!
        </div>
      )}

      {/* Premium Header */}
      <header className="app-header" style={{ minHeight: 'auto', padding: '0', position: 'relative', overflow: 'hidden' }}>
        <div className="app-header__bg" style={{ background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 30%, #ede9fe 70%, #e0e7ff 100%)' }} />
        <div className="app-header__glow app-header__glow--right" style={{ background: 'rgba(139, 92, 246, 0.15)', width: '20rem', height: '20rem' }} />
        <div className="app-header__glow app-header__glow--left" style={{ background: 'rgba(99, 102, 241, 0.12)', width: '24rem', height: '24rem' }} />
        
        <div className="app-header__content" style={{ padding: '1.5rem 2rem', position: 'relative', zIndex: 1 }}>
          <nav className="navbar" style={{ borderBottom: 'none', maxWidth: '1400px', margin: '0 auto' }}>
            <div className="navbar__brand">
              <div className="brand-icon" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', color: 'white', fontSize: '1.25rem' }}>⚙️</div>
              <div className="brand-meta">
                <p className="brand-tagline" style={{ color: '#8b5cf6', fontWeight: '600' }}>CONFIGURATION LAB</p>
                <h1 className="brand-title" style={{ fontSize: '1.25rem', background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>CIVISIM</h1>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button onClick={() => navigate('/')} className="secondary-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Home size={16} />
                Home
              </button>
              <button 
                onClick={() => navigate('/simulation-engine')} 
                className="secondary-button"
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <Play size={16} />
                Simulation
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
            <Settings size={16} />
            Policy Management
          </div>
          <h2 style={{ fontSize: '2.5rem', fontWeight: '700', marginBottom: '1rem', background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Policy Configuration
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#64748b', maxWidth: '700px', margin: '0 auto' }}>
            Manage and create policy presets for rapid scenario simulation and analysis
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="app-main" style={{ padding: '2rem' }}>
        <div className="layout-container" style={{ maxWidth: '1400px', margin: '0 auto' }}>
          
          {/* ML Analysis Banner */}
          {showMlBanner && mlParams && (
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
                    <Sparkles size={16} style={{ color: '#16a34a' }} />
                    <span style={{ fontWeight: '700', color: '#166534', fontSize: '1rem' }}>ML Analysis Available</span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.875rem', color: '#047857' }}>
                    Policy: <span style={{ fontWeight: '600' }}>{mlParams.policyName}</span>
                    {mlParams.classification && <> • Type: <span style={{ fontWeight: '600' }}>{mlParams.classification}</span></>}
                  </p>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                <button
                  onClick={createPresetFromML}
                  style={{
                    padding: '0.75rem 1.25rem',
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    border: 'none',
                    borderRadius: '10px',
                    color: 'white',
                    fontWeight: '600',
                    fontSize: '0.875rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    boxShadow: '0 8px 20px rgba(16,185,129,0.3)',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <Plus size={16} />
                  Create Preset from ML
                </button>
                <button
                  onClick={() => navigate('/simulation-engine')}
                  style={{
                    padding: '0.75rem 1.25rem',
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
                  <Play size={16} />
                  Run Simulation
                </button>
                <button
                  onClick={() => setShowMlBanner(false)}
                  style={{
                    padding: '0.625rem',
                    background: 'transparent',
                    border: '1px solid #fca5a5',
                    borderRadius: '8px',
                    color: '#dc2626',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.25rem',
                    lineHeight: 1,
                    width: '36px',
                    height: '36px',
                    transition: 'all 0.2s ease'
                  }}
                >
                  ×
                </button>
              </div>
            </div>
          )}
          
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 350px) 1fr', gap: '2rem' }}>
            {/* Preset List */}
            <div style={{ 
              display: 'flex', 
              flexDirection: 'column', 
              gap: '1rem',
              background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)',
              borderRadius: '20px',
              padding: '1.5rem',
              border: '1px solid rgba(139,92,246,0.1)',
              backdropFilter: 'blur(20px)',
              boxShadow: '0 20px 50px rgba(139,92,246,0.08)',
              height: 'fit-content'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', margin: 0 }}>Policy Presets</h3>
                <button
                  onClick={() => setShowCreateForm(true)}
                  className="primary-button"
                  style={{ padding: '0.5rem 0.75rem', fontSize: '0.875rem', background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', boxShadow: '0 8px 20px rgba(139,92,246,0.25)' }}
                >
                  <Plus size={16} />
                  New
                </button>
              </div>

              {/* Preset Cards */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {presets.map((preset) => (
                  <div
                    key={preset.id}
                    onClick={() => handleSelectPreset(preset)}
                    style={{
                      padding: '1rem',
                      background: selectedPreset?.id === preset.id 
                        ? 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)' 
                        : 'white',
                      borderRadius: '14px',
                      border: selectedPreset?.id === preset.id 
                        ? '2px solid #8b5cf6' 
                        : '1px solid rgba(139,92,246,0.1)',
                      cursor: 'pointer',
                      transition: 'all 0.3s',
                      boxShadow: selectedPreset?.id === preset.id 
                        ? '0 8px 24px rgba(139,92,246,0.15)' 
                        : '0 2px 8px rgba(0,0,0,0.03)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '28px', height: '28px', borderRadius: '8px', background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          <FileText size={14} style={{ color: 'white' }} />
                        </div>
                        <h4 style={{ fontSize: '0.9375rem', fontWeight: '600', color: '#1e1b4b', margin: 0 }}>{preset.name}</h4>
                      </div>
                      {preset.id.startsWith('custom-') && (
                        <button
                          onClick={(e) => { e.stopPropagation(); handleDeletePreset(preset.id) }}
                          style={{ padding: '4px', background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
                        >
                          <Trash2 size={14} />
                        </button>
                      )}
                    </div>
                    <p style={{ fontSize: '0.8125rem', color: '#64748b', lineHeight: '1.4', margin: 0 }}>
                      {preset.description}
                    </p>
                  </div>
                ))}
              </div>

              {/* Create Form */}
              {showCreateForm && (
                <div style={{ padding: '1.25rem', background: 'white', borderRadius: '14px', border: '1px solid rgba(139,92,246,0.15)', boxShadow: '0 8px 24px rgba(139,92,246,0.1)' }}>
                  <h4 style={{ fontSize: '1rem', fontWeight: '600', color: '#1e1b4b', marginBottom: '1rem' }}>Create New Preset</h4>
                  <input
                    type="text"
                    placeholder="Preset name"
                    value={newPresetName}
                    onChange={(e) => setNewPresetName(e.target.value)}
                    style={{ width: '100%', padding: '0.75rem', marginBottom: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.875rem', outline: 'none', transition: 'border-color 0.2s' }}
                  />
                  <textarea
                    placeholder="Description (optional)"
                    value={newPresetDescription}
                    onChange={(e) => setNewPresetDescription(e.target.value)}
                    style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.875rem', resize: 'none', minHeight: '60px', outline: 'none' }}
                  />
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      onClick={handleCreatePreset}
                      disabled={!newPresetName.trim()}
                      className="primary-button"
                      style={{ flex: 1, padding: '0.625rem', opacity: newPresetName.trim() ? 1 : 0.5, background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)' }}
                    >
                      Create
                    </button>
                    <button
                      onClick={() => setShowCreateForm(false)}
                      className="secondary-button"
                      style={{ padding: '0.625rem 1rem' }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Configuration Detail */}
            <div>
              {!selectedPreset ? (
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
                    <Settings size={36} style={{ color: '#8b5cf6' }} />
                  </div>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e1b4b', marginBottom: '0.5rem' }}>Select a Preset</h3>
                  <p style={{ color: '#64748b', fontSize: '1rem' }}>
                    Choose a policy preset from the list to view and edit its configuration
                  </p>
                </div>
              ) : (
                <div style={{ 
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)', 
                  borderRadius: '24px', 
                  padding: '2rem', 
                  boxShadow: '0 25px 60px rgba(139,92,246,0.08)', 
                  border: '1px solid rgba(139,92,246,0.1)',
                  backdropFilter: 'blur(20px)'
                }}>
                  {/* Header */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '1px solid rgba(139,92,246,0.1)' }}>
                    <div>
                      <h3 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e1b4b', marginBottom: '0.5rem' }}>{selectedPreset.name}</h3>
                      <p style={{ color: '#64748b', margin: 0 }}>{selectedPreset.description}</p>
                    </div>
                    <button
                      onClick={() => setIsEditing(!isEditing)}
                      className={isEditing ? "primary-button" : "secondary-button"}
                      style={{ padding: '0.5rem 1rem', background: isEditing ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' : undefined }}
                    >
                      <Edit2 size={16} />
                      {isEditing ? 'Editing' : 'Edit'}
                    </button>
                  </div>

                  {/* Configuration Grid */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.25rem', marginBottom: '1.5rem' }}>
                    {/* Night Shifts */}
                    <div style={{ padding: '1.25rem', background: 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)', borderRadius: '16px', border: '1px solid rgba(139,92,246,0.08)' }}>
                      <label style={{ display: 'block', fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Night Shifts</label>
                      {isEditing ? (
                        <select
                          value={editedConfig?.night_shifts ? 'true' : 'false'}
                          onChange={(e) => setEditedConfig({ ...editedConfig!, night_shifts: e.target.value === 'true' })}
                          style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.9375rem' }}
                        >
                          <option value="false">Daylight Only</option>
                          <option value="true">24/7 Operations</option>
                        </select>
                      ) : (
                        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', margin: 0 }}>{selectedPreset.config.night_shifts ? '24/7 Operations' : 'Daylight Only'}</p>
                      )}
                    </div>

                    {/* Safety Level */}
                    <div style={{ padding: '1.25rem', background: 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)', borderRadius: '16px', border: '1px solid rgba(139,92,246,0.08)' }}>
                      <label style={{ display: 'block', fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Safety Level</label>
                      {isEditing ? (
                        <select
                          value={editedConfig?.safety_level}
                          onChange={(e) => setEditedConfig({ ...editedConfig!, safety_level: e.target.value as any })}
                          style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.9375rem' }}
                        >
                          <option value="low">Low</option>
                          <option value="standard">Standard</option>
                          <option value="high">High (International)</option>
                        </select>
                      ) : (
                        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: selectedPreset.config.safety_level === 'high' ? '#16a34a' : selectedPreset.config.safety_level === 'low' ? '#f59e0b' : '#1e1b4b', margin: 0 }}>
                          {selectedPreset.config.safety_level.charAt(0).toUpperCase() + selectedPreset.config.safety_level.slice(1)}
                          {selectedPreset.config.safety_level === 'low' && <AlertTriangle size={16} style={{ marginLeft: '6px', verticalAlign: 'middle' }} />}
                        </p>
                      )}
                    </div>

                    {/* Urgency */}
                    <div style={{ padding: '1.25rem', background: 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)', borderRadius: '16px', border: '1px solid rgba(139,92,246,0.08)' }}>
                      <label style={{ display: 'block', fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Urgency</label>
                      {isEditing ? (
                        <select
                          value={editedConfig?.urgency}
                          onChange={(e) => setEditedConfig({ ...editedConfig!, urgency: e.target.value as any })}
                          style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.9375rem' }}
                        >
                          <option value="standard">Standard</option>
                          <option value="high">High (Election)</option>
                        </select>
                      ) : (
                        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: selectedPreset.config.urgency === 'high' ? '#dc2626' : '#1e1b4b', margin: 0 }}>
                          {selectedPreset.config.urgency === 'high' ? 'Election Deadline' : 'Standard Timeline'}
                        </p>
                      )}
                    </div>

                    {/* Labor */}
                    <div style={{ padding: '1.25rem', background: 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)', borderRadius: '16px', border: '1px solid rgba(139,92,246,0.08)' }}>
                      <label style={{ display: 'block', fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Labor Force</label>
                      {isEditing ? (
                        <select
                          value={editedConfig?.labor}
                          onChange={(e) => setEditedConfig({ ...editedConfig!, labor: e.target.value as any })}
                          style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.9375rem' }}
                        >
                          <option value="standard">Standard</option>
                          <option value="increased">Increased</option>
                        </select>
                      ) : (
                        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', margin: 0 }}>
                          {selectedPreset.config.labor === 'increased' ? 'Increased' : 'Standard'}
                        </p>
                      )}
                    </div>

                    {/* Traffic */}
                    <div style={{ padding: '1.25rem', background: 'linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%)', borderRadius: '16px', gridColumn: 'span 2', border: '1px solid rgba(139,92,246,0.08)' }}>
                      <label style={{ display: 'block', fontSize: '0.8125rem', color: '#8b5cf6', marginBottom: '0.5rem', fontWeight: '600' }}>Traffic Management</label>
                      {isEditing ? (
                        <select
                          value={editedConfig?.traffic}
                          onChange={(e) => setEditedConfig({ ...editedConfig!, traffic: e.target.value as any })}
                          style={{ width: '100%', padding: '0.75rem', background: 'white', border: '2px solid rgba(139,92,246,0.15)', borderRadius: '10px', color: '#1e1b4b', fontSize: '0.9375rem' }}
                        >
                          <option value="basic">Basic</option>
                          <option value="advanced">Advanced</option>
                        </select>
                      ) : (
                        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e1b4b', margin: 0 }}>
                          {selectedPreset.config.traffic === 'advanced' ? 'Advanced' : 'Basic'}
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div style={{ display: 'flex', gap: '12px' }}>
                    {isEditing && (
                      <button
                        onClick={handleSaveEdit}
                        className="primary-button"
                        style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', boxShadow: '0 8px 24px rgba(16,185,129,0.25)' }}
                      >
                        <Save size={18} />
                        Save Changes
                      </button>
                    )}
                    <button
                      onClick={handleApplyToSimulation}
                      className="primary-button"
                      style={{ flex: 1, background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', boxShadow: '0 8px 24px rgba(139,92,246,0.25)' }}
                    >
                      Apply & Run Simulation
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer style={{ background: 'linear-gradient(135deg, #faf5ff 0%, #ede9fe 100%)', borderTop: '1px solid rgba(139,92,246,0.1)', padding: '1.5rem' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', textAlign: 'center' }}>
          <p style={{ color: '#7c3aed', fontSize: '0.875rem', margin: 0, fontWeight: '500' }}>
            🏛️ CIVISIM - Civic Intelligence Platform • Policy Configuration
          </p>
        </div>
      </footer>
    </div>
  )
}

export default PolicyConfigurationPage
