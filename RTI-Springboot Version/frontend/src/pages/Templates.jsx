import React, { useState } from 'react';
import Button from '../components/Button';
import { Link } from 'react-router-dom';

const templatesData = [
    { id: 1, title: 'Delayed Scholarship', category: 'Education', uses: 1200, dept: 'Social Welfare' },
    { id: 2, title: 'Road Repair Status', category: 'Municipal', uses: 850, dept: 'PWD' },
    { id: 3, title: 'FIR Not Registered', category: 'Police', uses: 2300, dept: 'Police Station' },
    { id: 4, title: 'Exam Answer Sheet Copy', category: 'Education', uses: 5000, dept: 'University' },
    { id: 5, title: 'Pending Ration Card', category: 'Civil Supplies', uses: 1500, dept: 'Food & Supply' },
    { id: 6, title: 'Pension Disbursement', category: 'Welfare', uses: 900, dept: 'Social Welfare' },
];

const categories = ['All', 'Education', 'Police', 'Municipal', 'Welfare', 'Civil Supplies'];

const Templates = () => {
    const [activeCategory, setActiveCategory] = useState('All');
    const [search, setSearch] = useState('');

    const filteredTemplates = templatesData.filter(t =>
        (activeCategory === 'All' || t.category === activeCategory) &&
        t.title.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="min-h-screen bg-gradient-to-b from-stone-50 to-white py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                {/* Hero Section */}
                <div className="text-center mb-16 relative">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-orange-400 to-amber-600 rounded-full opacity-20 blur-sm"></div>
                    <h1 className="font-serif font-bold text-5xl text-indigo-deep mb-6 tracking-tight">
                        RTI Templates <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-800 to-indigo-600">Library</span>
                    </h1>
                    <p className="text-lg text-gray-500 max-w-2xl mx-auto leading-relaxed">
                        Don't know where to start? Choose a pre-drafted template vetted by experts to ensure your application gets results.
                    </p>
                </div>

                {/* Filters & Search */}
                <div className="flex flex-col lg:flex-row justify-between items-center gap-8 mb-14 bg-white/80 backdrop-blur-sm p-4 rounded-2xl border border-gray-100 shadow-sm sticky top-4 z-20">
                    <div className="flex flex-wrap gap-2 justify-center">
                        {categories.map(cat => (
                            <button
                                key={cat}
                                onClick={() => setActiveCategory(cat)}
                                className={`px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${activeCategory === cat
                                    ? 'bg-indigo-deep text-white shadow-lg shadow-indigo-900/20 transform scale-105'
                                    : 'bg-transparent text-gray-500 hover:bg-gray-50 hover:text-indigo-600'
                                    }`}
                            >
                                {cat}
                            </button>
                        ))}
                    </div>

                    <div className="relative w-full lg:w-80 group">
                        <input
                            type="text"
                            placeholder="Search templates..."
                            className="w-full pl-11 pr-4 py-3 bg-gray-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-100 focus:border-indigo-200 outline-none transition-all duration-300 group-hover:bg-white group-hover:border-gray-200"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                        <svg className="w-5 h-5 text-gray-400 absolute left-4 top-3.5 transition-colors group-hover:text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                </div>

                {/* Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-12">
                    {filteredTemplates.map(template => (
                        <div key={template.id} className="group relative bg-white rounded-2xl p-8 border border-gray-100 transition-all duration-500 hover:shadow-2xl hover:shadow-indigo-900/5 hover:-translate-y-2 overflow-hidden">
                            {/* Decorative Background Icon */}
                            <div className="absolute -right-6 -top-6 transition-transform duration-700 group-hover:rotate-12 group-hover:scale-110">
                                <div className={`w-36 h-36 rounded-full opacity-5 group-hover:opacity-10 transition-opacity duration-500 ${template.category === 'Education' ? 'bg-blue-500' :
                                        template.category === 'Police' ? 'bg-red-500' :
                                            template.category === 'Municipal' ? 'bg-green-500' :
                                                'bg-orange-500'
                                    }`}></div>
                            </div>

                            {/* Content */}
                            <div className="relative z-10 flex flex-col h-full">
                                <div className="mb-6 flex items-start justify-between">
                                    <span className={`inline-flex items-center px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wide ${template.category === 'Education' ? 'bg-blue-50 text-blue-700' :
                                            template.category === 'Police' ? 'bg-red-50 text-red-700' :
                                                template.category === 'Municipal' ? 'bg-green-50 text-green-700' :
                                                    'bg-orange-50 text-orange-700'
                                        }`}>
                                        {template.category}
                                    </span>
                                    <div className="text-gray-300">
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                                    </div>
                                </div>

                                <h3 className="font-serif font-bold text-2xl text-slate-800 mb-2 group-hover:text-indigo-900 transition-colors">
                                    {template.title}
                                </h3>
                                <p className="text-sm text-slate-500 font-medium mb-8">
                                    Target Dept: <span className="text-slate-700">{template.dept}</span>
                                </p>

                                <div className="mt-auto pt-6 border-t border-gray-50 flex items-center justify-between">
                                    <div className="flex items-center text-xs text-gray-400 font-semibold uppercase tracking-wider">
                                        <svg className="w-4 h-4 mr-1.5 text-gray-300 group-hover:text-amber-500 transition-colors" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                                        {template.uses}+ Used
                                    </div>
                                    <Button
                                        to="/generate"
                                        state={{ intent: `I want to file an RTI to ${template.dept} regarding ${template.title}. Please provide details.` }}
                                        variant="outline"
                                        className="border-gray-200 hover:border-indigo-600 hover:bg-indigo-600 hover:text-white px-5 py-2 text-sm transition-all duration-300 shadow-sm hover:shadow-indigo-500/20"
                                    >
                                        Use Template
                                    </Button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Simple footer note to fill space professionally */}
            <div className="text-center text-xs text-gray-300 mt-12 pb-8">
                RTI-Gen Templates • Helping {filteredTemplates.reduce((acc, curr) => acc + curr.uses, 0).toLocaleString()}+ Citizens
            </div>
        </div>
    );
};

export default Templates;
