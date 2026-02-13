import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * LLM Enhancement Service
 * Provides AI-powered text improvement while preserving legal accuracy.
 * 
 * PRINCIPLE: "Rules decide what is allowed. LLMs improve how it is expressed."
 */

/**
 * Check if LLM enhancement is available
 */
export const getLLMStatus = async () => {
  try {
    const response = await axios.get(`${API_URL}/llm/status`);
    return response.data;
  } catch (error) {
    console.error('LLM status check failed:', error);
    return {
      available: false,
      enabled: false,
      model: 'none',
      features: []
    };
  }
};

/**
 * Enhance text using LLM
 * @param {string} text - Text to enhance
 * @param {string} mode - Enhancement mode: 'polish', 'clarify', 'translate', 'tone_adjust'
 * @param {Object} options - Additional options
 */
export const enhanceText = async (text, mode = 'polish', options = {}) => {
  try {
    const response = await axios.post(`${API_URL}/llm/enhance`, {
      text,
      mode,
      target_language: options.targetLanguage || null,
      target_tone: options.targetTone || null,
      preserve_placeholders: options.preservePlaceholders !== false
    });
    return response.data;
  } catch (error) {
    console.error('Text enhancement failed:', error);
    // Return original text on failure
    return {
      original_text: text,
      enhanced_text: text,
      was_enhanced: false,
      enhancement_mode: 'error',
      changes_summary: error.response?.data?.detail || 'Enhancement failed',
      tokens_used: 0,
      model_used: 'none'
    };
  }
};

/**
 * Clarify an issue description
 * @param {string} description - User's issue description
 * @param {string} category - Issue category for context
 */
export const clarifyIssue = async (description, category = null) => {
  try {
    const response = await axios.post(`${API_URL}/llm/clarify-issue`, {
      description,
      category
    });
    return response.data;
  } catch (error) {
    console.error('Issue clarification failed:', error);
    return {
      original: description,
      clarified: description,
      was_clarified: false,
      suggestions: ['Clarification service unavailable']
    };
  }
};

/**
 * Polish draft text for better readability
 */
export const polishDraft = async (draftText) => {
  return enhanceText(draftText, 'polish', { preservePlaceholders: true });
};

/**
 * Translate text to Hindi
 */
export const translateToHindi = async (text) => {
  return enhanceText(text, 'translate', { targetLanguage: 'Hindi' });
};

/**
 * Adjust tone of text
 */
export const adjustTone = async (text, targetTone = 'formal') => {
  return enhanceText(text, 'tone_adjust', { targetTone });
};
