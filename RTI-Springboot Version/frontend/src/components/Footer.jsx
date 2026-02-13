import React from 'react';

const Footer = () => {
    return (
        <footer className="text-white py-6" style={{ backgroundColor: '#000000' }}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                    {/* Brand */}
                    <div className="col-span-1 md:col-span-1">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center text-indigo-deep font-serif font-bold text-lg">
                                R
                            </div>
                            <span className="font-serif font-bold text-lg tracking-tight">RTI-Gen</span>
                        </div>
                        <p className="text-gray-400 text-sm leading-relaxed mb-6">
                            Empowering citizens with AI-driven tools to file Right to Information applications. Transparent, private, and efficient.
                        </p>
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-900/50 rounded-full border border-indigo-800">
                            <span className="w-2 h-2 bg-saffron rounded-full"></span>
                            <span className="text-xs font-medium text-gray-300">GSoC 2026 Mentorship Organization</span>
                        </div>
                    </div>

                    {/* Links */}
                    <div>
                        <h3 className="font-serif font-bold text-lg mb-4">Product</h3>
                        <ul className="space-y-3 text-sm text-gray-400">
                            <li><a href="#" className="hover:text-green-light transition-colors">Dashboard</a></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="font-serif font-bold text-lg mb-4">Resources</h3>
                        <ul className="space-y-3 text-sm text-gray-400">
                            <li><a href="https://www.linkedin.com/posts/anuragmishra5159_aipowered-public-complaint-rti-generator-activity-7424077025256173568-nc1I?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAEgGHnoBNHQryVzjQRluYcFEFFGY7CeKzeU" target="_blank" rel="noopener noreferrer" className="hover:text-green-light transition-colors">Documentation</a></li>
                        </ul>
                    </div>

                    {/* Social */}
                    <div>
                        <h3 className="font-serif font-bold text-lg mb-4">Connect</h3>
                        <div className="flex gap-4">
                            <a href="https://github.com/ChronalLabs/AI-Powered-Public-Complaint-and-RTI-Generator" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-green-light hover:text-black transition-all">
                                {/* GitHub Icon */}
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" /></svg>
                            </a>
                        </div>
                    </div>
                </div>

                <div className="pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-gray-500">
                    <span>&copy; 2026 RTI-Gen. Open Source (MIT License).</span>
                    <div className="flex gap-4">
                        <a href="#" className="hover:text-green-light transition-colors">Terms</a>
                        <a href="#" className="hover:text-green-light transition-colors">Sitemap</a>
                    </div>
                </div>
            </div>
        </footer >
    );
};

export default Footer;
