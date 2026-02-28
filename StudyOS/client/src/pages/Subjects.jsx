import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import RightPanel from '../components/RightPanel';
import { Search, Bell, Plus, BookOpen, Clock, CheckCircle, BarChart3, ChevronRight, Filter, SortAsc } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const Subjects = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState('');
    const [activeFilter, setActiveFilter] = useState('all');
    const [selectedSubject, setSelectedSubject] = useState(null);

    const handleFeatureClick = (feature) => {
        alert(`${feature} feature is coming soon!`);
    };

    // ── Mock Subject Data ────────────────────────────────────────────
    const subjects = [
        {
            id: 1,
            name: 'Advanced Mathematics',
            icon: '📐',
            color: 'from-indigo-500 to-purple-500',
            bgLight: 'bg-indigo-500/10',
            textColor: 'text-indigo-400',
            borderColor: 'border-indigo-500/20',
            progress: 60,
            totalChapters: 12,
            completedChapters: 7,
            totalTasks: 24,
            completedTasks: 14,
            studyHours: 18.5,
            lastStudied: '2 hours ago',
            status: 'in-progress',
            chapters: [
                { name: 'Linear Algebra', progress: 100, tasks: 3, completed: 3 },
                { name: 'Calculus I', progress: 100, tasks: 2, completed: 2 },
                { name: 'Calculus II', progress: 80, tasks: 3, completed: 2 },
                { name: 'Differential Equations', progress: 45, tasks: 4, completed: 2 },
                { name: 'Probability & Statistics', progress: 20, tasks: 3, completed: 1 },
                { name: 'Number Theory', progress: 0, tasks: 2, completed: 0 },
            ],
        },
        {
            id: 2,
            name: 'Physics - Quantum Mechanics',
            icon: '⚛️',
            color: 'from-cyan-500 to-blue-500',
            bgLight: 'bg-cyan-500/10',
            textColor: 'text-cyan-400',
            borderColor: 'border-cyan-500/20',
            progress: 30,
            totalChapters: 10,
            completedChapters: 3,
            totalTasks: 20,
            completedTasks: 6,
            studyHours: 12.0,
            lastStudied: '1 day ago',
            status: 'in-progress',
            chapters: [
                { name: 'Wave-Particle Duality', progress: 100, tasks: 2, completed: 2 },
                { name: 'Schrödinger Equation', progress: 100, tasks: 3, completed: 3 },
                { name: 'Quantum States', progress: 60, tasks: 3, completed: 1 },
                { name: 'Wave Motion', progress: 10, tasks: 4, completed: 0 },
                { name: 'Quantum Entanglement', progress: 0, tasks: 2, completed: 0 },
            ],
        },
        {
            id: 3,
            name: 'Organic Chemistry',
            icon: '🧪',
            color: 'from-emerald-500 to-green-500',
            bgLight: 'bg-emerald-500/10',
            textColor: 'text-emerald-400',
            borderColor: 'border-emerald-500/20',
            progress: 15,
            totalChapters: 14,
            completedChapters: 2,
            totalTasks: 28,
            completedTasks: 4,
            studyHours: 8.0,
            lastStudied: '3 days ago',
            status: 'needs-attention',
            chapters: [
                { name: 'Hydrocarbons', progress: 100, tasks: 2, completed: 2 },
                { name: 'Functional Groups', progress: 50, tasks: 3, completed: 2 },
                { name: 'Stereochemistry', progress: 10, tasks: 3, completed: 0 },
                { name: 'Reaction Mechanisms', progress: 0, tasks: 4, completed: 0 },
            ],
        },
        {
            id: 4,
            name: 'Data Structures & Algorithms',
            icon: '💻',
            color: 'from-orange-500 to-amber-500',
            bgLight: 'bg-orange-500/10',
            textColor: 'text-orange-400',
            borderColor: 'border-orange-500/20',
            progress: 85,
            totalChapters: 8,
            completedChapters: 7,
            totalTasks: 16,
            completedTasks: 14,
            studyHours: 32.0,
            lastStudied: '5 hours ago',
            status: 'almost-done',
            chapters: [
                { name: 'Arrays & Strings', progress: 100, tasks: 2, completed: 2 },
                { name: 'Linked Lists', progress: 100, tasks: 2, completed: 2 },
                { name: 'Trees & Graphs', progress: 100, tasks: 3, completed: 3 },
                { name: 'Dynamic Programming', progress: 80, tasks: 3, completed: 2 },
                { name: 'Sorting & Searching', progress: 100, tasks: 2, completed: 2 },
                { name: 'Advanced Graphs', progress: 40, tasks: 2, completed: 1 },
            ],
        },
        {
            id: 5,
            name: 'English Literature',
            icon: '📚',
            color: 'from-rose-500 to-pink-500',
            bgLight: 'bg-rose-500/10',
            textColor: 'text-rose-400',
            borderColor: 'border-rose-500/20',
            progress: 100,
            totalChapters: 6,
            completedChapters: 6,
            totalTasks: 12,
            completedTasks: 12,
            studyHours: 15.0,
            lastStudied: '1 week ago',
            status: 'completed',
            chapters: [
                { name: 'Shakespeare', progress: 100, tasks: 2, completed: 2 },
                { name: 'Romantic Poetry', progress: 100, tasks: 2, completed: 2 },
                { name: 'Modern Fiction', progress: 100, tasks: 3, completed: 3 },
                { name: 'Literary Criticism', progress: 100, tasks: 2, completed: 2 },
            ],
        },
        {
            id: 6,
            name: 'Calculus III',
            icon: '📊',
            color: 'from-violet-500 to-fuchsia-500',
            bgLight: 'bg-violet-500/10',
            textColor: 'text-violet-400',
            borderColor: 'border-violet-500/20',
            progress: 10,
            totalChapters: 10,
            completedChapters: 1,
            totalTasks: 20,
            completedTasks: 2,
            studyHours: 4.5,
            lastStudied: '5 days ago',
            status: 'needs-attention',
            chapters: [
                { name: 'Vectors in Space', progress: 100, tasks: 2, completed: 2 },
                { name: 'Partial Derivatives', progress: 15, tasks: 3, completed: 0 },
                { name: 'Multiple Integrals', progress: 0, tasks: 3, completed: 0 },
                { name: 'Vector Calculus', progress: 0, tasks: 4, completed: 0 },
            ],
        },
    ];

    const filters = [
        { key: 'all', label: 'All Subjects' },
        { key: 'in-progress', label: 'In Progress' },
        { key: 'needs-attention', label: 'Needs Attention' },
        { key: 'almost-done', label: 'Almost Done' },
        { key: 'completed', label: 'Completed' },
    ];

    const filteredSubjects = subjects.filter((s) => {
        const matchesSearch = s.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesFilter = activeFilter === 'all' || s.status === activeFilter;
        return matchesSearch && matchesFilter;
    });

    const getStatusBadge = (status) => {
        const styles = {
            'in-progress': { bg: 'bg-blue-500/10', text: 'text-blue-400', label: 'In Progress' },
            'needs-attention': { bg: 'bg-amber-500/10', text: 'text-amber-400', label: 'Needs Attention' },
            'almost-done': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: 'Almost Done' },
            'completed': { bg: 'bg-green-500/10', text: 'text-green-400', label: 'Completed' },
        };
        return styles[status] || styles['in-progress'];
    };

    // ── Summary Stats ────────────────────────────────────────────────
    const totalSubjects = subjects.length;
    const totalStudyHours = subjects.reduce((acc, s) => acc + s.studyHours, 0);
    const avgProgress = Math.round(subjects.reduce((acc, s) => acc + s.progress, 0) / totalSubjects);
    const completedSubjects = subjects.filter(s => s.status === 'completed').length;

    return (
        <div className="min-h-screen bg-background flex font-sans text-text-main relative overflow-hidden">
            <Sidebar />

            <main className="flex-1 md:ml-20 main-content right-panel-transition p-8 overflow-y-auto">
                {/* Header */}
                <header className="flex justify-between items-center mb-10">
                    <div className="relative w-96">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-secondary" size={20} />
                        <input
                            type="text"
                            placeholder="Search subjects..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="input-field pl-12"
                        />
                    </div>

                    <div className="flex items-center gap-6">
                        <button
                            onClick={() => handleFeatureClick('Notifications')}
                            className="relative p-2 text-text-secondary hover:text-primary transition-colors hover:bg-surface-hover rounded-xl shadow-inner border border-transparent hover:border-border/50"
                        >
                            <Bell size={24} />
                            <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-surface"></span>
                        </button>
                        <div className="flex items-center gap-3 pl-6 border-l border-border/50">
                            <div className="text-right hidden md:block">
                                <p className="text-sm font-bold text-text-main">{user?.username || 'Arin GUPTA'}</p>
                                <p className="text-xs text-text-secondary">Level 1 Scholar</p>
                            </div>
                            <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary font-bold cursor-pointer hover:bg-primary/20 transition-all">
                                {user?.username ? user.username[0].toUpperCase() : 'A'}
                            </div>
                        </div>
                    </div>
                </header>

                {/* Page Title & Add Button */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-2xl font-bold text-text-main">My Subjects</h1>
                        <p className="text-sm text-text-secondary mt-1">Track your progress across all subjects</p>
                    </div>
                    <button
                        onClick={() => handleFeatureClick('Add Subject')}
                        className="flex items-center gap-2 btn-primary"
                    >
                        <Plus size={18} />
                        Add Subject
                    </button>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    {[
                        { label: 'Total Subjects', value: totalSubjects, icon: '📚', trend: `${completedSubjects} done` },
                        { label: 'Study Hours', value: `${totalStudyHours.toFixed(1)}h`, icon: '⏱️', trend: 'This semester' },
                        { label: 'Avg Progress', value: `${avgProgress}%`, icon: '📈', trend: 'Across all' },
                        { label: 'Completed', value: completedSubjects, icon: '✅', trend: `of ${totalSubjects}` },
                    ].map((stat, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            className="card"
                        >
                            <div className="flex justify-between items-start mb-4">
                                <span className="text-2xl group-hover:scale-110 transition-transform duration-200">{stat.icon}</span>
                                <span className="text-xs font-bold text-text-secondary bg-surface-hover px-2 py-1 rounded-md shadow-inner">{stat.trend}</span>
                            </div>
                            <h4 className="text-2xl font-bold text-text-main mb-1">{stat.value}</h4>
                            <p className="text-xs text-text-secondary font-medium">{stat.label}</p>
                        </motion.div>
                    ))}
                </div>

                {/* Filters */}
                <div className="flex items-center gap-3 mb-6 overflow-x-auto pb-1">
                    {filters.map((filter) => (
                        <button
                            key={filter.key}
                            onClick={() => setActiveFilter(filter.key)}
                            className={`px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all duration-200 ${activeFilter === filter.key
                                ? 'bg-primary text-white shadow-glow border-none'
                                : 'bg-surface text-text-secondary shadow-soft hover:shadow-card hover:text-primary border border-transparent'
                                }`}
                        >
                            {filter.label}
                        </button>
                    ))}
                </div>

                {/* Subject Cards Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    <AnimatePresence mode="popLayout">
                        {filteredSubjects.map((subject, i) => {
                            const badge = getStatusBadge(subject.status);
                            return (
                                <motion.div
                                    key={subject.id}
                                    layout
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    transition={{ delay: i * 0.05 }}
                                    whileHover={{ y: -4 }}
                                    onClick={() => setSelectedSubject(selectedSubject?.id === subject.id ? null : subject)}
                                    className={`card p-6 cursor-pointer transition-all duration-300 ${selectedSubject?.id === subject.id
                                        ? 'shadow-inner border-transparent'
                                        : 'hover:shadow-float border-transparent'
                                        }`}
                                >
                                    {/* Card Header */}
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="flex items-center gap-3">
                                            <div className={`w-12 h-12 rounded-xl ${subject.bgLight} flex items-center justify-center text-xl`}>
                                                {subject.icon}
                                            </div>
                                            <div>
                                                <h3 className="font-bold text-text-main text-sm">{subject.name}</h3>
                                                <p className="text-xs text-text-secondary mt-0.5">
                                                    {subject.completedChapters}/{subject.totalChapters} chapters
                                                </p>
                                            </div>
                                        </div>
                                        <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${badge.bg} ${badge.text}`}>
                                            {badge.label}
                                        </span>
                                    </div>

                                    {/* Progress Bar */}
                                    <div className="mb-4">
                                        <div className="flex justify-between items-center mb-1.5">
                                            <span className="text-xs text-text-secondary font-medium">Progress</span>
                                            <span className="text-xs font-bold text-text-main">{subject.progress}%</span>
                                        </div>
                                        <div className="w-full bg-background rounded-full h-2 shadow-inner">
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${subject.progress}%` }}
                                                transition={{ duration: 0.8, delay: i * 0.1 }}
                                                className={`h-2 rounded-full bg-linear-to-r ${subject.color}`}
                                            />
                                        </div>
                                    </div>

                                    {/* Stats Row */}
                                    <div className="flex items-center gap-4 text-xs text-text-secondary">
                                        <div className="flex items-center gap-1.5">
                                            <CheckCircle size={13} className={subject.textColor} />
                                            <span>{subject.completedTasks}/{subject.totalTasks} tasks</span>
                                        </div>
                                        <div className="flex items-center gap-1.5">
                                            <Clock size={13} className={subject.textColor} />
                                            <span>{subject.studyHours}h studied</span>
                                        </div>
                                        <div className="flex items-center gap-1.5 ml-auto">
                                            <span className="text-text-secondary">{subject.lastStudied}</span>
                                        </div>
                                    </div>

                                    {/* Expanded Chapter View */}
                                    <AnimatePresence>
                                        {selectedSubject?.id === subject.id && (
                                            <motion.div
                                                initial={{ height: 0, opacity: 0 }}
                                                animate={{ height: 'auto', opacity: 1 }}
                                                exit={{ height: 0, opacity: 0 }}
                                                transition={{ duration: 0.3 }}
                                                className="overflow-hidden"
                                            >
                                                <div className="mt-5 pt-5 border-t border-border space-y-3">
                                                    <h4 className="text-xs font-bold text-text-secondary uppercase tracking-wider">Chapters</h4>
                                                    {subject.chapters.map((ch, ci) => (
                                                        <div
                                                            key={ci}
                                                            className="flex items-center gap-3 p-3 rounded-xl bg-background shadow-inner hover:bg-surface-hover transition-colors group/ch"
                                                        >
                                                            <div className={`w-8 h-8 rounded-lg ${ch.progress === 100 ? 'bg-green-500/20' : subject.bgLight} flex items-center justify-center shrink-0`}>
                                                                {ch.progress === 100 ? (
                                                                    <CheckCircle size={14} className="text-green-400" />
                                                                ) : (
                                                                    <BookOpen size={14} className={subject.textColor} />
                                                                )}
                                                            </div>
                                                            <div className="flex-1 min-w-0">
                                                                <div className="flex items-center justify-between mb-1">
                                                                    <span className="text-xs font-semibold text-text-main truncate">{ch.name}</span>
                                                                    <span className="text-[11px] font-bold text-text-secondary ml-2">{ch.progress}%</span>
                                                                </div>
                                                                <div className="w-full bg-background rounded-full h-1 shadow-inner">
                                                                    <div
                                                                        className={`h-1 rounded-full transition-all ${ch.progress === 100 ? 'bg-green-400' : 'bg-primary'}`}
                                                                        style={{ width: `${ch.progress}%` }}
                                                                    />
                                                                </div>
                                                            </div>
                                                            <span className="text-[10px] text-text-secondary whitespace-nowrap">
                                                                {ch.completed}/{ch.tasks} tasks
                                                            </span>
                                                            <ChevronRight size={14} className="text-text-muted group-hover/ch:text-primary transition-colors shrink-0" />
                                                        </div>
                                                    ))}
                                                    <button
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            handleFeatureClick(`Study ${subject.name}`);
                                                        }}
                                                        className="w-full mt-2 py-2.5 rounded-xl bg-primary/10 text-primary text-sm font-bold hover:bg-primary/20 transition-colors"
                                                    >
                                                        Continue Studying
                                                    </button>
                                                </div>
                                            </motion.div>
                                        )}
                                    </AnimatePresence>
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>
                </div>

                {/* Empty State */}
                {filteredSubjects.length === 0 && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-center py-16"
                    >
                        <div className="text-5xl mb-4">📭</div>
                        <h3 className="text-lg font-bold text-text-main mb-2">No subjects found</h3>
                        <p className="text-sm text-text-secondary">Try adjusting your search or filters</p>
                    </motion.div>
                )}
            </main>
        </div>
    );
};

export default Subjects;

