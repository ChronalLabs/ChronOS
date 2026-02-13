import React from 'react';
import Button from '../components/Button';

const Community = () => {
    return (
        <div className="min-h-screen bg-stone-50 text-stone-800 font-sans selection:bg-stone-200">
            <div className="max-w-4xl mx-auto px-6 py-20 lg:py-28">

                {/* Header Section */}
                <header className="mb-24 border-b border-stone-200 pb-12">
                    <p className="font-mono text-xs uppercase tracking-widest text-stone-500 mb-4">/ Community_Interface</p>
                    <h1 className="font-serif text-5xl md:text-6xl text-stone-900 tracking-tight mb-8">
                        Public Infrastructure <br />
                        <span className="italic text-stone-600">Research Network</span>
                    </h1>
                    <p className="text-lg md:text-xl text-stone-600 max-w-2xl leading-relaxed">
                        An open civic-tech network built in public. We build systems to decentralize information access and empower citizens through transparent technology.
                    </p>
                </header>

                {/* Contribution Interface */}
                <section className="mb-24">
                    <div className="flex items-center justify-between mb-12">
                        <h2 className="font-mono text-sm uppercase tracking-widest text-stone-400">/ CONTRIBUTION_INTERFACE</h2>
                        <div className="h-px bg-stone-200 flex-grow ml-6"></div>
                    </div>

                    <div className="mb-12">
                        <h3 className="text-3xl font-serif text-stone-900 mb-4">CONTRIBUTE <br /> TO THE SYSTEM_</h3>
                        <p className="text-stone-600 max-w-xl">
                            ChronalLabs invites contributors to shape tools, research, and interfaces.
                            We are building civic systems in public. You can help shape them.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Option 01 */}
                        <div className="group border-l sm:border-l-0 sm:border-t border-stone-200 pt-6 sm:pl-0 pl-6 hover:bg-stone-100/50 transition-colors duration-500 -ml-6 sm:ml-0 p-6 sm:p-0">
                            <span className="font-mono text-xs text-stone-400 block mb-3">01 — CONTRIBUTE_CODE</span>
                            <p className="text-stone-600 text-sm leading-relaxed mb-8 min-h-[80px]">
                                Work on open-source civic tools, APIs, and system prototypes designed to decentralize information access.
                            </p>
                            <Button
                                to="https://github.com/ChronalLabs"
                                target="_blank"
                                variant="outline"
                                className="font-mono text-xs uppercase tracking-wider border-stone-300 text-stone-600 hover:bg-stone-900 hover:text-white hover:border-stone-900 rounded-none px-6"
                            >
                                View_Repositories
                            </Button>
                        </div>

                        {/* Option 02 */}
                        <div className="group border-l sm:border-l-0 sm:border-t border-stone-200 pt-6 sm:pl-0 pl-6 hover:bg-stone-100/50 transition-colors duration-500 -ml-6 sm:ml-0 p-6 sm:p-0">
                            <span className="font-mono text-xs text-stone-400 block mb-3">02 — RESEARCH_&_IDEAS</span>
                            <p className="text-stone-600 text-sm leading-relaxed mb-8 min-h-[80px]">
                                Help define problem statements, workflows, and system designs for civic technology in public interest.
                            </p>
                            <Button
                                to="#"
                                variant="outline"
                                className="font-mono text-xs uppercase tracking-wider border-stone-300 text-stone-600 hover:bg-stone-900 hover:text-white hover:border-stone-900 rounded-none px-6"
                            >
                                Explore_Ideas
                            </Button>
                        </div>

                        {/* Option 03 */}
                        <div className="group border-l sm:border-l-0 sm:border-t border-stone-200 pt-6 sm:pl-0 pl-6 hover:bg-stone-100/50 transition-colors duration-500 -ml-6 sm:ml-0 p-6 sm:p-0">
                            <span className="font-mono text-xs text-stone-400 block mb-3">03 — JOIN_GSOC_PROJECTS</span>
                            <p className="text-stone-600 text-sm leading-relaxed mb-8 min-h-[80px]">
                                Collaborate on structured project ideas designed for Google Summer of Code and long-term development.
                            </p>
                            <Button
                                to="#"
                                variant="outline"
                                className="font-mono text-xs uppercase tracking-wider border-stone-300 text-stone-600 hover:bg-stone-900 hover:text-white hover:border-stone-900 rounded-none px-6"
                            >
                                View_GSoC_Ideas
                            </Button>
                        </div>
                    </div>
                </section>

                {/* Contributors Index */}
                <section className="mb-24">
                    <div className="flex items-center justify-between mb-12">
                        <h2 className="font-mono text-sm uppercase tracking-widest text-stone-400">/ CONTRIBUTORS_INDEX</h2>
                        <div className="h-px bg-stone-200 flex-grow ml-6"></div>
                    </div>

                    <div className="flex flex-col md:flex-row gap-12 md:gap-24">
                        <div className="md:w-1/3">
                            <h3 className="text-2xl font-serif text-stone-900 mb-2">PEOPLE <br /> NETWORK_</h3>
                            <p className="text-stone-500 text-sm">
                                An open network of developers and researchers collaborating on public infrastructure.
                            </p>
                        </div>

                        <div className="md:w-2/3 grid grid-cols-1 sm:grid-cols-2 gap-y-4 gap-x-8">
                            {[
                                "Anurag Mishra",
                                "Ananya Sharma",
                                "Ananya Tiwari",
                                "Arin Gupta",
                                "Krish Dargar",
                                "Yogesh Sanodiya"
                            ].map((name, index) => (
                                <div key={index} className="flex items-baseline border-b border-stone-100 pb-2">
                                    <span className="font-mono text-xs text-stone-300 mr-4">0{index + 1}</span>
                                    <span className="text-stone-800 text-lg font-medium">{name}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Guidance Section */}
                <section className="bg-stone-100 p-8 md:p-12 mb-24">
                    <h4 className="font-mono text-xs uppercase tracking-widest text-stone-500 mb-6">Guidance & Mentorship</h4>
                    <p className="text-stone-700 text-lg font-serif italic mb-2">
                        "Guided under GSoC-style mentorship at ChronalLabs"
                    </p>
                    <p className="text-stone-900 font-medium">
                        Manan Chawla — <span className="text-stone-500 font-normal">Google Cloud Platform Engineer</span>
                    </p>
                </section>

                {/* Footer Credit - STRICT */}
                <footer className="text-center pt-12 border-t border-stone-200">
                    <p className="font-mono text-xs text-stone-400 uppercase tracking-widest">
                        Made by Yogesh Sanodiya
                    </p>
                </footer>

            </div>
        </div>
    );
};

export default Community;
