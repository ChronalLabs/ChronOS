import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

interface ProtectedRouteProps {
  children: ReactNode
  requireAdmin?: boolean
}

export default function ProtectedRoute({ children, requireAdmin = false }: ProtectedRouteProps) {
  const { isAuthenticated, isAdmin } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requireAdmin && !isAdmin) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)',
        padding: '2rem'
      }}>
        <div style={{
          background: 'white',
          borderRadius: '24px',
          padding: '3rem',
          maxWidth: '500px',
          textAlign: 'center',
          boxShadow: '0 20px 60px rgba(239, 68, 68, 0.2)'
        }}>
          <div style={{
            width: '80px',
            height: '80px',
            background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 2rem',
            fontSize: '2.5rem'
          }}>
            🔒
          </div>
          <h1 style={{ fontSize: '2rem', fontWeight: '800', color: '#0f172a', marginBottom: '1rem' }}>
            Access Denied
          </h1>
          <p style={{ color: '#64748b', fontSize: '1.125rem', marginBottom: '2rem' }}>
            This feature requires <span style={{ color: '#ef4444', fontWeight: '700' }}>Admin</span> privileges.
            <br />You are currently logged in as a <span style={{ color: '#6366f1', fontWeight: '700' }}>Public</span> user.
          </p>
          <button
            onClick={() => window.history.back()}
            style={{
              background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
              color: 'white',
              padding: '0.75rem 2rem',
              borderRadius: '12px',
              border: 'none',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: 'pointer',
              boxShadow: '0 8px 24px rgba(99, 102, 241, 0.3)'
            }}
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  return <>{children}</>
}
