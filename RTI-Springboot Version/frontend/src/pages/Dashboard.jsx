import React from 'react';
import Button from '../components/Button';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const drafts = [
        { id: 101, subject: 'Scholarship Delay 2023', dept: 'Social Welfare', date: '2 days ago', status: 'Draft', progress: 40 },
        { id: 102, subject: 'Road Repair Complaint', dept: 'Municipal Corp', date: '1 week ago', status: 'Completed', progress: 100 },
    ];

    const submitted = [
        { id: 201, subject: 'University Answer Sheet', dept: 'Delhi University', filedDate: 'Jan 15, 2026', rtiNumber: 'DU/RTI/2026/889', status: 'Pending Reply', daysElapsed: 16 }
    ];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
                <div>
                    <h1 className="font-serif font-bold text-3xl text-indigo-deep">My Dashboard</h1>
                    <p className="text-gray-600">Track your RTI applications and drafts.</p>
                </div>
                <Button variant="primary" className="py-2.5 px-6 shadow-lg" to="/generate">
                    + New RTI Application
                </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Stats & Drafts */}
                <div className="lg:col-span-2 space-y-8">

                    {/* Section: Saved Drafts */}
                    <div className="bg-white rounded-xl shadow-paper border border-gray-100 p-6">
                        <h2 className="font-serif font-bold text-xl text-gray-800 mb-6 flex items-center gap-2">
                            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                            Saved Drafts
                        </h2>

                        <div className="space-y-4">
                            {drafts.map(draft => (
                                <div key={draft.id} className="flex flex-col sm:flex-row items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100 hover:border-indigo-100 transition-colors">
                                    <div className="flex-1 w-full sm:w-auto mb-4 sm:mb-0">
                                        <h3 className="font-bold text-indigo-deep text-lg">{draft.subject}</h3>
                                        <div className="flex items-center gap-3 text-sm text-gray-500 mt-1">
                                            <span>{draft.dept}</span>
                                            <span className="w-1 h-1 bg-gray-300 rounded-full"></span>
                                            <span>Edited {draft.date}</span>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-4 w-full sm:w-auto justify-end">
                                        <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                                            <div className="h-full bg-saffron" style={{ width: `${draft.progress}%` }}></div>
                                        </div>
                                        <Button variant="secondary" className="py-1.5 px-4 text-xs font-semibold" to="/generate">
                                            Resume
                                        </Button>
                                    </div>
                                </div>
                            ))}

                            {drafts.length === 0 && (
                                <p className="text-gray-400 italic text-center py-4">No drafts found.</p>
                            )}
                        </div>
                    </div>

                    {/* Section: Submitted / Tracking */}
                    <div className="bg-white rounded-xl shadow-paper border border-gray-100 p-6">
                        <h2 className="font-serif font-bold text-xl text-gray-800 mb-6 flex items-center gap-2">
                            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            Active Applications
                        </h2>

                        <div className="space-y-4">
                            {submitted.map(app => (
                                <div key={app.id} className="border border-gray-200 rounded-lg p-5 hover:shadow-sm transition-shadow">
                                    <div className="flex justify-between items-start mb-4">
                                        <div>
                                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wide">Pending Reply</span>
                                            <h3 className="font-bold text-lg text-indigo-deep mt-1">{app.subject}</h3>
                                            <p className="text-sm text-gray-500">{app.dept} • Ref: {app.rtiNumber}</p>
                                        </div>
                                        <div className="text-center bg-orange-50 px-3 py-2 rounded-lg border border-orange-100">
                                            <span className="block text-xl font-bold text-orange-600">{app.daysElapsed}</span>
                                            <span className="text-[10px] text-orange-400 font-bold uppercase">Days Elapsed</span>
                                        </div>
                                    </div>

                                    {/* Timeline */}
                                    <div className="relative pt-4">
                                        <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 mt-[1.2rem] -z-10"></div>
                                        <div className="flex justify-between text-xs font-medium text-gray-400">
                                            <div className="flex flex-col items-center gap-1 text-indigo-600">
                                                <div className="w-3 h-3 bg-indigo-600 rounded-full ring-4 ring-white"></div>
                                                <span>Filed</span>
                                            </div>
                                            <div className="flex flex-col items-center gap-1 text-orange-500">
                                                <div className="w-3 h-3 bg-orange-500 rounded-full ring-4 ring-white animate-pulse"></div>
                                                <span>Waiting (30 days)</span>
                                            </div>
                                            <div className="flex flex-col items-center gap-1 opacity-50">
                                                <div className="w-3 h-3 bg-gray-300 rounded-full ring-4 ring-white"></div>
                                                <span>First Appeal</span>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="mt-6 flex gap-3">
                                        <Button variant="outline" className="py-2 px-4 text-xs w-full sm:w-auto">View Details</Button>
                                        <Button variant="ghost" className="py-2 px-4 text-xs w-full sm:w-auto">Download Receipt</Button>
                                    </div>
                                </div>
                            ))}

                            {submitted.length === 0 && (
                                <div className="p-8 text-center bg-gray-50 rounded-lg border border-dashed border-gray-200">
                                    <p className="text-gray-500 mb-2">You haven't submitted any RTIs yet.</p>
                                    <p className="text-sm text-gray-400">Once filed, track their status here.</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Column: System Status & User Profile */}
                <div className="space-y-8">
                    <div className="bg-indigo-deep text-white rounded-xl shadow-lg p-6 relative overflow-hidden">
                        <div className="absolute -right-6 -top-6 w-32 h-32 bg-indigo-500/20 rounded-full blur-2xl"></div>
                        <div className="relative z-10">
                            <h3 className="font-serif font-bold text-lg mb-4">System Status</h3>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between p-3 bg-indigo-900/50 rounded-lg border border-indigo-800">
                                    <span className="text-sm text-indigo-200 flex items-center gap-2">
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" /></svg>
                                        API Backend
                                    </span>
                                    <span className="px-2 py-0.5 bg-green-900/50 text-green-400 text-xs font-bold rounded flex items-center gap-1">
                                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span> Online
                                    </span>
                                </div>
                                <div className="flex items-center justify-between p-3 bg-indigo-900/50 rounded-lg border border-indigo-800">
                                    <span className="text-sm text-indigo-200 flex items-center gap-2">
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                                        Validation Engine
                                    </span>
                                    <span className="px-2 py-0.5 bg-green-900/50 text-green-400 text-xs font-bold rounded flex items-center gap-1">
                                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span> Active
                                    </span>
                                </div>
                            </div>
                            <div className="mt-6 pt-4 border-t border-indigo-800 text-xs text-indigo-400 text-center">
                                Powered by Spring Boot
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-paper border border-gray-100 p-6">
                        <h3 className="font-serif font-bold text-lg text-gray-800 mb-4">Quick Actions</h3>
                        <div className="space-y-2">
                            <button className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700 flex items-center gap-3 transition-colors">
                                <span className="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
                                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                                </span>
                                Edit Profile
                            </button>
                            <button className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700 flex items-center gap-3 transition-colors">
                                <span className="w-8 h-8 rounded-full bg-purple-50 flex items-center justify-center text-purple-600">
                                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                                </span>
                                Settings
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
