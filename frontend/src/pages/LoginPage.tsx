import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { GoogleLogin, CredentialResponse } from '@react-oauth/google'
import { useAuth } from '../context/AuthContext'
import { Shield, Users, Lock, MapPin } from 'lucide-react'

export default function LoginPage() {
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/')
    }
  }, [isAuthenticated, navigate])

  const handleSuccess = (credentialResponse: CredentialResponse) => {
    if (credentialResponse.credential) {
      login(credentialResponse.credential)
      navigate('/')
    }
  }

  const handleError = () => {
    console.error('Login Failed')
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <div style={{
        maxWidth: '900px',
        width: '100%',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        alignItems: 'center'
      }}>
        {/* Left Side - Branding */}
        <div style={{ color: 'white' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
            <div style={{
              width: '60px',
              height: '60px',
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              borderRadius: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2rem'
            }}>
              🗺️
            </div>
            <div>
              <h1 style={{ fontSize: '2.5rem', fontWeight: '800', margin: 0 }}>CIVISIM</h1>
              <p style={{ color: '#10b981', fontWeight: '600', margin: 0 }}>Construction Intelligence Platform</p>
            </div>
          </div>

          <p style={{ fontSize: '1.125rem', lineHeight: '1.75', color: '#cbd5e1', marginBottom: '2rem' }}>
            Analyze construction policies, simulate impacts, and visualize geographic data with AI-powered insights.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <Shield size={24} style={{ color: '#10b981' }} />
              <span style={{ color: '#e2e8f0' }}>Role-based access control</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <MapPin size={24} style={{ color: '#10b981' }} />
              <span style={{ color: '#e2e8f0' }}>Real-time geographic visualization</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <Users size={24} style={{ color: '#10b981' }} />
              <span style={{ color: '#e2e8f0' }}>Multi-user collaboration</span>
            </div>
          </div>
        </div>

        {/* Right Side - Login */}
        <div style={{
          background: 'white',
          borderRadius: '24px',
          padding: '3rem',
          boxShadow: '0 20px 60px rgba(0,0,0,0.4)'
        }}>
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.875rem', fontWeight: '700', color: '#0f172a', marginBottom: '0.5rem' }}>
              Welcome Back
            </h2>
            <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
              Sign in with your Google account
            </p>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <div style={{
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '12px',
              padding: '1rem',
              marginBottom: '1rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                <Shield size={20} style={{ color: '#10b981' }} />
                <span style={{ fontWeight: '600', color: '#0f172a', fontSize: '0.875rem' }}>Admin Access</span>
              </div>
              <p style={{ fontSize: '0.75rem', color: '#64748b', margin: 0 }}>
                Full control: Create, edit, delete policies and simulations
              </p>
            </div>

            <div style={{
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '12px',
              padding: '1rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                <Users size={20} style={{ color: '#6366f1' }} />
                <span style={{ fontWeight: '600', color: '#0f172a', fontSize: '0.875rem' }}>Public Access</span>
              </div>
              <p style={{ fontSize: '0.75rem', color: '#64748b', margin: 0 }}>
                View-only: Explore policies, visualizations, and reports
              </p>
            </div>
          </div>

          <div style={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '1.5rem'
          }}>
            <GoogleLogin
              onSuccess={handleSuccess}
              onError={handleError}
              theme="filled_blue"
              size="large"
              text="signin_with"
              shape="rectangular"
            />
          </div>

          <div style={{
            textAlign: 'center',
            padding: '1rem',
            background: '#fef3c7',
            borderRadius: '8px',
            border: '1px solid #fbbf24'
          }}>
            <Lock size={16} style={{ color: '#d97706', marginBottom: '0.25rem' }} />
            <p style={{ fontSize: '0.75rem', color: '#92400e', margin: 0 }}>
              Secure authentication powered by Google OAuth 2.0
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
