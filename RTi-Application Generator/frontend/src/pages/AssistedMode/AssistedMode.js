import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { 
  FileText, Globe, RefreshCw, 
  ArrowLeft, Zap, CheckCircle, AlertCircle, PenTool, Sparkles, HelpCircle, Scale, Layers
} from 'lucide-react';
import useDebounce from '../../hooks/useDebounce';
import { generateDraft } from '../../services/draftService';
import { getLLMStatus } from '../../services/llmService';
import ApplicantForm from '../../components/ApplicantForm/ApplicantForm';
import DraftPreview from '../../components/DraftPreview/DraftPreview';
import DownloadPanel from '../../components/DownloadPanel/DownloadPanel';
import ConfidenceNotice from '../../components/ConfidenceNotice/ConfidenceNotice';
import './AssistedMode.css';

const AssistedMode = () => {
  const location = useLocation();
  const prefillData = location.state || {};

  const [formData, setFormData] = useState({
    applicant_name: '',
    applicant_address: '',
    applicant_state: '',
    applicant_phone: '',
    applicant_email: '',
    issue_description: prefillData.prefillDescription || '',
    document_type: prefillData.documentType || 'information_request',
    language: prefillData.language || 'english',
    tone: 'neutral',
    enable_llm_enhancement: true  // AI enhancement enabled by default
  });

  const [draft, setDraft] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [llmStatus, setLlmStatus] = useState({ available: false, enabled: false });

  // Check LLM status on mount
  useEffect(() => {
    const checkLLM = async () => {
      const status = await getLLMStatus();
      setLlmStatus(status);
    };
    checkLLM();
  }, []);

  // Handle prefill data from navigation (e.g., from Templates page)
  useEffect(() => {
    if (location.state?.prefillDescription) {
      setFormData(prev => ({
        ...prev,
        issue_description: location.state.prefillDescription,
        document_type: location.state.documentType || prev.document_type,
        language: location.state.language || prev.language
      }));
      toast.success('Template loaded! Fill in your details to generate the draft.', { autoClose: 4000 });
    }
  }, [location.state]);

  // Debounce the entire form data to prevent too many API calls
  const debouncedData = useDebounce(formData, 1500);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    // Only generate if we have all minimum required fields
    const hasName = debouncedData.applicant_name && debouncedData.applicant_name.length >= 2;
    const hasAddress = debouncedData.applicant_address && debouncedData.applicant_address.length >= 10;
    const hasState = debouncedData.applicant_state && debouncedData.applicant_state.length >= 2;
    const hasDescription = debouncedData.issue_description && debouncedData.issue_description.length >= 20;
    
    if (hasName && hasAddress && hasState && hasDescription) {
      handleGenerateDraft(debouncedData);
    }
  }, [debouncedData]);

  const handleGenerateDraft = async (data) => {
    setLoading(true);
    setError(null);
    try {
      const result = await generateDraft(data);
      setDraft(result);
      
      // Show toast if LLM enhanced
      if (result.llm_enhanced) {
        toast.info('✨ Draft enhanced by AI for better clarity', { autoClose: 3000 });
      }
    } catch (err) {
      console.error(err);
      // Handle validation errors differently
      if (err.isValidationError) {
        setError(`Please fill required fields: ${err.validationErrors.join(', ')}`);
      } else {
        setError("Could not update draft. Please check your connection.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleManualRegenerate = () => {
     if (!formData.issue_description) {
        toast.warning("Please describe your issue first.");
        return;
     }
     handleGenerateDraft(formData);
  };

  const handleDraftEdit = (newText) => {
    setDraft(prev => ({ ...prev, draft_text: newText }));
  };

  // Calculate progress
  const getProgress = () => {
    let filled = 0;
    if (formData.applicant_name?.length >= 2) filled++;
    if (formData.applicant_address?.length >= 10) filled++;
    if (formData.applicant_state?.length >= 2) filled++;
    if (formData.issue_description?.length >= 20) filled++;
    return filled;
  };

  const progress = getProgress();
  const progressPercent = (progress / 4) * 100;
  
  // Status text helper
  const getDraftStatus = () => {
    if (loading) return "Generating...";
    if (progress < 4) return "More details needed";
    return "Ready for review";
  };

  return (
    <div className="assisted-mode-page">
      {/* Page Header */}
      <div className="assisted-page-header">
        <div className="container">
          <Link to="/" className="back-link">
            <ArrowLeft size={16} />
            <span>Back to Home</span>
          </Link>
          
          <div className="page-header-row">
            <div className="page-header-content">
              <div className="page-header-icon">
                <Layers size={24} />
              </div>
              <div className="page-header-text">
                <h1>Assisted Drafting</h1>
                <p>Free-text input with rule-based formatting. Optional AI language enhancement.</p>
              </div>
            </div>
            
            <div className="page-header-badges">
              <div className="header-badge">
                <Scale size={14} />
                <span>Rule-Based Core</span>
              </div>
              <div className="header-badge ai-badge">
                <Sparkles size={14} />
                <span>AI Polish Available</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-container">
        <div className="container progress-inner">
          <div className="progress-info">
            <div className="progress-label">
              <CheckCircle size={16} className={progress === 4 ? "text-success" : "text-muted"} />
              <span>Draft Completion</span>
            </div>
            <div className="progress-bar-wrapper">
              <div 
                className="progress-fill" 
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
          
          <div className={`status-indicator ${progress === 4 ? 'ready' : 'drafting'}`}>
            {progress === 4 ? <Sparkles size={16} /> : <FileText size={16} />}
            <span>{getDraftStatus()}</span>
          </div>
        </div>
      </div>

      <div className="main-content">
        <div className="split-view">
          {/* Input Panel (Left Side - Scrollable) */}
          <div className="input-panel">
            
            {/* Step 1: Applicant Info */}
            <div className="panel-card">
              <div className="section-header-inline">
                <h2>Your Information</h2>
                <span className="section-badge">Step 1</span>
              </div>
              <ApplicantForm 
                data={formData} 
                onChange={(newData) => setFormData(newData)} 
              />
            </div>
            
            {/* Step 2: Issue Details */}
            <div className="panel-card">
              <div className="section-header-inline">
                <h2>Issue Details</h2>
                <span className="section-badge">Step 2</span>
              </div>
              
              <div className="issue-input-card">
                <label className="input-label-large">
                  <span>Describe your issue or request <span className="required-star">*</span></span>
                  <HelpCircle size={14} className="help-icon" title="Be specific. Include dates, locations, and names of officials if known." />
                </label>
                
                <div className="ai-textarea-wrapper">
                  <textarea
                    className="form-textarea ai-input"
                    rows="8"
                    placeholder="Example: On 15th March 2024, I visited the Municipal Office to submit my property tax payment. The clerk demanded ₹500 extra... I request information on..."
                    value={formData.issue_description}
                    onChange={(e) => setFormData({ ...formData, issue_description: e.target.value })}
                  />
                  <div className="textarea-footer">
                    <div className={`char-indicator ${formData.issue_description.length >= 20 ? 'valid' : ''}`}>
                      {formData.issue_description.length}/20 chars
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="controls-grid">
                <div className="control-card">
                  <label className="control-label">
                    <FileText size={13} /> Document Type
                  </label>
                  <select 
                    className="form-select-modern"
                    value={formData.document_type}
                    onChange={(e) => setFormData({ ...formData, document_type: e.target.value })}
                  >
                    <option value="information_request">RTI - Information</option>
                    <option value="records_request">RTI - Records</option>
                    <option value="inspection_request">RTI - Inspection</option>
                    <option value="grievance">Complaint - General</option>
                  </select>
                </div>

                <div className="control-card">
                  <label className="control-label">
                    <Globe size={13} /> Language
                  </label>
                  <select 
                    className="form-select-modern"
                    value={formData.language}
                    onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                  >
                    <option value="english">English</option>
                    <option value="hindi">Hindi</option>
                  </select>
                </div>

                {/* Tone removed to simplify UI based on "avoid superficial" - can be added back if needed, but keeping it clean */}
              </div>

              {/* AI Enhancement Toggle */}
              {llmStatus.available && (
                <div className="ai-enhancement-toggle">
                  <span className="toggle-text">
                    <Sparkles size={14} style={{ marginRight: '6px' }} />
                    AI Polish
                  </span>
                  <label className="toggle-label">
                    <input
                      type="checkbox"
                      checked={formData.enable_llm_enhancement}
                      onChange={(e) => setFormData({ ...formData, enable_llm_enhancement: e.target.checked })}
                    />
                    <div className="toggle-switch"></div>
                  </label>
                </div>
              )}

              <button 
                className={`generate-btn ${loading ? 'loading' : ''}`} 
                onClick={handleManualRegenerate}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <RefreshCw className="spin" size={18} />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <Zap size={18} />
                    <span>Update Draft</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Preview Panel (Right Side - Document Review) */}
          <div className="preview-panel">
            {/* Phase indicator */}
            <div className="phase-indicator">
              <span className="phase-label">Phase 2</span>
              <span className="phase-title">Document Review</span>
            </div>

            {error && (
              <div className="error-card">
                <AlertCircle size={20} />
                <p>{error}</p>
              </div>
            )}
            
            {draft ? (
              <div className="document-review-section">
                {/* AI Enhancement Badge - subtle */}
                {draft.llm_enhanced && (
                  <div className="enhancement-notice">
                    <Sparkles size={14} />
                    <span>AI-polished for clarity</span>
                  </div>
                )}

                {draft.confidence && (
                  <ConfidenceNotice 
                    level={draft.confidence.level} 
                    explanation={draft.confidence.explanation}
                  />
                )}
                
                {/* The Document Review Pane */}
                <div className="document-container">
                   <DraftPreview 
                     draftText={draft.draft_text} 
                     onEdit={handleDraftEdit}
                     documentType={formData.document_type}
                     language={formData.language}
                     mode="Assisted"
                     isReady={!loading}
                   />
                </div>

                {/* Export Section - Separated from document */}
                <div className="export-section">
                  <div className="export-header">
                    <h3>Export RTI Document</h3>
                    <p>Download your reviewed document for submission</p>
                  </div>
                  <DownloadPanel draftData={{ ...formData, draft_text: draft.draft_text }} />
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-icon-container">
                  <div className="empty-icon-paper"></div>
                  <PenTool size={32} className="empty-icon-pen" />
                </div>
                <h3>Document Preview</h3>
                <p>Complete the required fields to generate your legal document.</p>
                <div className="empty-checklist">
                  <div className={`checklist-item ${formData.applicant_name?.length >= 2 ? 'done' : ''}`}>
                    <span className="checkbox">{formData.applicant_name?.length >= 2 && <CheckCircle size={12} />}</span>
                    Applicant Name
                  </div>
                  <div className={`checklist-item ${formData.applicant_address?.length >= 10 ? 'done' : ''}`}>
                    <span className="checkbox">{formData.applicant_address?.length >= 10 && <CheckCircle size={12} />}</span>
                    Address
                  </div>
                  <div className={`checklist-item ${formData.issue_description?.length >= 20 ? 'done' : ''}`}>
                    <span className="checkbox">{formData.issue_description?.length >= 20 && <CheckCircle size={12} />}</span>
                    Issue Description
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssistedMode;
