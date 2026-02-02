import React, { useRef, useState } from 'react';
import { FileText, Edit3, Lock, AlertTriangle, CheckCircle, Shield } from 'lucide-react';
import './DraftPreview.css';

/**
 * DraftPreview - Legal Document Review Component
 * 
 * This is NOT a "live AI preview". This is a legal document review pane.
 * The goal is to make users feel they are reviewing a complete, stable,
 * and printable RTI/Complaint document.
 */
const DraftPreview = ({ 
  draftText, 
  onEdit, 
  documentType = 'RTI Application',
  language = 'English',
  mode = 'Assisted',
  isReady = true 
}) => {
  const textareaRef = useRef(null);
  const [editingEnabled, setEditingEnabled] = useState(false);
  const [showEditWarning, setShowEditWarning] = useState(false);

  const handleEnableEditing = () => {
    if (!editingEnabled) {
      setShowEditWarning(true);
    } else {
      setEditingEnabled(false);
    }
  };

  const confirmEditing = () => {
    setEditingEnabled(true);
    setShowEditWarning(false);
    setTimeout(() => {
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    }, 100);
  };

  const cancelEditing = () => {
    setShowEditWarning(false);
  };

  const getDocumentTypeLabel = () => {
    const type = documentType?.toLowerCase() || '';
    if (type.includes('information') || type.includes('rti')) {
      return 'RTI Application';
    } else if (type.includes('grievance') || type.includes('complaint')) {
      return 'Public Grievance';
    } else if (type.includes('records')) {
      return 'RTI - Records Request';
    } else if (type.includes('inspection')) {
      return 'RTI - Inspection Request';
    }
    return 'Official Document';
  };

  return (
    <div className="document-review-pane">
      {/* Context Header - Builds Trust */}
      <div className="document-context-header">
        <div className="context-info">
          <div className="context-badge document-type">
            <FileText size={14} />
            <span>{getDocumentTypeLabel()}</span>
          </div>
          <div className="context-badge language">
            <span>{language === 'hindi' ? 'हिंदी' : 'English'}</span>
          </div>
          <div className="context-badge mode">
            <span>{mode} Mode</span>
          </div>
        </div>
        <div className={`status-badge ${isReady ? 'ready' : 'processing'}`}>
          {isReady ? (
            <>
              <CheckCircle size={14} />
              <span>Ready for Review</span>
            </>
          ) : (
            <>
              <div className="status-spinner"></div>
              <span>Generating...</span>
            </>
          )}
        </div>
      </div>

      {/* Edit Warning Modal */}
      {showEditWarning && (
        <div className="edit-warning-overlay">
          <div className="edit-warning-modal">
            <div className="warning-icon">
              <AlertTriangle size={32} />
            </div>
            <h4>Enable Document Editing?</h4>
            <p>
              Manual changes will need to be reviewed for legal correctness. 
              The system cannot verify manually edited content.
            </p>
            <div className="warning-actions">
              <button className="btn-cancel" onClick={cancelEditing}>
                Cancel
              </button>
              <button className="btn-confirm" onClick={confirmEditing}>
                <Edit3 size={14} />
                Enable Editing
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Document Header */}
      <div className="document-header">
        <h3>
          <Shield size={18} />
          Generated Document
        </h3>
        <button 
          className={`edit-toggle-btn ${editingEnabled ? 'active' : ''}`}
          onClick={handleEnableEditing}
          title={editingEnabled ? 'Lock document' : 'Enable editing'}
        >
          {editingEnabled ? (
            <>
              <Edit3 size={14} />
              <span>Editing Mode</span>
            </>
          ) : (
            <>
              <Lock size={14} />
              <span>View Only</span>
            </>
          )}
        </button>
      </div>

      {/* The Document Container - Independent Scroll */}
      <div className="document-scroll-container">
        <div className="document-page">
          <textarea
            ref={textareaRef}
            value={draftText || ''}
            onChange={(e) => editingEnabled && onEdit(e.target.value)}
            className={`document-content ${editingEnabled ? 'editable' : 'readonly'}`}
            placeholder="Your legal document will appear here..."
            spellCheck={editingEnabled}
            readOnly={!editingEnabled}
          />
        </div>
      </div>

      {/* Editing Status Footer */}
      {editingEnabled && (
        <div className="editing-status-bar">
          <AlertTriangle size={14} />
          <span>Editing enabled — Changes require manual review before submission</span>
        </div>
      )}
    </div>
  );
};

export default DraftPreview;
