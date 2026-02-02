import React, { useState } from 'react';
import { Shield, Trash2, Download, AlertTriangle, CheckCircle, Info, Eye, EyeOff } from 'lucide-react';
import './PrivacyControls.css';

const PrivacyControls = ({ 
  language = 'english',
  onClearData,
  onDownloadData,
  dataFields = ['applicant_name', 'applicant_address', 'applicant_phone', 'applicant_email', 'issue_description']
}) => {
  const [showConfirmClear, setShowConfirmClear] = useState(false);
  const [cleared, setCleared] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  const isHindi = language === 'hindi';

  const handleClearData = () => {
    if (onClearData) {
      onClearData();
    }
    setCleared(true);
    setShowConfirmClear(false);
    
    // Reset cleared state after 3 seconds
    setTimeout(() => setCleared(false), 3000);
  };

  const handleDownloadData = () => {
    if (onDownloadData) {
      onDownloadData();
    }
  };

  return (
    <div className="privacy-controls">
      <div className="privacy-header">
        <Shield size={18} />
        <h3>{isHindi ? 'गोपनीयता नियंत्रण' : 'Privacy Controls'}</h3>
      </div>

      {/* Privacy Notice */}
      <div className="privacy-notice">
        <Info size={14} />
        <div>
          <strong>{isHindi ? 'आपका डेटा सुरक्षित है' : 'Your Data is Safe'}</strong>
          <p>
            {isHindi 
              ? 'हम कोई व्यक्तिगत जानकारी संग्रहीत नहीं करते। सभी प्रसंस्करण आपके ब्राउज़र में होता है।'
              : 'We do not store any personal information. All processing happens in your browser.'}
          </p>
        </div>
      </div>

      {/* Privacy Features */}
      <div className="privacy-features">
        <div className="feature-item">
          <CheckCircle size={14} className="feature-icon success" />
          <span>{isHindi ? 'कोई डेटाबेस संग्रहण नहीं' : 'No database storage'}</span>
        </div>
        <div className="feature-item">
          <CheckCircle size={14} className="feature-icon success" />
          <span>{isHindi ? 'कोई उपयोगकर्ता ट्रैकिंग नहीं' : 'No user tracking'}</span>
        </div>
        <div className="feature-item">
          <CheckCircle size={14} className="feature-icon success" />
          <span>{isHindi ? 'कोई तृतीय-पक्ष साझाकरण नहीं' : 'No third-party sharing'}</span>
        </div>
        <div className="feature-item">
          <CheckCircle size={14} className="feature-icon success" />
          <span>{isHindi ? 'सत्र समाप्ति पर स्वतः हटाना' : 'Auto-delete on session end'}</span>
        </div>
      </div>

      {/* What Data We Process */}
      <div className="data-processed">
        <button 
          className="data-toggle"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? <EyeOff size={14} /> : <Eye size={14} />}
          {isHindi ? 'हम क्या प्रोसेस करते हैं देखें' : 'See what we process'}
        </button>

        {showDetails && (
          <div className="data-list">
            <p className="data-intro">
              {isHindi 
                ? 'निम्नलिखित जानकारी केवल आपके ड्राफ्ट बनाने के लिए अस्थायी रूप से उपयोग की जाती है:'
                : 'The following information is temporarily used only to generate your draft:'}
            </p>
            <ul>
              {dataFields.map((field, idx) => (
                <li key={idx}>
                  {field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  <span className="data-note">
                    ({isHindi ? 'संग्रहीत नहीं' : 'Not stored'})
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="privacy-actions">
        <button 
          className="btn btn-outline download-btn"
          onClick={handleDownloadData}
          title={isHindi ? 'अपना डेटा डाउनलोड करें' : 'Download your data'}
        >
          <Download size={16} />
          {isHindi ? 'डेटा डाउनलोड करें' : 'Download My Data'}
        </button>

        <button 
          className="btn btn-outline delete-btn"
          onClick={() => setShowConfirmClear(true)}
          title={isHindi ? 'सभी डेटा साफ़ करें' : 'Clear all data'}
        >
          <Trash2 size={16} />
          {isHindi ? 'सभी साफ़ करें' : 'Clear All'}
        </button>
      </div>

      {/* Success Message */}
      {cleared && (
        <div className="clear-success">
          <CheckCircle size={14} />
          {isHindi ? 'सभी डेटा साफ़ कर दिया गया!' : 'All data cleared!'}
        </div>
      )}

      {/* Confirm Clear Modal */}
      {showConfirmClear && (
        <div className="confirm-overlay">
          <div className="confirm-modal">
            <AlertTriangle size={24} className="warning-icon" />
            <h4>{isHindi ? 'डेटा साफ़ करें?' : 'Clear All Data?'}</h4>
            <p>
              {isHindi 
                ? 'यह आपके वर्तमान सत्र से सभी दर्ज किए गए डेटा को हटा देगा। यह क्रिया पूर्ववत नहीं की जा सकती।'
                : 'This will remove all entered data from your current session. This action cannot be undone.'}
            </p>
            <div className="confirm-actions">
              <button 
                className="btn btn-secondary"
                onClick={() => setShowConfirmClear(false)}
              >
                {isHindi ? 'रद्द करें' : 'Cancel'}
              </button>
              <button 
                className="btn btn-danger"
                onClick={handleClearData}
              >
                <Trash2 size={14} />
                {isHindi ? 'हां, साफ़ करें' : 'Yes, Clear All'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Legal Footer */}
      <div className="privacy-footer">
        <p>
          {isHindi 
            ? 'हम भारत के डेटा संरक्षण कानूनों का अनुपालन करते हैं। कोई व्यक्तिगत डेटा स्थायी रूप से संग्रहीत नहीं किया जाता।'
            : 'We comply with Indian data protection laws. No personal data is permanently stored.'}
        </p>
      </div>
    </div>
  );
};

export default PrivacyControls;
