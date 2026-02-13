import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Docs = () => {
    const [activeSection, setActiveSection] = useState('basics');

    const sections = [
        { id: 'basics', title: 'RTI Basics', icon: '📘' },
        { id: 'how-it-works', title: 'How It Works', icon: '⚙️' },
        { id: 'assisted', title: 'Assisted Mode', icon: '🤖' },
        { id: 'ai-mode', title: 'AI Mode', icon: '🧠' },
        { id: 'legal', title: 'Legal Safety', icon: '⚖️' },
        { id: 'faqs', title: 'FAQs', icon: '❓' },
    ];

    const content = {
        basics: (
            <div className="space-y-6">
                <h2 className="text-3xl font-serif font-bold text-indigo-900">RTI Basics (For First-Time Users)</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Card title="What is RTI?" icon="🔍">
                        The Right to Information (RTI) Act is a law specifically designed to empower you to ask questions to the government. Think of it as a tool to demand transparency.
                    </Card>
                    <Card title="RTI Act 2005" icon="📜">
                        Enacted in 2005, this act gives every Indian citizen the right to secure access to information under the control of public authorities, promoting transparency and accountability.
                    </Card>
                    <Card title="Section 6(1)" icon="§">
                        This is the golden key. Section 6(1) allows you to file a simple request in writing (or electronically) specifying the details of the information sought.
                    </Card>
                    <Card title="RTI vs Complaint" icon="⚖️">
                        <strong>RTI:</strong> Asking for information (e.g., "Status of my road repair").<br />
                        <strong>Complaint:</strong> Reporting misconduct. RTI is often the first step to gather evidence for a complaint.
                    </Card>
                </div>
            </div>
        ),
        'how-it-works': (
            <div className="space-y-6">
                <h2 className="text-3xl font-serif font-bold text-indigo-900">How RTI-Gen Works</h2>
                <div className="bg-white rounded-xl p-6 shadow-lg border border-indigo-50">
                    <ul className="space-y-4">
                        <ListItem title="Assisted Mode vs AI Mode">
                            <strong>Assisted:</strong> Best for beginners. Guide you step-by-step using templates.<br />
                            <strong>AI Mode:</strong> For complex queries. You type freely, and AI drafts the legal text.
                        </ListItem>
                        <ListItem title="Template-based Flow">
                            Choose a proven template (e.g., "Delayed Scholarship"), fill in the blanks, and download ready-to-print PDFs.
                        </ListItem>
                        <ListItem title="Department Selection">
                            Our smart logic (or manual choice) directs your application to the correct Public Information Officer (PIO).
                        </ListItem>
                        <ListItem title="Language Toggle">
                            Instantly switch between English and Hindi. The legal structure remains robust in both languages.
                        </ListItem>
                    </ul>
                </div>
            </div>
        ),
        assisted: (
            <div className="space-y-6">
                <h2 className="text-3xl font-serif font-bold text-indigo-900">Assisted Mode Guide</h2>
                <div className="relative border-l-4 border-indigo-200 pl-6 space-y-8">
                    <Step number="1" title="Select Template">
                        Browse our library of vetted templates for common issues like Scholarships, Road Repairs, and Police FIRs.
                    </Step>
                    <Step number="2" title="Fill Details">
                        Enter simple details like your Name, Address, and specific Issue description.
                    </Step>
                    <Step number="3" title="Review & Download">
                        Preview the generated draft. If it looks good, download the PDF immediately.
                    </Step>
                </div>
            </div>
        ),
        'ai-mode': (
            <div className="space-y-6">
                <h2 className="text-3xl font-serif font-bold text-indigo-900">AI Mode Guide</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-6 rounded-2xl border border-green-100">
                        <h3 className="text-xl font-bold text-green-800 mb-4">✅ What AI Will Do</h3>
                        <ul className="list-disc pl-5 space-y-2 text-green-900">
                            <li>Draft professional legal text based on your rough input.</li>
                            <li>Suggest relevant questions you might have missed.</li>
                            <li>Format everything perfectly for the PIO.</li>
                        </ul>
                    </div>
                    <div className="bg-gradient-to-br from-red-50 to-orange-50 p-6 rounded-2xl border border-red-100">
                        <h3 className="text-xl font-bold text-red-800 mb-4">❌ What AI Will NOT Do</h3>
                        <ul className="list-disc pl-5 space-y-2 text-red-900">
                            <li>It cannot predict the exact future outcome of your RTI.</li>
                            <li>It is not a substitute for a human lawyer for court cases.</li>
                        </ul>
                    </div>
                </div>
            </div>
        ),
        legal: (
            <div className="space-y-6">
                <h2 className="text-3xl font-serif font-bold text-indigo-900">Legal Safety & Compliance</h2>
                <div className="space-y-4">
                    <Accordion title="Common Rejection Reasons">
                        RTIs are often rejected for being vague, asking for "opinions" instead of "records", or missing the application fee proof.
                    </Accordion>
                    <Accordion title="Opinion vs Record">
                        <strong>Bad:</strong> "Why did you not repair the road?" (Asking for opinion/reason usually fails)<br />
                        <strong>Good:</strong> "Please provide the daily progress report of the road repair." (Asking for a record)
                    </Accordion>
                    <Accordion title="Proper Addressing">
                        Always address the "Public Information Officer" (PIO) directly. Our tool handles this automatically.
                    </Accordion>
                </div>
            </div>
        ),
        faqs: (
            <div className="space-y-6">
                <h2 className="text-3xl font-serif font-bold text-indigo-900">Frequently Asked Questions</h2>
                <div className="grid grid-cols-1 gap-4">
                    <FaqQuestion q="What is the response time?" a="By law, the PIO must reply within 30 days of receiving your application." />
                    <FaqQuestion q="Is there a fee?" a="Yes, usually ₹10 for Central Govt RTIs. State fees vary. BPL (Below Poverty Line) applicants are exempt." />
                    <FaqQuestion q="Can I file anonymously?" a="No, you must provide a name and address for the reply to reach you. However, Post Box numbers are sometimes accepted." />
                </div>
            </div>
        )
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row font-sans">
            {/* Sidebar Navigation */}
            <aside className="w-full md:w-80 bg-white border-r border-gray-100 p-6 md:h-screen sticky top-0 overflow-y-auto z-20 shadow-xl">
                <div className="mb-10">
                    <h1 className="text-2xl font-serif font-bold text-indigo-deep">Knowledge Base</h1>
                    <p className="text-sm text-gray-500 mt-2">Master the Right to Information</p>
                </div>
                <nav className="space-y-2">
                    {sections.map(section => (
                        <button
                            key={section.id}
                            onClick={() => setActiveSection(section.id)}
                            className={`w-full flex items-center p-4 rounded-xl transition-all duration-300 transform ${activeSection === section.id
                                    ? 'bg-indigo-deep text-white shadow-lg scale-105 translate-x-2'
                                    : 'text-gray-600 hover:bg-gray-50 hover:pl-6'
                                }`}
                        >
                            <span className="mr-3 text-xl">{section.icon}</span>
                            <span className="font-medium">{section.title}</span>
                        </button>
                    ))}
                </nav>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 p-8 md:p-12 lg:p-16 overflow-y-auto scroll-smooth perspective-1000">
                <div className="max-w-4xl mx-auto">
                    <AnimatePresence mode='wait'>
                        <motion.div
                            key={activeSection}
                            initial={{ opacity: 0, y: 20, rotateX: -5 }}
                            animate={{ opacity: 1, y: 0, rotateX: 0 }}
                            exit={{ opacity: 0, y: -20, rotateX: 5 }}
                            transition={{ duration: 0.4, type: "spring", stiffness: 100 }}
                            className="bg-white rounded-3xl p-10 shadow-2xl shadow-indigo-100/50 border border-white/50 backdrop-blur-xl"
                            style={{ transformStyle: 'preserve-3d' }}
                        >
                            {content[activeSection]}
                        </motion.div>
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
};

// UI Components
const Card = ({ title, icon, children }) => (
    <div className="bg-gray-50 hover:bg-white p-6 rounded-2xl border border-transparent hover:border-indigo-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 group">
        <div className="text-3xl mb-4 group-hover:scale-110 transition-transform origin-left">{icon}</div>
        <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600 text-sm leading-relaxed">{children}</p>
    </div>
);

const ListItem = ({ title, children }) => (
    <li className="flex items-start">
        <span className="h-6 w-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold mr-3 mt-0.5">✓</span>
        <div>
            <h4 className="font-bold text-gray-900 text-sm mb-1">{title}</h4>
            <p className="text-gray-600 text-sm">{children}</p>
        </div>
    </li>
);

const Step = ({ number, title, children }) => (
    <div className="relative">
        <div className="absolute -left-[41px] top-0 h-8 w-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold shadow-lg ring-4 ring-white">
            {number}
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600">{children}</p>
    </div>
);

const Accordion = ({ title, children }) => (
    <details className="group bg-white rounded-xl border border-gray-200 overflow-hidden transition-all duration-300 open:shadow-lg open:border-indigo-200 open:bg-indigo-50/30">
        <summary className="flex items-center justify-between p-4 cursor-pointer font-bold text-gray-800 marker:content-none hover:bg-gray-50 transition-colors">
            {title}
            <span className="transform group-open:rotate-180 transition-transform duration-300 text-indigo-500">▼</span>
        </summary>
        <div className="p-4 pt-0 text-gray-600 border-t border-transparent group-open:border-indigo-100">
            {children}
        </div>
    </details>
);

const FaqQuestion = ({ q, a }) => (
    <div className="border-b border-gray-100 last:border-0 py-4">
        <h4 className="font-bold text-gray-900 mb-2 flex items-center">
            <span className="text-indigo-500 mr-2">Q.</span> {q}
        </h4>
        <p className="text-gray-600 pl-6">{a}</p>
    </div>
);

export default Docs;
