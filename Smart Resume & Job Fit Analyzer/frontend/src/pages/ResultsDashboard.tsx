
import { useState, useEffect, useMemo } from 'react';
import type { SessionState, SkillMatch } from '../services/types';
import { exportResults } from '../services/api';
import {
    Download, RefreshCw, CheckCircle2,
    XCircle, ChevronDown, ChevronUp,
    Briefcase, Sparkles, TrendingUp, AlertCircle,
    FileText, GraduationCap, LayoutDashboard,
    Share2, Check, Target, Zap
} from 'lucide-react';

interface ResultsDashboardProps {
    session: SessionState;
    onStartOver: () => void;
}

// --- Animated Counter Hook ---
const useAnimatedCounter = (end: number, duration: number = 1500) => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        let startTime: number | null = null;
        const animate = (timestamp: number) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            setCount(Math.floor(easeOutQuart * end));
            if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
    }, [end, duration]);

    return count;
};

// --- Enhanced Score Hero with Animation ---
const ScoreHero = ({ score, confidence, explanation }: { score: number, confidence: string, explanation: string }) => {
    const animatedScore = useAnimatedCounter(score, 1800);
    const [showCelebration, setShowCelebration] = useState(false);
    const radius = 58;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (animatedScore / 100) * circumference;

    useEffect(() => {
        if (score > 75) {
            const timer = setTimeout(() => setShowCelebration(true), 1200);
            return () => clearTimeout(timer);
        }
    }, [score]);

    // Color logic
    let colorClass = 'text-[var(--color-primary-500)]';
    let strokeColor = 'var(--color-primary-500)';
    let bgGradient = 'from-[var(--color-primary-50)] to-white';
    if (score > 80) {
        colorClass = 'text-[var(--color-green-500)]';
        strokeColor = 'var(--color-green-500)';
        bgGradient = 'from-[var(--color-green-50)] to-white';
    }
    else if (score < 50) {
        colorClass = 'text-[var(--color-secondary-500)]';
        strokeColor = 'var(--color-secondary-500)';
        bgGradient = 'from-[var(--color-secondary-50)] to-white';
    }

    return (
        <div className={`bg-gradient-to-b ${bgGradient} border-b border-[var(--color-neutral-200)] pb-12 pt-8 px-6 relative overflow-hidden`}>
            {/* Celebration particles for high scores */}
            {showCelebration && (
                <div className="absolute inset-0 pointer-events-none">
                    {[...Array(12)].map((_, i) => (
                        <div
                            key={i}
                            className="absolute w-2 h-2 rounded-full animate-float"
                            style={{
                                left: `${Math.random() * 100}%`,
                                top: `${Math.random() * 100}%`,
                                backgroundColor: ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b'][i % 4],
                                animationDelay: `${i * 0.1}s`,
                                animationDuration: `${2 + Math.random() * 2}s`,
                            }}
                        />
                    ))}
                </div>
            )}

            <div className="max-w-5xl mx-auto grid md:grid-cols-[200px_1fr] gap-8 items-center relative z-10">
                {/* Chart */}
                <div className="relative w-32 h-32 md:w-40 md:h-40 mx-auto flex items-center justify-center transform hover:scale-105 transition-transform duration-500">
                    <svg className="w-full h-full transform -rotate-90 drop-shadow-xl">
                        <circle cx="50%" cy="50%" r={radius} fill="white" stroke="var(--color-neutral-100)" strokeWidth="12" />
                        <circle
                            cx="50%" cy="50%" r={radius} fill="transparent"
                            stroke={strokeColor} strokeWidth="12"
                            strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
                            className="transition-all duration-100"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className={`text-5xl font-black tracking-tighter ${colorClass} transition-all`}>{animatedScore}</span>
                        <span className="text-xs font-bold text-[var(--color-neutral-400)] uppercase mt-1">Job Fit</span>
                    </div>
                </div>

                {/* Text content */}
                <div className="text-center md:text-left space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/80 backdrop-blur border border-[var(--color-neutral-200)] shadow-sm">
                        <span className={`w-2.5 h-2.5 rounded-full ${confidence === 'high' ? 'bg-[var(--color-green-500)]' : 'bg-[var(--color-secondary-500)]'} animate-pulse`}></span>
                        <span className="text-xs font-bold uppercase tracking-wider text-[var(--color-neutral-600)]">{confidence} Confidence Match</span>
                    </div>

                    <h1 className="text-3xl lg:text-4xl font-bold text-[var(--color-neutral-900)] leading-tight">
                        {score > 75 ? "🎯 Strong alignment with this role!" : score > 50 ? "💡 Moderate alignment found." : "⚠️ Low alignment detected."}
                    </h1>

                    <p className="text-lg text-[var(--color-neutral-600)] leading-relaxed max-w-3xl">
                        {explanation}
                    </p>
                </div>
            </div>
        </div>
    );
};

// --- Visual Match Bar ---
const MatchBar = ({ matched, partial, missing }: { matched: number, partial: number, missing: number }) => {
    const total = matched + partial + missing;
    if (total === 0) return null;

    const matchedPct = (matched / total) * 100;
    const partialPct = (partial / total) * 100;
    const missingPct = (missing / total) * 100;

    return (
        <div className="mb-8">
            <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-[var(--color-neutral-700)]">Skill Match Overview</span>
                <span className="text-sm text-[var(--color-neutral-500)]">{matched + partial} of {total} matched</span>
            </div>
            <div className="h-4 rounded-full bg-[var(--color-neutral-100)] overflow-hidden flex shadow-inner">
                <div
                    className="bg-gradient-to-r from-[var(--color-green-400)] to-[var(--color-green-500)] transition-all duration-1000 ease-out"
                    style={{ width: `${matchedPct}%` }}
                    title={`${matched} matched`}
                />
                <div
                    className="bg-gradient-to-r from-[var(--color-amber-400)] to-[var(--color-amber-500)] transition-all duration-1000 ease-out delay-200"
                    style={{ width: `${partialPct}%` }}
                    title={`${partial} partial`}
                />
                <div
                    className="bg-gradient-to-r from-[var(--color-red-300)] to-[var(--color-red-400)] transition-all duration-1000 ease-out delay-400"
                    style={{ width: `${missingPct}%` }}
                    title={`${missing} missing`}
                />
            </div>
            <div className="flex gap-4 mt-2 text-xs">
                <div className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-[var(--color-green-500)]"></span>
                    <span className="text-[var(--color-neutral-600)]">Matched ({matched})</span>
                </div>
                <div className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-[var(--color-amber-500)]"></span>
                    <span className="text-[var(--color-neutral-600)]">Partial ({partial})</span>
                </div>
                <div className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-[var(--color-red-400)]"></span>
                    <span className="text-[var(--color-neutral-600)]">Missing ({missing})</span>
                </div>
            </div>
        </div>
    );
};

// --- Category Tabs ---
type FilterTab = 'all' | 'matched' | 'partial' | 'missing';

const CategoryTabs = ({
    activeTab,
    onTabChange,
    counts
}: {
    activeTab: FilterTab,
    onTabChange: (tab: FilterTab) => void,
    counts: { all: number, matched: number, partial: number, missing: number }
}) => {
    const tabs: { id: FilterTab, label: string, icon: any, color: string }[] = [
        { id: 'all', label: 'All', icon: LayoutDashboard, color: 'var(--color-primary-500)' },
        { id: 'matched', label: 'Matched', icon: CheckCircle2, color: 'var(--color-green-500)' },
        { id: 'partial', label: 'Partial', icon: AlertCircle, color: 'var(--color-amber-500)' },
        { id: 'missing', label: 'Missing', icon: XCircle, color: 'var(--color-red-500)' },
    ];

    return (
        <div className="flex gap-2 p-1 bg-[var(--color-neutral-100)] rounded-xl mb-4 overflow-x-auto no-scrollbar">
            {tabs.map(tab => (
                <button
                    key={tab.id}
                    onClick={() => onTabChange(tab.id)}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === tab.id
                        ? 'bg-white shadow-sm text-[var(--color-neutral-900)]'
                        : 'text-[var(--color-neutral-500)] hover:text-[var(--color-neutral-700)]'
                        }`}
                >
                    <tab.icon className="w-4 h-4" style={{ color: activeTab === tab.id ? tab.color : undefined }} />
                    <span>{tab.label}</span>
                    <span className={`px-1.5 py-0.5 rounded-full text-xs ${activeTab === tab.id
                        ? 'bg-[var(--color-neutral-100)]'
                        : 'bg-[var(--color-neutral-200)]'
                        }`}>
                        {counts[tab.id]}
                    </span>
                </button>
            ))}
        </div>
    );
};

const ExtractionInsight = ({ resume }: { resume: any }) => {
    if (!resume) return null;
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white p-4 rounded-xl border border-[var(--color-neutral-200)] shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-2 text-[var(--color-primary-500)]">
                    <Target className="w-5 h-5" />
                    <span className="text-xs font-bold uppercase text-[var(--color-neutral-500)]">Skills Found</span>
                </div>
                <p className="text-3xl font-bold text-[var(--color-neutral-900)]">{resume.skills.length}</p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-[var(--color-neutral-200)] shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-2 text-[var(--color-amber-500)]">
                    <Briefcase className="w-5 h-5" />
                    <span className="text-xs font-bold uppercase text-[var(--color-neutral-500)]">Experience</span>
                </div>
                <p className="text-3xl font-bold text-[var(--color-neutral-900)]">{resume.experience.length} <span className="text-sm font-normal text-[var(--color-neutral-400)]">roles</span></p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-[var(--color-neutral-200)] shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-2 text-[var(--color-green-500)]">
                    <GraduationCap className="w-5 h-5" />
                    <span className="text-xs font-bold uppercase text-[var(--color-neutral-500)]">Education</span>
                </div>
                <p className="text-3xl font-bold text-[var(--color-neutral-900)]">{resume.education.length} <span className="text-sm font-normal text-[var(--color-neutral-400)]">entries</span></p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-[var(--color-neutral-200)] shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-2 text-[var(--color-purple-500)]">
                    <FileText className="w-5 h-5" />
                    <span className="text-xs font-bold uppercase text-[var(--color-neutral-500)]">Word Count</span>
                </div>
                <p className="text-3xl font-bold text-[var(--color-neutral-900)]">{resume.raw_text?.split(/\s+/).length || 0}</p>
            </div>
        </div>
    );
};

const SkillRow = ({ skill, onClick, isExpanded }: { skill: SkillMatch, onClick: () => void, isExpanded: boolean }) => {
    let Icon = CheckCircle2;
    let iconColor = "text-[var(--color-neutral-300)]";
    let bgClass = "hover:bg-[var(--color-neutral-50)]";

    if (skill.match_type === 'matched') {
        Icon = CheckCircle2;
        iconColor = "text-[var(--color-green-500)]";
        bgClass = "hover:bg-[var(--color-green-50)/50]";
    } else if (skill.match_type === 'partial') {
        Icon = AlertCircle;
        iconColor = "text-[var(--color-amber-500)]";
        bgClass = "hover:bg-[var(--color-amber-50)/50]";
    } else {
        Icon = XCircle;
        iconColor = "text-[var(--color-red-400)]";
        bgClass = "hover:bg-[var(--color-red-50)/50]";
    }

    return (
        <div className="border-b border-[var(--color-neutral-100)] last:border-0">
            <button
                onClick={onClick}
                className={`w-full flex items-center justify-between p-4 transition-colors text-left group ${isExpanded ? 'bg-[var(--color-neutral-50)]' : bgClass}`}
            >
                <div className="flex items-center gap-4">
                    <Icon className={`w-5 h-5 ${iconColor}`} />
                    <div>
                        <span className={`font-semibold text-[var(--color-neutral-900)] block ${skill.match_type === 'missing' ? 'text-[var(--color-neutral-500)]' : ''}`}>
                            {skill.skill_name}
                        </span>
                        {skill.match_type !== 'missing' && (
                            <span className="text-xs text-[var(--color-neutral-500)] font-medium">
                                {skill.match_type === 'matched' ? '✓ Confirmed by evidence' : '~ Partial alignment found'}
                            </span>
                        )}
                    </div>
                </div>
                {skill.evidence && (
                    <div className="flex items-center gap-2 text-[var(--color-neutral-400)] group-hover:text-[var(--color-primary-500)] transition-colors">
                        <span className="text-xs font-semibold uppercase">Evidence</span>
                        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </div>
                )}
            </button>
            {isExpanded && skill.evidence && (
                <div className="px-14 pb-6 pt-2 animate-fade-in">
                    <div className="bg-white rounded-lg border border-[var(--color-neutral-200)] p-4 shadow-sm relative">
                        <div className="absolute -top-2 left-6 w-4 h-4 bg-white border-t border-l border-[var(--color-neutral-200)] transform rotate-45"></div>
                        <h4 className="text-xs font-bold text-[var(--color-neutral-400)] uppercase mb-1">Found in Resume</h4>
                        <p className="font-mono text-sm text-[var(--color-neutral-700)] bg-[var(--color-neutral-50)] p-3 rounded border border-[var(--color-neutral-200)]">
                            "{skill.evidence}"
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

// --- Priority Badge ---
const PriorityBadge = ({ priority }: { priority: string | number }) => {
    const config: Record<string, { bg: string, text: string, icon: string }> = {
        high: { bg: 'bg-red-100', text: 'text-red-700', icon: '🔴' },
        medium: { bg: 'bg-amber-100', text: 'text-amber-700', icon: '🟡' },
        low: { bg: 'bg-green-100', text: 'text-green-700', icon: '🟢' },
    };

    // Convert numeric priority (1-5) to level, or use string directly
    let level: string;
    if (typeof priority === 'number') {
        if (priority <= 2) level = 'high';
        else if (priority <= 4) level = 'medium';
        else level = 'low';
    } else {
        level = (priority || 'medium').toLowerCase();
    }

    const { bg, text, icon } = config[level] || config.medium;

    return (
        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${bg} ${text}`}>
            {icon} {typeof priority === 'number' ? `P${priority}` : priority}
        </span>
    );
};

export default function ResultsDashboard({ session, onStartOver }: ResultsDashboardProps) {
    const [expandedSkill, setExpandedSkill] = useState<string | null>(null);
    const [isExporting, setIsExporting] = useState(false);
    const [activeTab, setActiveTab] = useState<FilterTab>('all');
    const [copied, setCopied] = useState(false);

    if (!session.evaluation || !session.resume) return null;
    const { job_fit_score, confidence_level, explanation, skill_matches, experience_signals, improvement_suggestions } = session.evaluation;

    // Filter skills
    const matched = skill_matches.filter((s: SkillMatch) => s.match_type === 'matched');
    const partial = skill_matches.filter((s: SkillMatch) => s.match_type === 'partial');
    const missing = skill_matches.filter((s: SkillMatch) => s.match_type === 'missing');

    // Filtered skills based on active tab
    const filteredSkills = useMemo(() => {
        switch (activeTab) {
            case 'matched': return matched;
            case 'partial': return partial;
            case 'missing': return missing;
            default: return skill_matches;
        }
    }, [activeTab, matched, partial, missing, skill_matches]);

    const hasRequirements = skill_matches.length > 0;

    const handleDownload = async () => {
        if (!session.sessionId) return;
        setIsExporting(true);
        try { await exportResults(session.sessionId); }
        catch (e) { alert("Download failed"); }
        finally { setIsExporting(false); }
    };

    const handleShare = async () => {
        const summary = `📊 Job Fit Score: ${job_fit_score}/100
✅ Matched Skills: ${matched.length}
⚠️ Partial Matches: ${partial.length}
❌ Missing Skills: ${missing.length}

${explanation}

Generated by Smart Resume Analyzer`;

        await navigator.clipboard.writeText(summary);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="min-h-screen bg-[var(--color-neutral-50)] pb-24 font-sans">

            {/* A. Fit Summary (Hero) */}
            <ScoreHero
                score={job_fit_score}
                confidence={confidence_level || 'medium'}
                explanation={explanation}
            />

            <div className="max-w-5xl mx-auto px-6 -mt-8 relative z-10 space-y-8">

                {/* B. Extraction Insight (What we parsed) */}
                <ExtractionInsight resume={session.resume} />

                {/* C. Visual Match Bar */}
                <MatchBar matched={matched.length} partial={partial.length} missing={missing.length} />

                <div className="grid lg:grid-cols-3 gap-8">
                    {/* D. Skill Match Breakdown (Left Column - 2/3 width) */}
                    <div className="lg:col-span-2 space-y-8">
                        <section className="bg-white rounded-[24px] shadow-sm border border-[var(--color-neutral-200)] overflow-hidden">
                            <div className="p-6 border-b border-[var(--color-neutral-100)] bg-[var(--color-neutral-50)/50]">
                                <div className="flex items-center justify-between mb-4">
                                    <div className="flex items-center gap-3">
                                        <LayoutDashboard className="w-5 h-5 text-[var(--color-primary-600)]" />
                                        <h3 className="h2 text-xl m-0">Gap Analysis</h3>
                                    </div>
                                    <span className="text-sm font-medium text-[var(--color-neutral-500)]">
                                        {matched.length + partial.length} of {skill_matches.length} matches
                                    </span>
                                </div>

                                {/* Category Tabs */}
                                <CategoryTabs
                                    activeTab={activeTab}
                                    onTabChange={setActiveTab}
                                    counts={{
                                        all: skill_matches.length,
                                        matched: matched.length,
                                        partial: partial.length,
                                        missing: missing.length
                                    }}
                                />
                            </div>

                            {hasRequirements ? (
                                <div className="divide-y divide-[var(--color-neutral-100)] max-h-[500px] overflow-y-auto">
                                    {filteredSkills.length > 0 ? (
                                        filteredSkills.map(skill => (
                                            <SkillRow
                                                key={skill.skill_name}
                                                skill={skill}
                                                isExpanded={expandedSkill === skill.skill_name}
                                                onClick={() => setExpandedSkill(expandedSkill === skill.skill_name ? null : skill.skill_name)}
                                            />
                                        ))
                                    ) : (
                                        <div className="p-8 text-center text-[var(--color-neutral-500)]">
                                            No skills in this category
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div className="p-12 text-center">
                                    <div className="w-16 h-16 bg-[var(--color-neutral-100)] rounded-full flex items-center justify-center mx-auto mb-4">
                                        <AlertCircle className="w-8 h-8 text-[var(--color-neutral-400)]" />
                                    </div>
                                    <p className="text-[var(--color-neutral-600)] font-medium">No specific skill requirements found in Job Description.</p>
                                    <p className="text-sm text-[var(--color-neutral-400)] mt-2">Try pasting a more detailed job description.</p>
                                </div>
                            )}
                        </section>

                        {/* Improvement Plan */}
                        <section>
                            <div className="flex items-center gap-3 mb-6">
                                <Sparkles className="w-6 h-6 text-[var(--color-primary-600)]" />
                                <h2 className="text-2xl font-bold text-[var(--color-neutral-900)]">Action Plan</h2>
                            </div>
                            <div className="space-y-4">
                                {improvement_suggestions.length > 0 ? (
                                    improvement_suggestions.slice(0, 5).map((suggestion, idx) => (
                                        <div key={idx} className="bg-white p-5 rounded-[16px] border border-[var(--color-neutral-200)] shadow-sm flex gap-4 hover:border-[var(--color-primary-300)] hover:shadow-md transition-all group">
                                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-primary-100)] to-[var(--color-primary-50)] flex-shrink-0 flex items-center justify-center text-[var(--color-primary-600)] font-bold text-sm group-hover:scale-110 transition-transform">
                                                {idx + 1}
                                            </div>
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <h4 className="font-bold text-[var(--color-neutral-900)]">{suggestion.category}</h4>
                                                    <PriorityBadge priority={suggestion.priority || 3} />
                                                </div>
                                                <p className="text-sm text-[var(--color-neutral-600)] leading-relaxed">{suggestion.suggestion}</p>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="p-8 bg-gradient-to-br from-[var(--color-green-50)] to-white rounded-xl border border-[var(--color-green-200)] text-center">
                                        <CheckCircle2 className="w-12 h-12 text-[var(--color-green-500)] mx-auto mb-3" />
                                        <p className="text-[var(--color-green-700)] font-semibold">Your resume is very strong!</p>
                                        <p className="text-sm text-[var(--color-green-600)] mt-1">No immediate improvements needed.</p>
                                    </div>
                                )}
                            </div>
                        </section>
                    </div>

                    {/* E. Signals & Actions (Right Column - 1/3 width) */}
                    <div className="space-y-8">
                        {/* Experience Signal Card */}
                        {experience_signals && (
                            <div className="bg-white rounded-[24px] p-6 border border-[var(--color-neutral-200)] shadow-sm">
                                <div className="flex items-center gap-3 mb-6">
                                    <TrendingUp className="w-6 h-6 text-[var(--color-accent-600)]" />
                                    <h3 className="font-bold text-lg text-[var(--color-neutral-900)]">Career Impact</h3>
                                </div>

                                <div className="space-y-6">
                                    <div>
                                        <label className="text-xs font-bold text-[var(--color-neutral-400)] uppercase block mb-2">Ownership Level</label>
                                        <div className={`px-4 py-3 rounded-xl border flex items-center justify-between ${experience_signals.ownership_strength === 'High'
                                            ? 'bg-green-50 border-green-200 text-green-800'
                                            : 'bg-indigo-50 border-indigo-200 text-indigo-800'
                                            }`}>
                                            <span className="font-bold">{experience_signals.ownership_strength} Impact</span>
                                            {experience_signals.ownership_strength === 'High' ? '🚀' : '⚡'}
                                        </div>
                                    </div>

                                    <div>
                                        <label className="text-xs font-bold text-[var(--color-neutral-400)] uppercase block mb-2">Key Signals Detected</label>
                                        {experience_signals.leadership_signals.length > 0 ? (
                                            <div className="flex flex-wrap gap-2">
                                                {experience_signals.leadership_signals.slice(0, 5).map((sig: string, i: number) => (
                                                    <span key={i} className="px-2 py-1 bg-[var(--color-neutral-100)] text-[var(--color-neutral-700)] text-xs rounded-md border border-[var(--color-neutral-200)]">
                                                        {sig}
                                                    </span>
                                                ))}
                                            </div>
                                        ) : (
                                            <p className="text-sm text-[var(--color-neutral-400)] italic">No specific leadership keywords found.</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Ready to Apply */}
                        <div className="bg-gradient-to-br from-[var(--color-neutral-900)] to-[var(--color-neutral-800)] rounded-[24px] p-8 text-center text-white space-y-6 shadow-xl">
                            <div className="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center mx-auto">
                                <Zap className="w-7 h-7" />
                            </div>
                            <h3 className="text-xl font-bold">Ready to apply?</h3>
                            <div className="flex flex-col gap-3">
                                <button
                                    onClick={handleDownload}
                                    disabled={isExporting}
                                    className="btn bg-white text-[var(--color-neutral-900)] hover:bg-[var(--color-neutral-100)] border-0 w-full justify-center font-semibold active:scale-95 transition-all"
                                >
                                    <Download className="w-4 h-4 mr-2" />
                                    {isExporting ? 'Generating...' : 'Download Report'}
                                </button>
                                <button
                                    onClick={handleShare}
                                    className="btn border border-white/20 hover:border-white/40 text-white bg-white/10 hover:bg-white/20 w-full justify-center active:scale-95 transition-all"
                                >
                                    {copied ? <Check className="w-4 h-4 mr-2" /> : <Share2 className="w-4 h-4 mr-2" />}
                                    {copied ? 'Copied!' : 'Share Summary'}
                                </button>
                                <button
                                    onClick={onStartOver}
                                    className="btn border border-white/20 hover:border-white/40 text-white bg-transparent w-full justify-center active:scale-95 transition-all"
                                >
                                    <RefreshCw className="w-4 h-4 mr-2" />
                                    New Analysis
                                </button>
                            </div>
                            <p className="text-xs text-[var(--color-neutral-400)] leading-relaxed">
                                AI analysis is advisory only.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
