import { motion } from 'framer-motion';
import Button from '../components/Button';

const Landing = () => {
    return (
        <div className="flex flex-col">
            {/* Hero Section */}
            <section className="relative pt-20 pb-32 overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 flex flex-col md:flex-row items-center gap-12">

                    {/* Text Content */}
                    <div className="flex-1 text-center md:text-left">
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 rounded-full border border-indigo-100 mb-6 animate-fade-in text-indigo-700 text-sm font-medium">
                            <span className="w-2 h-2 bg-saffron rounded-full"></span>
                            AI-Powered Rti Application Generator
                        </div>

                        <motion.h1
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.8, ease: "easeOut" }}
                            className="font-serif font-bold text-4xl md:text-6xl text-indigo-deep leading-tight mb-6"
                        >
                            Empowering Citizens, <br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-deep to-indigo-600">One RTI at a Time</span>
                        </motion.h1>

                        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto md:mx-0 leading-relaxed font-light">
                            Transform your plain-language queries into legally compliant RTI drafts instantly. No lawyers needed, just your voice and our AI.
                        </p>

                        <div className="flex flex-col sm:flex-row items-center gap-4 justify-center md:justify-start">
                            <Button
                                variant="primary"
                                className="w-full sm:w-auto text-lg px-8 py-4 shadow-xl hover:shadow-2xl"
                                onClick={() => window.location.href = '/generate'}
                            >
                                Generate RTI Now
                            </Button>
                            <Button variant="outline" className="w-full sm:w-auto text-lg px-8 py-4">
                                View Templates
                            </Button>
                        </div>

                        <div className="mt-8 flex items-center justify-center md:justify-start gap-6 text-sm text-gray-500">
                            <div className="flex items-center gap-2">
                                <svg className="w-5 h-5 text-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                <span>RTI Act 2005 Compliant</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <svg className="w-5 h-5 text-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                                <span>Private & Secure</span>
                            </div>
                        </div>
                    </div>

                    {/* Hero Visual / Card Preview */}
                    <div className="flex-1 w-full max-w-lg md:max-w-none relative">
                        <div className="absolute top-0 right-0 w-72 h-72 bg-saffron/10 rounded-full blur-3xl -z-10"></div>
                        <div className="relative bg-white rounded-2xl shadow-paper border border-gray-100 p-6 md:p-8 transform rotate-2 hover:rotate-0 transition-transform duration-500">
                            {/* Mock RTI Preview */}
                            <div className="flex justify-between items-start mb-6 border-b border-gray-100 pb-4">
                                <div>
                                    <div className="h-4 w-32 bg-gray-200 rounded mb-2"></div>
                                    <div className="h-3 w-24 bg-gray-100 rounded"></div>
                                </div>
                                <div className="w-12 h-12 border-2 border-indigo-deep/20 rounded-full flex items-center justify-center">
                                    <span className="text-xs font-serif text-indigo-deep/50 uppercase transform -rotate-12">Stamp</span>
                                </div>
                            </div>

                            <div className="space-y-4 font-serif text-gray-800">
                                <p className="text-sm">To,<br />The Public Information Officer,<br />Department of Example...</p>
                                <p className="text-sm font-bold mt-4">Subject: Application under RTI Act, 2005.</p>
                                <div className="bg-blue-50/50 p-4 rounded border border-blue-100">
                                    <p className="text-sm italic text-gray-600 mb-2">Sir/Madam,</p>
                                    <p className="text-sm">Please provide certified copies of records showing the scholarship disbursement status...</p>
                                </div>
                            </div>

                            <div className="mt-6 flex justify-between items-center text-xs text-gray-400">
                                <span>Generated via RTI-Gen</span>
                                <span className="text-teal font-medium">Quality Score: 98/100</span>
                            </div>
                        </div>
                    </div>

                </div>
            </section>

            {/* How It Works */}
            <section className="py-20 bg-white relative">
                <div className="absolute inset-0 bg-grain opacity-30 pointer-events-none"></div>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <div className="text-center mb-16">
                        <h2 className="font-serif font-bold text-3xl text-indigo-deep mb-4">How it Works</h2>
                        <p className="text-gray-600 max-w-2xl mx-auto">Three simple steps to claim your right to information.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            { step: '01', title: 'Describe Issue', desc: 'Type your problem in plain language. "My road is broken" or "Scholarship delayed".', icon: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' },
                            { step: '02', title: 'AI Drafting', desc: 'Our engine converts your text into legally compliant questions and formats the application.', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
                            { step: '03', title: 'Download & File', desc: 'Get a ready-to-print PDF. Sign it and submit it to the relevant department.', icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4' }
                        ].map((item, idx) => (
                            <div key={idx} className="group bg-white rounded-2xl p-8 border border-gray-100 hover:border-orange-200 shadow-xl hover:shadow-2xl transition-all duration-300 relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-orange-50 rounded-bl-full -mr-16 -mt-16 transition-transform group-hover:scale-110"></div>

                                <div className="relative z-10">
                                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-6 text-orange-600 group-hover:text-orange-700 transition-colors">
                                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} /></svg>
                                    </div>

                                    <h3 className="font-serif font-bold text-2xl text-stone-800 mb-3">{item.title}</h3>
                                    <p className="text-stone-600 leading-relaxed">{item.desc}</p>
                                </div>

                                <div className="absolute bottom-4 right-6 text-6xl font-serif font-bold text-gray-50 opacity-50 group-hover:opacity-100 group-hover:text-orange-50 transition-all select-none">
                                    {item.step}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Landing;


