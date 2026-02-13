import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const getCategories = async () => {
  try {
    const response = await axios.get(`${API_URL}/authority/categories`);
    return response.data;
  } catch (error) {
    console.error('Fetch categories error:', error);
    // Fallback if API fails
    return [
      { id: 'electricity', name: 'Electricity' },
      { id: 'water', name: 'Water Supply' },
      { id: 'police', name: 'Police' },
      { id: 'municipal', name: 'Municipal Corporation' },
      { id: 'education', name: 'Education' },
      { id: 'health', name: 'Health' },
      { id: 'transport', name: 'Transport' },
      { id: 'other', name: 'Other' }
    ];
  }
};

export const suggestAuthority = async (issueCategory, state, district) => {
  try {
    const response = await axios.post(`${API_URL}/authority`, { 
      issue_category: issueCategory,
      state,
      district
    });
    return response.data;
  } catch (error) {
    console.error('Authority suggestion error:', error);
    throw error;
  }
};
