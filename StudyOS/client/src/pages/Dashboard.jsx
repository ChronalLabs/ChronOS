import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import RightPanel from '../components/RightPanel';
import { Search, Bell, Clock, CheckCircle2, TrendingUp, Zap, Menu, X, Filter } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState('');
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isRightPanelOpen, setIsRightPanelOpen] = useState(false);

    const handleFeatureClick = (feature) => {
        alert(`${feature} feature is coming soon!`);
    };

    return (
        <div className="min-h-screen bg-background flex font-sans text-text-main relative overflow-hidden">
            
            {/* Mobile Sidebar Overlay */}
            {isSidebarOpen && (
                <div 
                    onClick={() => setIsSidebarOpen(false)} 
                    className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm transition-opacity" 
                />
            )}

            {/* Sidebar Wrapper */}
            <div className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <Sidebar onMobileClose={() => setIsSidebarOpen(false)} />
            </div>

            {/* Main Content Area */}
            <main className="flex-1 md:ml-20 main-content right-panel-transition p-4 md:p-8 overflow-y-auto h-screen relative z-0">
                {/* Header */}
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                    
                    {/* Mobile Menu Button */}
                    <div className="flex items-center justify-between w-full md:hidden mb-4">
                         <button 
                            onClick={() => setIsSidebarOpen(true)}
                            className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50"
                        >
                            <Menu size={24} />
                        </button>
                        <div className="flex items-center gap-2">
                             <div className="w-8 h-8 bg-primary/20 rounded-lg flex items-center justify-center text-primary font-bold">S</div>
                             <span className="font-bold text-lg text-text-main">StudyOS</span>
                        </div>
                        <button 
                            onClick={() => setIsRightPanelOpen(true)}
                            className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50"
                        >
                            <Filter size={24} />
                        </button>
                    </div>

                    <div className="relative w-full md:w-96 group">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors" size={20} />
                        <input
                            type="text"
                            placeholder="Search tasks, notes..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-12 pr-4 py-3.5 bg-surface border border-transparent focus:bg-surface focus:border-primary/20 focus:ring-4 focus:ring-primary/5 rounded-2xl text-text-main shadow-card hover:shadow-soft transition-all outline-none placeholder:text-text-muted transition-all"
                        />
                    </div>

                    <div className="hidden md:flex items-center gap-8">
                        <button
                            onClick={() => handleFeatureClick('Notifications')}
                            className="relative p-3 bg-surface rounded-xl text-text-secondary hover:text-primary hover:bg-white/5 hover:shadow-soft transition-all duration-200 border border-transparent hover:border-border/50"
                        >
                            <Bell size={22} />
                            <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-surface"></span>
                        </button>
                        
                        <div className="flex items-center gap-4 pl-8 border-l border-border/60">
                            <div className="text-right hidden lg:block">
                                <p className="text-sm font-bold text-text-main tracking-tight">{user?.username || 'Arin GUPTA'}</p>
                                <p className="text-xs text-text-secondary font-medium">Level 1 Scholar</p>
                            </div>
                            <div className="w-12 h-12 bg-primary/10 rounded-2xl flex items-center justify-center text-primary font-bold text-lg shadow-inner cursor-pointer hover:scale-105 transition-transform">
                                {user?.username ? user.username[0].toUpperCase() : 'A'}
                            </div>
                        </div>
                    </div>
                </header>

                {/* Welcome Banner */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-10 bg-primary/10 rounded-3xl p-8 shadow-card border border-primary/20 relative overflow-hidden flex flex-col md:flex-row items-center justify-between group hover:shadow-float transition-all duration-500"
                >
                    <div className="relative z-10 max-w-xl">
                        <h1 className="text-3xl font-bold text-text-main mb-3 tracking-tight">
                            Hi {user?.username || 'Arin'}, <span className="text-text-secondary font-normal">ready to focus?</span>
                        </h1>
                        <p className="text-text-secondary leading-relaxed mb-8 text-lg">
                            You have <span className="font-bold text-primary">4 tasks</span> pending for today. Your productivity score is looking great!
                        </p>
                        <div className="flex gap-4">
                             <button
                                onClick={() => navigate('/focus')}
                                className="btn-primary"
                            >
                                Start Session
                            </button>
                             <button
                                className="bg-surface text-text-main border border-border px-8 py-3.5 rounded-2xl font-semibold shadow-soft hover:shadow-card transition-all duration-200"
                             >
                                View Calendar
                             </button>
                        </div>
                       
                    </div>
                    
                    {/* Decorative Abstract Shapes */}
                    <div className="absolute right-0 top-0 h-full w-1/3 opacity-50 pointer-events-none">
                        <div className="absolute top-10 right-10 w-32 h-32 bg-primary rounded-full blur-3xl animate-pulse"></div>
                    </div>
                </motion.div>

                {/* Stats Grid */}
                <div className="flex items-center gap-3 mb-6">
                     <TrendingUp size={20} className="text-primary" />
                     <h3 className="text-lg font-bold text-text-main">Overview</h3>
                </div>
               
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                    {[
                        { label: 'Study Hours', value: '42.5h', icon: Clock, color: 'text-blue-500', bg: 'bg-blue-100', trend: '+12%' },
                        { label: 'Tasks Done', value: '18', icon: CheckCircle2, color: 'text-primary', bg: 'bg-primary-light', trend: '+5%' },
                        { label: 'Current Streak', value: '7 Days', icon: Zap, color: 'text-amber-500', bg: 'bg-amber-100', trend: 'Map' },
                        { label: 'Focus Score', value: '85', icon: TrendingUp, color: 'text-purple-500', bg: 'bg-purple-100', trend: '+2' },
                    ].map((stat, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            onClick={() => handleFeatureClick(stat.label)}
                            className="card cursor-pointer group"
                        >
                            <div className="flex justify-between items-start mb-4">
                                <div className={`p-3 rounded-xl ${stat.bg} ${stat.color} shadow-inner group-hover:scale-110 transition-transform duration-300`}>
                                    <stat.icon size={24} strokeWidth={2.5} />
                                </div>
                                <span className={`text-xs font-bold px-2.5 py-1 rounded-lg shadow-inner ${stat.trend === 'Map' ? 'text-amber-500 bg-amber-100' : 'text-primary bg-primary-light'}`}>
                                    {stat.trend}
                                </span>
                            </div>
                            <h4 className="text-2xl font-bold text-text-main mb-1 tracking-tight">{stat.value}</h4>
                            <p className="text-sm text-text-secondary font-medium">{stat.label}</p>
                        </motion.div>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 space-y-8">
                        <div>
                            <div className="flex justify-between items-center mb-6">
                                <h3 className="text-lg font-bold text-text-main">Today's Focus</h3>
                                <button
                                    onClick={() => navigate('/subjects')}
                                    className="text-sm font-semibold text-primary hover:text-primary-dark hover:underline bg-primary/5 px-4 py-2 rounded-lg transition-colors"
                                >
                                    View All
                                </button>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                {['Advanced Mathematics', 'Physics - Quantum Mechanics'].map((subject, i) => (
                                    <motion.div
                                        key={i}
                                        whileHover={{ y: -5 }}
                                        onClick={() => navigate('/subjects')}
                                        className="card group cursor-pointer"
                                    >
                                        <div className="w-10 h-10 rounded-xl bg-background shadow-inner flex items-center justify-center text-primary mb-4 group-hover:bg-primary group-hover:text-white transition-colors">
                                            {i === 0 ? '📐' : '⚛️'}
                                        </div>
                                        <h4 className="font-bold text-text-main mb-2">{subject}</h4>
                                        <p className="text-xs text-text-secondary mb-4">Chapter 4 • 2 Tasks Pending</p>
                                        <div className="w-full bg-background shadow-inner rounded-full h-1.5">
                                            <div className="bg-primary h-1.5 rounded-full" style={{ width: i === 0 ? '60%' : '30%' }}></div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="space-y-8">
                        <div className="card text-text-main relative overflow-hidden group">
                            <div className="relative z-10">
                                <h3 className="text-lg font-bold mb-1">Upcoming Quiz</h3>
                                <p className="text-sm text-text-secondary mb-6">Physics: Wave Motion</p>
                                <div className="flex justify-between items-end">
                                    <div className="flex -space-x-3">
                                        {[1, 2, 3].map(i => (
                                            <div key={i} className="w-8 h-8 rounded-full bg-background shadow-inner border-2 border-surface flex items-center justify-center text-xs">P{i}</div>
                                        ))}
                                    </div>
                                    <button
                                        onClick={() => handleFeatureClick('Quiz Prep')}
                                className="bg-white text-primary px-4 py-2 rounded-lg text-xs font-bold hover:bg-gray-100 transition-colors"
                            >
                                Prepare
                            </button>
                        </div>
                    </div>
                    <div className="absolute right-0 bottom-0 w-32 h-32 bg-primary-light rounded-full blur-3xl opacity-20 group-hover:opacity-40 transition-opacity"></div>
                </div>

                        <div
                            onClick={() => handleFeatureClick('Weekly Analytics')}
                            className="card cursor-pointer"
                        >
                            <h3 className="font-bold text-text-main mb-4">Weekly Activity</h3>
                            <div className="h-32 flex items-end justify-between px-2">
                                {[40, 70, 50, 90, 60, 80].map((h, i) => (
                                    <div key={i} className="w-2 bg-background shadow-inner rounded-t-sm relative group cursor-pointer">
                                        <div className="absolute bottom-0 w-full bg-primary rounded-t-sm transition-all duration-500 group-hover:bg-primary-dark" style={{ height: `${h}%` }}></div>
                                        <div className="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 -translate-x-1/2 bg-surface text-text-main text-[10px] px-2 py-1 rounded shadow-soft transition-opacity pointer-events-none">
                                            {h}%
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Mobile RightPanel Overlay */}
            {isRightPanelOpen && (
                <div 
                    onClick={() => setIsRightPanelOpen(false)} 
                    className="fixed inset-0 bg-black/60 z-40 xl:hidden backdrop-blur-sm transition-opacity" 
                />
            )}

            {/* Right Panel Wrapper */}
            <div className={`fixed inset-y-0 right-0 z-50 transform transition-transform duration-300 ease-in-out xl:relative xl:transform-none xl:translate-x-0 ${isRightPanelOpen ? 'translate-x-0' : 'translate-x-full'}`}>
                <RightPanel />
            </div>
        </div>
    );
};

export default Dashboard;


