import React, { useState, useEffect } from 'react';
import { Clock, FileText, Trash2, Download, ChevronRight, RefreshCw, AlertCircle } from 'lucide-react';
import { getDraftHistory, deleteDraft, clearDraftHistory, exportDraft, getStorageInfo } from '../../services/draftHistoryService';
import './DraftHistoryPanel.css';

const DraftHistoryPanel = ({ onLoadDraft, language = 'english' }) => {
  const [history, setHistory] = useState([]);
  const [storageInfo, setStorageInfo] = useState(null);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const isHindi = language === 'hindi';

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = () => {
    const drafts = getDraftHistory();
    setHistory(drafts);
    setStorageInfo(getStorageInfo());
  };

  const handleLoadDraft = (draft) => {
    if (onLoadDraft) {
      onLoadDraft(draft);
    }
  };

  const handleDeleteDraft = (id, e) => {
    e.stopPropagation();
    setDeletingId(id);
    
    setTimeout(() => {
      deleteDraft(id);
      loadHistory();
      setDeletingId(null);
    }, 300);
  };

  const handleExportDraft = (draft, e) => {
    e.stopPropagation();
    exportDraft(draft);
  };

  const handleClearAll = () => {
    clearDraftHistory();
    loadHistory();
    setShowClearConfirm(false);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return isHindi ? 'अभी' : 'Just now';
    if (diffMins < 60) return isHindi ? `${diffMins} मिनट पहले` : `${diffMins}m ago`;
    if (diffHours < 24) return isHindi ? `${diffHours} घंटे पहले` : `${diffHours}h ago`;
    if (diffDays < 7) return isHindi ? `${diffDays} दिन पहले` : `${diffDays}d ago`;
    
    return date.toLocaleDateString(isHindi ? 'hi-IN' : 'en-IN', {
      month: 'short',
      day: 'numeric'
    });
  };

  const getTypeLabel = (type) => {
    if (type === 'rti') {
      return isHindi ? 'RTI' : 'RTI';
    }
    return isHindi ? 'शिकायत' : 'Complaint';
  };

  if (history.length === 0) {
    return (
      <div className="draft-history-panel empty">
        <div className="empty-state">
          <Clock size={32} strokeWidth={1.5} />
          <h4>{isHindi ? 'कोई हाल के ड्राफ्ट नहीं' : 'No Recent Drafts'}</h4>
          <p>
            {isHindi 
              ? 'आपके ड्राफ्ट स्वचालित रूप से यहां सहेजे जाएंगे।'
              : 'Your drafts will be automatically saved here.'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="draft-history-panel">
      <div className="panel-header">
        <div className="header-left">
          <Clock size={16} />
          <h4>{isHindi ? 'हाल के ड्राफ्ट' : 'Recent Drafts'}</h4>
          <span className="count-badge">{history.length}</span>
        </div>
        <div className="header-actions">
          <button 
            className="btn-icon" 
            onClick={loadHistory}
            title={isHindi ? 'रिफ्रेश' : 'Refresh'}
            aria-label={isHindi ? 'रिफ्रेश करें' : 'Refresh drafts'}
          >
            <RefreshCw size={14} />
          </button>
          <button 
            className="btn-icon danger"
            onClick={() => setShowClearConfirm(true)}
            title={isHindi ? 'सभी साफ़ करें' : 'Clear all'}
            aria-label={isHindi ? 'सभी ड्राफ्ट साफ़ करें' : 'Clear all drafts'}
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <div className="history-list" role="list" aria-label={isHindi ? 'ड्राफ्ट सूची' : 'Draft list'}>
        {history.map((draft) => (
          <div 
            key={draft.id}
            className={`history-item ${deletingId === draft.id ? 'deleting' : ''}`}
            onClick={() => handleLoadDraft(draft)}
            role="listitem"
            tabIndex={0}
            onKeyPress={(e) => e.key === 'Enter' && handleLoadDraft(draft)}
            aria-label={`${draft.title}, ${getTypeLabel(draft.type)}, ${formatDate(draft.updatedAt)}`}
          >
            <div className="item-icon">
              <FileText size={16} />
            </div>
            
            <div className="item-content">
              <div className="item-title">{draft.title}</div>
              <div className="item-meta">
                <span className={`type-badge ${draft.type}`}>
                  {getTypeLabel(draft.type)}
                </span>
                <span className="item-date">{formatDate(draft.updatedAt)}</span>
              </div>
            </div>

            <div className="item-actions">
              <button 
                className="action-btn"
                onClick={(e) => handleExportDraft(draft, e)}
                title={isHindi ? 'डाउनलोड' : 'Download'}
                aria-label={isHindi ? 'ड्राफ्ट डाउनलोड करें' : 'Download draft'}
              >
                <Download size={14} />
              </button>
              <button 
                className="action-btn danger"
                onClick={(e) => handleDeleteDraft(draft.id, e)}
                title={isHindi ? 'हटाएं' : 'Delete'}
                aria-label={isHindi ? 'ड्राफ्ट हटाएं' : 'Delete draft'}
              >
                <Trash2 size={14} />
              </button>
              <ChevronRight size={14} className="chevron" />
            </div>
          </div>
        ))}
      </div>

      {storageInfo && (
        <div className="storage-info">
          <span>
            {storageInfo.itemCount}/{storageInfo.maxItems} {isHindi ? 'ड्राफ्ट' : 'drafts'}
          </span>
          <span className="separator">•</span>
          <span>{storageInfo.sizeKB} KB</span>
        </div>
      )}

      {/* Clear All Confirmation */}
      {showClearConfirm && (
        <div className="confirm-overlay" role="dialog" aria-modal="true">
          <div className="confirm-dialog">
            <AlertCircle size={24} className="warning-icon" />
            <h4>{isHindi ? 'सभी ड्राफ्ट हटाएं?' : 'Clear All Drafts?'}</h4>
            <p>
              {isHindi 
                ? 'यह क्रिया पूर्ववत नहीं की जा सकती। सभी सहेजे गए ड्राफ्ट स्थायी रूप से हटा दिए जाएंगे।'
                : 'This action cannot be undone. All saved drafts will be permanently deleted.'}
            </p>
            <div className="confirm-actions">
              <button 
                className="btn btn-secondary"
                onClick={() => setShowClearConfirm(false)}
              >
                {isHindi ? 'रद्द करें' : 'Cancel'}
              </button>
              <button 
                className="btn btn-danger"
                onClick={handleClearAll}
              >
                <Trash2 size={14} />
                {isHindi ? 'सभी हटाएं' : 'Delete All'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DraftHistoryPanel;
