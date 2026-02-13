import React, { useState, useMemo, useCallback } from 'react';
import { AlertTriangle, Shield, Eye, EyeOff, X, Info } from 'lucide-react';
import './PIIWarning.css';

// PII Detection Patterns
const PII_PATTERNS = {
  aadhaar: {
    pattern: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
    label: { en: 'Aadhaar Number', hi: 'आधार नंबर' },
    severity: 'high',
    hint: { 
      en: 'Consider using only last 4 digits (XXXX-XXXX-1234)',
      hi: 'केवल अंतिम 4 अंक उपयोग करें (XXXX-XXXX-1234)'
    }
  },
  pan: {
    pattern: /\b[A-Z]{5}\d{4}[A-Z]\b/gi,
    label: { en: 'PAN Number', hi: 'पैन नंबर' },
    severity: 'high',
    hint: {
      en: 'Consider masking: XXXXX1234X',
      hi: 'मास्क करें: XXXXX1234X'
    }
  },
  phone: {
    pattern: /\b(?:\+91[\s-]?)?[6-9]\d{9}\b/g,
    label: { en: 'Phone Number', hi: 'फोन नंबर' },
    severity: 'medium',
    hint: {
      en: 'Phone numbers are sometimes necessary for contact',
      hi: 'संपर्क के लिए फोन नंबर कभी-कभी आवश्यक होते हैं'
    }
  },
  email: {
    pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
    label: { en: 'Email Address', hi: 'ईमेल पता' },
    severity: 'medium',
    hint: {
      en: 'Email may be needed for official correspondence',
      hi: 'आधिकारिक पत्राचार के लिए ईमेल आवश्यक हो सकता है'
    }
  },
  bankAccount: {
    pattern: /\b\d{9,18}\b/g,
    label: { en: 'Possible Bank Account', hi: 'संभावित बैंक खाता' },
    severity: 'high',
    hint: {
      en: 'Avoid including full bank account numbers',
      hi: 'पूर्ण बैंक खाता संख्या शामिल करने से बचें'
    }
  },
  passport: {
    pattern: /\b[A-Z]\d{7}\b/gi,
    label: { en: 'Possible Passport', hi: 'संभावित पासपोर्ट' },
    severity: 'high',
    hint: {
      en: 'Consider if passport number is necessary',
      hi: 'विचार करें कि क्या पासपोर्ट नंबर आवश्यक है'
    }
  },
  voterID: {
    pattern: /\b[A-Z]{3}\d{7}\b/gi,
    label: { en: 'Possible Voter ID', hi: 'संभावित मतदाता पहचान पत्र' },
    severity: 'medium',
    hint: {
      en: 'Voter ID may be needed for identity verification',
      hi: 'पहचान सत्यापन के लिए मतदाता पहचान पत्र आवश्यक हो सकता है'
    }
  }
};

// Detect PII in text
export const detectPII = (text) => {
  if (!text || typeof text !== 'string') return [];
  
  const detections = [];
  
  Object.entries(PII_PATTERNS).forEach(([type, config]) => {
    const matches = text.match(config.pattern);
    if (matches) {
      matches.forEach(match => {
        // Avoid duplicate detections
        const existing = detections.find(d => d.match === match);
        if (!existing) {
          detections.push({
            type,
            match,
            label: config.label,
            severity: config.severity,
            hint: config.hint
          });
        }
      });
    }
  });
  
  // Sort by severity
  const severityOrder = { high: 0, medium: 1, low: 2 };
  detections.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);
  
  return detections;
};

// Mask PII value
const maskPII = (value, type) => {
  if (!value) return value;
  
  switch (type) {
    case 'aadhaar':
      return 'XXXX-XXXX-' + value.slice(-4);
    case 'pan':
      return 'XXXXX' + value.slice(5, 9) + 'X';
    case 'phone':
      return value.slice(0, -4).replace(/\d/g, 'X') + value.slice(-4);
    case 'email':
      const [local, domain] = value.split('@');
      return local.slice(0, 2) + '***@' + domain;
    case 'bankAccount':
      return 'X'.repeat(value.length - 4) + value.slice(-4);
    default:
      return value.slice(0, 2) + 'X'.repeat(value.length - 4) + value.slice(-2);
  }
};

const PIIWarning = ({ 
  text, 
  onMaskPII,
  language = 'english',
  dismissible = true,
  showDetails = true
}) => {
  const [dismissed, setDismissed] = useState(false);
  const [expandedItem, setExpandedItem] = useState(null);
  const [showAllValues, setShowAllValues] = useState(false);
  
  const isHindi = language === 'hindi';
  
  const detections = useMemo(() => detectPII(text), [text]);
  
  const handleMask = useCallback((detection) => {
    if (onMaskPII) {
      const maskedValue = maskPII(detection.match, detection.type);
      onMaskPII(detection.match, maskedValue);
    }
  }, [onMaskPII]);
  
  const handleMaskAll = useCallback(() => {
    if (onMaskPII) {
      detections.forEach(detection => {
        const maskedValue = maskPII(detection.match, detection.type);
        onMaskPII(detection.match, maskedValue);
      });
    }
  }, [detections, onMaskPII]);
  
  // No PII detected or dismissed
  if (detections.length === 0 || dismissed) {
    return null;
  }
  
  const highSeverityCount = detections.filter(d => d.severity === 'high').length;
  
  return (
    <div 
      className={`pii-warning ${highSeverityCount > 0 ? 'high-severity' : 'medium-severity'}`}
      role="alert"
      aria-live="polite"
    >
      <div className="warning-header">
        <div className="warning-icon">
          <Shield size={20} />
        </div>
        
        <div className="warning-content">
          <h4 className="warning-title">
            {isHindi ? 'व्यक्तिगत जानकारी पाई गई' : 'Personal Information Detected'}
          </h4>
          <p className="warning-summary">
            {isHindi 
              ? `${detections.length} संभावित संवेदनशील जानकारी पाई गई। कृपया समीक्षा करें।`
              : `Found ${detections.length} potentially sensitive item${detections.length > 1 ? 's' : ''}. Please review.`}
          </p>
        </div>
        
        <div className="warning-actions-header">
          {onMaskPII && detections.length > 1 && (
            <button 
              className="btn-mask-all"
              onClick={handleMaskAll}
              aria-label={isHindi ? 'सभी मास्क करें' : 'Mask all'}
            >
              <EyeOff size={14} />
              {isHindi ? 'सभी मास्क करें' : 'Mask All'}
            </button>
          )}
          
          {dismissible && (
            <button 
              className="btn-dismiss"
              onClick={() => setDismissed(true)}
              aria-label={isHindi ? 'बंद करें' : 'Dismiss'}
            >
              <X size={16} />
            </button>
          )}
        </div>
      </div>
      
      {showDetails && (
        <div className="detection-list" role="list">
          {detections.map((detection, index) => (
            <div 
              key={`${detection.type}-${index}`}
              className={`detection-item ${detection.severity}`}
              role="listitem"
            >
              <div 
                className="detection-main"
                onClick={() => setExpandedItem(expandedItem === index ? null : index)}
                tabIndex={0}
                onKeyPress={(e) => e.key === 'Enter' && setExpandedItem(expandedItem === index ? null : index)}
              >
                <div className="detection-info">
                  <span className={`severity-badge ${detection.severity}`}>
                    {detection.severity === 'high' 
                      ? (isHindi ? 'उच्च' : 'HIGH')
                      : (isHindi ? 'मध्यम' : 'MEDIUM')}
                  </span>
                  <span className="detection-label">
                    {isHindi ? detection.label.hi : detection.label.en}
                  </span>
                </div>
                
                <div className="detection-value-container">
                  <code className="detection-value">
                    {showAllValues ? detection.match : maskPII(detection.match, detection.type)}
                  </code>
                  <button
                    className="btn-toggle-visibility"
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowAllValues(!showAllValues);
                    }}
                    aria-label={showAllValues ? 'Hide value' : 'Show value'}
                  >
                    {showAllValues ? <EyeOff size={14} /> : <Eye size={14} />}
                  </button>
                </div>
                
                {onMaskPII && (
                  <button
                    className="btn-mask-item"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleMask(detection);
                    }}
                    aria-label={isHindi ? 'इसे मास्क करें' : 'Mask this'}
                  >
                    <EyeOff size={14} />
                  </button>
                )}
              </div>
              
              {expandedItem === index && (
                <div className="detection-hint">
                  <Info size={14} />
                  <span>{isHindi ? detection.hint.hi : detection.hint.en}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      
      <div className="warning-footer">
        <AlertTriangle size={14} />
        <span>
          {isHindi 
            ? 'RTI/शिकायत में आवश्यकता से अधिक व्यक्तिगत जानकारी साझा करने से बचें।'
            : 'Avoid sharing more personal information than necessary in RTI/complaints.'}
        </span>
      </div>
    </div>
  );
};

export default PIIWarning;
