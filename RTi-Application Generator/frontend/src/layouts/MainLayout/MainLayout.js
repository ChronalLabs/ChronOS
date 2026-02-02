import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Scale, Menu, X, Shield } from 'lucide-react';
import './MainLayout.css';

const MainLayout = ({ children }) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <div className="main-layout">
      <header className="app-header">
        <div className="header-container">
          {/* Left: Brand */}
          <Link to="/" className="brand-logo">
            <div className="logo-icon-wrapper">
              <Scale size={20} strokeWidth={2.5} />
            </div>
            <div className="brand-text">
              <span className="brand-name">CivicDraft</span>
              <span className="brand-tagline">Rule-Based Drafting System</span>
            </div>
          </Link>

          {/* Center: Navigation */}
          <nav className={`main-nav ${mobileMenuOpen ? 'mobile-open' : ''}`}>
            <Link 
              to="/" 
              className={`nav-link ${isActive('/')}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link 
              to="/guided" 
              className={`nav-link ${isActive('/guided')}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Guided Mode
            </Link>
            <Link 
              to="/assisted" 
              className={`nav-link ${isActive('/assisted')}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Assisted Mode
            </Link>
            <Link 
              to="/templates" 
              className={`nav-link ${isActive('/templates')}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Templates
            </Link>
          </nav>

          {/* Right: Status Badge */}
          <div className="header-status">
            <div className="status-badge">
              <Shield size={14} />
              <span>No Login Required</span>
            </div>
          </div>

          {/* Mobile Menu Toggle */}
          <button 
            className="mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </header>

      <main className="app-content">
        {children}
      </main>

      <footer className="app-footer">
        <div className="container footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <Scale size={18} />
              <h3>CivicDraft</h3>
            </div>
            <p>Rule-Based Civic Drafting System</p>
            <p className="footer-note">No accounts. No data stored. Privacy by default.</p>
          </div>
          <div className="footer-links">
            <div className="footer-nav">
              <Link to="/guided">Guided Mode</Link>
              <Link to="/assisted">Assisted Mode</Link>
              <Link to="/templates">Templates</Link>
            </div>
            <p className="copyright">
              &copy; {new Date().getFullYear()} CivicDraft. Open-source civic infrastructure.
            </p>
          </div>
        </div>
        <div className="container footer-disclaimer">
          <p>
            <strong>Disclaimer:</strong> CivicDraft is a rule-based document drafting tool, not a legal service. 
            All legal structure is determined by deterministic rules, not AI. Users are responsible for 
            verifying content accuracy before submission to any authority. This platform does not file 
            applications on your behalf.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;
