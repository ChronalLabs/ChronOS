import React, { useMemo } from 'react';
import { AlertTriangle, CheckCircle, Info } from 'lucide-react';
import './CharacterLimitIndicator.css';

const CharacterLimitIndicator = ({ 
  current, 
  max, 
  min = 0,
  showProgressBar = true,
  warningThreshold = 0.8,  // Show warning at 80%
  dangerThreshold = 0.95,  // Show danger at 95%
  language = 'english'
}) => {
  const isHindi = language === 'hindi';
  
  const { percentage, status, message } = useMemo(() => {
    const pct = (current / max) * 100;
    const rem = max - current;
    
    let stat = 'normal';
    let msg = '';
    
    // Check minimum requirement
    if (min > 0 && current < min) {
      stat = 'below-min';
      const needed = min - current;
      msg = isHindi 
        ? `${needed} और अक्षर आवश्यक हैं`
        : `${needed} more characters needed`;
    }
    // Check if exceeding max
    else if (current > max) {
      stat = 'exceeded';
      const over = current - max;
      msg = isHindi 
        ? `${over} अक्षर अधिक हैं`
        : `${over} characters over limit`;
    }
    // Check danger threshold
    else if (pct >= dangerThreshold * 100) {
      stat = 'danger';
      msg = isHindi 
        ? `केवल ${rem} अक्षर शेष`
        : `Only ${rem} characters remaining`;
    }
    // Check warning threshold
    else if (pct >= warningThreshold * 100) {
      stat = 'warning';
      msg = isHindi 
        ? `${rem} अक्षर शेष`
        : `${rem} characters remaining`;
    }
    // Normal state
    else {
      msg = isHindi 
        ? `${rem} अक्षर शेष`
        : `${rem} characters remaining`;
    }
    
    return {
      percentage: Math.min(pct, 100),
      status: stat,
      message: msg
    };
  }, [current, max, min, warningThreshold, dangerThreshold, isHindi]);

  const getIcon = () => {
    switch (status) {
      case 'exceeded':
      case 'danger':
        return <AlertTriangle size={14} />;
      case 'below-min':
        return <Info size={14} />;
      case 'warning':
        return <AlertTriangle size={14} />;
      default:
        if (current >= min && current > 0) {
          return <CheckCircle size={14} />;
        }
        return null;
    }
  };

  return (
    <div 
      className={`character-limit-indicator ${status}`}
      role="status"
      aria-live="polite"
      aria-label={`${current} of ${max} characters. ${message}`}
    >
      {showProgressBar && (
        <div className="progress-container">
          <div 
            className="progress-bar"
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
          {status === 'exceeded' && (
            <div 
              className="progress-overflow"
              style={{ width: `${((current - max) / max) * 100}%` }}
            />
          )}
        </div>
      )}
      
      <div className="indicator-content">
        <span className="count-display">
          <span className={`current ${status}`}>{current.toLocaleString()}</span>
          <span className="separator">/</span>
          <span className="max">{max.toLocaleString()}</span>
        </span>
        
        <span className="message">
          {getIcon()}
          {message}
        </span>
      </div>
    </div>
  );
};

// Preset configurations for common RTI/Complaint fields
export const FIELD_LIMITS = {
  // RTI Fields
  subject: { min: 10, max: 150 },
  information_sought: { min: 50, max: 2000 },
  reason: { min: 0, max: 500 },
  
  // Complaint Fields
  complaint_subject: { min: 10, max: 200 },
  complaint_description: { min: 100, max: 3000 },
  
  // Common Fields
  name: { min: 2, max: 100 },
  address: { min: 10, max: 300 },
  phone: { min: 10, max: 15 },
  email: { min: 5, max: 100 },
  
  // Legal References
  legal_section: { min: 0, max: 200 },
  supporting_details: { min: 0, max: 1000 }
};

// Helper hook for using field limits
export const useFieldLimit = (fieldName, customLimits = {}) => {
  const limits = {
    ...FIELD_LIMITS[fieldName],
    ...customLimits
  };
  
  return {
    min: limits.min || 0,
    max: limits.max || 500,
    ...limits
  };
};

export default CharacterLimitIndicator;
