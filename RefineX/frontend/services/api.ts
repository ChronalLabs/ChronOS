import axios from 'axios';
import { DatasetPreviewResponse, AnalysisResponse } from '../types';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const uploadDataset = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const getDatasetPreview = async (): Promise<DatasetPreviewResponse> => {
  const response = await api.get('/preview');
  return response.data;
};

export const getAnalysis = async (): Promise<AnalysisResponse> => {
  const response = await api.get('/analyze');
  return response.data;
};

export const getReport = async () => {
  const response = await api.get('/report');
  return response.data;
};
