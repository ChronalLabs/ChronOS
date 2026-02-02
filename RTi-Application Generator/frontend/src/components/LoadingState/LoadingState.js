import React from 'react';
import { Loader2, AlertCircle, RefreshCw, WifiOff, Clock, ServerCrash } from 'lucide-react';
import './LoadingState.css';

// Loading spinner with message
export const LoadingSpinner = ({ 
  message, 
  size = 'medium',
  language = 'english' 
}) => {
  const isHindi = language === 'hindi';
  const defaultMessage = isHindi ? 'लोड हो रहा है...' : 'Loading...';
  
  return (
    <div className={`loading-spinner ${size}`} role="status" aria-live="polite">
      <Loader2 className="spinner-icon" />
      <span className="loading-message">{message || defaultMessage}</span>
    </div>
  );
};

// Full page loading overlay
export const LoadingOverlay = ({ 
  message, 
  language = 'english',
  transparent = false 
}) => {
  const isHindi = language === 'hindi';
  
  return (
    <div className={`loading-overlay ${transparent ? 'transparent' : ''}`} role="status" aria-live="polite">
      <div className="loading-content">
        <Loader2 className="spinner-icon large" />
        <p>{message || (isHindi ? 'कृपया प्रतीक्षा करें...' : 'Please wait...')}</p>
      </div>
    </div>
  );
};

// Skeleton loader for content placeholders
export const SkeletonLoader = ({ lines = 3, type = 'text' }) => {
  return (
    <div className={`skeleton-loader ${type}`} aria-hidden="true">
      {type === 'card' ? (
        <div className="skeleton-card">
          <div className="skeleton-header" />
          <div className="skeleton-body">
            {Array(lines).fill(0).map((_, i) => (
              <div 
                key={i} 
                className="skeleton-line" 
                style={{ width: `${100 - (i * 15)}%` }}
              />
            ))}
          </div>
        </div>
      ) : (
        Array(lines).fill(0).map((_, i) => (
          <div 
            key={i} 
            className="skeleton-line" 
            style={{ width: `${100 - (i * 10)}%` }}
          />
        ))
      )}
    </div>
  );
};

// Error display with retry option
export const ErrorDisplay = ({ 
  error, 
  onRetry, 
  language = 'english',
  type = 'general'
}) => {
  const isHindi = language === 'hindi';
  
  const getErrorConfig = () => {
    switch (type) {
      case 'network':
        return {
          icon: WifiOff,
          title: isHindi ? 'नेटवर्क त्रुटि' : 'Network Error',
          description: isHindi 
            ? 'इंटरनेट कनेक्शन की जांच करें और पुनः प्रयास करें।'
            : 'Please check your internet connection and try again.',
          color: 'orange'
        };
      case 'timeout':
        return {
          icon: Clock,
          title: isHindi ? 'समय समाप्त' : 'Request Timeout',
          description: isHindi 
            ? 'सर्वर प्रतिक्रिया में बहुत समय लग रहा है। कृपया पुनः प्रयास करें।'
            : 'The server is taking too long to respond. Please try again.',
          color: 'yellow'
        };
      case 'server':
        return {
          icon: ServerCrash,
          title: isHindi ? 'सर्वर त्रुटि' : 'Server Error',
          description: isHindi 
            ? 'सर्वर में कोई समस्या है। कृपया कुछ समय बाद पुनः प्रयास करें।'
            : 'Something went wrong on our end. Please try again later.',
          color: 'red'
        };
      default:
        return {
          icon: AlertCircle,
          title: isHindi ? 'त्रुटि हुई' : 'Something Went Wrong',
          description: error?.message || (isHindi 
            ? 'एक अप्रत्याशित त्रुटि हुई। कृपया पुनः प्रयास करें।'
            : 'An unexpected error occurred. Please try again.'),
          color: 'red'
        };
    }
  };
  
  const config = getErrorConfig();
  const Icon = config.icon;
  
  return (
    <div className={`error-display ${config.color}`} role="alert">
      <div className="error-icon">
        <Icon size={32} />
      </div>
      <div className="error-content">
        <h4 className="error-title">{config.title}</h4>
        <p className="error-description">{config.description}</p>
        {error?.code && (
          <span className="error-code">
            {isHindi ? 'कोड' : 'Code'}: {error.code}
          </span>
        )}
      </div>
      {onRetry && (
        <button className="retry-button" onClick={onRetry}>
          <RefreshCw size={16} />
          {isHindi ? 'पुनः प्रयास करें' : 'Try Again'}
        </button>
      )}
    </div>
  );
};

// Inline error message
export const InlineError = ({ message, language = 'english' }) => {
  const isHindi = language === 'hindi';
  
  return (
    <div className="inline-error" role="alert">
      <AlertCircle size={14} />
      <span>{message || (isHindi ? 'कोई त्रुटि हुई' : 'An error occurred')}</span>
    </div>
  );
};

// Success message
export const SuccessMessage = ({ message, language = 'english', onDismiss }) => {
  const isHindi = language === 'hindi';
  
  return (
    <div className="success-message" role="status">
      <svg className="success-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
      <span>{message || (isHindi ? 'सफल!' : 'Success!')}</span>
      {onDismiss && (
        <button className="dismiss-btn" onClick={onDismiss} aria-label="Dismiss">
          ×
        </button>
      )}
    </div>
  );
};

// Progress indicator for multi-step operations
export const ProgressIndicator = ({ 
  current, 
  total, 
  message,
  language = 'english' 
}) => {
  const isHindi = language === 'hindi';
  const percentage = Math.round((current / total) * 100);
  
  return (
    <div className="progress-indicator" role="progressbar" aria-valuenow={percentage} aria-valuemin="0" aria-valuemax="100">
      <div className="progress-header">
        <span className="progress-message">{message}</span>
        <span className="progress-count">{current}/{total}</span>
      </div>
      <div className="progress-bar-container">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="progress-percentage">
        {percentage}% {isHindi ? 'पूर्ण' : 'complete'}
      </span>
    </div>
  );
};

// Empty state placeholder
export const EmptyState = ({ 
  icon: Icon = AlertCircle,
  title,
  description,
  action,
  actionLabel,
  language = 'english'
}) => {
  const isHindi = language === 'hindi';
  
  return (
    <div className="empty-state" role="status">
      <div className="empty-icon">
        <Icon size={48} strokeWidth={1.5} />
      </div>
      <h4 className="empty-title">
        {title || (isHindi ? 'कोई डेटा नहीं' : 'No Data')}
      </h4>
      <p className="empty-description">
        {description || (isHindi ? 'यहां अभी कुछ नहीं है।' : 'Nothing here yet.')}
      </p>
      {action && (
        <button className="empty-action" onClick={action}>
          {actionLabel || (isHindi ? 'शुरू करें' : 'Get Started')}
        </button>
      )}
    </div>
  );
};

const LoadingState = {
  LoadingSpinner,
  LoadingOverlay,
  SkeletonLoader,
  ErrorDisplay,
  InlineError,
  SuccessMessage,
  ProgressIndicator,
  EmptyState
};

export default LoadingState;
