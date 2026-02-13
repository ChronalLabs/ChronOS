import React, { useState } from 'react';
import { User, Phone } from 'lucide-react';
import './ApplicantForm.css';

const ApplicantForm = ({ data, onChange }) => {
  const [activeTab, setActiveTab] = useState('general');

  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange({ ...data, [name]: value });
  };

  return (
    <div className="applicant-form-container">
      <div className="form-tabs">
        <button 
          className={`tab-btn ${activeTab === 'general' ? 'active' : ''}`}
          onClick={() => setActiveTab('general')}
        >
          <User size={16} /> General Info
        </button>
        <button 
          className={`tab-btn ${activeTab === 'contact' ? 'active' : ''}`}
          onClick={() => setActiveTab('contact')}
        >
          <Phone size={16} /> Contact Details
        </button>
      </div>

      <div className="form-content">
        {activeTab === 'general' && (
          <div className="tab-panel fade-in">
            <div className="input-group">
              <label>Full Name</label>
              <input
                type="text"
                name="applicant_name"
                value={data.applicant_name || ''}
                onChange={handleChange}
                placeholder="e.g. Rahul Sharma"
                required
              />
            </div>

            <div className="input-group">
              <label>Address</label>
              <textarea
                name="applicant_address"
                value={data.applicant_address || ''}
                onChange={handleChange}
                className="form-textarea"
                rows="3"
                placeholder="Street Name, Area, Pincode"
                required
              />
            </div>

            <div className="input-group">
              <label>State</label>
              <input
                type="text"
                name="applicant_state"
                value={data.applicant_state || ''}
                onChange={handleChange}
                placeholder="State of Residence"
                required
              />
            </div>
          </div>
        )}

        {activeTab === 'contact' && (
          <div className="tab-panel fade-in">
            <div className="input-group">
              <label>Phone Number</label>
              <input
                type="tel"
                name="applicant_phone"
                value={data.applicant_phone || ''}
                onChange={handleChange}
                placeholder="+91 XXXXX XXXXX"
              />
            </div>

            <div className="input-group">
              <label>Email Address</label>
              <input
                type="email"
                name="applicant_email"
                value={data.applicant_email || ''}
                onChange={handleChange}
                placeholder="example@domain.com"
              />
            </div>
            
             <div className="info-box">
               <p>These details help authorities contact you regarding your application.</p>
             </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ApplicantForm;
