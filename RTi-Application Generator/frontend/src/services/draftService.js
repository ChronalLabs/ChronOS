import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Validate required fields before API call
 */
const validateDraftData = (data) => {
  const errors = [];
  
  if (!data.applicant_name || data.applicant_name.length < 2) {
    errors.push('Name is required (min 2 characters)');
  }
  if (!data.applicant_address || data.applicant_address.length < 10) {
    errors.push('Address is required (min 10 characters)');
  }
  if (!data.applicant_state || data.applicant_state.length < 2) {
    errors.push('State is required');
  }
  if (!data.issue_description || data.issue_description.length < 20) {
    errors.push('Issue description is required (min 20 characters)');
  }
  
  return errors;
};

/**
 * Transform flat frontend data to nested backend schema
 */
const transformToBackendSchema = (data) => {
  // Build authority object from department_hint if provided
  const authority = data.authority || (data.department_hint ? {
    department_name: data.department_hint,
    department_address: '[Department Address]',
    designation: 'Public Information Officer'
  } : null);

  return {
    document_type: data.document_type || 'information_request',
    applicant: {
      name: data.applicant_name || '',
      address: data.applicant_address || '',
      state: data.applicant_state || '',
      district: data.applicant_district || null,
      phone: data.applicant_phone || null,
      email: data.applicant_email || null
    },
    issue: {
      description: data.issue_description || '',
      specific_request: data.specific_request || null,
      time_period: data.time_period || null,
      category: data.issue_category || data.department_hint || null
    },
    authority: authority,
    language: data.language || 'english',
    tone: data.tone || 'neutral',
    additional_context: data.additional_context || null,
    // LLM Enhancement toggle (defaults to true for better output)
    enable_llm_enhancement: data.enable_llm_enhancement !== false
  };
};

/**
 * Transform backend response to include confidence info for frontend
 */
const transformResponse = (response) => {
  return {
    draft_text: response.draft_text,
    document_type: response.document_type,
    template_used: response.template_used,
    language: response.language,
    word_count: response.word_count,
    placeholders: response.placeholders,
    editable_sections: response.editable_sections,
    warnings: response.warnings || [],
    suggestions: response.suggestions || [],
    // LLM enhancement info
    llm_enhanced: response.llm_enhanced || false,
    original_draft: response.original_draft || null,
    enhancement_summary: response.enhancement_summary || null,
    // Add confidence object for ConfidenceNotice component
    confidence: {
      level: response.warnings?.length > 0 ? 'medium' : 'high',
      explanation: response.warnings?.length > 0 
        ? 'Some fields may need your attention. Please review highlighted sections.'
        : response.llm_enhanced 
          ? 'Draft generated and AI-enhanced for clarity.'
          : 'Draft generated successfully with all required information.'
    }
  };
};

export const generateDraft = async (data) => {
  // Validate required fields first
  const validationErrors = validateDraftData(data);
  if (validationErrors.length > 0) {
    const error = new Error('Validation failed');
    error.validationErrors = validationErrors;
    error.isValidationError = true;
    throw error;
  }
  
  try {
    const backendPayload = transformToBackendSchema(data);
    const response = await axios.post(`${API_URL}/draft`, backendPayload);
    return transformResponse(response.data);
  } catch (error) {
    console.error('Draft generation error:', error);
    throw error;
  }
};

export const downloadDocument = async (draftData, format) => {
  try {
    // Transform to backend schema for download endpoint
    const backendPayload = {
      draft_text: draftData.draft_text,
      document_type: draftData.document_type || 'information_request',
      format: format,
      applicant: {
        name: draftData.applicant_name || '',
        address: draftData.applicant_address || '',
        state: draftData.applicant_state || '',
        district: draftData.applicant_district || null,
        phone: draftData.applicant_phone || null,
        email: draftData.applicant_email || null
      },
      authority: draftData.authority || null
    };
    
    const response = await axios.post(`${API_URL}/download`, backendPayload, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error('Download error:', error);
    throw error;
  }
};
