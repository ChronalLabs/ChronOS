import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Home, Map, Brain, Play, Layers, Building2, AlertTriangle, TrendingUp, MapPin, Navigation, Search, Filter, RefreshCw, Download, Share2, Settings } from 'lucide-react'
import GoogleMapComponent, { MapZone } from '../components/GoogleMap'

// Indian cities for location selection
const indianCities = [
  { name: 'New Delhi', lat: 28.6139, lng: 77.2090 },
  { name: 'Mumbai', lat: 19.0760, lng: 72.8777 },
  { name: 'Bangalore', lat: 12.9716, lng: 77.5946 },
  { name: 'Chennai', lat: 13.0827, lng: 80.2707 },
  { name: 'Kolkata', lat: 22.5726, lng: 88.3639 },
  { name: 'Hyderabad', lat: 17.3850, lng: 78.4867 },
  { name: 'Pune', lat: 18.5204, lng: 73.8567 },
  { name: 'Ahmedabad', lat: 23.0225, lng: 72.5714 },
  { name: 'Jaipur', lat: 26.9124, lng: 75.7873 },
  { name: 'Lucknow', lat: 26.8467, lng: 80.9462 }
]

// Generate zones for selected city
const generateZonesForCity = (city: typeof indianCities[0]): MapZone[] => {
  const baseZones: Omit<MapZone, 'center'>[] = [
    { id: '1', name: 'Highway Expansion Project', type: 'construction', radius: 600, impact: 'high', description: 'Major highway widening and flyover construction' },
    { id: '2', name: 'Metro Rail Extension', type: 'construction', radius: 400, impact: 'high', description: 'Underground metro line construction' },
    { id: '3', name: 'Commercial Construction Zone', type: 'construction', radius: 350, impact: 'medium', description: 'IT park and commercial complex development' },
    { id: '4', name: 'Residential Construction Project', type: 'construction', radius: 500, impact: 'medium', description: 'Affordable housing project under PMAY' },
    { id: '5', name: 'Industrial Park Construction', type: 'construction', radius: 700, impact: 'medium', description: 'Manufacturing and logistics hub' },
    { id: '6', name: 'Bridge Construction Site', type: 'construction', radius: 300, impact: 'high', description: 'Major bridge construction over river' },
    { id: '7', name: 'Bus Terminal Construction', type: 'construction', radius: 250, impact: 'medium', description: 'Bus terminal and interchange construction' },
    { id: '8', name: 'Water Treatment Construction', type: 'construction', radius: 450, impact: 'low', description: 'Municipal water infrastructure upgrade' }
  ]

  return baseZones.map((zone, idx) => ({
    ...zone,
    center: {
      lat: city.lat + (Math.random() - 0.5) * 0.08,
      lng: city.lng + (Math.random() - 0.5) * 0.08
    }
  }))
}

function ImpactMapPage() {
  const navigate = useNavigate()
  const [selectedCity, setSelectedCity] = useState(indianCities[0])
  const [zones, setZones] = useState<MapZone[]>([])
  const [simulationActive, setSimulationActive] = useState(false)
  const [impactLevel, setImpactLevel] = useState<'low' | 'medium' | 'high'>('medium')
  const [selectedZone, setSelectedZone] = useState<MapZone | null>(null)
  const [filterType, setFilterType] = useState<'all' | 'construction' | 'traffic' | 'residential' | 'commercial' | 'industrial'>('construction')
  const [mlParams, setMlParams] = useState<any>(null)

  useEffect(() => {
    setZones(generateZonesForCity(selectedCity))
    
    // Check for ML analysis params
    const stored = localStorage.getItem('ml_analysis_params')
    if (stored) {
      try {
        setMlParams(JSON.parse(stored))
      } catch (e) {
        console.error('Failed to parse ML params:', e)
      }
    }
  }, [selectedCity])

  const handleCityChange = (cityName: string) => {
    const city = indianCities.find(c => c.name === cityName)
    if (city) {
      setSelectedCity(city)
      setSelectedZone(null)
    }
  }

  const handleSimulateImpact = () => {
    setSimulationActive(true)
    // Simulate for 5 seconds then stop
    setTimeout(() => setSimulationActive(false), 5000)
  }

  const filteredZones = filterType === 'all' 
    ? zones 
    : zones.filter(z => z.type === filterType)

  const zoneStats = {
    total: zones.length,
    highImpact: zones.filter(z => z.impact === 'high').length,
    construction: zones.filter(z => z.type === 'construction').length,
    traffic: zones.filter(z => z.type === 'traffic').length
  }

  return (
    <div className="app" style={{ background: 'linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)', minHeight: '100vh' }}>
      {/* Premium Header */}
      <header className="app-header" style={{ minHeight: 'auto', padding: '0', position: 'relative', overflow: 'hidden' }}>
        <div className="app-header__bg" style={{ background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 30%, #ecfdf5 70%, #d1fae5 100%)' }} />
        <div className="app-header__glow app-header__glow--right" style={{ background: 'rgba(16, 185, 129, 0.15)', width: '20rem', height: '20rem' }} />
        <div className="app-header__glow app-header__glow--left" style={{ background: 'rgba(34, 197, 94, 0.12)', width: '24rem', height: '24rem' }} />
        
        <div className="app-header__content" style={{ padding: '1.5rem 2rem', position: 'relative', zIndex: 1 }}>
          <nav className="navbar" style={{ borderBottom: 'none', maxWidth: '1600px', margin: '0 auto' }}>
            <div className="navbar__brand">
              <div className="brand-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', color: 'white', fontSize: '1.25rem' }}>🗺️</div>
              <div className="brand-meta">
                <p className="brand-tagline" style={{ color: '#10b981', fontWeight: '600' }}>GEOGRAPHIC INTELLIGENCE</p>
                <h1 className="brand-title" style={{ fontSize: '1.25rem', background: 'linear-gradient(135deg, #065f46 0%, #047857 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>CIVISIM</h1>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button onClick={() => navigate('/')} className="secondary-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Home size={16} />
                Home
              </button>
              <button onClick={() => navigate('/simulation-engine')} className="secondary-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Play size={16} />
                Simulation
              </button>
              <button 
                onClick={() => navigate('/ml-analysis')} 
                className="primary-button"
                style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', padding: '0.5rem 1rem', fontSize: '0.875rem', boxShadow: '0 8px 24px rgba(16,185,129,0.25)' }}
              >
                <Brain size={16} />
                ML Analysis
              </button>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ padding: '2rem' }}>
        <div style={{ maxWidth: '1600px', margin: '0 auto' }}>
          
          {/* ML Analysis Banner */}
          {mlParams && (
            <div style={{ 
              marginBottom: '1.5rem', 
              padding: '1rem 1.5rem', 
              background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
              border: '2px solid #86efac', 
              borderRadius: '14px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '1rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Brain size={20} style={{ color: '#16a34a' }} />
                <span style={{ fontWeight: '600', color: '#166534' }}>
                  ML Analysis: <span style={{ fontWeight: '700' }}>{mlParams.policyName}</span>
                  {mlParams.classification && <span style={{ marginLeft: '0.5rem', opacity: 0.8 }}>({mlParams.classification})</span>}
                </span>
              </div>
              <button
                onClick={handleSimulateImpact}
                disabled={simulationActive}
                style={{
                  padding: '0.5rem 1rem',
                  background: simulationActive ? '#94a3b8' : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontWeight: '600',
                  fontSize: '0.875rem',
                  cursor: simulationActive ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}
              >
                {simulationActive ? <RefreshCw size={14} className="animate-spin" /> : <Play size={14} />}
                {simulationActive ? 'Simulating...' : 'Visualize Impact'}
              </button>
            </div>
          )}

          {/* Controls Bar */}
          <div style={{ 
            display: 'flex', 
            flexWrap: 'wrap',
            gap: '1rem', 
            marginBottom: '1.5rem', 
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            {/* Left Controls */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center' }}>
              {/* City Selector */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                background: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '12px',
                border: '2px solid #e2e8f0',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
              }}>
                <MapPin size={18} style={{ color: '#10b981' }} />
                <select
                  value={selectedCity.name}
                  onChange={(e) => handleCityChange(e.target.value)}
                  style={{
                    padding: '0.5rem',
                    border: 'none',
                    background: 'transparent',
                    fontSize: '0.9rem',
                    fontWeight: '600',
                    color: '#1e293b',
                    cursor: 'pointer',
                    outline: 'none',
                    minWidth: '140px'
                  }}
                >
                  {indianCities.map((city) => (
                    <option key={city.name} value={city.name}>{city.name}</option>
                  ))}
                </select>
              </div>

              {/* Filter */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                background: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '12px',
                border: '2px solid #e2e8f0',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
              }}>
                <Filter size={18} style={{ color: '#8b5cf6' }} />
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value as any)}
                  style={{
                    padding: '0.5rem',
                    border: 'none',
                    background: 'transparent',
                    fontSize: '0.9rem',
                    fontWeight: '600',
                    color: '#1e293b',
                    cursor: 'pointer',
                    outline: 'none',
                    minWidth: '120px'
                  }}
                >
                  <option value="all">All Zones</option>
                  <option value="construction">Construction</option>
                  <option value="traffic">Traffic</option>
                  <option value="residential">Residential</option>
                  <option value="commercial">Commercial</option>
                  <option value="industrial">Industrial</option>
                </select>
              </div>

              {/* Impact Level */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                background: 'white',
                padding: '0.5rem',
                borderRadius: '12px',
                border: '2px solid #e2e8f0',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
              }}>
                {(['low', 'medium', 'high'] as const).map((level) => (
                  <button
                    key={level}
                    onClick={() => setImpactLevel(level)}
                    style={{
                      padding: '0.5rem 0.75rem',
                      background: impactLevel === level 
                        ? level === 'high' ? '#ef4444' : level === 'medium' ? '#f59e0b' : '#10b981'
                        : 'transparent',
                      color: impactLevel === level ? 'white' : '#64748b',
                      border: 'none',
                      borderRadius: '8px',
                      fontSize: '0.8rem',
                      fontWeight: '600',
                      cursor: 'pointer',
                      textTransform: 'capitalize',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            {/* Right Controls */}
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={handleSimulateImpact}
                disabled={simulationActive}
                style={{
                  padding: '0.75rem 1.5rem',
                  background: simulationActive 
                    ? '#94a3b8' 
                    : 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  fontWeight: '600',
                  fontSize: '0.9rem',
                  cursor: simulationActive ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  boxShadow: simulationActive ? 'none' : '0 8px 24px rgba(139,92,246,0.3)',
                  transition: 'all 0.2s ease'
                }}
              >
                <Play size={18} />
                {simulationActive ? 'Simulating...' : 'Run Impact Simulation'}
              </button>
            </div>
          </div>

          {/* Main Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: '1.5rem' }}>
            {/* Map */}
            <div style={{
              background: 'white',
              borderRadius: '20px',
              overflow: 'hidden',
              boxShadow: '0 15px 50px rgba(0,0,0,0.1)',
              border: '1px solid #e2e8f0'
            }}>
              <GoogleMapComponent
                zones={filteredZones}
                center={selectedCity}
                zoom={13}
                height="600px"
                simulationActive={simulationActive}
                impactLevel={impactLevel}
                onZoneClick={setSelectedZone}
              />
            </div>

            {/* Stats Panel */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {/* Quick Stats */}
              <div style={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,250,255,0.9) 100%)',
                borderRadius: '16px',
                padding: '1.5rem',
                border: '1px solid #e2e8f0',
                boxShadow: '0 8px 24px rgba(0,0,0,0.05)'
              }}>
                <h3 style={{ margin: '0 0 1rem', fontSize: '1rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <TrendingUp size={18} style={{ color: '#10b981' }} />
                  Impact Statistics
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div style={{ padding: '1rem', background: '#f0fdf4', borderRadius: '12px', textAlign: 'center' }}>
                    <p style={{ margin: 0, fontSize: '1.75rem', fontWeight: '700', color: '#166534' }}>{zoneStats.total}</p>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#047857', fontWeight: '600' }}>Total Zones</p>
                  </div>
                  <div style={{ padding: '1rem', background: '#fef2f2', borderRadius: '12px', textAlign: 'center' }}>
                    <p style={{ margin: 0, fontSize: '1.75rem', fontWeight: '700', color: '#dc2626' }}>{zoneStats.highImpact}</p>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#b91c1c', fontWeight: '600' }}>High Impact</p>
                  </div>
                  <div style={{ padding: '1rem', background: '#fef3c7', borderRadius: '12px', textAlign: 'center' }}>
                    <p style={{ margin: 0, fontSize: '1.75rem', fontWeight: '700', color: '#d97706' }}>{zoneStats.construction}</p>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#b45309', fontWeight: '600' }}>Construction</p>
                  </div>
                  <div style={{ padding: '1rem', background: '#eef2ff', borderRadius: '12px', textAlign: 'center' }}>
                    <p style={{ margin: 0, fontSize: '1.75rem', fontWeight: '700', color: '#4f46e5' }}>{zoneStats.traffic}</p>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#3730a3', fontWeight: '600' }}>Traffic Zones</p>
                  </div>
                </div>
              </div>

              {/* Selected Zone Info */}
              {selectedZone && (
                <div style={{
                  background: 'white',
                  borderRadius: '16px',
                  padding: '1.5rem',
                  border: '2px solid #10b981',
                  boxShadow: '0 8px 24px rgba(16,185,129,0.15)'
                }}>
                  <h3 style={{ margin: '0 0 1rem', fontSize: '1rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <MapPin size={18} style={{ color: '#10b981' }} />
                    Selected Zone
                  </h3>
                  <h4 style={{ margin: '0 0 0.5rem', fontSize: '1.1rem', fontWeight: '700', color: '#065f46' }}>{selectedZone.name}</h4>
                  <p style={{ margin: '0 0 1rem', fontSize: '0.875rem', color: '#475569', lineHeight: '1.5' }}>{selectedZone.description}</p>
                  <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <span style={{
                      padding: '0.35rem 0.75rem',
                      background: selectedZone.impact === 'high' ? '#fee2e2' : selectedZone.impact === 'medium' ? '#fef3c7' : '#dcfce7',
                      color: selectedZone.impact === 'high' ? '#dc2626' : selectedZone.impact === 'medium' ? '#d97706' : '#16a34a',
                      borderRadius: '6px',
                      fontSize: '0.75rem',
                      fontWeight: '700',
                      textTransform: 'uppercase'
                    }}>
                      {selectedZone.impact} Impact
                    </span>
                    <span style={{
                      padding: '0.35rem 0.75rem',
                      background: '#f1f5f9',
                      color: '#475569',
                      borderRadius: '6px',
                      fontSize: '0.75rem',
                      fontWeight: '600',
                      textTransform: 'capitalize'
                    }}>
                      {selectedZone.type}
                    </span>
                  </div>
                </div>
              )}

              {/* City Info */}
              <div style={{
                background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
                borderRadius: '16px',
                padding: '1.5rem',
                border: '1px solid #a7f3d0'
              }}>
                <h3 style={{ margin: '0 0 0.75rem', fontSize: '1rem', fontWeight: '700', color: '#065f46', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Navigation size={18} />
                  {selectedCity.name}
                </h3>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#047857' }}>
                  Coordinates: {selectedCity.lat.toFixed(4)}°N, {selectedCity.lng.toFixed(4)}°E
                </p>
                <p style={{ margin: '0.5rem 0 0', fontSize: '0.85rem', color: '#047857' }}>
                  Active Projects: {zones.filter(z => z.type === 'construction').length} construction sites
                </p>
              </div>

              {/* Actions */}
              <div style={{
                background: 'white',
                borderRadius: '16px',
                padding: '1.5rem',
                border: '1px solid #e2e8f0',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.75rem'
              }}>
                <button
                  onClick={() => navigate('/simulation-engine')}
                  style={{
                    padding: '0.875rem',
                    background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '10px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    boxShadow: '0 8px 20px rgba(139,92,246,0.3)'
                  }}
                >
                  <Play size={18} />
                  Run Full Simulation
                </button>
                <button
                  onClick={() => navigate('/impact-analysis')}
                  style={{
                    padding: '0.875rem',
                    background: 'white',
                    color: '#475569',
                    border: '2px solid #e2e8f0',
                    borderRadius: '10px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <TrendingUp size={18} />
                  View Impact Analysis
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer style={{ background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)', borderTop: '1px solid #a7f3d0', padding: '1.5rem', marginTop: '2rem' }}>
        <div style={{ maxWidth: '1600px', margin: '0 auto', textAlign: 'center' }}>
          <p style={{ color: '#047857', fontSize: '0.875rem', margin: 0, fontWeight: '500' }}>
            🗺️ CIVISIM - Civic Intelligence Platform • Geographic Impact Analysis powered by Google Maps
          </p>
        </div>
      </footer>
    </div>
  )
}

export default ImpactMapPage
