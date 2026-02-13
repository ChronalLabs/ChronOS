
import { useEffect, useState } from 'react';
import type { SessionState } from '../services/types';
import { evaluateResume } from '../services/api';
import { CheckCircle2, Circle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface AnalysisProgressProps {
    session: SessionState;
    setSession: (session: SessionState) => void;
}

const ANALYSIS_STEPS = [
    { id: 1, label: 'Parsing resume structure' },
    { id: 2, label: 'Extracting skills & experience' },
    { id: 3, label: 'Matching against job requirements' },
    { id: 4, label: 'Calculating fit score' },
    { id: 5, label: 'Preparing explanation report' },
];

export default function AnalysisProgress({ session, setSession }: AnalysisProgressProps) {
    const navigate = useNavigate();
    const [currentStepIndex, setCurrentStepIndex] = useState(0);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        const runAnalysis = async () => {
            // If we already have results, jump to end
            if (session.evaluation) {
                navigate('/results');
                return;
            }

            if (!session.sessionId || !session.resume || !session.jobDescription) {
                setError("Missing session data. Please restart.");
                return;
            }

            try {
                // Determine source for analysis (raw text or parsed)
                // The backend analyze_resume takes session_id. The session should already have the JD text stored on backend or we send it?
                // Actually the `analyze_resume` endpoint triggers the full pipeline. 
                // We assume JD was stored/sent in the Input step (via analyzeJobDescription which creates the JD object on backend).

                // Simulate step progress for calming effect (UX requirement: "Prevent anxiety... Step list")
                const progressInterval = setInterval(() => {
                    if (isMounted) {
                        setCurrentStepIndex(prev => Math.min(prev + 1, ANALYSIS_STEPS.length - 1));
                    }
                }, 1500);

                const result = await evaluateResume(session.sessionId);

                clearInterval(progressInterval);

                if (isMounted) {
                    setSession({
                        ...session,
                        evaluation: result.result,
                        isLoading: false
                    });
                    // Small delay to show final checkmark
                    setTimeout(() => {
                        navigate('/results');
                    }, 800);
                }
            } catch (err) {
                if (isMounted) {
                    console.error("Analysis failed:", err);
                    setError("Analysis failed. Please try again.");
                }
            }
        };

        runAnalysis();

        return () => { isMounted = false; };
    }, [session.sessionId, navigate]); // Removed setSession dependency to avoid loops

    if (error) {
        return (
            <div className="max-w-md mx-auto mt-20 text-center">
                <div className="w-16 h-16 bg-[var(--color-red-50)] text-[var(--color-red-500)] rounded-full flex items-center justify-center mx-auto mb-6">
                    !
                </div>
                <h2 className="h2 mb-4">Analysis Error</h2>
                <p className="text-[var(--color-neutral-600)] mb-8">{error}</p>
                <button
                    onClick={() => navigate('/input')}
                    className="btn btn-secondary"
                >
                    Return to Input
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-[420px] w-full mx-auto py-20 px-6 animate-fade-in">
            <h2 className="h2 text-center mb-10">Analyzing Profile</h2>

            <div className="space-y-4">
                {ANALYSIS_STEPS.map((step, index) => {
                    const isCompleted = index < currentStepIndex;
                    const isCurrent = index === currentStepIndex;

                    return (
                        <div
                            key={step.id}
                            className={`flex items-center gap-4 p-3 rounded-[8px] transition-colors ${isCurrent ? 'bg-[var(--color-neutral-50)]' : ''}`}
                        >
                            <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center">
                                {isCompleted ? (
                                    <CheckCircle2 className="w-5 h-5 text-[var(--color-green-500)]" />
                                ) : isCurrent ? (
                                    <div className="w-2.5 h-2.5 bg-[var(--color-primary-600)] rounded-full animate-pulse" />
                                ) : (
                                    <Circle className="w-2 h-2 text-[var(--color-neutral-300)] fill-[var(--color-neutral-300)]" />
                                )}
                            </div>
                            <span className={`text-sm font-medium ${isCurrent || isCompleted ? 'text-[var(--color-neutral-900)]' : 'text-[var(--color-neutral-400)]'}`}>
                                {step.label}
                            </span>
                        </div>
                    );
                })}
            </div>

            <p className="text-center text-xs text-[var(--color-neutral-400)] mt-12">
                This usually takes about 10-15 seconds.
            </p>
        </div>
    );
}
