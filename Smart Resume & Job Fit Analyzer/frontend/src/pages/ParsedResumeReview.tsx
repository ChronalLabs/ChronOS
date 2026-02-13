
import { useState, useMemo } from 'react';
import type { ParsedResume, ExtractedSkill, SkillCategory, ExperienceEntry, EducationEntry, ProjectEntry } from '../services/types';
import { updateResume } from '../services/api';
import {
    User, Briefcase, GraduationCap, Code, FolderGit2,
    AlertCircle, ArrowRight, Loader2, Trash2, Plus, AlertTriangle,
    CheckCircle2, Calendar
} from 'lucide-react';

interface ParsedResumeReviewProps {
    resume: ParsedResume | null;
    sessionId: string;
    onContinue: () => void;
}

type SectionType = 'personal' | 'skills' | 'experience' | 'education' | 'projects';

// Empty state component
const EmptyState = ({ icon: Icon, title, description, onAdd }: {
    icon: any;
    title: string;
    description: string;
    onAdd: () => void;
}) => (
    <div className="flex flex-col items-center justify-center py-12 px-6 text-center">
        <div className="w-16 h-16 rounded-full bg-[var(--color-neutral-100)] flex items-center justify-center mb-4">
            <Icon className="w-8 h-8 text-[var(--color-neutral-400)]" />
        </div>
        <h3 className="text-lg font-semibold text-[var(--color-neutral-700)] mb-2">{title}</h3>
        <p className="text-sm text-[var(--color-neutral-500)] mb-6 max-w-md">{description}</p>
        <button
            onClick={onAdd}
            className="btn btn-primary flex items-center gap-2"
        >
            <Plus className="w-4 h-4" />
            Add Entry
        </button>
    </div>
);

// Confidence badge component
const ConfidenceBadge = ({ level }: { level: string }) => {
    const config = {
        high: { color: 'bg-green-500', label: '●' },
        medium: { color: 'bg-yellow-500', label: '●' },
        low: { color: 'bg-red-500', label: '●' },
    };
    const { color } = config[level as keyof typeof config] || config.medium;
    return (
        <span className={`inline-block w-2 h-2 rounded-full ${color} mr-2`} title={`${level} confidence`} />
    );
};

export default function ParsedResumeReview({ resume, sessionId, onContinue }: ParsedResumeReviewProps) {
    const [localResume, setLocalResume] = useState<ParsedResume | null>(resume);
    const [activeSection, setActiveSection] = useState<SectionType>('experience');
    const [isSaving, setIsSaving] = useState(false);
    const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

    // Group skills by category for display
    const skillGroups = useMemo(() => {
        if (!localResume?.skills) return {};
        const groups: Record<string, ExtractedSkill[]> = {};
        localResume.skills.forEach(skill => {
            const cat = skill.category || 'other';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(skill);
        });
        return groups;
    }, [localResume?.skills]);

    if (!localResume) return null;

    // --- Update Handler ---
    const handleSave = async (updatedData: ParsedResume) => {
        setIsSaving(true);
        try {
            await updateResume(sessionId, updatedData);
            setLocalResume(updatedData);
            setHasUnsavedChanges(false);
        } catch (error) {
            console.error("Failed to save resume updates", error);
            alert("Failed to save changes. Please try again.");
        } finally {
            setIsSaving(false);
        }
    };

    // Generic Field Updater
    const updateField = (section: keyof ParsedResume, value: any) => {
        const updated = { ...localResume, [section]: value };
        setLocalResume(updated);
        setHasUnsavedChanges(true);
    };

    // Helper to update contact info specifically
    const updateContactInfo = (key: string, value: string) => {
        const updatedContact = { ...localResume.contact_info, [key]: value };
        updateField('contact_info', updatedContact);
    };

    // --- Add Entry Handlers ---
    const addExperience = () => {
        const newEntry: ExperienceEntry = {
            company: 'New Company',
            title: 'Job Title',
            description: '',
            responsibilities: [],
            source_text: 'Manually added',
            start_date: '',
            end_date: ''
        };
        updateField('experience', [...localResume.experience, newEntry]);
    };

    const addEducation = () => {
        const newEntry: EducationEntry = {
            institution: 'University Name',
            degree: 'Degree',
            source_text: 'Manually added',
            start_date: '',
            end_date: ''
        };
        updateField('education', [...localResume.education, newEntry]);
    };

    const addProject = () => {
        const newEntry: ProjectEntry = {
            name: 'Project Name',
            description: '',
            technologies: [],
            source_text: 'Manually added'
        };
        updateField('projects', [...localResume.projects, newEntry]);
    };

    // --- Delete Entry Handlers ---
    const deleteExperience = (idx: number) => {
        if (confirm('Are you sure you want to delete this experience entry?')) {
            const newExp = localResume.experience.filter((_, i) => i !== idx);
            updateField('experience', newExp);
        }
    };

    const deleteEducation = (idx: number) => {
        if (confirm('Are you sure you want to delete this education entry?')) {
            const newEdu = localResume.education.filter((_, i) => i !== idx);
            updateField('education', newEdu);
        }
    };

    const deleteProject = (idx: number) => {
        if (confirm('Are you sure you want to delete this project?')) {
            const newProj = localResume.projects.filter((_, i) => i !== idx);
            updateField('projects', newProj);
        }
    };

    // --- Render Helpers ---

    const SidebarItem = ({ id, icon: Icon, label, count }: { id: SectionType, icon: any, label: string, count?: number }) => (
        <button
            onClick={() => setActiveSection(id)}
            className={`
                w-full flex items-center justify-between p-4 rounded-[12px] mb-2 transition-all
                ${activeSection === id
                    ? 'bg-white shadow-sm border border-[var(--color-primary-200)] ring-1 ring-[var(--color-primary-100)]'
                    : 'hover:bg-white hover:shadow-sm text-[var(--color-neutral-600)] border border-transparent'}
            `}
        >
            <div className="flex items-center gap-3">
                <Icon className={`w-5 h-5 ${activeSection === id ? 'text-[var(--color-primary-600)]' : 'text-[var(--color-neutral-400)]'}`} />
                <span className={`font-medium ${activeSection === id ? 'text-[var(--color-neutral-900)]' : ''}`}>{label}</span>
            </div>
            {count !== undefined && (
                <span className={`text-xs py-0.5 px-2 rounded-full ${count === 0 ? 'bg-[var(--color-red-100)] text-[var(--color-red-600)]' : 'bg-[var(--color-neutral-100)] text-[var(--color-neutral-600)]'}`}>
                    {count}
                </span>
            )}
        </button>
    );

    // --- Main Actions ---
    const handleRunAnalysis = async () => {
        if (hasUnsavedChanges && localResume) {
            await handleSave(localResume);
        }
        onContinue();
    };

    // Category display names
    const categoryLabels: Record<string, string> = {
        programming_languages: 'Programming Languages',
        frameworks: 'Frameworks & Libraries',
        databases: 'Databases',
        tools: 'Tools & Technologies',
        cloud: 'Cloud & DevOps',
        soft_skills: 'Soft Skills',
        other: 'Other Skills'
    };

    return (
        <div className="max-w-[1240px] mx-auto animate-fade-in h-[calc(100vh-140px)] flex flex-col">
            {/* Summary Stats Bar */}
            <div className="flex flex-wrap items-center justify-center gap-4 mb-4 p-4 bg-white border border-[var(--color-neutral-200)] rounded-[12px] shadow-sm">
                <div className="flex items-center gap-2">
                    <Code className="w-5 h-5 text-[var(--color-primary-500)]" />
                    <span className="font-semibold text-[var(--color-neutral-900)]">{localResume.skills.length}</span>
                    <span className="text-sm text-[var(--color-neutral-500)]">skills</span>
                </div>
                <div className="hidden sm:block w-px h-6 bg-[var(--color-neutral-200)]" />
                <div className="flex items-center gap-2">
                    <Briefcase className="w-5 h-5 text-[var(--color-amber-500)]" />
                    <span className="font-semibold text-[var(--color-neutral-900)]">{localResume.experience.length}</span>
                    <span className="text-sm text-[var(--color-neutral-500)]">roles</span>
                </div>
                <div className="hidden sm:block w-px h-6 bg-[var(--color-neutral-200)]" />
                <div className="flex items-center gap-2">
                    <GraduationCap className="w-5 h-5 text-[var(--color-green-500)]" />
                    <span className="font-semibold text-[var(--color-neutral-900)]">{localResume.education.length}</span>
                    <span className="text-sm text-[var(--color-neutral-500)]">degrees</span>
                </div>
                <div className="hidden sm:block w-px h-6 bg-[var(--color-neutral-200)]" />
                <div className="flex items-center gap-2">
                    <FolderGit2 className="w-5 h-5 text-[var(--color-purple-500)]" />
                    <span className="font-semibold text-[var(--color-neutral-900)]">{localResume.projects.length}</span>
                    <span className="text-sm text-[var(--color-neutral-500)]">projects</span>
                </div>
            </div>

            {/* Parsing Warnings */}
            {localResume.parsing_warnings && localResume.parsing_warnings.length > 0 && (
                <div className="mb-4 p-4 bg-[var(--color-amber-50)] border border-[var(--color-amber-200)] rounded-[12px]">
                    <div className="flex items-start gap-3">
                        <AlertTriangle className="w-5 h-5 text-[var(--color-amber-600)] flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-[var(--color-amber-800)] mb-1">Parsing Notes</h4>
                            <ul className="text-sm text-[var(--color-amber-700)] space-y-1">
                                {localResume.parsing_warnings.map((warning, idx) => (
                                    <li key={idx}>• {warning}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            )}

            {/* Top Banner */}
            <div className="flex items-center justify-between mb-6 bg-[var(--color-primary-50)] border border-[var(--color-primary-100)] p-4 rounded-[12px]">
                <div className="flex items-center gap-3">
                    <CheckCircle2 className="w-5 h-5 text-[var(--color-primary-600)]" />
                    <p className="text-[var(--color-primary-800)] text-sm font-medium">
                        Review how we interpreted your resume. You can edit anything before analysis.
                    </p>
                </div>
                <button
                    onClick={handleRunAnalysis}
                    disabled={isSaving}
                    className="btn btn-primary h-10 px-6 shadow-sm flex items-center gap-2"
                >
                    {isSaving ? (
                        <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            Saving...
                        </>
                    ) : (
                        <>
                            Run Analysis
                            <ArrowRight className="w-4 h-4" />
                        </>
                    )}
                </button>
            </div>

            {/* Split Layout */}
            <div className="flex-1 grid grid-cols-1 md:grid-cols-12 gap-8 min-h-0">

                {/* Left Panel: Navigation */}
                <div className="md:col-span-3 lg:col-span-3 overflow-y-auto pr-2">
                    <h3 className="label-text mb-4 px-2">SECTIONS</h3>
                    <nav>
                        <SidebarItem id="personal" icon={User} label="Personal Info" />
                        <SidebarItem id="skills" icon={Code} label="Skills" count={localResume.skills.length} />
                        <SidebarItem id="experience" icon={Briefcase} label="Experience" count={localResume.experience.length} />
                        <SidebarItem id="education" icon={GraduationCap} label="Education" count={localResume.education.length} />
                        <SidebarItem id="projects" icon={FolderGit2} label="Projects" count={localResume.projects.length} />
                    </nav>
                </div>

                {/* Right Panel: Editor */}
                <div className="md:col-span-9 lg:col-span-9 bg-white border border-[var(--color-neutral-200)] rounded-[16px] shadow-sm overflow-hidden flex flex-col">
                    <div className="p-6 border-b border-[var(--color-neutral-100)] bg-[var(--color-neutral-50)] flex items-center justify-between">
                        <h2 className="h2 capitalize">{activeSection} Details</h2>
                        {(activeSection === 'experience' || activeSection === 'education' || activeSection === 'projects') && (
                            <button
                                onClick={activeSection === 'experience' ? addExperience : activeSection === 'education' ? addEducation : addProject}
                                className="btn btn-secondary flex items-center gap-2 text-sm"
                            >
                                <Plus className="w-4 h-4" />
                                Add {activeSection === 'experience' ? 'Role' : activeSection === 'education' ? 'Degree' : 'Project'}
                            </button>
                        )}
                    </div>

                    <div className="flex-1 overflow-y-auto p-6">
                        {/* Personal Info Editor */}
                        {activeSection === 'personal' && (
                            <div className="space-y-6 max-w-2xl">
                                <div>
                                    <label className="block text-sm font-medium text-[var(--color-neutral-700)] mb-1">Full Name</label>
                                    <input
                                        type="text"
                                        className="input"
                                        value={localResume.contact_info.name || ''}
                                        onChange={(e) => updateContactInfo('name', e.target.value)}
                                        placeholder="Enter your full name"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-[var(--color-neutral-700)] mb-1">Email</label>
                                    <input
                                        type="email"
                                        className="input"
                                        value={localResume.contact_info.email || ''}
                                        onChange={(e) => updateContactInfo('email', e.target.value)}
                                        placeholder="your@email.com"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-[var(--color-neutral-700)] mb-1">Phone</label>
                                    <input
                                        type="text"
                                        className="input"
                                        value={localResume.contact_info.phone || ''}
                                        onChange={(e) => updateContactInfo('phone', e.target.value)}
                                        placeholder="+1 (555) 123-4567"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-[var(--color-neutral-700)] mb-1">Location</label>
                                    <input
                                        type="text"
                                        className="input"
                                        value={localResume.contact_info.location || ''}
                                        onChange={(e) => updateContactInfo('location', e.target.value)}
                                        placeholder="City, State"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-[var(--color-neutral-700)] mb-1">LinkedIn</label>
                                    <input
                                        type="url"
                                        className="input"
                                        value={localResume.contact_info.linkedin || ''}
                                        onChange={(e) => updateContactInfo('linkedin', e.target.value)}
                                        placeholder="linkedin.com/in/yourprofile"
                                    />
                                </div>
                            </div>
                        )}

                        {/* Skills Editor */}
                        {activeSection === 'skills' && (
                            <div className="space-y-6">
                                {localResume.skills.length === 0 ? (
                                    <EmptyState
                                        icon={Code}
                                        title="No Skills Detected"
                                        description="We couldn't find any skills in your resume. Try uploading a different format or add skills manually."
                                        onAdd={() => {
                                            const newSkillName = prompt("Enter skill name:");
                                            if (newSkillName) {
                                                const newSkillObj: ExtractedSkill = {
                                                    name: newSkillName,
                                                    canonical_name: newSkillName,
                                                    category: 'other',
                                                    confidence: 'medium',
                                                    source_text: 'Manual Entry'
                                                };
                                                updateField('skills', [...localResume.skills, newSkillObj]);
                                            }
                                        }}
                                    />
                                ) : (
                                    <>
                                        <p className="text-sm text-[var(--color-neutral-500)] mb-4">
                                            Skills extracted from your resume, grouped by category. Click × to remove or + to add.
                                        </p>
                                        {Object.entries(skillGroups).map(([category, skills]) => (
                                            <div key={category} className="mb-6 pb-6 border-b border-[var(--color-neutral-100)] last:border-0">
                                                <div className="flex items-center justify-between mb-3">
                                                    <h4 className="font-semibold text-[var(--color-neutral-800)]">
                                                        {categoryLabels[category] || category}
                                                    </h4>
                                                    <span className="text-xs text-[var(--color-neutral-500)]">{skills.length} skills</span>
                                                </div>
                                                <div className="flex flex-wrap gap-2">
                                                    {skills.map((skill, idx) => (
                                                        <span key={`${skill.name}-${idx}`} className="inline-flex items-center px-3 py-1.5 rounded-full bg-white border border-[var(--color-neutral-200)] text-sm text-[var(--color-neutral-700)] hover:border-[var(--color-primary-300)] transition-colors">
                                                            <ConfidenceBadge level={skill.confidence} />
                                                            {skill.name}
                                                            <button
                                                                onClick={() => {
                                                                    const newSkills = localResume.skills.filter(s => s !== skill);
                                                                    updateField('skills', newSkills);
                                                                }}
                                                                className="ml-2 text-[var(--color-neutral-400)] hover:text-[var(--color-red-500)]"
                                                            >
                                                                ×
                                                            </button>
                                                        </span>
                                                    ))}
                                                    <button
                                                        className="px-3 py-1.5 rounded-full border border-dashed border-[var(--color-neutral-300)] text-sm text-[var(--color-neutral-500)] hover:border-[var(--color-primary-400)] hover:text-[var(--color-primary-600)] transition-colors"
                                                        onClick={() => {
                                                            const newSkillName = prompt("Add skill to " + (categoryLabels[category] || category));
                                                            if (newSkillName) {
                                                                const newSkillObj: ExtractedSkill = {
                                                                    name: newSkillName,
                                                                    canonical_name: newSkillName,
                                                                    category: category as SkillCategory,
                                                                    confidence: 'medium',
                                                                    source_text: 'Manual Entry'
                                                                };
                                                                updateField('skills', [...localResume.skills, newSkillObj]);
                                                            }
                                                        }}
                                                    >
                                                        + Add
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </>
                                )}
                            </div>
                        )}

                        {/* Experience Editor */}
                        {activeSection === 'experience' && (
                            <div className="space-y-6">
                                {localResume.experience.length === 0 ? (
                                    <EmptyState
                                        icon={Briefcase}
                                        title="No Experience Detected"
                                        description="We couldn't find work experience in your resume. Add your roles manually to improve your analysis."
                                        onAdd={addExperience}
                                    />
                                ) : (
                                    localResume.experience.map((exp, idx) => (
                                        <div key={idx} className="p-5 bg-[var(--color-neutral-50)] rounded-[12px] border border-[var(--color-neutral-200)] relative group">
                                            <button
                                                onClick={() => deleteExperience(idx)}
                                                className="absolute top-4 right-4 p-2 rounded-lg text-[var(--color-neutral-400)] hover:text-[var(--color-red-500)] hover:bg-[var(--color-red-50)] opacity-0 group-hover:opacity-100 transition-all"
                                                title="Delete entry"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Company</label>
                                                    <input
                                                        className="input mt-1"
                                                        value={exp.company}
                                                        onChange={(e) => {
                                                            const newExp = [...localResume.experience];
                                                            newExp[idx] = { ...exp, company: e.target.value };
                                                            updateField('experience', newExp);
                                                        }}
                                                    />
                                                </div>
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Title</label>
                                                    <input
                                                        className="input mt-1"
                                                        value={exp.title}
                                                        onChange={(e) => {
                                                            const newExp = [...localResume.experience];
                                                            newExp[idx] = { ...exp, title: e.target.value };
                                                            updateField('experience', newExp);
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase flex items-center gap-1">
                                                        <Calendar className="w-3 h-3" /> Start Date
                                                    </label>
                                                    <input
                                                        type="text"
                                                        className="input mt-1"
                                                        placeholder="e.g., Jan 2020"
                                                        value={exp.start_date || ''}
                                                        onChange={(e) => {
                                                            const newExp = [...localResume.experience];
                                                            newExp[idx] = { ...exp, start_date: e.target.value };
                                                            updateField('experience', newExp);
                                                        }}
                                                    />
                                                </div>
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase flex items-center gap-1">
                                                        <Calendar className="w-3 h-3" /> End Date
                                                    </label>
                                                    <input
                                                        type="text"
                                                        className="input mt-1"
                                                        placeholder="e.g., Present"
                                                        value={exp.end_date || ''}
                                                        onChange={(e) => {
                                                            const newExp = [...localResume.experience];
                                                            newExp[idx] = { ...exp, end_date: e.target.value };
                                                            updateField('experience', newExp);
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                            <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Description / Responsibilities</label>
                                            <textarea
                                                className="textarea mt-1 h-32"
                                                placeholder="Describe your key responsibilities and achievements..."
                                                value={exp.description}
                                                onChange={(e) => {
                                                    const newExp = [...localResume.experience];
                                                    newExp[idx] = { ...exp, description: e.target.value };
                                                    updateField('experience', newExp);
                                                }}
                                            />
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                        {/* Education Editor */}
                        {activeSection === 'education' && (
                            <div className="space-y-6">
                                {localResume.education.length === 0 ? (
                                    <EmptyState
                                        icon={GraduationCap}
                                        title="No Education Detected"
                                        description="We couldn't find education details in your resume. Add your qualifications manually."
                                        onAdd={addEducation}
                                    />
                                ) : (
                                    localResume.education.map((edu, idx) => (
                                        <div key={idx} className="p-5 bg-[var(--color-neutral-50)] rounded-[12px] border border-[var(--color-neutral-200)] relative group">
                                            <button
                                                onClick={() => deleteEducation(idx)}
                                                className="absolute top-4 right-4 p-2 rounded-lg text-[var(--color-neutral-400)] hover:text-[var(--color-red-500)] hover:bg-[var(--color-red-50)] opacity-0 group-hover:opacity-100 transition-all"
                                                title="Delete entry"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Institution</label>
                                                    <input
                                                        className="input mt-1"
                                                        value={edu.institution}
                                                        onChange={(e) => {
                                                            const newEdu = [...localResume.education];
                                                            newEdu[idx] = { ...edu, institution: e.target.value };
                                                            updateField('education', newEdu);
                                                        }}
                                                    />
                                                </div>
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Degree</label>
                                                    <input
                                                        className="input mt-1"
                                                        value={edu.degree}
                                                        onChange={(e) => {
                                                            const newEdu = [...localResume.education];
                                                            newEdu[idx] = { ...edu, degree: e.target.value };
                                                            updateField('education', newEdu);
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Field of Study</label>
                                                    <input
                                                        className="input mt-1"
                                                        placeholder="e.g., Computer Science"
                                                        value={edu.field_of_study || ''}
                                                        onChange={(e) => {
                                                            const newEdu = [...localResume.education];
                                                            newEdu[idx] = { ...edu, field_of_study: e.target.value };
                                                            updateField('education', newEdu);
                                                        }}
                                                    />
                                                </div>
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase flex items-center gap-1">
                                                        <Calendar className="w-3 h-3" /> Start Year
                                                    </label>
                                                    <input
                                                        type="text"
                                                        className="input mt-1"
                                                        placeholder="e.g., 2018"
                                                        value={edu.start_date || ''}
                                                        onChange={(e) => {
                                                            const newEdu = [...localResume.education];
                                                            newEdu[idx] = { ...edu, start_date: e.target.value };
                                                            updateField('education', newEdu);
                                                        }}
                                                    />
                                                </div>
                                                <div>
                                                    <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase flex items-center gap-1">
                                                        <Calendar className="w-3 h-3" /> End Year
                                                    </label>
                                                    <input
                                                        type="text"
                                                        className="input mt-1"
                                                        placeholder="e.g., 2022"
                                                        value={edu.end_date || ''}
                                                        onChange={(e) => {
                                                            const newEdu = [...localResume.education];
                                                            newEdu[idx] = { ...edu, end_date: e.target.value };
                                                            updateField('education', newEdu);
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                        {/* Projects Editor */}
                        {activeSection === 'projects' && (
                            <div className="space-y-6">
                                {localResume.projects.length === 0 ? (
                                    <EmptyState
                                        icon={FolderGit2}
                                        title="No Projects Detected"
                                        description="We couldn't find project details in your resume. Add your projects to showcase your work."
                                        onAdd={addProject}
                                    />
                                ) : (
                                    localResume.projects.map((proj, idx) => (
                                        <div key={idx} className="p-5 bg-[var(--color-neutral-50)] rounded-[12px] border border-[var(--color-neutral-200)] relative group">
                                            <button
                                                onClick={() => deleteProject(idx)}
                                                className="absolute top-4 right-4 p-2 rounded-lg text-[var(--color-neutral-400)] hover:text-[var(--color-red-500)] hover:bg-[var(--color-red-50)] opacity-0 group-hover:opacity-100 transition-all"
                                                title="Delete entry"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                            <div className="mb-4">
                                                <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Project Name</label>
                                                <input
                                                    className="input mt-1"
                                                    value={proj.name}
                                                    onChange={(e) => {
                                                        const newProj = [...localResume.projects];
                                                        newProj[idx] = { ...proj, name: e.target.value };
                                                        updateField('projects', newProj);
                                                    }}
                                                />
                                            </div>
                                            <div className="mb-4">
                                                <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Technologies Used</label>
                                                <input
                                                    className="input mt-1"
                                                    placeholder="e.g., React, Node.js, PostgreSQL"
                                                    value={proj.technologies?.join(', ') || ''}
                                                    onChange={(e) => {
                                                        const newProj = [...localResume.projects];
                                                        newProj[idx] = { ...proj, technologies: e.target.value.split(',').map(t => t.trim()).filter(Boolean) };
                                                        updateField('projects', newProj);
                                                    }}
                                                />
                                            </div>
                                            <label className="text-xs font-medium text-[var(--color-neutral-500)] uppercase">Description</label>
                                            <textarea
                                                className="textarea mt-1 h-32"
                                                placeholder="Describe what you built and the impact it had..."
                                                value={proj.description}
                                                onChange={(e) => {
                                                    const newProj = [...localResume.projects];
                                                    newProj[idx] = { ...proj, description: e.target.value };
                                                    updateField('projects', newProj);
                                                }}
                                            />
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                    </div>
                    {/* Unsaved Changes Indicator */}
                    {hasUnsavedChanges && (
                        <div className="p-3 bg-[var(--color-amber-50)] border-t border-[var(--color-amber-200)] text-[var(--color-amber-600)] text-sm flex items-center justify-center font-medium">
                            <AlertCircle className="w-4 h-4 mr-2" />
                            You have unsaved changes — they will be applied when you run analysis
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
