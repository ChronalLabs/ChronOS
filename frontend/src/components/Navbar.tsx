import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Home, Map, Brain, Play, LogOut, Shield, User } from 'lucide-react'

interface NavbarProps {
  activePage?: string
}

export default function Navbar({ activePage }: NavbarProps) {
  const navigate = useNavigate()
  const { user, isAdmin, logout } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar" style={{ borderBottom: 'none', maxWidth: '1600px', margin: '0 auto' }}>
      <div className="navbar__brand">
        <div className="brand-icon" style={{ 
          background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', 
          color: 'white', 
          fontSize: '1.25rem' 
        }}>
          🗺️
        </div>
        <div className="brand-meta">
          <p className="brand-tagline" style={{ color: '#10b981', fontWeight: '600' }}>
            CONSTRUCTION INTELLIGENCE
          </p>
          <h1 className="brand-title" style={{ 
            fontSize: '1.25rem', 
            background: 'linear-gradient(135deg, #065f46 0%, #047857 100%)', 
            WebkitBackgroundClip: 'text', 
            WebkitTextFillColor: 'transparent' 
          }}>
            CIVISIM
          </h1>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        {/* Navigation Buttons */}
        <button 
          onClick={() => navigate('/')} 
          className={activePage === 'home' ? 'primary-button' : 'secondary-button'}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <Home size={16} />
          Home
        </button>

        {isAdmin && (
          <>
            <button 
              onClick={() => navigate('/simulation-engine')} 
              className={activePage === 'simulation' ? 'primary-button' : 'secondary-button'}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            >
              <Play size={16} />
              Simulation
            </button>
            <button 
              onClick={() => navigate('/ml-analysis')} 
              className={activePage === 'ml' ? 'primary-button' : 'secondary-button'}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            >
              <Brain size={16} />
              ML Analysis
            </button>
          </>
        )}

        <button 
          onClick={() => navigate('/impact-map')} 
          className={activePage === 'map' ? 'primary-button' : 'secondary-button'}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <Map size={16} />
          Map
        </button>

        {/* User Info */}
        {user && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            marginLeft: '1rem',
            paddingLeft: '1rem',
            borderLeft: '2px solid #e2e8f0'
          }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5rem',
              background: isAdmin ? 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)' : 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
              padding: '0.5rem 1rem',
              borderRadius: '12px',
              border: isAdmin ? '2px solid #fbbf24' : '2px solid #60a5fa'
            }}>
              {user.picture ? (
                <img 
                  src={user.picture} 
                  alt={user.name}
                  style={{ 
                    width: '32px', 
                    height: '32px', 
                    borderRadius: '50%',
                    border: '2px solid white'
                  }}
                />
              ) : (
                <User size={20} />
              )}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <span style={{ fontWeight: '600', fontSize: '0.875rem', color: '#0f172a' }}>
                  {user.name}
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  {isAdmin ? (
                    <Shield size={12} style={{ color: '#d97706' }} />
                  ) : (
                    <User size={12} style={{ color: '#2563eb' }} />
                  )}
                  <span style={{ 
                    fontSize: '0.75rem', 
                    fontWeight: '600',
                    color: isAdmin ? '#d97706' : '#2563eb'
                  }}>
                    {isAdmin ? 'Admin' : 'Public'}
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={handleLogout}
              style={{
                background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                padding: '0.5rem 1rem',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '0.875rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)'
              }}
            >
              <LogOut size={16} />
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}
