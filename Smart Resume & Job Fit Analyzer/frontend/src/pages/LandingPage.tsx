import { useNavigate } from 'react-router-dom';
import { Upload, FileText, CheckCircle, Shield, ArrowRight, Zap, Target, Sparkles, Brain, BarChart3 } from 'lucide-react';

export default function LandingPage() {
    const navigate = useNavigate();

    return (
        <div className="animate-fade-in">
            {/* Hero Section */}
            <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden">
                {/* Animated Background */}
                <div className="absolute inset-0 -z-10">
                    <div className="absolute top-1/4 right-1/4 w-[500px] h-[500px] bg-gradient-to-br from-[var(--color-primary-200)] to-[var(--color-primary-100)] opacity-50 blur-[100px] rounded-full animate-pulse"></div>
                    <div className="absolute bottom-1/4 left-1/4 w-[400px] h-[400px] bg-gradient-to-tr from-[var(--color-accent-200)] to-[var(--color-secondary-100)] opacity-40 blur-[80px] rounded-full" style={{ animationDelay: '1s' }}></div>
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-white/80 to-transparent rounded-full"></div>
                </div>

                <div className="text-center max-w-5xl mx-auto px-6">
                    {/* Badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/80 backdrop-blur-sm border border-[var(--color-neutral-200)] shadow-sm mb-8 hover:shadow-md transition-all">
                        <Sparkles className="w-4 h-4 text-[var(--color-accent-500)]" />
                        <span className="text-sm font-semibold text-[var(--color-neutral-700)]">AI-Powered Analysis</span>
                        <span className="px-2 py-0.5 bg-[var(--color-green-100)] text-[var(--color-green-700)] text-xs font-bold rounded-full">FREE</span>
                    </div>

                    {/* Headline */}
                    <h1 className="text-4xl md:text-7xl font-bold text-[var(--color-neutral-900)] mb-6 leading-tight tracking-tight">
                        Land Your Dream Job
                        <br />
                        <span className="relative">
                            <span className="bg-gradient-to-r from-[var(--color-primary-600)] via-[var(--color-primary-500)] to-[var(--color-accent-500)] bg-clip-text text-transparent">
                                With Confidence
                            </span>
                            <svg className="absolute -bottom-2 left-0 w-full" viewBox="0 0 300 12" fill="none">
                                <path d="M2 10C50 4 150 4 298 10" stroke="url(#underline-gradient)" strokeWidth="4" strokeLinecap="round" />
                                <defs>
                                    <linearGradient id="underline-gradient" x1="0" y1="0" x2="300" y2="0">
                                        <stop stopColor="var(--color-primary-500)" />
                                        <stop offset="1" stopColor="var(--color-accent-500)" />
                                    </linearGradient>
                                </defs>
                            </svg>
                        </span>
                    </h1>

                    {/* Subheadline */}
                    <p className="text-xl md:text-2xl text-[var(--color-neutral-600)] mb-10 max-w-2xl mx-auto leading-relaxed">
                        Get an instant <strong>fit score</strong>, discover <strong>missing keywords</strong>,
                        and receive <strong>actionable suggestions</strong> to beat the ATS.
                    </p>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
                        <button
                            onClick={() => navigate('/mode')}
                            className="group btn btn-primary h-14 text-lg px-8 shadow-xl shadow-[var(--color-primary-500)]/20 hover:shadow-[var(--color-primary-500)]/40 active:scale-95 transition-all"
                        >
                            <span>Start Free Analysis</span>
                            <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                        </button>
                        <a href="#features" className="btn btn-secondary h-14 text-lg px-8 active:scale-95 transition-transform">
                            How It Works
                        </a>
                    </div>

                    {/* Trust Indicators */}
                    <div className="flex items-center justify-center gap-6 text-sm text-[var(--color-neutral-500)]">
                        <div className="flex items-center gap-2">
                            <Shield className="w-4 h-4" />
                            <span>100% Private</span>
                        </div>
                        <div className="w-1 h-1 rounded-full bg-[var(--color-neutral-300)]"></div>
                        <div className="flex items-center gap-2">
                            <Zap className="w-4 h-4" />
                            <span>Results in Seconds</span>
                        </div>
                        <div className="w-1 h-1 rounded-full bg-[var(--color-neutral-300)]"></div>
                        <div className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4" />
                            <span>No Sign-up Required</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-24 bg-[var(--color-neutral-50)]">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-[var(--color-neutral-900)] mb-4">
                            Everything You Need to <span className="text-[var(--color-primary-600)]">Stand Out</span>
                        </h2>
                        <p className="text-lg text-[var(--color-neutral-600)] max-w-2xl mx-auto">
                            Our AI analyzes your resume against the job description and provides detailed, actionable insights.
                        </p>
                    </div>

                    {/* Bento Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-12 gap-6 px-4 md:px-0">

                        {/* Main Feature - Fit Score */}
                        <div className="md:col-span-7 bg-gradient-to-br from-[var(--color-primary-600)] to-[var(--color-primary-700)] rounded-3xl p-8 text-white relative overflow-hidden group">
                            <div className="absolute top-0 right-0 w-80 h-80 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:scale-110 transition-transform duration-700"></div>
                            <div className="relative z-10">
                                <div className="flex items-center gap-2 mb-6">
                                    <BarChart3 className="w-6 h-6" />
                                    <span className="text-sm font-semibold uppercase tracking-wide opacity-80">Smart Scoring</span>
                                </div>
                                <h3 className="text-3xl md:text-4xl font-bold mb-4">Instant Fit Score</h3>
                                <p className="text-white/80 text-lg mb-8 max-w-md">
                                    Get a 0-100 score showing exactly how well your resume matches the job requirements.
                                </p>
                                <div className="flex gap-4">
                                    <div className="bg-white/15 backdrop-blur-sm rounded-2xl p-4 flex-1 text-center">
                                        <div className="text-3xl font-bold">95%</div>
                                        <div className="text-xs opacity-70 uppercase">Accuracy</div>
                                    </div>
                                    <div className="bg-white/15 backdrop-blur-sm rounded-2xl p-4 flex-1 text-center">
                                        <div className="text-3xl font-bold">&lt;5s</div>
                                        <div className="text-xs opacity-70 uppercase">Analysis</div>
                                    </div>
                                    <div className="bg-white/15 backdrop-blur-sm rounded-2xl p-4 flex-1 text-center">
                                        <div className="text-3xl font-bold">264</div>
                                        <div className="text-xs opacity-70 uppercase">Skills</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Privacy Feature */}
                        <div className="md:col-span-5 bg-white rounded-3xl p-8 border border-[var(--color-neutral-200)] hover:shadow-xl hover:border-[var(--color-primary-200)] transition-all duration-300 group">
                            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--color-green-100)] to-[var(--color-green-50)] flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                <Shield className="w-7 h-7 text-[var(--color-green-600)]" />
                            </div>
                            <h3 className="text-2xl font-bold text-[var(--color-neutral-900)] mb-3">Privacy First</h3>
                            <p className="text-[var(--color-neutral-600)] mb-6">
                                Your resume data is never stored or shared. All processing happens in real-time with instant deletion.
                            </p>
                            <div className="flex items-center gap-2 text-sm font-semibold text-[var(--color-green-600)]">
                                <span className="w-2 h-2 rounded-full bg-[var(--color-green-500)] animate-pulse"></span>
                                <span>GDPR Compliant</span>
                            </div>
                        </div>

                        {/* Skill Matching */}
                        <div className="md:col-span-5 bg-[var(--color-neutral-900)] rounded-3xl p-8 text-white relative overflow-hidden">
                            <div className="absolute bottom-0 right-0 w-40 h-40 bg-[var(--color-accent-500)]/20 rounded-full blur-2xl"></div>
                            <div className="relative z-10">
                                <div className="w-14 h-14 rounded-2xl bg-[var(--color-neutral-800)] flex items-center justify-center mb-6">
                                    <Target className="w-7 h-7 text-[var(--color-accent-500)]" />
                                </div>
                                <h3 className="text-2xl font-bold mb-3">Skill Gap Analysis</h3>
                                <p className="text-[var(--color-neutral-400)] mb-6">
                                    See exactly which skills you're missing and get suggestions on how to address them.
                                </p>
                                <div className="flex gap-2 flex-wrap">
                                    {['Python', 'React', 'SQL', 'AWS'].map(skill => (
                                        <span key={skill} className="px-3 py-1 bg-[var(--color-neutral-800)] rounded-full text-sm text-[var(--color-neutral-300)]">
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* AI Suggestions */}
                        <div className="md:col-span-7 bg-gradient-to-br from-[var(--color-accent-400)] to-[var(--color-accent-500)] rounded-3xl p-8 text-[var(--color-neutral-900)] relative overflow-hidden group">
                            <div className="absolute top-0 left-0 w-60 h-60 bg-white/20 rounded-full blur-3xl -translate-y-1/2 -translate-x-1/2 group-hover:scale-110 transition-transform duration-700"></div>
                            <div className="relative z-10">
                                <div className="flex items-center gap-2 mb-6">
                                    <Brain className="w-6 h-6" />
                                    <span className="text-sm font-semibold uppercase tracking-wide opacity-80">AI-Powered</span>
                                </div>
                                <h3 className="text-3xl font-bold mb-4">Actionable Suggestions</h3>
                                <p className="opacity-80 text-lg mb-6 max-w-lg">
                                    Get personalized recommendations on keywords to add, experience to highlight, and how to phrase achievements.
                                </p>
                                <button
                                    onClick={() => navigate('/mode')}
                                    className="px-6 py-3 bg-[var(--color-neutral-900)] text-white rounded-xl font-semibold hover:bg-[var(--color-neutral-800)] transition-colors"
                                >
                                    Try It Now →
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section className="py-24">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-[var(--color-neutral-900)] mb-4">
                            Three Simple Steps
                        </h2>
                        <p className="text-lg text-[var(--color-neutral-600)]">
                            From upload to insights in under a minute
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
                        {[
                            { icon: Upload, title: "Upload Resume", desc: "Drop your PDF or paste text", color: "primary" },
                            { icon: FileText, title: "Add Job Description", desc: "Paste the job posting", color: "secondary" },
                            { icon: CheckCircle, title: "Get Results", desc: "View your fit score & action items", color: "green" }
                        ].map((step, i) => (
                            <div key={i} className="relative group">
                                {i < 2 && (
                                    <div className="hidden md:block absolute top-10 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-[var(--color-neutral-200)] to-transparent"></div>
                                )}
                                <div className="relative bg-white rounded-2xl p-6 border border-[var(--color-neutral-200)] hover:shadow-lg hover:border-[var(--color-primary-200)] transition-all text-center">
                                    <div className={`w-16 h-16 mx-auto rounded-2xl bg-[var(--color-${step.color}-100)] flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                                        <step.icon className={`w-8 h-8 text-[var(--color-${step.color}-600)]`} />
                                    </div>
                                    <div className="absolute -top-3 -right-3 w-8 h-8 bg-[var(--color-neutral-900)] text-white rounded-full flex items-center justify-center font-bold text-sm">
                                        {i + 1}
                                    </div>
                                    <h4 className="text-lg font-bold text-[var(--color-neutral-900)] mb-2">{step.title}</h4>
                                    <p className="text-sm text-[var(--color-neutral-500)]">{step.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20">
                <div className="container">
                    <div className="bg-gradient-to-br from-[var(--color-primary-600)] to-[var(--color-primary-700)] rounded-3xl p-12 text-center text-white relative overflow-hidden">
                        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
                        <div className="relative z-10">
                            <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Improve Your Resume?</h2>
                            <p className="text-white/80 text-lg mb-8 max-w-xl mx-auto">
                                Join thousands of job seekers who have optimized their resumes with our AI tool.
                            </p>
                            <button
                                onClick={() => navigate('/mode')}
                                className="btn h-14 text-lg px-10 bg-white text-[var(--color-primary-700)] font-bold hover:bg-[var(--color-neutral-100)] shadow-xl active:scale-95 transition-all"
                            >
                                Analyze My Resume Free
                                <ArrowRight className="w-5 h-5 ml-2" />
                            </button>
                        </div>
                    </div>
                </div>
            </section>


        </div>
    );
}
