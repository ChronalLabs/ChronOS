/**
 * API client for Smart Resume & Job Fit Analyzer
 */
import axios, { AxiosError } from 'axios';
import type {
    ResumeUploadResponse,
    JobDescriptionResponse,
    EvaluationResponse,
    ExportResponse,
    EvaluationResult,
    ParsedResume,
    ParsedJobDescription,
} from './types';

const API_BASE = import.meta.env.VITE_API_URL || '/api';
console.log('API Base URL:', API_BASE);

const api = axios.create({
    baseURL: API_BASE,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Error handling helper
function handleApiError(error: unknown): never {
    if (error instanceof AxiosError) {
        const message = error.response?.data?.detail || error.message;
        throw new Error(message);
    }
    throw error;
}

/**
 * Upload a resume file (PDF or DOCX)
 */
export async function uploadResume(file: File): Promise<ResumeUploadResponse> {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post<ResumeUploadResponse>('/upload-resume', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Analyze a job description
 */
export async function analyzeJobDescription(
    jobDescription: string,
    sessionId?: string
): Promise<JobDescriptionResponse> {
    try {
        const response = await api.post<JobDescriptionResponse>(
            '/analyze-jd',
            { job_description: jobDescription },
            { params: sessionId ? { session_id: sessionId } : undefined }
        );

        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Run evaluation of resume against job description
 */
export async function evaluateResume(sessionId: string): Promise<EvaluationResponse> {
    try {
        const response = await api.post<EvaluationResponse>('/evaluate', {
            session_id: sessionId,
        });

        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Get evaluation results for a session
 */
export async function getResults(sessionId: string): Promise<EvaluationResponse> {
    try {
        const response = await api.get<EvaluationResponse>(`/results/${sessionId}`);
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Export results as PDF or JSON
 */
export async function exportResults(
    sessionId: string,
    format: 'pdf' | 'json' = 'pdf'
): Promise<ExportResponse> {
    try {
        const response = await api.get<ExportResponse>(`/export/${sessionId}`, {
            params: { format },
        });
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Export results as a Blob for direct download (PDF)
 */
export async function exportResultsAsBlob(
    sessionId: string,
    format: 'pdf' | 'json' = 'pdf'
): Promise<Blob> {
    try {
        const response = await api.get(`/export/${sessionId}`, {
            params: { format },
            responseType: 'blob',
        });
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Get session data
 */
export async function getSession(sessionId: string): Promise<{
    session_id: string;
    resume: ParsedResume | null;
    job_description: ParsedJobDescription | null;
    evaluation: EvaluationResult | null;
    created_at: string;
    updated_at: string;
}> {
    try {
        const response = await api.get(`/session/${sessionId}`);
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

export async function deleteSession(sessionId: string): Promise<{ message: string }> {
    try {
        const response = await api.delete(`/session/${sessionId}`);
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Update parsed resume data (Human-in-the-Loop)
 */
export async function updateResume(sessionId: string, resume: ParsedResume): Promise<any> {
    try {
        const response = await api.put(`/session/${sessionId}/resume`, resume);
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{
    status: string;
    service: string;
    spacy_loaded: boolean;
}> {
    try {
        const response = await axios.get('/health');
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
}

export default api;
