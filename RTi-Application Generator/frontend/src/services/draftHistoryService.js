/**
 * Draft History Service
 * Persists drafts to localStorage and provides history management
 */

const STORAGE_KEY = 'civicdraft_history';
const CURRENT_DRAFT_KEY = 'civicdraft_current';
const MAX_HISTORY_ITEMS = 10;

/**
 * Draft item structure
 * @typedef {Object} DraftHistoryItem
 * @property {string} id - Unique identifier
 * @property {string} title - Draft title (auto-generated from description)
 * @property {string} type - 'rti' or 'complaint'
 * @property {Object} formData - Full form data
 * @property {string} draftText - Generated draft text
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Last update timestamp
 */

/**
 * Generate unique ID
 */
const generateId = () => {
  return `draft_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Generate title from description
 */
const generateTitle = (description, type) => {
  if (!description) {
    return type === 'rti' ? 'New RTI Application' : 'New Complaint';
  }
  
  // Take first 50 chars of description
  const truncated = description.substring(0, 50).trim();
  return truncated.length < description.length ? `${truncated}...` : truncated;
};

/**
 * Get all draft history items
 * @returns {DraftHistoryItem[]}
 */
export const getDraftHistory = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    
    const history = JSON.parse(stored);
    // Sort by updatedAt descending (most recent first)
    return history.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
  } catch (error) {
    console.error('Error reading draft history:', error);
    return [];
  }
};

/**
 * Save a draft to history
 * @param {Object} formData - Form data to save
 * @param {string} draftText - Generated draft text (optional)
 * @param {string} existingId - Existing draft ID to update (optional)
 * @returns {DraftHistoryItem} Saved draft item
 */
export const saveDraft = (formData, draftText = '', existingId = null) => {
  try {
    const history = getDraftHistory();
    const now = new Date().toISOString();
    
    const type = formData.document_type?.includes('request') || 
                 formData.intent === 'info' ? 'rti' : 'complaint';
    
    let draftItem;
    
    if (existingId) {
      // Update existing draft
      const index = history.findIndex(item => item.id === existingId);
      if (index !== -1) {
        draftItem = {
          ...history[index],
          title: generateTitle(formData.issue_description || formData.information_sought, type),
          formData: { ...formData },
          draftText: draftText || history[index].draftText,
          updatedAt: now
        };
        history[index] = draftItem;
      }
    }
    
    if (!draftItem) {
      // Create new draft
      draftItem = {
        id: generateId(),
        title: generateTitle(formData.issue_description || formData.information_sought, type),
        type,
        formData: { ...formData },
        draftText,
        createdAt: now,
        updatedAt: now
      };
      history.unshift(draftItem);
    }
    
    // Keep only MAX_HISTORY_ITEMS
    const trimmedHistory = history.slice(0, MAX_HISTORY_ITEMS);
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmedHistory));
    return draftItem;
  } catch (error) {
    console.error('Error saving draft:', error);
    return null;
  }
};

/**
 * Get a specific draft by ID
 * @param {string} id - Draft ID
 * @returns {DraftHistoryItem|null}
 */
export const getDraftById = (id) => {
  const history = getDraftHistory();
  return history.find(item => item.id === id) || null;
};

/**
 * Delete a draft from history
 * @param {string} id - Draft ID to delete
 * @returns {boolean} Success status
 */
export const deleteDraft = (id) => {
  try {
    const history = getDraftHistory();
    const filtered = history.filter(item => item.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    return true;
  } catch (error) {
    console.error('Error deleting draft:', error);
    return false;
  }
};

/**
 * Clear all draft history
 * @returns {boolean} Success status
 */
export const clearDraftHistory = () => {
  try {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(CURRENT_DRAFT_KEY);
    return true;
  } catch (error) {
    console.error('Error clearing draft history:', error);
    return false;
  }
};

/**
 * Save current working draft (auto-save)
 * @param {Object} formData - Current form data
 */
export const saveCurrentDraft = (formData) => {
  try {
    const data = {
      formData,
      savedAt: new Date().toISOString()
    };
    localStorage.setItem(CURRENT_DRAFT_KEY, JSON.stringify(data));
  } catch (error) {
    console.error('Error saving current draft:', error);
  }
};

/**
 * Get current working draft (for recovery after refresh)
 * @returns {Object|null} Current draft data
 */
export const getCurrentDraft = () => {
  try {
    const stored = localStorage.getItem(CURRENT_DRAFT_KEY);
    if (!stored) return null;
    
    const data = JSON.parse(stored);
    
    // Check if draft is less than 24 hours old
    const savedAt = new Date(data.savedAt);
    const now = new Date();
    const hoursDiff = (now - savedAt) / (1000 * 60 * 60);
    
    if (hoursDiff > 24) {
      // Expired, clear it
      localStorage.removeItem(CURRENT_DRAFT_KEY);
      return null;
    }
    
    return data;
  } catch (error) {
    console.error('Error getting current draft:', error);
    return null;
  }
};

/**
 * Clear current working draft
 */
export const clearCurrentDraft = () => {
  localStorage.removeItem(CURRENT_DRAFT_KEY);
};

/**
 * Export draft as JSON file
 * @param {DraftHistoryItem} draft - Draft to export
 */
export const exportDraft = (draft) => {
  const dataStr = JSON.stringify(draft, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `draft_${draft.id}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

/**
 * Export all user data (for privacy compliance)
 */
export const exportAllData = () => {
  const history = getDraftHistory();
  const current = getCurrentDraft();
  
  const allData = {
    draftHistory: history,
    currentDraft: current,
    exportedAt: new Date().toISOString()
  };
  
  const dataStr = JSON.stringify(allData, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `civicdraft_data_export_${Date.now()}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

/**
 * Get storage usage info
 */
export const getStorageInfo = () => {
  const history = getDraftHistory();
  const historySize = new Blob([JSON.stringify(history)]).size;
  
  return {
    itemCount: history.length,
    maxItems: MAX_HISTORY_ITEMS,
    sizeBytes: historySize,
    sizeKB: (historySize / 1024).toFixed(2)
  };
};

const draftHistoryService = {
  getDraftHistory,
  saveDraft,
  getDraftById,
  deleteDraft,
  clearDraftHistory,
  saveCurrentDraft,
  getCurrentDraft,
  clearCurrentDraft,
  exportDraft,
  exportAllData,
  getStorageInfo
};

export default draftHistoryService;
