import React, { useState, useEffect, useRef } from 'react';
import { AlertTriangle, Edit3, Eye, Shield, CheckCircle, X, RotateCcw } from 'lucide-react';
import './ConstrainedDraftEditor.css';

// Critical patterns that should be preserved
const CRITICAL_PATTERNS = {
  rti: [
    { pattern: /RTI\s*(Act|अधिनियम)/gi, label: 'RTI Act Reference', labelHi: 'RTI अधिनियम संदर्भ' },
    { pattern: /(Section|धारा)\s*6/gi, label: 'Section 6 Reference', labelHi: 'धारा 6 संदर्भ' },
    { pattern: /citizen\s*of\s*India|भारत\s*का\s*नागरिक/gi, label: 'Citizenship Declaration', labelHi: 'नागरिकता घोषणा' },
    { pattern: /Public\s*Information\s*Officer|लोक\s*सूचना\s*अधिकारी|PIO/gi, label: 'PIO Addressee', labelHi: 'PIO पता' },
  ],
  complaint: [
    { pattern: /Subject:/gi, label: 'Subject Line', labelHi: 'विषय पंक्ति' },
    { pattern: /grievance|complaint|शिकायत/gi, label: 'Complaint Reference', labelHi: 'शिकायत संदर्भ' },
  ]
};

// Sections that are editable vs protected (used for future validation)
// eslint-disable-next-line no-unused-vars
const SECTION_TYPES = {
  protected: ['addressee', 'legal_reference', 'signature_block'],
  editable: ['information_sought', 'time_period', 'additional_details']
};

const ConstrainedDraftEditor = ({ 
  draftText, 
  originalText,
  documentType = 'information_request',
  language = 'english',
  onEdit,
  onValidationChange 
}) => {
  const [editedText, setEditedText] = useState(draftText);
  const [warnings, setWarnings] = useState([]);
  const [showWarningModal, setShowWarningModal] = useState(false);
  const [pendingEdit, setPendingEdit] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [highlightedRanges, setHighlightedRanges] = useState([]);
  const textareaRef = useRef(null);

  const isHindi = language === 'hindi';
  const isRTI = documentType.includes('request') || documentType.includes('rti');

  // Check for warnings when text changes
  useEffect(() => {
    if (editedText !== originalText) {
      const newWarnings = checkForWarnings(originalText, editedText);
      setWarnings(newWarnings);
      if (onValidationChange) {
        onValidationChange(newWarnings.length === 0, newWarnings);
      }
    } else {
      setWarnings([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [editedText, originalText]);

  // Find critical patterns in text and highlight them
  useEffect(() => {
    const patterns = isRTI ? CRITICAL_PATTERNS.rti : CRITICAL_PATTERNS.complaint;
    const ranges = [];
    
    patterns.forEach(({ pattern, label }) => {
      let match;
      const regex = new RegExp(pattern.source, pattern.flags);
      while ((match = regex.exec(editedText)) !== null) {
        ranges.push({
          start: match.index,
          end: match.index + match[0].length,
          label,
          text: match[0]
        });
      }
    });
    
    setHighlightedRanges(ranges);
  }, [editedText, isRTI]);

  const checkForWarnings = (original, edited) => {
    const warnings = [];
    const patterns = isRTI ? CRITICAL_PATTERNS.rti : CRITICAL_PATTERNS.complaint;

    patterns.forEach(({ pattern, label, labelHi }) => {
      const originalHas = pattern.test(original);
      pattern.lastIndex = 0; // Reset regex
      const editedHas = pattern.test(edited);
      pattern.lastIndex = 0; // Reset regex

      if (originalHas && !editedHas) {
        warnings.push({
          type: 'critical_removed',
          message: isHindi 
            ? `महत्वपूर्ण तत्व हटाया गया: ${labelHi}`
            : `Critical element removed: ${label}`,
          label: isHindi ? labelHi : label,
          severity: 'error'
        });
      }
    });

    // Check if structure is broken
    if (original.includes('Subject:') && !edited.includes('Subject:')) {
      warnings.push({
        type: 'structure_broken',
        message: isHindi 
          ? 'विषय पंक्ति हटा दी गई है - यह औपचारिक आवेदनों के लिए आवश्यक है'
          : 'Subject line removed - this is required for formal applications',
        severity: 'warning'
      });
    }

    // Check if significantly shortened
    if (edited.length < original.length * 0.5) {
      warnings.push({
        type: 'significantly_shortened',
        message: isHindi 
          ? 'ड्राफ्ट काफी छोटा कर दिया गया है। सुनिश्चित करें कि सभी आवश्यक जानकारी शामिल है।'
          : 'Draft has been significantly shortened. Ensure all required information is included.',
        severity: 'warning'
      });
    }

    return warnings;
  };

  const handleTextChange = (e) => {
    const newText = e.target.value;
    const newWarnings = checkForWarnings(originalText, newText);
    
    // If there are critical warnings, show modal
    const criticalWarnings = newWarnings.filter(w => w.severity === 'error');
    if (criticalWarnings.length > 0 && warnings.filter(w => w.severity === 'error').length === 0) {
      setPendingEdit(newText);
      setShowWarningModal(true);
    } else {
      setEditedText(newText);
      if (onEdit) onEdit(newText);
    }
  };

  const confirmEdit = () => {
    if (pendingEdit !== null) {
      setEditedText(pendingEdit);
      if (onEdit) onEdit(pendingEdit);
      setPendingEdit(null);
    }
    setShowWarningModal(false);
  };

  const cancelEdit = () => {
    setPendingEdit(null);
    setShowWarningModal(false);
  };

  const revertToOriginal = () => {
    setEditedText(originalText);
    if (onEdit) onEdit(originalText);
    setWarnings([]);
  };

  const hasChanges = editedText !== originalText;

  return (
    <div className="constrained-editor">
      {/* Editor Header */}
      <div className="editor-header">
        <div className="editor-title">
          <Edit3 size={18} />
          <h3>{isHindi ? 'ड्राफ्ट संपादित करें' : 'Edit Draft'}</h3>
        </div>
        <div className="editor-actions">
          {hasChanges && (
            <button className="btn-icon" onClick={revertToOriginal} title={isHindi ? 'मूल पर वापस जाएं' : 'Revert to original'}>
              <RotateCcw size={16} />
            </button>
          )}
          <button 
            className={`view-toggle ${isEditing ? 'active' : ''}`}
            onClick={() => setIsEditing(!isEditing)}
          >
            {isEditing ? <Eye size={16} /> : <Edit3 size={16} />}
            {isEditing ? (isHindi ? 'पूर्वावलोकन' : 'Preview') : (isHindi ? 'संपादित करें' : 'Edit')}
          </button>
        </div>
      </div>

      {/* Warning Banner */}
      {warnings.length > 0 && (
        <div className={`warning-banner ${warnings.some(w => w.severity === 'error') ? 'error' : 'warning'}`}>
          <AlertTriangle size={16} />
          <div className="warning-content">
            <strong>
              {isHindi ? 'संपादन चेतावनी' : 'Edit Warning'}
            </strong>
            <ul>
              {warnings.map((w, idx) => (
                <li key={idx}>{w.message}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Protected Elements Info */}
      <div className="protected-info">
        <Shield size={14} />
        <span>
          {isHindi 
            ? 'हाइलाइट किए गए तत्व कानूनी रूप से महत्वपूर्ण हैं। इन्हें हटाने से पहले सावधान रहें।'
            : 'Highlighted elements are legally important. Be cautious before removing them.'}
        </span>
      </div>

      {/* Editor / Preview */}
      <div className="editor-content">
        {isEditing ? (
          <textarea
            ref={textareaRef}
            className="draft-textarea"
            value={editedText}
            onChange={handleTextChange}
            rows={15}
            placeholder={isHindi ? 'अपना ड्राफ्ट यहां संपादित करें...' : 'Edit your draft here...'}
          />
        ) : (
          <div className="draft-preview">
            <HighlightedText 
              text={editedText} 
              highlights={highlightedRanges}
              isHindi={isHindi}
            />
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="editor-status">
        <div className="status-left">
          {hasChanges ? (
            <span className="status-modified">
              <Edit3 size={12} />
              {isHindi ? 'संशोधित' : 'Modified'}
            </span>
          ) : (
            <span className="status-original">
              <CheckCircle size={12} />
              {isHindi ? 'मूल' : 'Original'}
            </span>
          )}
        </div>
        <div className="status-right">
          <span>{editedText.length} {isHindi ? 'अक्षर' : 'characters'}</span>
          <span>{editedText.split(/\s+/).filter(Boolean).length} {isHindi ? 'शब्द' : 'words'}</span>
        </div>
      </div>

      {/* Warning Modal */}
      {showWarningModal && (
        <div className="warning-modal-overlay">
          <div className="warning-modal">
            <div className="modal-header">
              <AlertTriangle size={24} className="warning-icon" />
              <h3>{isHindi ? 'महत्वपूर्ण चेतावनी' : 'Important Warning'}</h3>
              <button className="modal-close" onClick={cancelEdit}>
                <X size={20} />
              </button>
            </div>
            <div className="modal-body">
              <p>
                {isHindi 
                  ? 'आपके संपादन ने महत्वपूर्ण कानूनी तत्वों को हटा दिया है:'
                  : 'Your edit has removed critical legal elements:'}
              </p>
              <ul>
                {warnings.filter(w => w.severity === 'error').map((w, idx) => (
                  <li key={idx}>{w.label}</li>
                ))}
              </ul>
              <p className="modal-warning-text">
                {isHindi 
                  ? 'इन तत्वों को हटाने से आपका RTI अमान्य हो सकता है। क्या आप सुनिश्चित हैं?'
                  : 'Removing these elements may invalidate your RTI application. Are you sure?'}
              </p>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={cancelEdit}>
                {isHindi ? 'रद्द करें' : 'Cancel'}
              </button>
              <button className="btn btn-warning" onClick={confirmEdit}>
                {isHindi ? 'फिर भी जारी रखें' : 'Proceed Anyway'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Component to render text with highlighted critical elements
const HighlightedText = ({ text, highlights, isHindi }) => {
  if (!highlights.length) {
    return <pre className="preview-text">{text}</pre>;
  }

  // Sort highlights by start position
  const sortedHighlights = [...highlights].sort((a, b) => a.start - b.start);
  
  const parts = [];
  let lastEnd = 0;

  sortedHighlights.forEach((highlight, idx) => {
    // Add text before highlight
    if (highlight.start > lastEnd) {
      parts.push(
        <span key={`text-${idx}`}>{text.slice(lastEnd, highlight.start)}</span>
      );
    }
    
    // Add highlighted text
    parts.push(
      <span 
        key={`highlight-${idx}`} 
        className="protected-text"
        title={`${isHindi ? 'संरक्षित:' : 'Protected:'} ${highlight.label}`}
      >
        {highlight.text}
      </span>
    );
    
    lastEnd = highlight.end;
  });

  // Add remaining text
  if (lastEnd < text.length) {
    parts.push(<span key="text-end">{text.slice(lastEnd)}</span>);
  }

  return <pre className="preview-text">{parts}</pre>;
};

export default ConstrainedDraftEditor;
