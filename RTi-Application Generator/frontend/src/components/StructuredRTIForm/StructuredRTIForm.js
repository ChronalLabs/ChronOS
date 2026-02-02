import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, HelpCircle, Calendar, Building, FileText, Info } from 'lucide-react';
import './StructuredRTIForm.css';

// Validation rules for RTI requests
const VALIDATION_RULES = {
  information_sought: {
    required: true,
    minLength: 20,
    maxLength: 2000,
    patterns: [
      { regex: /\?|जानकारी|details|information|records|copies/i, message: "Should clearly state what information is being sought" }
    ]
  },
  time_period: {
    required: true,
    validate: (value) => {
      if (!value) return { valid: false, message: "Time period is required" };
      // Check for date patterns
      const hasDatePattern = /\d{4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|january|february|march|april|may|june|july|august|september|october|november|december|जनवरी|फ़रवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर|last\s+\d+\s+(years?|months?)|पिछले/i.test(value);
      if (!hasDatePattern) return { valid: false, message: "Please specify a clear time period (e.g., '2023-2024' or 'Last 2 years')" };
      return { valid: true };
    }
  },
  department: {
    required: true,
    minLength: 3
  },
  record_type: {
    required: true
  }
};

// Record types for RTI
const RECORD_TYPES = [
  { value: 'documents', label: 'Official Documents', labelHi: 'आधिकारिक दस्तावेज़', description: 'Orders, circulars, notifications' },
  { value: 'files', label: 'Files/Notings', labelHi: 'फाइलें/टिप्पणियां', description: 'File notings, internal correspondence' },
  { value: 'data', label: 'Data/Statistics', labelHi: 'डेटा/आंकड़े', description: 'Numerical data, statistics, reports' },
  { value: 'correspondence', label: 'Correspondence', labelHi: 'पत्राचार', description: 'Letters, emails, communications' },
  { value: 'contracts', label: 'Contracts/Agreements', labelHi: 'अनुबंध/समझौते', description: 'Tenders, contracts, MOUs' },
  { value: 'inspection', label: 'Inspection of Records', labelHi: 'अभिलेखों का निरीक्षण', description: 'Physical inspection of documents' },
  { value: 'certified_copies', label: 'Certified Copies', labelHi: 'प्रमाणित प्रतियां', description: 'Attested copies of documents' },
  { value: 'samples', label: 'Samples/Materials', labelHi: 'नमूने/सामग्री', description: 'Physical samples of materials' }
];

// Common departments
const COMMON_DEPARTMENTS = [
  { value: 'pwd', label: 'Public Works Department (PWD)', labelHi: 'लोक निर्माण विभाग' },
  { value: 'electricity', label: 'Electricity Department', labelHi: 'विद्युत विभाग' },
  { value: 'water', label: 'Water Supply Department', labelHi: 'जल आपूर्ति विभाग' },
  { value: 'municipal', label: 'Municipal Corporation', labelHi: 'नगर निगम' },
  { value: 'police', label: 'Police Department', labelHi: 'पुलिस विभाग' },
  { value: 'health', label: 'Health Department', labelHi: 'स्वास्थ्य विभाग' },
  { value: 'education', label: 'Education Department', labelHi: 'शिक्षा विभाग' },
  { value: 'revenue', label: 'Revenue Department', labelHi: 'राजस्व विभाग' },
  { value: 'transport', label: 'Transport Department', labelHi: 'परिवहन विभाग' },
  { value: 'panchayat', label: 'Panchayat/Rural Development', labelHi: 'पंचायत/ग्रामीण विकास' },
  { value: 'other', label: 'Other Department', labelHi: 'अन्य विभाग' }
];

const StructuredRTIForm = ({ data, onChange, language = 'english', onValidationChange }) => {
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [showHelp, setShowHelp] = useState({});

  const isHindi = language === 'hindi';

  // Validate all fields
  const validateField = (fieldName, value) => {
    const rule = VALIDATION_RULES[fieldName];
    if (!rule) return { valid: true };

    if (rule.required && (!value || value.trim() === '')) {
      return { valid: false, message: isHindi ? 'यह फ़ील्ड आवश्यक है' : 'This field is required' };
    }

    if (rule.minLength && value && value.length < rule.minLength) {
      return { valid: false, message: isHindi ? `न्यूनतम ${rule.minLength} अक्षर आवश्यक` : `Minimum ${rule.minLength} characters required` };
    }

    if (rule.maxLength && value && value.length > rule.maxLength) {
      return { valid: false, message: isHindi ? `अधिकतम ${rule.maxLength} अक्षर` : `Maximum ${rule.maxLength} characters allowed` };
    }

    if (rule.validate) {
      return rule.validate(value);
    }

    if (rule.patterns) {
      for (const pattern of rule.patterns) {
        if (!pattern.regex.test(value || '')) {
          return { valid: false, message: pattern.message };
        }
      }
    }

    return { valid: true };
  };

  // Validate all fields and notify parent
  useEffect(() => {
    const newErrors = {};
    let isValid = true;

    ['information_sought', 'time_period', 'department', 'record_type'].forEach(field => {
      const result = validateField(field, data[field]);
      if (!result.valid) {
        newErrors[field] = result.message;
        isValid = false;
      }
    });

    setErrors(newErrors);
    if (onValidationChange) {
      onValidationChange(isValid, newErrors);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, language]);

  const handleBlur = (fieldName) => {
    setTouched(prev => ({ ...prev, [fieldName]: true }));
  };

  const handleChange = (fieldName, value) => {
    onChange({ ...data, [fieldName]: value });
  };

  const toggleHelp = (fieldName) => {
    setShowHelp(prev => ({ ...prev, [fieldName]: !prev[fieldName] }));
  };

  const renderFieldStatus = (fieldName) => {
    if (!touched[fieldName] && !data[fieldName]) return null;
    
    if (errors[fieldName]) {
      return <AlertCircle size={16} className="field-status error" />;
    }
    if (data[fieldName]) {
      return <CheckCircle size={16} className="field-status success" />;
    }
    return null;
  };

  return (
    <div className="structured-rti-form">
      <div className="form-section">
        <h3 className="section-title">
          <FileText size={18} />
          {isHindi ? 'मांगी गई जानकारी' : 'Information Sought'}
          <span className="required-badge">*</span>
        </h3>
        
        <div className="field-help-toggle" onClick={() => toggleHelp('information_sought')}>
          <HelpCircle size={14} />
          {isHindi ? 'यह क्यों महत्वपूर्ण है?' : 'Why is this important?'}
        </div>
        
        {showHelp.information_sought && (
          <div className="help-box">
            <Info size={14} />
            <p>
              {isHindi 
                ? 'स्पष्ट और विशिष्ट प्रश्न पूछें। अस्पष्ट अनुरोध अक्सर अस्वीकार कर दिए जाते हैं। प्रत्येक प्रश्न को अलग-अलग बिंदुओं में लिखें।'
                : 'Ask clear, specific questions. Vague requests are often rejected. Frame each question as a separate point. The PIO must understand exactly what you want.'}
            </p>
          </div>
        )}

        <div className="input-wrapper">
          <textarea
            className={`form-textarea ${touched.information_sought && errors.information_sought ? 'error' : ''}`}
            rows="5"
            value={data.information_sought || ''}
            onChange={(e) => handleChange('information_sought', e.target.value)}
            onBlur={() => handleBlur('information_sought')}
            placeholder={isHindi 
              ? "उदाहरण:\n1. वित्त वर्ष 2023-24 में सड़क निर्माण पर खर्च की गई कुल राशि\n2. ठेकेदार का नाम और पता\n3. कार्य पूर्णता प्रमाण पत्र की प्रति"
              : "Example:\n1. Total amount spent on road construction in FY 2023-24\n2. Name and address of the contractor\n3. Copy of work completion certificate"}
          />
          {renderFieldStatus('information_sought')}
        </div>
        
        {touched.information_sought && errors.information_sought && (
          <div className="error-message">
            <AlertCircle size={14} />
            {errors.information_sought}
          </div>
        )}

        <div className="char-count">
          {(data.information_sought || '').length} / 2000
        </div>
      </div>

      <div className="form-row">
        <div className="form-section half">
          <h3 className="section-title">
            <Calendar size={18} />
            {isHindi ? 'समय अवधि' : 'Time Period'}
            <span className="required-badge">*</span>
          </h3>

          <div className="field-help-toggle" onClick={() => toggleHelp('time_period')}>
            <HelpCircle size={14} />
            {isHindi ? 'यह क्यों महत्वपूर्ण है?' : 'Why is this important?'}
          </div>

          {showHelp.time_period && (
            <div className="help-box">
              <Info size={14} />
              <p>
                {isHindi 
                  ? 'RTI अधिनियम के तहत, आपको उस समय अवधि को निर्दिष्ट करना होगा जिसके लिए जानकारी चाहिए। बिना समय अवधि के अनुरोध अस्वीकार किए जा सकते हैं।'
                  : 'Under the RTI Act, you must specify the time period for which information is sought. Requests without time periods can be rejected as too broad.'}
              </p>
            </div>
          )}

          <div className="input-wrapper">
            <input
              type="text"
              className={`form-input ${touched.time_period && errors.time_period ? 'error' : ''}`}
              value={data.time_period || ''}
              onChange={(e) => handleChange('time_period', e.target.value)}
              onBlur={() => handleBlur('time_period')}
              placeholder={isHindi ? "जैसे: 2023-2024 या पिछले 2 वर्ष" : "e.g., 2023-2024 or Last 2 years"}
            />
            {renderFieldStatus('time_period')}
          </div>
          
          {touched.time_period && errors.time_period && (
            <div className="error-message">
              <AlertCircle size={14} />
              {errors.time_period}
            </div>
          )}

          <div className="quick-options">
            <button type="button" onClick={() => handleChange('time_period', 'Last 1 year')}>
              {isHindi ? 'पिछला 1 वर्ष' : 'Last 1 year'}
            </button>
            <button type="button" onClick={() => handleChange('time_period', 'Last 3 years')}>
              {isHindi ? 'पिछले 3 वर्ष' : 'Last 3 years'}
            </button>
            <button type="button" onClick={() => handleChange('time_period', '2024-2025')}>
              2024-2025
            </button>
          </div>
        </div>

        <div className="form-section half">
          <h3 className="section-title">
            <Building size={18} />
            {isHindi ? 'संबंधित विभाग' : 'Concerned Department'}
            <span className="required-badge">*</span>
          </h3>

          <div className="field-help-toggle" onClick={() => toggleHelp('department')}>
            <HelpCircle size={14} />
            {isHindi ? 'यह क्यों महत्वपूर्ण है?' : 'Why is this important?'}
          </div>

          {showHelp.department && (
            <div className="help-box warning">
              <AlertCircle size={14} />
              <p>
                {isHindi 
                  ? '⚠️ गलत विभाग में RTI दाखिल करना = तुरंत अस्वीकृति। यदि आप सुनिश्चित नहीं हैं, तो हम सही विभाग खोजने में मदद करेंगे।'
                  : '⚠️ Filing RTI to wrong department = instant rejection. If you\'re unsure, we\'ll help identify the correct department.'}
              </p>
            </div>
          )}

          <div className="input-wrapper">
            <select
              className={`form-select ${touched.department && errors.department ? 'error' : ''}`}
              value={data.department || ''}
              onChange={(e) => handleChange('department', e.target.value)}
              onBlur={() => handleBlur('department')}
            >
              <option value="">{isHindi ? '-- विभाग चुनें --' : '-- Select Department --'}</option>
              {COMMON_DEPARTMENTS.map(dept => (
                <option key={dept.value} value={dept.value}>
                  {isHindi ? dept.labelHi : dept.label}
                </option>
              ))}
            </select>
            {renderFieldStatus('department')}
          </div>

          {data.department === 'other' && (
            <input
              type="text"
              className="form-input mt-2"
              value={data.department_other || ''}
              onChange={(e) => handleChange('department_other', e.target.value)}
              placeholder={isHindi ? "विभाग का नाम लिखें" : "Enter department name"}
            />
          )}

          {touched.department && errors.department && (
            <div className="error-message">
              <AlertCircle size={14} />
              {errors.department}
            </div>
          )}
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">
          <FileText size={18} />
          {isHindi ? 'अभिलेखों का प्रकार' : 'Type of Records'}
          <span className="required-badge">*</span>
        </h3>

        <div className="field-help-toggle" onClick={() => toggleHelp('record_type')}>
          <HelpCircle size={14} />
          {isHindi ? 'यह क्यों महत्वपूर्ण है?' : 'Why is this important?'}
        </div>

        {showHelp.record_type && (
          <div className="help-box">
            <Info size={14} />
            <p>
              {isHindi 
                ? 'विशिष्ट प्रकार के अभिलेख मांगने से प्रसंस्करण तेज होता है और अस्पष्ट प्रतिक्रियाओं से बचा जा सकता है।'
                : 'Specifying the type of records speeds up processing and avoids vague responses. You can select multiple types.'}
            </p>
          </div>
        )}

        <div className="record-type-grid">
          {RECORD_TYPES.map(type => (
            <label 
              key={type.value} 
              className={`record-type-option ${(data.record_types || []).includes(type.value) ? 'selected' : ''}`}
            >
              <input
                type="checkbox"
                checked={(data.record_types || []).includes(type.value)}
                onChange={(e) => {
                  const currentTypes = data.record_types || [];
                  const newTypes = e.target.checked 
                    ? [...currentTypes, type.value]
                    : currentTypes.filter(t => t !== type.value);
                  handleChange('record_types', newTypes);
                  handleChange('record_type', newTypes.length > 0 ? newTypes.join(', ') : '');
                }}
              />
              <div className="option-content">
                <span className="option-label">{isHindi ? type.labelHi : type.label}</span>
                <span className="option-desc">{type.description}</span>
              </div>
            </label>
          ))}
        </div>

        {touched.record_type && errors.record_type && (
          <div className="error-message">
            <AlertCircle size={14} />
            {errors.record_type}
          </div>
        )}
      </div>

      {/* Validation Summary */}
      <div className="validation-summary">
        <h4>{isHindi ? 'सत्यापन स्थिति' : 'Validation Status'}</h4>
        <div className="validation-items">
          <div className={`validation-item ${data.information_sought && !errors.information_sought ? 'valid' : 'invalid'}`}>
            {data.information_sought && !errors.information_sought ? <CheckCircle size={14} /> : <AlertCircle size={14} />}
            {isHindi ? 'जानकारी विवरण' : 'Information Details'}
          </div>
          <div className={`validation-item ${data.time_period && !errors.time_period ? 'valid' : 'invalid'}`}>
            {data.time_period && !errors.time_period ? <CheckCircle size={14} /> : <AlertCircle size={14} />}
            {isHindi ? 'समय अवधि' : 'Time Period'}
          </div>
          <div className={`validation-item ${data.department && !errors.department ? 'valid' : 'invalid'}`}>
            {data.department && !errors.department ? <CheckCircle size={14} /> : <AlertCircle size={14} />}
            {isHindi ? 'विभाग' : 'Department'}
          </div>
          <div className={`validation-item ${data.record_type && !errors.record_type ? 'valid' : 'invalid'}`}>
            {data.record_type && !errors.record_type ? <CheckCircle size={14} /> : <AlertCircle size={14} />}
            {isHindi ? 'अभिलेख प्रकार' : 'Record Type'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StructuredRTIForm;
