
import React from 'react';
import { Stepper, ANALYZER_STEPS, ASSISTED_STEPS } from './Stepper';
import type { AnalysisMode } from '../services/types';

interface LayoutProps {
    children: React.ReactNode;
    currentStep?: number;
    completedSteps?: number[];
    onReset?: () => void;
    showReset?: boolean;
    onBack?: () => void;
    title?: string;
    mode?: AnalysisMode | null;
}

export const Layout: React.FC<LayoutProps> = ({
    children,
    currentStep = 0,
    completedSteps = [],
    onReset,
    showReset = false,
    onBack,
    mode,
}) => {
    // Use assisted steps if in assisted mode
    const steps = mode === 'assisted' ? ASSISTED_STEPS : ANALYZER_STEPS;

    return (
        <div className="min-h-screen bg-gradient-to-br from-[var(--color-neutral-50)] to-[var(--color-neutral-100)] flex flex-col font-sans text-[var(--color-text-primary)]">
            {/* Accessibility Skip Link */}
            <a href="#main-content" className="skip-link sr-only focus:not-sr-only">
                Skip to main content
            </a>

            {/* Premium Navbar */}
            <header className="sticky top-0 z-50 w-full border-b border-[var(--color-neutral-200)]/50 bg-white/80 backdrop-blur-xl">
                <div className="container h-16 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        {onBack && (
                            <button
                                onClick={onBack}
                                className="p-2 hover:bg-[var(--color-neutral-100)] rounded-xl transition-all hover:scale-105"
                                aria-label="Go back"
                            >
                                <svg className="w-5 h-5 text-[var(--color-neutral-600)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                                </svg>
                            </button>
                        )}

                        <div
                            className="flex items-center gap-3 cursor-pointer group"
                            onClick={onReset}
                            role="button"
                            tabIndex={0}
                            onKeyDown={(e) => e.key === 'Enter' && onReset?.()}
                        >
                            {/* Logo Icon */}
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-primary-500)] to-[var(--color-primary-700)] flex items-center justify-center shadow-lg shadow-[var(--color-primary-500)]/20 group-hover:shadow-[var(--color-primary-500)]/40 transition-all group-hover:scale-105">
                                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            {/* Logo Text */}
                            <div className="flex flex-col">
                                <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-[var(--color-primary-600)] to-[var(--color-primary-500)] bg-clip-text text-transparent leading-tight">
                                    ResumeAI
                                </h1>
                                <span className="text-[10px] font-medium text-[var(--color-neutral-400)] uppercase tracking-widest">
                                    Smart Analyzer
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        {showReset && onReset && (
                            <button
                                onClick={onReset}
                                className="flex items-center gap-2 text-sm font-semibold text-[var(--color-primary-600)] hover:text-[var(--color-primary-700)] transition-colors px-3 py-2 md:px-4 md:py-2 rounded-xl hover:bg-[var(--color-primary-50)] border border-transparent hover:border-[var(--color-primary-200)]"
                                aria-label="New Analysis"
                            >
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                                </svg>
                                <span className="hidden md:inline">New Analysis</span>
                            </button>
                        )}
                    </div>
                </div>
            </header>

            {/* Progress Stepper - Context Aware */}
            {currentStep > 1 && (
                <div className="border-b border-[var(--color-border)] bg-[var(--color-surface)] shadow-sm">
                    <div className="container py-2">
                        <Stepper
                            steps={steps}
                            currentStep={currentStep}
                            completedSteps={completedSteps}
                        />
                    </div>
                </div>
            )}

            {/* Main Content */}
            <main
                id="main-content"
                className="flex-1 container py-8 animate-fade-in"
                role="main"
            >
                {children}
            </main>

            {/* Footer */}
            {/* Footer */}
            <footer className="border-t border-[var(--color-border)] bg-[var(--color-surface)] py-8 mt-auto">
                <div className="container flex flex-col md:flex-row items-center justify-between gap-6 text-sm text-[var(--color-text-muted)]">
                    <div className="flex flex-col items-center md:items-start gap-1">
                        <p>© {new Date().getFullYear()} Smart Resume Analyzer</p>
                        <p className="text-xs">
                            An Open Source Project by <a href="https://chronallab-site.vercel.app/" target="_blank" rel="noopener noreferrer" className="text-[var(--color-primary-600)] hover:text-[var(--color-primary-700)] font-medium transition-colors hover:underline">ChronalLabs</a>
                        </p>
                    </div>

                    <div className="flex flex-wrap items-center justify-center gap-4 md:gap-6">
                        <a
                            href="https://github.com/ChronalLabs"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 hover:text-[var(--color-primary-600)] transition-colors group"
                        >
                            <svg className="w-4 h-4 transition-transform group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                            </svg>
                            <span className="font-medium">GitHub</span>
                        </a>
                        <span className="hidden md:inline text-[var(--color-neutral-300)]">|</span>
                        <span>Privacy-First</span>
                        <span className="hidden md:inline text-[var(--color-neutral-300)]">|</span>
                        <span>Advisory Only</span>
                    </div>
                </div>
            </footer>
        </div>
    );
};
