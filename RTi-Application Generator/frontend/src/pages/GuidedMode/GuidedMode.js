import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Check, ArrowLeft, ClipboardList, Shield, Scale } from 'lucide-react';
import { generateDraft } from '../../services/draftService';
import { getCategories } from '../../services/authorityService';
import ApplicantForm from '../../components/ApplicantForm/ApplicantForm';
import DraftPreview from '../../components/DraftPreview/DraftPreview';
import DownloadPanel from '../../components/DownloadPanel/DownloadPanel';
import './GuidedMode.css';

const GuidedMode = () => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [draft, setDraft] = useState(null);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCats = async () => {
      const data = await getCategories();
      setCategories(data);
    };
    fetchCats();
  }, []);
  
  const [formData, setFormData] = useState({
    applicant_name: '',
    applicant_address: '',
    applicant_state: '',
    applicant_phone: '',
    applicant_email: '',
    // Guided specific fields
    intent: '', // 'info' or 'complaint'
    issue_description: '',
    department_hint: '',
    issue_category: '',
    time_period: '',
    // Output fields
    document_type: 'information_request',
    language: 'english',
    tone: 'neutral'
  });

  const nextStep = () => {
    // Validation
    if (step === 1) {
      if (!formData.applicant_name || !formData.applicant_address || !formData.applicant_state) {
        toast.error("Please fill in all required applicant details.");
        return;
      }
    }
    
    if (step === 2) {
       if (!formData.intent || !formData.issue_description) {
         toast.error("Please answer the required questions.");
         return;
       }
       // Determine document type based on intent
       const docType = formData.intent === 'info' ? 'information_request' : 'grievance';
       // We can trigger generation here
       generateDocument({ ...formData, document_type: docType });
    }

    setStep(step + 1);
  };

  const prevStep = () => setStep(step - 1);

  const generateDocument = async (data) => {
    setLoading(true);
    try {
      const result = await generateDraft(data);
      setDraft(result);
    } catch (err) {
      toast.error("Failed to generate draft. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch(step) {
      case 1:
        return (
          <div className="step-content">
            <div className="step-header">
              <h2>Applicant Details</h2>
              <p className="text-muted">We need your personal details to file the application officially.</p>
            </div>
            <div className="input-card">
              <ApplicantForm data={formData} onChange={setFormData} />
            </div>
          </div>
        );
      case 2:
        return (
          <div className="step-content">
            <div className="step-header">
              <h2>Request Details</h2>
              <p className="text-muted">Tell us about the issue or information you are seeking.</p>
            </div>
            <div className="input-card">
              <div className="input-group">
                <label className="input-label">What document do you need? *</label>
                <div className="radio-group">
                    <label className={`radio-card ${formData.intent === 'info' ? 'selected' : ''}`}>
                        <input 
                            type="radio" 
                            name="intent" 
                            value="info"
                            checked={formData.intent === 'info'}
                            onChange={(e) => setFormData({...formData, intent: e.target.value})}
                        />
                        <span>Ask for Information (RTI)</span>
                    </label>
                    <label className={`radio-card ${formData.intent === 'complaint' ? 'selected' : ''}`}>
                        <input 
                            type="radio" 
                            name="intent" 
                            value="complaint"
                            checked={formData.intent === 'complaint'}
                            onChange={(e) => setFormData({...formData, intent: e.target.value})}
                        />
                        <span>File a Complaint</span>
                    </label>
                </div>
              </div>

              <div className="input-group">
                <label className="input-label">Which department is involved? (Optional)</label>
                <select 
                  className="form-input"
                  style={{ marginBottom: '0.5rem' }}
                  value={formData.issue_category || (formData.department_hint ? 'other' : '')}
                  onChange={(e) => {
                    const val = e.target.value;
                    if (val === 'other') {
                        setFormData({...formData, issue_category: 'other', department_hint: ' '});
                    } else if (!val) {
                         setFormData({...formData, issue_category: '', department_hint: ''});
                    } else {
                        const cat = categories.find(c => c.id === val);
                        setFormData({...formData, issue_category: val, department_hint: cat ? cat.name : val});
                    }
                  }}
                >
                    <option value="">-- Select Department --</option>
                    {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                    <option value="other">Other / Not Listed</option>
                </select>
                
                {(formData.issue_category === 'other' || (formData.department_hint && !categories.some(c => c.id === formData.issue_category))) ? (
                    <input
                      type="text"
                      className="form-input"
                      value={formData.department_hint === ' ' ? '' : formData.department_hint}
                      onChange={(e) => setFormData({...formData, department_hint: e.target.value, issue_category: 'other'})}
                      placeholder="Type the department name here..."
                      autoFocus
                    />
                ) : null}
              </div>

              <div className="input-group">
                <label className="input-label">
                    {formData.intent === 'complaint' ? "Describe your grievance *" : "What information do you need? *"}
                </label>
                <textarea
                  className="form-textarea"
                  rows="4"
                  value={formData.issue_description}
                  onChange={(e) => setFormData({...formData, issue_description: e.target.value})}
                  placeholder="Be specific about dates, names, and places."
                />
              </div>
            </div>
          </div>
        );
      case 3:
        return (
           <div className="step-content review-phase">
              <div className="step-header">
                <h2>Review Your Document</h2>
                <p className="text-muted">Review the generated document carefully before downloading.</p>
              </div>
              {loading ? (
                <div className="loading-state">
                  <div className="loading-spinner"></div>
                  <p>Creating your document...</p>
                </div>
              ) : draft ? (
                <div className="document-review-layout">
                   {/* Document Review Pane */}
                   <div className="review-document-container">
                     <DraftPreview 
                       draftText={draft.draft_text} 
                       onEdit={(text) => setDraft({...draft, draft_text: text})}
                       documentType={formData.document_type}
                       language={formData.language}
                       mode="Guided"
                       isReady={!loading}
                     />
                   </div>
                   
                   {/* Export Section - Separated */}
                   <div className="export-section-guided">
                     <div className="export-header-guided">
                       <h3>Export Your Document</h3>
                       <p>Download in your preferred format for submission</p>
                     </div>
                     <DownloadPanel draftData={{...formData, draft_text: draft.draft_text}} />
                   </div>
                </div>
              ) : (
                <div className="error-state">
                  <p>Something went wrong. Please go back and try again.</p>
                </div>
              )}
           </div>
        );
      default: return null;
    }
  };

  return (
    <div className="guided-mode-page">
      {/* Page Header */}
      <div className="guided-page-header">
        <div className="container">
          <Link to="/" className="back-link">
            <ArrowLeft size={16} />
            <span>Back to Home</span>
          </Link>
          
          <div className="page-header-row">
            <div className="page-header-content">
              <div className="page-header-icon">
                <ClipboardList size={24} />
              </div>
              <div className="page-header-text">
                <h1>Guided Drafting</h1>
                <p>Step-by-step questionnaire to generate a rule-compliant draft. No AI involved.</p>
              </div>
            </div>
            
            <div className="page-header-badges">
              <div className="header-badge">
                <Scale size={14} />
                <span>100% Rule-Based</span>
              </div>
              <div className="header-badge">
                <Shield size={14} />
                <span>No Data Stored</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="guided-mode container">
       <div className="guided-layout">
         {/* Sidebar Stepper */}
         <div className="guided-sidebar">
           <h3>Progress</h3>
           <div className="stepper-container">
              {/* Step 1 */}
              <div className={`step-item ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
                 <div className="step-indicator">
                    {step > 1 ? <Check size={16} /> : 1}
                 </div>
                 <div className="step-content-wrapper">
                    <span className="step-label">Personal Details</span>
                    <span className="step-desc">Your contact info</span>
                 </div>
              </div>
              
              {/* Step 2 */}
              <div className={`step-item ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
                 <div className="step-indicator">
                    {step > 2 ? <Check size={16} /> : 2}
                 </div>
                 <div className="step-content-wrapper">
                    <span className="step-label">The Issue</span>
                    <span className="step-desc">What do you need?</span>
                 </div>
              </div>
              
              {/* Step 3 */}
              <div className={`step-item ${step >= 3 ? 'active' : ''}`}>
                 <div className="step-indicator">3</div>
                 <div className="step-content-wrapper">
                    <span className="step-label">Review</span>
                    <span className="step-desc">Download & Print</span>
                 </div>
              </div>
           </div>
         </div>

         {/* Content Area */}
         <div className="guided-content">
           {renderStep()}

           {/* Navigation Buttons */}
           <div className="navigation-buttons">
              {step > 1 ? (
                 <button className="btn btn-secondary" onClick={prevStep} disabled={loading}>
                    Back
                 </button>
              ) : <div></div> /* Spacer */}
              
              {step < 3 && (
                 <button className="btn btn-primary" onClick={nextStep}>
                    Next Step
                 </button>
              )}
           </div>
         </div>
       </div>
      </div>
    </div>
  );
};

export default GuidedMode;
