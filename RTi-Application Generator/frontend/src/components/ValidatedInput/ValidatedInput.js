import React, { useState, useEffect, useCallback } from 'react';
import { CheckCircle, AlertCircle, AlertTriangle, Info, Loader2 } from 'lucide-react';
import useDebounce from '../../hooks/useDebounce';
import './ValidatedInput.css';

// Validation status types
export const ValidationStatus = {
  IDLE: 'idle',
  VALIDATING: 'validating',
  VALID: 'valid',
  WARNING: 'warning',
  ERROR: 'error',
  INFO: 'info'
};

// Common validation rules
export const ValidationRules = {
  required: (value, msg) => ({
    test: (v) => v && v.trim().length > 0,
    message: msg || { en: 'This field is required', hi: 'यह फ़ील्ड आवश्यक है' }
  }),
  
  minLength: (min, msg) => ({
    test: (v) => !v || v.length >= min,
    message: msg || { en: `Minimum ${min} characters required`, hi: `न्यूनतम ${min} अक्षर आवश्यक हैं` }
  }),
  
  maxLength: (max, msg) => ({
    test: (v) => !v || v.length <= max,
    message: msg || { en: `Maximum ${max} characters allowed`, hi: `अधिकतम ${max} अक्षर अनुमत हैं` }
  }),
  
  email: (msg) => ({
    test: (v) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
    message: msg || { en: 'Please enter a valid email', hi: 'कृपया वैध ईमेल दर्ज करें' }
  }),
  
  phone: (msg) => ({
    test: (v) => !v || /^(\+91[\s-]?)?[6-9]\d{9}$/.test(v.replace(/\s/g, '')),
    message: msg || { en: 'Please enter a valid phone number', hi: 'कृपया वैध फोन नंबर दर्ज करें' }
  }),
  
  pincode: (msg) => ({
    test: (v) => !v || /^\d{6}$/.test(v),
    message: msg || { en: 'Please enter a valid 6-digit pincode', hi: 'कृपया वैध 6-अंकीय पिनकोड दर्ज करें' }
  }),
  
  aadhaar: (msg) => ({
    test: (v) => !v || /^\d{4}[\s-]?\d{4}[\s-]?\d{4}$/.test(v),
    message: msg || { en: 'Please enter a valid Aadhaar number', hi: 'कृपया वैध आधार नंबर दर्ज करें' }
  }),
  
  noSpecialChars: (msg) => ({
    test: (v) => !v || /^[a-zA-Z0-9\s\u0900-\u097F]+$/.test(v),
    message: msg || { en: 'Special characters not allowed', hi: 'विशेष वर्ण अनुमत नहीं हैं' }
  }),
  
  alphanumeric: (msg) => ({
    test: (v) => !v || /^[a-zA-Z0-9]+$/.test(v),
    message: msg || { en: 'Only letters and numbers allowed', hi: 'केवल अक्षर और संख्याएं अनुमत हैं' }
  }),
  
  pattern: (regex, msg) => ({
    test: (v) => !v || regex.test(v),
    message: msg || { en: 'Invalid format', hi: 'अमान्य प्रारूप' }
  }),
  
  custom: (testFn, msg) => ({
    test: testFn,
    message: msg
  })
};

// Main ValidatedInput component
const ValidatedInput = ({
  type = 'text',
  name,
  value,
  onChange,
  onValidate,
  placeholder,
  label,
  hint,
  rules = [],
  validateOnChange = true,
  validateOnBlur = true,
  debounceMs = 300,
  language = 'english',
  disabled = false,
  required = false,
  maxLength,
  showCharCount = false,
  rows = 3,
  className = '',
  ...props
}) => {
  const [status, setStatus] = useState(ValidationStatus.IDLE);
  const [message, setMessage] = useState(null);
  const [touched, setTouched] = useState(false);
  
  const isHindi = language === 'hindi';
  const debouncedValue = useDebounce(value, debounceMs);
  
  // Run validation
  const validate = useCallback((val) => {
    if (!val && !required) {
      setStatus(ValidationStatus.IDLE);
      setMessage(null);
      return true;
    }
    
    // Add required rule if prop is set
    const allRules = required 
      ? [ValidationRules.required(), ...rules]
      : rules;
    
    for (const rule of allRules) {
      if (!rule.test(val)) {
        setStatus(ValidationStatus.ERROR);
        setMessage(typeof rule.message === 'object' 
          ? (isHindi ? rule.message.hi : rule.message.en)
          : rule.message);
        onValidate?.(false, rule.message);
        return false;
      }
    }
    
    setStatus(ValidationStatus.VALID);
    setMessage(null);
    onValidate?.(true);
    return true;
  }, [rules, required, isHindi, onValidate]);
  
  // Validate on debounced value change
  useEffect(() => {
    if (validateOnChange && touched && debouncedValue !== undefined) {
      setStatus(ValidationStatus.VALIDATING);
      // Small delay to show validating state
      const timer = setTimeout(() => {
        validate(debouncedValue);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [debouncedValue, validateOnChange, touched, validate]);
  
  const handleChange = (e) => {
    onChange?.(e);
    if (!touched) setTouched(true);
  };
  
  const handleBlur = () => {
    setTouched(true);
    if (validateOnBlur) {
      validate(value);
    }
  };
  
  const getStatusIcon = () => {
    switch (status) {
      case ValidationStatus.VALIDATING:
        return <Loader2 size={16} className="status-icon validating" />;
      case ValidationStatus.VALID:
        return <CheckCircle size={16} className="status-icon valid" />;
      case ValidationStatus.WARNING:
        return <AlertTriangle size={16} className="status-icon warning" />;
      case ValidationStatus.ERROR:
        return <AlertCircle size={16} className="status-icon error" />;
      case ValidationStatus.INFO:
        return <Info size={16} className="status-icon info" />;
      default:
        return null;
    }
  };
  
  const inputId = `input-${name}`;
  const errorId = `error-${name}`;
  const isTextarea = type === 'textarea';
  
  const InputComponent = isTextarea ? 'textarea' : 'input';
  
  return (
    <div className={`validated-input ${status} ${className}`}>
      {label && (
        <label htmlFor={inputId} className="input-label">
          {label}
          {required && <span className="required-mark" aria-hidden="true">*</span>}
        </label>
      )}
      
      <div className="input-wrapper">
        <InputComponent
          id={inputId}
          type={isTextarea ? undefined : type}
          name={name}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          maxLength={maxLength}
          rows={isTextarea ? rows : undefined}
          aria-invalid={status === ValidationStatus.ERROR}
          aria-describedby={message ? errorId : undefined}
          aria-required={required}
          {...props}
        />
        
        <div className="input-status">
          {getStatusIcon()}
        </div>
      </div>
      
      <div className="input-footer">
        {message && (
          <span 
            id={errorId} 
            className={`validation-message ${status}`}
            role={status === ValidationStatus.ERROR ? 'alert' : 'status'}
          >
            {message}
          </span>
        )}
        
        {hint && !message && (
          <span className="input-hint">{hint}</span>
        )}
        
        {showCharCount && maxLength && (
          <span className={`char-count ${value?.length > maxLength * 0.9 ? 'warning' : ''}`}>
            {value?.length || 0}/{maxLength}
          </span>
        )}
      </div>
    </div>
  );
};

// Pre-configured input variants
export const NameInput = (props) => (
  <ValidatedInput
    type="text"
    rules={[
      ValidationRules.minLength(2),
      ValidationRules.maxLength(100),
      ValidationRules.pattern(/^[a-zA-Z\s\u0900-\u097F.]+$/, {
        en: 'Only letters allowed',
        hi: 'केवल अक्षर अनुमत हैं'
      })
    ]}
    {...props}
  />
);

export const EmailInput = (props) => (
  <ValidatedInput
    type="email"
    rules={[ValidationRules.email()]}
    {...props}
  />
);

export const PhoneInput = (props) => (
  <ValidatedInput
    type="tel"
    rules={[ValidationRules.phone()]}
    {...props}
  />
);

export const PincodeInput = (props) => (
  <ValidatedInput
    type="text"
    maxLength={6}
    rules={[ValidationRules.pincode()]}
    {...props}
  />
);

export const AddressInput = (props) => (
  <ValidatedInput
    type="textarea"
    rows={3}
    rules={[
      ValidationRules.minLength(10, { en: 'Address too short', hi: 'पता बहुत छोटा है' }),
      ValidationRules.maxLength(500)
    ]}
    {...props}
  />
);

export default ValidatedInput;
