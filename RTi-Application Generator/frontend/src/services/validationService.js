import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Validate an RTI request before generation
 * @param {Object} data - RTI request data
 * @returns {Promise<Object>} Validation result with score, issues, and grade
 */
export const validateRTIRequest = async (data) => {
  try {
    const response = await axios.post(`${API_BASE}/validate/rti`, {
      information_sought: data.information_sought || data.issue_description,
      time_period: data.time_period,
      department: data.department,
      record_type: data.record_type,
      applicant_name: data.applicant_name,
      applicant_address: data.applicant_address,
      applicant_state: data.applicant_state,
      document_type: data.document_type || 'information_request',
      language: data.language || 'english'
    });
    return response.data;
  } catch (error) {
    console.error('Validation error:', error);
    // Return a default validation result on error
    return {
      is_valid: true,
      can_generate: true,
      score: 50,
      grade: 'C',
      scores_breakdown: {},
      issues: [],
      summary: 'Validation service unavailable. Proceed with caution.',
      summary_hi: 'सत्यापन सेवा उपलब्ध नहीं है। सावधानी से आगे बढ़ें।'
    };
  }
};

/**
 * Validate user edits to a draft
 * @param {string} originalText - Original draft text
 * @param {string} editedText - Edited draft text
 * @param {string} documentType - Type of document
 * @returns {Promise<Object>} Edit validation result
 */
export const validateDraftEdit = async (originalText, editedText, documentType = 'information_request') => {
  try {
    const response = await axios.post(`${API_BASE}/validate/edit`, {
      original_text: originalText,
      edited_text: editedText,
      document_type: documentType
    });
    return response.data;
  } catch (error) {
    console.error('Edit validation error:', error);
    return {
      is_safe: true,
      issues: [],
      warnings: []
    };
  }
};

/**
 * Local validation rules (client-side quick check)
 * Use this for immediate feedback without API call
 */
export const quickValidate = (data) => {
  const issues = [];
  
  // Check required fields
  if (!data.information_sought && !data.issue_description) {
    issues.push({
      code: 'MISSING_INFO',
      message: 'Please describe what information you need',
      severity: 'error',
      field: 'information_sought'
    });
  } else if ((data.information_sought || data.issue_description || '').length < 20) {
    issues.push({
      code: 'TOO_SHORT',
      message: 'Description is too brief. Please provide more details.',
      severity: 'warning',
      field: 'information_sought'
    });
  }
  
  if (!data.time_period) {
    issues.push({
      code: 'MISSING_TIME',
      message: 'Time period is required for RTI requests',
      severity: 'error',
      field: 'time_period'
    });
  }
  
  if (!data.department) {
    issues.push({
      code: 'MISSING_DEPT',
      message: 'Please select a department',
      severity: 'error',
      field: 'department'
    });
  }
  
  if (!data.applicant_name) {
    issues.push({
      code: 'MISSING_NAME',
      message: 'Applicant name is required',
      severity: 'error',
      field: 'applicant_name'
    });
  }
  
  if (!data.applicant_address) {
    issues.push({
      code: 'MISSING_ADDRESS',
      message: 'Address is required for receiving response',
      severity: 'warning',
      field: 'applicant_address'
    });
  }
  
  // Check for vague language
  const vaguePatterns = [
    /^(all|any|every)\s+(information|details)/i,
    /etc\.?$/,
    /\ball\s+related\b/i
  ];
  
  const text = data.information_sought || data.issue_description || '';
  for (const pattern of vaguePatterns) {
    if (pattern.test(text)) {
      issues.push({
        code: 'VAGUE_REQUEST',
        message: 'Avoid vague terms like "all", "any", "etc." Be specific.',
        severity: 'warning',
        field: 'information_sought'
      });
      break;
    }
  }
  
  // Calculate quick score
  const errorCount = issues.filter(i => i.severity === 'error').length;
  const warningCount = issues.filter(i => i.severity === 'warning').length;
  
  let score = 100;
  score -= errorCount * 25;
  score -= warningCount * 10;
  score = Math.max(0, score);
  
  const grade = score >= 90 ? 'A' : score >= 75 ? 'B' : score >= 60 ? 'C' : score >= 40 ? 'D' : 'F';
  
  return {
    is_valid: errorCount === 0,
    can_generate: errorCount === 0,
    score,
    grade,
    issues
  };
};

const validationService = {
  validateRTIRequest,
  validateDraftEdit,
  quickValidate
};

export default validationService;
