import { useState } from 'react';
import type { SessionState, AnalysisMode } from '../services/types';
import { uploadResume, analyzeJobDescription } from '../services/api';
import { Upload, FileText, AlertCircle, Trash2, ArrowRight, Zap, CheckCircle, Sparkles, Briefcase, FileCheck } from 'lucide-react';

interface ResumeJobInputProps {
    session: SessionState;
    setSession: (session: SessionState) => void;
    mode: AnalysisMode | null;
    onNext: () => void;
}

export default function ResumeJobInput({ session, setSession, mode, onNext }: ResumeJobInputProps) {
    const [dragActive, setDragActive] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [jdText, setJdText] = useState('');
    const [uploadError, setUploadError] = useState<string | null>(null);

    // Resume Upload Handlers
    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = async (file: File) => {
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            setUploadError("Please upload a valid PDF or DOCX file.");
            return;
        }

        setIsUploading(true);
        setUploadError(null);

        try {
            const result = await uploadResume(file);
            setSession({
                ...session,
                sessionId: result.session_id,
                resume: result.parsed_resume,
                error: null
            });
        } catch (err) {
            setUploadError(err instanceof Error ? err.message : "Failed to parse resume. Please try again.");
            console.error(err);
        } finally {
            setIsUploading(false);
        }
    };

    const handleAnalyze = async () => {
        if (!session.sessionId || !jdText.trim()) return;

        try {
            const result = await analyzeJobDescription(jdText, session.sessionId);
            setSession({
                ...session,
                jobDescription: result.parsed_jd
            });
            onNext();
        } catch (err: any) {
            console.error("JD Analysis failed", err);
            setUploadError(err.message || "JD Analysis failed. Please check the text and try again.");
        }
    };

    const canAnalyze = !!session.resume && jdText.trim().length >= 50;

    return (
        <div className="max-w-6xl mx-auto py-8 px-4 animate-fade-in">
            {/* Mode Indicator Banner */}
            {mode && (
                <div className={`mb-8 p-4 rounded-2xl flex items-center gap-4 ${mode === 'assisted'
                    ? 'bg-gradient-to-r from-[var(--color-accent-50)] to-[var(--color-accent-100)] border border-[var(--color-accent-200)]'
                    : 'bg-gradient-to-r from-[var(--color-primary-50)] to-[var(--color-primary-100)] border border-[var(--color-primary-200)]'
                    }`}>
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${mode === 'assisted' ? 'bg-[var(--color-accent-500)]' : 'bg-[var(--color-primary-500)]'}`}>
                        {mode === 'assisted' ? (
                            <Zap className="w-5 h-5 text-white" />
                        ) : (
                            <FileText className="w-5 h-5 text-white" />
                        )}
                    </div>
                    <div>
                        <span className={`text-sm font-bold ${mode === 'assisted' ? 'text-[var(--color-accent-700)]' : 'text-[var(--color-primary-700)]'}`}>
                            {mode === 'assisted' ? 'Quick Mode' : 'Guided Mode'}
                        </span>
                        <p className={`text-sm ${mode === 'assisted' ? 'text-[var(--color-accent-600)]' : 'text-[var(--color-primary-600)]'}`}>
                            {mode === 'assisted'
                                ? "Fast-track analysis. After uploading, we'll go straight to results."
                                : "After uploading, you'll review parsed data before analysis."}
                        </p>
                    </div>
                </div>
            )}

            <div className="grid lg:grid-cols-2 gap-8 items-stretch">

                {/* Left Column: Resume Upload */}
                <div className="flex flex-col">
                    <div className="flex items-center gap-4 mb-6">
                        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[var(--color-primary-500)] to-[var(--color-primary-600)] text-white flex items-center justify-center font-bold text-xl shadow-lg shadow-[var(--color-primary-500)]/30">
                            1
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-[var(--color-neutral-900)]">Upload Resume</h2>
                            <p className="text-sm text-[var(--color-neutral-500)]">PDF or DOCX format</p>
                        </div>
                    </div>

                    {!session.resume ? (
                        <div
                            className={`
                                flex-1 min-h-[360px] border-2 border-dashed rounded-3xl flex flex-col items-center justify-center text-center p-8 transition-all duration-300 cursor-pointer
                                ${dragActive
                                    ? 'border-[var(--color-primary-500)] bg-[var(--color-primary-50)] scale-[1.02] shadow-xl'
                                    : 'border-[var(--color-neutral-200)] bg-white hover:border-[var(--color-primary-300)] hover:bg-[var(--color-primary-50)]/50 hover:shadow-lg'}
                                ${uploadError ? 'border-[var(--color-red-400)] bg-[var(--color-red-50)]' : ''}
                            `}
                            onDragEnter={handleDrag}
                            onDragLeave={handleDrag}
                            onDragOver={handleDrag}
                            onDrop={handleDrop}
                            onClick={() => document.getElementById('resume-upload')?.click()}
                        >
                            <input
                                type="file"
                                id="resume-upload"
                                className="hidden"
                                accept=".pdf,.docx"
                                onChange={handleFileChange}
                                disabled={isUploading}
                            />

                            <div className={`w-20 h-20 rounded-3xl flex items-center justify-center mb-6 transition-all duration-300 ${dragActive
                                ? 'bg-[var(--color-primary-500)] scale-110'
                                : 'bg-gradient-to-br from-[var(--color-primary-100)] to-[var(--color-primary-50)]'
                                }`}>
                                {isUploading ? (
                                    <div className="w-8 h-8 border-3 border-[var(--color-primary-500)] border-t-transparent rounded-full animate-spin"></div>
                                ) : (
                                    <Upload className={`w-10 h-10 ${dragActive ? 'text-white' : 'text-[var(--color-primary-500)]'}`} />
                                )}
                            </div>

                            <h3 className="text-xl font-bold text-[var(--color-neutral-900)] mb-2">
                                {isUploading ? 'Parsing resume...' : dragActive ? 'Drop it here!' : 'Drop your resume here'}
                            </h3>
                            <p className="text-[var(--color-neutral-500)] mb-6">
                                {isUploading ? 'Extracting skills, experience & education' : 'or click anywhere to browse'}
                            </p>

                            {!isUploading && (
                                <div className="flex items-center gap-4 text-xs text-[var(--color-neutral-400)]">
                                    <span className="flex items-center gap-1">
                                        <FileText className="w-3 h-3" /> PDF
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <FileText className="w-3 h-3" /> DOCX
                                    </span>
                                    <span>Max 10MB</span>
                                </div>
                            )}

                            {uploadError && (
                                <div className="mt-6 flex items-center gap-2 text-[var(--color-red-600)] text-sm bg-white px-4 py-3 rounded-xl border border-[var(--color-red-200)] shadow-sm animate-fade-in">
                                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                                    {uploadError}
                                </div>
                            )}
                        </div>
                    ) : (
                        // File Uploaded State
                        <div className="flex-1 min-h-[360px] border-2 border-[var(--color-green-300)] rounded-3xl bg-gradient-to-br from-[var(--color-green-50)] to-white p-8 flex flex-col items-center justify-center relative shadow-lg">
                            <div className="absolute top-4 right-4">
                                <CheckCircle className="w-8 h-8 text-[var(--color-green-500)]" />
                            </div>

                            <div className="w-24 h-24 bg-[var(--color-green-100)] rounded-3xl flex items-center justify-center mb-6 shadow-inner">
                                <FileCheck className="w-12 h-12 text-[var(--color-green-600)]" />
                            </div>

                            <h3 className="text-2xl font-bold text-[var(--color-green-700)] mb-2">Resume Ready!</h3>
                            <p className="text-[var(--color-green-600)] mb-2 text-center">
                                Successfully parsed your resume
                            </p>

                            {session.resume?.skills && (
                                <div className="flex flex-wrap justify-center gap-2 mt-4 mb-6 max-w-sm">
                                    {session.resume.skills.slice(0, 5).map((skill, i) => (
                                        <span key={i} className="px-3 py-1 bg-white rounded-full text-xs font-medium text-[var(--color-green-700)] border border-[var(--color-green-200)]">
                                            {skill.name}
                                        </span>
                                    ))}
                                    {session.resume.skills.length > 5 && (
                                        <span className="px-3 py-1 bg-[var(--color-green-100)] rounded-full text-xs font-medium text-[var(--color-green-600)]">
                                            +{session.resume.skills.length - 5} more
                                        </span>
                                    )}
                                </div>
                            )}

                            <button
                                onClick={(e) => { e.stopPropagation(); setSession({ ...session, resume: null }); }}
                                className="flex items-center gap-2 text-[var(--color-neutral-500)] hover:text-[var(--color-red-500)] font-medium hover:bg-[var(--color-red-50)] px-4 py-2 rounded-xl transition-all"
                            >
                                <Trash2 className="w-4 h-4" />
                                Replace file
                            </button>
                        </div>
                    )}
                </div>

                {/* Right Column: Job Description */}
                <div className="flex flex-col">
                    <div className="flex items-center gap-4 mb-6">
                        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[var(--color-accent-500)] to-[var(--color-accent-600)] text-[var(--color-neutral-900)] flex items-center justify-center font-bold text-xl shadow-lg shadow-[var(--color-accent-500)]/30">
                            2
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-[var(--color-neutral-900)]">Job Description</h2>
                            <p className="text-sm text-[var(--color-neutral-500)]">Paste the full job posting</p>
                        </div>
                    </div>

                    <div className="relative flex-1 min-h-[360px]">
                        <div className="absolute top-0 left-0 right-0 flex items-center gap-2 px-6 py-4 bg-gradient-to-b from-white via-white to-transparent z-10 rounded-t-3xl border-b border-[var(--color-neutral-100)]">
                            <Briefcase className="w-4 h-4 text-[var(--color-neutral-400)]" />
                            <span className="text-sm font-medium text-[var(--color-neutral-500)]">Job Requirements</span>
                        </div>

                        <textarea
                            className="w-full h-full min-h-[360px] resize-none p-6 pt-16 text-base leading-relaxed rounded-3xl border-2 border-[var(--color-neutral-200)] bg-white focus:border-[var(--color-accent-400)] focus:ring-4 focus:ring-[var(--color-accent-100)] focus:shadow-xl transition-all outline-none"
                            placeholder="Paste the complete job description here...

Include:
• Job title and responsibilities
• Required skills and qualifications
• Years of experience needed
• Nice-to-have skills"
                            value={jdText}
                            onChange={(e) => setJdText(e.target.value)}
                        />

                        <div className={`absolute bottom-4 right-4 text-xs font-bold px-3 py-1.5 rounded-lg transition-all ${jdText.length >= 50
                            ? 'bg-[var(--color-green-100)] text-[var(--color-green-600)] border border-[var(--color-green-200)]'
                            : 'bg-[var(--color-neutral-100)] text-[var(--color-neutral-400)] border border-[var(--color-neutral-200)]'
                            }`}>
                            {jdText.length >= 50 ? (
                                <span className="flex items-center gap-1">
                                    <CheckCircle className="w-3 h-3" />
                                    {jdText.length} chars
                                </span>
                            ) : (
                                `${jdText.length}/50 min`
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Actions */}
            <div className="mt-12 flex flex-col items-center gap-4">
                <button
                    onClick={handleAnalyze}
                    disabled={!canAnalyze}
                    className={`
                        group flex items-center gap-3 min-w-[320px] h-16 px-10 rounded-2xl font-bold text-xl transition-all duration-300
                        ${canAnalyze
                            ? 'bg-gradient-to-r from-[var(--color-primary-600)] to-[var(--color-primary-500)] text-white shadow-xl shadow-[var(--color-primary-500)]/30 hover:shadow-[var(--color-primary-500)]/50 hover:scale-105'
                            : 'bg-[var(--color-neutral-100)] text-[var(--color-neutral-400)] cursor-not-allowed'}
                    `}
                >
                    <Sparkles className={`w-6 h-6 ${canAnalyze ? 'animate-pulse' : ''}`} />
                    <span>{mode === 'guided' ? 'Review Parsed Data' : 'Start Analysis'}</span>
                    <ArrowRight className={`w-6 h-6 transition-transform ${canAnalyze ? 'group-hover:translate-x-1' : ''}`} />
                </button>

                {!canAnalyze && (
                    <p className="text-sm text-[var(--color-neutral-400)] flex items-center gap-2">
                        {!session.resume && <span>📄 Upload resume</span>}
                        {!session.resume && jdText.length < 50 && <span>•</span>}
                        {jdText.length < 50 && <span>📝 Add job description ({50 - jdText.length} more chars)</span>}
                    </p>
                )}
            </div>
        </div>
    );
}
