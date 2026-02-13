import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const inferIntent = async (text, language = 'english') => {
  try {
    const response = await axios.post(`${API_URL}/infer`, { text, language });
    return response.data;
  } catch (error) {
    console.error('Inference error:', error);
    throw error;
  }
};
