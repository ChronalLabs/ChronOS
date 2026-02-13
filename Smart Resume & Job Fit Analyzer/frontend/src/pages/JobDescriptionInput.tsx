import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, AlertCircle, Loader2, Briefcase, Sparkles } from 'lucide-react';
import type { SessionState } from '../services/types';
import { analyzeJobDescription } from '../services/api';

interface JobDescriptionInputProps {
    session: SessionState;
    setSession: React.Dispatch<React.SetStateAction<SessionState>>;
}

export default function JobDescriptionInput({ session, setSession }: JobDescriptionInputProps) {
    const navigate = useNavigate();
    const [jobDescription, setJobDescription] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (jobDescription.trim().length < 50) {
            setError('Please enter a more detailed job description (at least 50 characters)');
            return;
        }

        setError(null);
        setIsAnalyzing(true);

        try {
            const response = await analyzeJobDescription(jobDescription, session.sessionId || undefined);

            setSession(prev => ({
                ...prev,
                sessionId: response.session_id,
                jobDescription: response.parsed_jd,
                error: null,
            }));

            // Navigate to analysis
            navigate('/analyzing');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to analyze job description');
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto animate-fade-in">
            {/* Header */}
            <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
                    Enter Job Description
                </h1>
                <p className="text-[var(--color-text-secondary)]">
                    Paste the job description you want to compare your resume against.
                    We'll extract the required skills and qualifications.
                </p>
            </div>

            {/* Resume Summary */}
            {session.resume && (
                <div className="mb-8 p-4 card flex items-center gap-4">
                    <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                        <Sparkles className="w-5 h-5 text-green-600" />
                    </div>
                    <div className="flex-1">
                        <p className="font-medium text-[var(--color-text-primary)]">Resume Uploaded</p>
                        <p className="text-sm text-[var(--color-text-secondary)]">
                            {session.resume.skills.length} skills detected • {session.resume.experience.length} experience entries
                        </p>
                    </div>
                </div>
            )}

            {/* Job Description Form */}
            <form onSubmit={handleSubmit}>
                <div className="card p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
                            <Briefcase className="w-5 h-5 text-indigo-600" />
                        </div>
                        <label className="font-medium text-[var(--color-text-primary)]">
                            Job Description
                        </label>
                    </div>

                    <textarea
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        placeholder="Paste the complete job description here, including requirements, qualifications, and responsibilities..."
                        className="w-full h-64 p-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:border-transparent resize-none"
                        disabled={isAnalyzing}
                    />

                    <div className="flex items-center justify-between mt-4">
                        <p className="text-sm text-[var(--color-text-muted)]">
                            {jobDescription.length} characters
                            {jobDescription.length > 0 && jobDescription.length < 50 && ' (minimum 50)'}
                        </p>
                        <button
                            type="submit"
                            disabled={isAnalyzing || jobDescription.trim().length < 50}
                            className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isAnalyzing ? (
                                <>
                                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    <Send className="w-5 h-5 mr-2" />
                                    Analyze Match
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="mt-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                        <div>
                            <p className="font-medium text-red-700 dark:text-red-400">Error</p>
                            <p className="text-sm text-red-600 dark:text-red-300">{error}</p>
                        </div>
                    </div>
                )}
            </form>

            {/* Tips */}
            <div className="mt-8 p-6 card">
                <h3 className="font-medium text-[var(--color-text-primary)] mb-4">
                    💡 What to include
                </h3>
                <ul className="space-y-3 text-sm text-[var(--color-text-secondary)]">
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2" />
                        Full job description with requirements section
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2" />
                        Required skills and qualifications
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2" />
                        Preferred/nice-to-have skills
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2" />
                        Experience requirements (e.g., "3+ years of experience")
                    </li>
                </ul>
            </div>
        </div>
    );
}
