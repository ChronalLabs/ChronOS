/**
 * API types matching backend Pydantic schemas
 */

// Enums
export type MatchType = 'matched' | 'partial' | 'missing';
export type ConfidenceLevel = 'high' | 'medium' | 'low';
export type SkillCategory =
    | 'programming_languages'
    | 'frameworks'
    | 'databases'
    | 'tools'
    | 'cloud'
    | 'soft_skills'
    | 'other';
export type SkillPriority = 'required' | 'optional';

// Resume types
export interface EducationEntry {
    institution: string;
    degree: string;
    field_of_study?: string;
    start_date?: string;
    end_date?: string;
    gpa?: string;
    source_text: string;
}

export interface ExperienceEntry {
    company: string;
    title: string;
    start_date?: string;
    end_date?: string;
    description: string;
    responsibilities: string[];
    source_text: string;
}

export interface ProjectEntry {
    name: string;
    description: string;
    technologies: string[];
    url?: string;
    source_text: string;
}

export interface ExtractedSkill {
    name: string;
    canonical_name: string;
    category: SkillCategory;
    confidence: ConfidenceLevel;
    source_text: string;
    line_number?: number;
}

export interface ParsedResume {
    raw_text: string;
    education: EducationEntry[];
    experience: ExperienceEntry[];
    projects: ProjectEntry[];
    skills: ExtractedSkill[];
    contact_info: Record<string, string>;
    parsing_warnings: string[];
}

// Job Description types
export interface JDRequirement {
    text: string;
    skills: string[];
    priority: SkillPriority;
}

export interface ParsedJobDescription {
    raw_text: string;
    title?: string;
    company?: string;
    requirements: JDRequirement[];
    required_skills: string[];
    optional_skills: string[];
    experience_requirements?: string;
    education_requirements?: string;
}

// Evaluation types
export interface SkillMatch {
    skill_name: string;
    canonical_name: string;
    match_type: MatchType;
    confidence: ConfidenceLevel;
    jd_priority: SkillPriority;
    evidence?: string;
    line_number?: number;
    match_score: number;
}

export interface ScoreBreakdown {
    required_skills_score: number;
    optional_skills_score: number;
    experience_depth_score: number;
    education_match_score: number;
    weights_applied: Record<string, number>;
    penalties_applied: string[];
}

export interface ImprovementSuggestion {
    category: string;
    priority: number;
    suggestion: string;
    evidence_gap?: string;
    affected_skills: string[];
}

export interface ExperienceSignals {
    relevant_years: number;
    ownership_strength: string;
    leadership_signals: string[];
    responsibility_alignment: string;
}

export interface EvaluationResult {
    job_fit_score: number;
    confidence_level: ConfidenceLevel;
    score_breakdown: ScoreBreakdown;
    skill_matches: SkillMatch[];
    matched_count: number;
    partial_count: number;
    missing_count: number;
    explanation: string;
    experience_signals?: ExperienceSignals;
    improvement_suggestions: ImprovementSuggestion[];
    advisory_notice: string;
}

// API Response types
export interface ResumeUploadResponse {
    session_id: string;
    filename: string;
    parsed_resume: ParsedResume;
    message: string;
}

export interface JobDescriptionResponse {
    session_id: string;
    parsed_jd: ParsedJobDescription;
    message: string;
}

export interface EvaluationResponse {
    session_id: string;
    result: EvaluationResult;
    evaluated_at: string;
    message: string;
}

export interface ExportResponse {
    session_id: string;
    download_url: string;
    format: string;
    expires_at: string;
}

// App state types
export interface SessionState {
    sessionId: string | null;
    resume: ParsedResume | null;
    jobDescription: ParsedJobDescription | null;
    evaluation: EvaluationResult | null;
    isLoading: boolean;
    error: string | null;
}

export type AnalysisMode = 'guided' | 'assisted';

export type AnalysisStep =
    | 'mode-selection'
    | 'resume-upload'
    | 'resume-review'
    | 'jd-input'
    | 'analyzing'
    | 'results';
