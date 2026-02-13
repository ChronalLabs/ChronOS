import React from 'react';

interface Step {
    id: number;
    name: string;
    description: string;
}

interface StepperProps {
    steps: Step[];
    currentStep: number;
    completedSteps?: number[];
}

/**
 * Stepper component for showing progress through multi-step flow.
 * Includes ARIA labels for accessibility.
 */
export const Stepper: React.FC<StepperProps> = ({
    steps,
    currentStep,
    completedSteps = [],
}) => {
    const getStepStatus = (stepId: number) => {
        if (completedSteps.includes(stepId)) return 'completed';
        if (stepId === currentStep) return 'current';
        return 'upcoming';
    };

    return (
        <nav aria-label="Progress" className="py-4">
            <ol role="list" className="flex items-center justify-between w-full max-w-2xl mx-auto px-4">
                {steps.map((step, index) => {
                    const status = getStepStatus(step.id);
                    const isCompleted = status === 'completed';
                    const isCurrent = status === 'current';

                    return (
                        <li key={step.id} className="flex-1 flex items-center">
                            {/* Step Circle + Label */}
                            <div className="flex flex-col items-center">
                                <div
                                    className={`
                                        flex items-center justify-center w-10 h-10 rounded-full transition-all duration-300 border-2
                                        ${isCompleted
                                            ? 'bg-[var(--color-green-500)] border-[var(--color-green-500)] text-white'
                                            : isCurrent
                                                ? 'bg-white border-[var(--color-primary-600)] text-[var(--color-primary-600)] shadow-md'
                                                : 'bg-white border-[var(--color-neutral-300)] text-[var(--color-neutral-400)]'}
                                    `}
                                >
                                    {isCompleted ? (
                                        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                                            <polyline points="20 6 9 17 4 12" />
                                        </svg>
                                    ) : (
                                        <span className="text-sm font-bold">{step.id}</span>
                                    )}
                                </div>
                                <span className={`mt-2 text-xs font-semibold uppercase tracking-wide ${isCurrent ? 'text-[var(--color-primary-600)]' : isCompleted ? 'text-[var(--color-green-600)]' : 'text-[var(--color-neutral-400)]'}`}>
                                    {step.name}
                                </span>
                            </div>

                            {/* Connector Line */}
                            {index !== steps.length - 1 && (
                                <div className="flex-1 h-0.5 mx-2 rounded-full bg-[var(--color-neutral-200)] relative">
                                    <div
                                        className="absolute top-0 left-0 h-full rounded-full bg-[var(--color-green-500)] transition-all duration-500"
                                        style={{ width: isCompleted ? '100%' : '0%' }}
                                    />
                                </div>
                            )}
                        </li>
                    );
                })}
            </ol>
        </nav>
    );
};

// Default steps for the resume analyzer flow (V1 Spec) - Guided Mode
export const ANALYZER_STEPS: Step[] = [
    { id: 1, name: 'Mode', description: 'Select mode' },
    { id: 2, name: 'Input', description: 'Resume & Job' },
    { id: 3, name: 'Review', description: 'Verify data' },
    { id: 4, name: 'Analyze', description: 'Processing' },
    { id: 5, name: 'Result', description: 'Fit score' },
];

// Assisted mode steps - skips Review
export const ASSISTED_STEPS: Step[] = [
    { id: 1, name: 'Mode', description: 'Select mode' },
    { id: 2, name: 'Input', description: 'Resume & Job' },
    { id: 4, name: 'Analyze', description: 'Processing' },
    { id: 5, name: 'Result', description: 'Fit score' },
];

export default Stepper;
