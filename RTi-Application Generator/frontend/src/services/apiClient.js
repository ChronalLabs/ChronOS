import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configuration
const DEFAULT_TIMEOUT = 30000; // 30 seconds
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1 second

// Error types for better handling
export const ErrorTypes = {
  NETWORK: 'NETWORK_ERROR',
  TIMEOUT: 'TIMEOUT_ERROR',
  SERVER: 'SERVER_ERROR',
  VALIDATION: 'VALIDATION_ERROR',
  AUTH: 'AUTH_ERROR',
  UNKNOWN: 'UNKNOWN_ERROR'
};

// User-friendly error messages
const ERROR_MESSAGES = {
  [ErrorTypes.NETWORK]: {
    en: 'Unable to connect to the server. Please check your internet connection.',
    hi: 'सर्वर से कनेक्ट करने में असमर्थ। कृपया अपना इंटरनेट कनेक्शन जांचें।'
  },
  [ErrorTypes.TIMEOUT]: {
    en: 'Request timed out. The server is taking too long to respond.',
    hi: 'अनुरोध का समय समाप्त हो गया। सर्वर जवाब देने में बहुत अधिक समय ले रहा है।'
  },
  [ErrorTypes.SERVER]: {
    en: 'Server error occurred. Please try again later.',
    hi: 'सर्वर त्रुटि हुई। कृपया बाद में पुनः प्रयास करें।'
  },
  [ErrorTypes.VALIDATION]: {
    en: 'Invalid request. Please check your input.',
    hi: 'अमान्य अनुरोध। कृपया अपना इनपुट जांचें।'
  },
  [ErrorTypes.AUTH]: {
    en: 'Authentication failed. Please refresh and try again.',
    hi: 'प्रमाणीकरण विफल। कृपया रिफ्रेश करें और पुनः प्रयास करें।'
  },
  [ErrorTypes.UNKNOWN]: {
    en: 'An unexpected error occurred. Please try again.',
    hi: 'एक अप्रत्याशित त्रुटि हुई। कृपया पुनः प्रयास करें।'
  }
};

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: DEFAULT_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add request timestamp for tracking
    config.metadata = { startTime: new Date() };
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Log response time in development
    if (process.env.NODE_ENV === 'development') {
      const duration = new Date() - response.config.metadata.startTime;
      console.log(`API ${response.config.method?.toUpperCase()} ${response.config.url} - ${duration}ms`);
    }
    return response;
  },
  (error) => Promise.reject(error)
);

/**
 * Classify error type from axios error
 */
const classifyError = (error) => {
  if (!error.response) {
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      return ErrorTypes.TIMEOUT;
    }
    return ErrorTypes.NETWORK;
  }

  const status = error.response.status;
  
  if (status >= 500) return ErrorTypes.SERVER;
  if (status === 422 || status === 400) return ErrorTypes.VALIDATION;
  if (status === 401 || status === 403) return ErrorTypes.AUTH;
  
  return ErrorTypes.UNKNOWN;
};

/**
 * Get user-friendly error message
 */
export const getErrorMessage = (error, language = 'en') => {
  const errorType = classifyError(error);
  const messages = ERROR_MESSAGES[errorType] || ERROR_MESSAGES[ErrorTypes.UNKNOWN];
  return messages[language] || messages.en;
};

/**
 * Sleep utility for retry delay
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Make API request with retry logic
 */
const makeRequest = async (config, retries = MAX_RETRIES) => {
  try {
    return await apiClient(config);
  } catch (error) {
    const errorType = classifyError(error);
    
    // Don't retry validation or auth errors
    if (errorType === ErrorTypes.VALIDATION || errorType === ErrorTypes.AUTH) {
      throw error;
    }
    
    // Retry on network/timeout/server errors
    if (retries > 0) {
      console.log(`Request failed, retrying... (${MAX_RETRIES - retries + 1}/${MAX_RETRIES})`);
      await sleep(RETRY_DELAY * (MAX_RETRIES - retries + 1)); // Exponential backoff
      return makeRequest(config, retries - 1);
    }
    
    throw error;
  }
};

/**
 * API methods with enhanced error handling
 */
export const api = {
  /**
   * GET request
   */
  get: async (url, config = {}) => {
    const response = await makeRequest({ method: 'get', url, ...config });
    return response.data;
  },

  /**
   * POST request
   */
  post: async (url, data, config = {}) => {
    const response = await makeRequest({ method: 'post', url, data, ...config });
    return response.data;
  },

  /**
   * POST request for file download (blob response)
   */
  postBlob: async (url, data, config = {}) => {
    const response = await makeRequest({ 
      method: 'post', 
      url, 
      data, 
      responseType: 'blob',
      ...config 
    });
    return response.data;
  },

  /**
   * PUT request
   */
  put: async (url, data, config = {}) => {
    const response = await makeRequest({ method: 'put', url, data, ...config });
    return response.data;
  },

  /**
   * DELETE request
   */
  delete: async (url, config = {}) => {
    const response = await makeRequest({ method: 'delete', url, ...config });
    return response.data;
  }
};

/**
 * Create custom error object with additional info
 */
export class APIError extends Error {
  constructor(error) {
    const errorType = classifyError(error);
    super(getErrorMessage(error, 'en'));
    
    this.name = 'APIError';
    this.type = errorType;
    this.status = error.response?.status;
    this.details = error.response?.data?.details || null;
    this.originalError = error;
  }
}

export default api;
