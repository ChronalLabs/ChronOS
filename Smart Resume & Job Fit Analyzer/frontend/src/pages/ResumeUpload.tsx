import { useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, Loader2 } from 'lucide-react';
import type { SessionState } from '../services/types';
import { uploadResume } from '../services/api';

interface ResumeUploadProps {
    session: SessionState;
    setSession: React.Dispatch<React.SetStateAction<SessionState>>;
}

export default function ResumeUpload({ setSession }: ResumeUploadProps) {
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (!file) return;

        // Validate file type
        const validTypes = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ];

        if (!validTypes.includes(file.type)) {
            setError('Please upload a PDF or DOCX file');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            setError('File size must be less than 10MB');
            return;
        }

        setError(null);
        setIsUploading(true);

        try {
            const response = await uploadResume(file);

            setSession(prev => ({
                ...prev,
                sessionId: response.session_id,
                resume: response.parsed_resume,
                error: null,
            }));

            // Navigate to next step
            navigate('/job-description');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to upload resume');
        } finally {
            setIsUploading(false);
        }
    }, [setSession, navigate]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        },
        maxFiles: 1,
        disabled: isUploading,
    });

    return (
        <div className="max-w-2xl mx-auto animate-fade-in">
            {/* Header */}
            <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
                    Upload Your Resume
                </h1>
                <p className="text-[var(--color-text-secondary)]">
                    Upload your resume in PDF or DOCX format. We'll parse it to extract your skills and experience.
                </p>
            </div>

            {/* Upload Zone */}
            <div
                {...getRootProps()}
                className={`upload-zone ${isDragActive ? 'active' : ''} ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
                <input {...getInputProps()} />

                <div className="flex flex-col items-center gap-4">
                    {isUploading ? (
                        <>
                            <Loader2 className="w-12 h-12 text-[var(--color-primary)] animate-spin" />
                            <p className="text-lg font-medium text-[var(--color-text-primary)]">
                                Processing your resume...
                            </p>
                            <p className="text-sm text-[var(--color-text-muted)]">
                                This may take a few seconds
                            </p>
                        </>
                    ) : isDragActive ? (
                        <>
                            <Upload className="w-12 h-12 text-[var(--color-primary)]" />
                            <p className="text-lg font-medium text-[var(--color-text-primary)]">
                                Drop your file here
                            </p>
                        </>
                    ) : (
                        <>
                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/10 to-indigo-500/10 flex items-center justify-center">
                                <FileText className="w-8 h-8 text-[var(--color-primary)]" />
                            </div>
                            <p className="text-lg font-medium text-[var(--color-text-primary)]">
                                Drag & drop your resume here
                            </p>
                            <p className="text-sm text-[var(--color-text-muted)]">
                                or click to browse files
                            </p>
                            <p className="text-xs text-[var(--color-text-muted)] mt-2">
                                Supports PDF and DOCX files up to 10MB
                            </p>
                        </>
                    )}
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="mt-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                    <div>
                        <p className="font-medium text-red-700 dark:text-red-400">Upload Error</p>
                        <p className="text-sm text-red-600 dark:text-red-300">{error}</p>
                    </div>
                </div>
            )}

            {/* Tips */}
            <div className="mt-8 p-6 card">
                <h3 className="font-medium text-[var(--color-text-primary)] mb-4">
                    💡 Tips for best results
                </h3>
                <ul className="space-y-3 text-sm text-[var(--color-text-secondary)]">
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2" />
                        Use a clean, well-formatted resume with clear section headers
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2" />
                        Include specific skills and technologies you've worked with
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2" />
                        Add quantifiable achievements (e.g., "Improved performance by 40%")
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2" />
                        Use standard section names like "Experience", "Education", "Skills"
                    </li>
                </ul>
            </div>
        </div>
    );
}
