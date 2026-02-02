import React from 'react';
import { Info, Send, FileSignature, Landmark, Clock, CheckCircle } from 'lucide-react';
import './SubmissionGuidancePanel.css';

const SubmissionGuidancePanel = ({ documentType, department }) => {
  const getGuidance = () => {
    if (documentType === 'rti' || documentType === 'information_request') {
      return (
        <>
            <div className="guidance-header">
              <Info className="text-blue-500" size={24} />
              <h3>How to Submit an RTI</h3>
            </div>
            <div className="steps-list">
                <div className="step-item">
                    <div className="step-icon"><FileSignature size={18} /></div>
                    <div className="step-content">
                        <strong>Print and Sign:</strong>
                        <p>Print the generated draft and sign it at the bottom.</p>
                    </div>
                </div>
                <div className="step-item">
                    <div className="step-icon"><Landmark size={18} /></div>
                    <div className="step-content">
                        <strong>Application Fee:</strong>
                        <p>Attach the required fee (usually ₹10) via Postal Order or Demand Draft favoring "Accounts Officer".</p>
                    </div>
                </div>
                <div className="step-item">
                    <div className="step-icon"><Send size={18} /></div>
                    <div className="step-content">
                        <strong>Submit:</strong>
                        <p>Send via Speed Post or submit in person at the {department || "concerned department's"} PIO office.</p>
                    </div>
                </div>
                <div className="step-item">
                    <div className="step-icon"><CheckCircle size={18} /></div>
                    <div className="step-content">
                        <strong>Acknowledgement:</strong>
                        <p>Keep the receipt and tracking number safe.</p>
                    </div>
                </div>
            </div>
            <div className="timeline-alert">
                <Clock size={16} />
                <span><strong>Timeline:</strong> You should receive a reply within 30 days.</span>
            </div>
        </>
      );
    } else {
       return (
        <>
            <div className="guidance-header">
              <Info className="text-amber-500" size={24} />
              <h3>How to Submit a Complaint</h3>
            </div>
            <div className="steps-list">
                <div className="step-item">
                    <div className="step-icon"><FileSignature size={18} /></div>
                    <div className="step-content">
                        <strong>Signature:</strong>
                        <p>Ensure the complaint is signed and dated.</p>
                    </div>
                </div>
                <div className="step-item">
                    <div className="step-icon"><CheckCircle size={18} /></div>
                    <div className="step-content">
                        <strong>Evidence:</strong>
                        <p>Attach copies of any supporting documents (photos, previous letters, receipts).</p>
                    </div>
                </div>
                <div className="step-item">
                    <div className="step-icon"><Send size={18} /></div>
                    <div className="step-content">
                        <strong>Submission Channel:</strong>
                        <p>Visit the official portal (e.g., CPGRAMS in India) or send via Registered Post.</p>
                    </div>
                </div>
                <div className="step-item">
                    <div className="step-icon"><Clock size={18} /></div>
                    <div className="step-content">
                        <strong>Follow-up:</strong>
                        <p>Note down the complaint reference number if submitted online.</p>
                    </div>
                </div>
            </div>
        </>
      );
    }
  };

  return (
    <div className="submission-guidance-card">
        {getGuidance()}
    </div>
  );
};

export default SubmissionGuidancePanel;
