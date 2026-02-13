import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Sparkles, Shield, Presentation, ArrowRight, BarChart3, Settings, Brain,
  Building2, Heart, GraduationCap, Car, Leaf, Scale, Briefcase, Zap, Lock, Map
} from 'lucide-react'

// Policy Domain Configuration
const policyDomains = [
  {
    id: 'construction',
    name: 'Construction & Infrastructure',
    icon: <Building2 size={28} />,
    description: 'Urban development, building permits, safety regulations',
    color: '#3b82f6',
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
    active: true,
    features: ['Simulation Engine', 'Risk Analysis', 'Impact Prediction']
  },
  {
    id: 'healthcare',
    name: 'Healthcare & Public Health',
    icon: <Heart size={28} />,
    description: 'Medical policies, hospital regulations, health emergencies',
    color: '#ef4444',
    gradient: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    active: false,
    features: ['Resource Allocation', 'Epidemic Modeling', 'Access Analysis']
  },
  {
    id: 'education',
    name: 'Education & Academia',
    icon: <GraduationCap size={28} />,
    description: 'School policies, curriculum changes, funding allocation',
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    active: false,
    features: ['Enrollment Impact', 'Budget Simulation', 'Quality Metrics']
  },
  {
    id: 'transportation',
    name: 'Transportation & Mobility',
    icon: <Car size={28} />,
    description: 'Traffic policies, public transit, road safety regulations',
    color: '#8b5cf6',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    active: false,
    features: ['Traffic Flow', 'Emission Analysis', 'Accessibility']
  },
  {
    id: 'environment',
    name: 'Environment & Sustainability',
    icon: <Leaf size={28} />,
    description: 'Green policies, pollution control, conservation laws',
    color: '#10b981',
    gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    active: false,
    features: ['Carbon Impact', 'Ecosystem Modeling', 'Compliance']
  },
  {
    id: 'legal',
    name: 'Legal & Governance',
    icon: <Scale size={28} />,
    description: 'Civil laws, regulatory compliance, citizen rights',
    color: '#6366f1',
    gradient: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
    active: false,
    features: ['Compliance Check', 'Rights Analysis', 'Conflict Detection']
  },
  {
    id: 'employment',
    name: 'Employment & Labor',
    icon: <Briefcase size={28} />,
    description: 'Labor laws, workplace safety, employment policies',
    color: '#ec4899',
    gradient: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
    active: false,
    features: ['Workforce Impact', 'Wage Analysis', 'Safety Metrics']
  },
  {
    id: 'energy',
    name: 'Energy & Utilities',
    icon: <Zap size={28} />,
    description: 'Power policies, utility regulations, renewable energy',
    color: '#f97316',
    gradient: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',
    active: false,
    features: ['Grid Simulation', 'Cost Projection', 'Demand Forecast']
  },
]

const LandingPage: React.FC = () => {
  const navigate = useNavigate()
  const [selectedDomain, setSelectedDomain] = useState('construction')

  const features = [
    {
      icon: <Brain size={24} />,
      title: 'ML Policy Analysis',
      description: 'AI-powered analysis: extract intent, detect risks, and classify policies',
      path: '/ml-analysis',
      highlight: true,
    },
    {
      icon: <Presentation size={24} />,
      title: 'Simulation Engine',
      description: 'Run scenarios to test policies before implementation',
      path: '/simulation-engine',
    },
    {
      icon: <Settings size={24} />,
      title: 'Policy Configuration',
      description: 'Fine-tune parameters for accurate impact modeling',
      path: '/policy-config',
    },
    {
      icon: <BarChart3 size={24} />,
      title: 'Impact Analysis',
      description: 'Compare metrics: risks, costs, and civic disruption',
      path: '/impact-analysis',
    },
    {
      icon: <Map size={24} />,
      title: 'Impact Map',
      description: 'Geographic visualization of policy impact zones with Google Maps',
      path: '/impact-map',
      highlight: true,
    },
  ]

  const activeDomain = policyDomains.find(d => d.id === selectedDomain)

  return (
    <div className="app">
      {/* Hero Section */}
      <div className="app-header" style={{ minHeight: '100vh' }}>
        <div className="app-header__bg" />
        <div className="app-header__glow app-header__glow--right" />
        <div className="app-header__glow app-header__glow--left" />

        <div className="app-header__content">
          <nav className="navbar navbar--centered">
            <div className="navbar__brand">
              <div className="brand-icon">🏛️</div>
              <div className="brand-meta">
                <p className="brand-tagline brand-tagline--center">CIVIC INTELLIGENCE PLATFORM</p>
                <h1 className="brand-title brand-title--center">CIVISIM</h1>
              </div>
            </div>
          </nav>

          <div className="hero-grid hero-grid--full">
            <div className="hero-content hero-content--spread">
              <p className="hero-badge">
                <Sparkles size={14} />
                Multi-Domain Policy Intelligence
              </p>
              <h2 className="hero-title hero-title--spread">
                Simulate the ripple effects of <span style={{ color: '#60a5fa' }}>any civic policy</span> before it impacts citizens.
              </h2>
              <p className="hero-text hero-text--spread">
                CIVISIM is a comprehensive platform for analyzing, simulating, and predicting the impact of 
                government policies across multiple domains — from construction to healthcare, education to environment.
              </p>
              <div className="hero-actions hero-actions--spread">
                <button 
                  onClick={() => navigate('/ml-analysis')} 
                  className="primary-button"
                  style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%)' }}
                >
                  <Brain size={18} />
                  Analyze Policy
                </button>
                <button 
                  onClick={() => navigate('/simulation-engine')} 
                  className="primary-button"
                >
                  <Presentation size={18} />
                  Launch Simulation
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <main className="app-main" style={{ padding: '4rem 2rem' }}>
        <div className="layout-container">
          
          {/* Policy Domains Section */}
          <section style={{ marginBottom: '5rem' }}>
            <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
              <p style={{ 
                color: '#8b5cf6', 
                fontWeight: '600', 
                fontSize: '0.875rem', 
                textTransform: 'uppercase', 
                letterSpacing: '0.1em',
                marginBottom: '0.5rem'
              }}>
                Policy Domains
              </p>
              <h2 style={{ fontSize: '2.5rem', fontWeight: '700', color: '#1a1a2e', marginBottom: '1rem' }}>
                One Platform, Multiple Domains
              </h2>
              <p style={{ fontSize: '1.125rem', color: '#64748b', maxWidth: '700px', margin: '0 auto' }}>
                CIVISIM supports policy analysis across all major civic sectors. 
                Select a domain to explore its capabilities.
              </p>
            </div>

            {/* Domain Grid */}
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '1.5rem',
              maxWidth: '1400px',
              margin: '0 auto 3rem'
            }}>
              {policyDomains.map((domain) => (
                <div
                  key={domain.id}
                  onClick={() => domain.active && setSelectedDomain(domain.id)}
                  style={{
                    background: selectedDomain === domain.id ? 'white' : domain.active ? 'white' : '#f8fafc',
                    borderRadius: '16px',
                    padding: '1.5rem',
                    border: selectedDomain === domain.id 
                      ? `2px solid ${domain.color}` 
                      : '2px solid transparent',
                    cursor: domain.active ? 'pointer' : 'default',
                    transition: 'all 0.3s ease',
                    boxShadow: selectedDomain === domain.id 
                      ? `0 10px 40px ${domain.color}20` 
                      : '0 2px 8px rgba(0,0,0,0.05)',
                    opacity: domain.active ? 1 : 0.7,
                    position: 'relative',
                    overflow: 'hidden'
                  }}
                  onMouseEnter={(e) => {
                    if (domain.active) {
                      e.currentTarget.style.transform = 'translateY(-4px)'
                      e.currentTarget.style.boxShadow = `0 15px 40px ${domain.color}25`
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)'
                    e.currentTarget.style.boxShadow = selectedDomain === domain.id 
                      ? `0 10px 40px ${domain.color}20` 
                      : '0 2px 8px rgba(0,0,0,0.05)'
                  }}
                >
                  {/* Coming Soon Badge */}
                  {!domain.active && (
                    <div style={{
                      position: 'absolute',
                      top: '12px',
                      right: '12px',
                      background: '#e2e8f0',
                      color: '#64748b',
                      fontSize: '0.7rem',
                      fontWeight: '600',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px'
                    }}>
                      <Lock size={10} />
                      COMING SOON
                    </div>
                  )}
                  
                  {/* Active Badge */}
                  {domain.active && (
                    <div style={{
                      position: 'absolute',
                      top: '12px',
                      right: '12px',
                      background: '#dcfce7',
                      color: '#16a34a',
                      fontSize: '0.7rem',
                      fontWeight: '600',
                      padding: '4px 8px',
                      borderRadius: '4px'
                    }}>
                      ✓ ACTIVE
                    </div>
                  )}

                  <div style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '12px',
                    background: domain.gradient,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    marginBottom: '1rem',
                    filter: domain.active ? 'none' : 'grayscale(50%)'
                  }}>
                    {domain.icon}
                  </div>
                  
                  <h3 style={{
                    fontSize: '1.125rem',
                    fontWeight: '600',
                    color: '#1a1a2e',
                    marginBottom: '0.5rem'
                  }}>
                    {domain.name}
                  </h3>
                  
                  <p style={{
                    fontSize: '0.875rem',
                    color: '#64748b',
                    lineHeight: '1.5',
                    marginBottom: '1rem'
                  }}>
                    {domain.description}
                  </p>
                  
                  {/* Features Tags */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {domain.features.map((feature, idx) => (
                      <span 
                        key={idx}
                        style={{
                          fontSize: '0.7rem',
                          padding: '4px 8px',
                          background: domain.active ? `${domain.color}15` : '#f1f5f9',
                          color: domain.active ? domain.color : '#94a3b8',
                          borderRadius: '4px',
                          fontWeight: '500'
                        }}
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Selected Domain Info */}
            {activeDomain && (
              <div style={{
                background: `linear-gradient(135deg, ${activeDomain.color}10 0%, ${activeDomain.color}05 100%)`,
                border: `1px solid ${activeDomain.color}30`,
                borderRadius: '16px',
                padding: '2rem',
                maxWidth: '900px',
                margin: '0 auto',
                textAlign: 'center'
              }}>
                <div style={{ 
                  display: 'inline-flex', 
                  alignItems: 'center', 
                  gap: '12px',
                  background: activeDomain.gradient,
                  color: 'white',
                  padding: '12px 24px',
                  borderRadius: '50px',
                  marginBottom: '1.5rem'
                }}>
                  {activeDomain.icon}
                  <span style={{ fontWeight: '600', fontSize: '1.1rem' }}>
                    {activeDomain.name}
                  </span>
                </div>
                <p style={{ color: '#475569', marginBottom: '1.5rem', fontSize: '1rem' }}>
                  Currently active domain. Use the ML Analysis tool to analyze {activeDomain.name.toLowerCase()} policies 
                  or run simulations to predict policy impacts.
                </p>
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                  <button 
                    onClick={() => navigate('/ml-analysis')} 
                    className="primary-button"
                    style={{ background: activeDomain.gradient }}
                  >
                    <Brain size={18} />
                    Analyze {activeDomain.name.split(' ')[0]} Policy
                  </button>
                  <button 
                    onClick={() => navigate('/simulation-engine')} 
                    className="primary-button"
                    style={{ background: '#1a1a2e' }}
                  >
                    <Presentation size={18} />
                    Run Simulation
                  </button>
                </div>
              </div>
            )}
          </section>

          {/* Platform Features Section */}
          <section style={{ marginBottom: '5rem' }}>
            <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
              <p style={{ 
                color: '#3b82f6', 
                fontWeight: '600', 
                fontSize: '0.875rem', 
                textTransform: 'uppercase', 
                letterSpacing: '0.1em',
                marginBottom: '0.5rem'
              }}>
                Core Capabilities
              </p>
              <h2 style={{ fontSize: '2rem', fontWeight: '600', color: '#1a1a2e', marginBottom: '1rem' }}>
                Platform Features
              </h2>
              <p style={{ fontSize: '1.125rem', color: '#64748b', maxWidth: '600px', margin: '0 auto' }}>
                Powerful tools for comprehensive policy analysis and simulation
              </p>
            </div>

            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '2rem',
              maxWidth: '1200px',
              margin: '0 auto'
            }}>
              {features.map((feature) => (
                <div
                  key={feature.title}
                  onClick={() => navigate(feature.path)}
                  style={{
                    background: 'white',
                    borderRadius: '12px',
                    padding: '2rem',
                    border: '1px solid #e2e8f0',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-4px)'
                    e.currentTarget.style.boxShadow = '0 10px 25px rgba(0,0,0,0.1)'
                    e.currentTarget.style.borderColor = '#3b82f6'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)'
                    e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)'
                    e.currentTarget.style.borderColor = '#e2e8f0'
                  }}
                >
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '8px',
                    background: (feature as any).highlight 
                      ? 'linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%)'
                      : 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    marginBottom: '1.25rem',
                    marginLeft: 'auto',
                    marginRight: 'auto'
                  }}>
                    {feature.icon}
                  </div>
                  <h3 style={{
                    fontSize: '1.25rem',
                    fontWeight: '600',
                    color: '#1a1a2e',
                    marginBottom: '0.75rem',
                    textAlign: 'center'
                  }}>
                    {feature.title}
                  </h3>
                  <p style={{
                    fontSize: '1rem',
                    color: '#64748b',
                    lineHeight: '1.6',
                    marginBottom: '1rem',
                    textAlign: 'center'
                  }}>
                    {feature.description}
                  </p>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#3b82f6',
                    fontWeight: '500',
                    fontSize: '0.9rem'
                  }}>
                    Explore <ArrowRight size={16} style={{ marginLeft: '0.5rem' }} />
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Stats Section */}
          <section style={{ 
            marginBottom: '5rem',
            background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)',
            borderRadius: '24px',
            padding: '4rem 2rem',
            color: 'white'
          }}>
            <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
              <h2 style={{ fontSize: '2rem', fontWeight: '600', marginBottom: '1rem' }}>
                Platform Capabilities
              </h2>
              <p style={{ fontSize: '1rem', color: '#a5b4fc', maxWidth: '600px', margin: '0 auto' }}>
                Built for comprehensive civic policy intelligence
              </p>
            </div>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '2rem',
              maxWidth: '1000px',
              margin: '0 auto',
              textAlign: 'center'
            }}>
              <div>
                <div style={{ fontSize: '3rem', fontWeight: '700', color: '#60a5fa' }}>8</div>
                <div style={{ color: '#a5b4fc' }}>Policy Domains</div>
              </div>
              <div>
                <div style={{ fontSize: '3rem', fontWeight: '700', color: '#34d399' }}>6</div>
                <div style={{ color: '#a5b4fc' }}>ML Models</div>
              </div>
              <div>
                <div style={{ fontSize: '3rem', fontWeight: '700', color: '#fbbf24' }}>∞</div>
                <div style={{ color: '#a5b4fc' }}>Simulations</div>
              </div>
              <div>
                <div style={{ fontSize: '3rem', fontWeight: '700', color: '#f472b6' }}>24/7</div>
                <div style={{ color: '#a5b4fc' }}>Analysis Ready</div>
              </div>
            </div>
          </section>

          {/* CTA Section */}
          <section style={{
            textAlign: 'center',
            padding: '3rem 2rem',
            background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
            borderRadius: '16px'
          }}>
            <Shield size={40} style={{ color: '#10b981', marginBottom: '1rem' }} />
            <h3 style={{
              fontSize: '1.75rem',
              fontWeight: '600',
              color: '#1a1a2e',
              marginBottom: '1rem'
            }}>
              Ready to transform policy decision-making?
            </h3>
            <p style={{
              fontSize: '1.125rem',
              color: '#64748b',
              marginBottom: '2rem',
              maxWidth: '600px',
              margin: '0 auto 2rem'
            }}>
              Start analyzing policies with AI and simulate their real-world impact before implementation.
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button 
                onClick={() => navigate('/ml-analysis')} 
                className="primary-button"
                style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%)' }}
              >
                <Brain size={18} />
                Start Analysis
              </button>
              <button 
                onClick={() => navigate('/simulation-engine')} 
                className="primary-button"
              >
                Get Started
                <ArrowRight size={16} />
              </button>
            </div>
          </section>

        </div>
      </main>

      {/* Footer */}
      <footer style={{
        background: '#1a1a2e',
        color: 'white',
        padding: '3rem 2rem',
        textAlign: 'center'
      }}>
        <div style={{ marginBottom: '1rem' }}>
          <span style={{ fontSize: '1.5rem' }}>🏛️</span>
          <span style={{ marginLeft: '0.5rem', fontWeight: '600', fontSize: '1.25rem' }}>CIVISIM</span>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '1rem' }}>
          Civic Intelligence Platform for Policy Simulation & Analysis
        </p>
        <div style={{ color: '#64748b', fontSize: '0.75rem' }}>
          © 2025 CIVISIM. Empowering data-driven governance.
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
