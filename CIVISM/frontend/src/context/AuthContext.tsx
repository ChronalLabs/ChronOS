import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { jwtDecode } from 'jwt-decode'

export type UserRole = 'admin' | 'public'

export interface User {
  email: string
  name: string
  picture?: string
  role: UserRole
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isAdmin: boolean
  login: (credential: string) => void
  logout: () => void
  setUserRole: (email: string, role: UserRole) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Admin emails list - add your admin emails here
const ADMIN_EMAILS = [
  'dargarkrish@gmail.com',
  'aringupta2244@gmail.com'
]

interface GoogleJwtPayload {
  email: string
  name: string
  picture?: string
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('civisim_user')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch (e) {
        localStorage.removeItem('civisim_user')
      }
    }
  }, [])

  const login = (credential: string) => {
    try {
      const decoded = jwtDecode<GoogleJwtPayload>(credential)
      const role: UserRole = ADMIN_EMAILS.includes(decoded.email) ? 'admin' : 'public'
      
      const userData: User = {
        email: decoded.email,
        name: decoded.name,
        picture: decoded.picture,
        role
      }

      setUser(userData)
      localStorage.setItem('civisim_user', JSON.stringify(userData))
    } catch (error) {
      console.error('Failed to decode credential:', error)
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('civisim_user')
  }

  const setUserRole = (email: string, role: UserRole) => {
    if (user && user.email === email) {
      const updatedUser = { ...user, role }
      setUser(updatedUser)
      localStorage.setItem('civisim_user', JSON.stringify(updatedUser))
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isAdmin: user?.role === 'admin',
        login,
        logout,
        setUserRole
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
