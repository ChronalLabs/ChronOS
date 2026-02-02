import React from 'react';
import { AlertTriangle, Info, AlertOctagon } from 'lucide-react';

const ConfidenceNotice = ({ level, explanation }) => {
  if (level === 'high') return null;

  // Configuration for different levels
  const config = {
    medium: {
      color: '#d97706', // Amber 600
      bg: '#fffbeb',    // Amber 50
      border: '#fcd34d', // Amber 300
      icon: Info,
      label: 'Moderate Confidence'
    },
    low: {
      color: '#ef4444', // Red 500
      bg: '#fef2f2',    // Red 50
      border: '#fca5a5', // Red 300
      icon: AlertTriangle,
      label: 'Low Confidence'
    },
    very_low: {
      color: '#b91c1c', // Red 700
      bg: '#fef2f2',
      border: '#f87171',
      icon: AlertOctagon,
      label: 'Very Low Confidence'
    }
  };

  const style = config[level] || config.low;
  const Icon = style.icon;

  return (
    <div 
      className="notice-card fade-in" 
      style={{ 
        backgroundColor: style.bg, 
        border: `1px solid ${style.border}`,
        borderRadius: '8px',
        padding: '1rem',
        marginBottom: '1.5rem',
        display: 'flex',
        gap: '0.75rem',
        alignItems: 'start'
      }}
    >
      <div style={{ color: style.color, marginTop: '2px' }}>
         <Icon size={20} />
      </div>
      <div>
        <h4 style={{ color: style.color, margin: '0 0 0.25rem 0', fontSize: '1rem' }}>
          {style.label}
        </h4>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5' }}>
          {explanation || "The AI is not fully sure about your request. Please review the generate draft carefully."}
        </p>
      </div>
    </div>
  );
};

export default ConfidenceNotice;
