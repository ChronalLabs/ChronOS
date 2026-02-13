import { useState } from 'react';
import type { AnalysisMode } from '../services/types';
import { FileText, Wand2, ArrowRight, Check, Clock, Eye, Zap, Sparkles } from 'lucide-react';

interface ModeSelectionProps {
    onModeSelect: (mode: AnalysisMode) => void;
}

export default function ModeSelection({ onModeSelect }: ModeSelectionProps) {
    const [selected, setSelected] = useState<AnalysisMode | null>(null);
    const [hovering, setHovering] = useState<AnalysisMode | null>(null);

    const modes = [
        {
            id: 'guided' as AnalysisMode,
            title: 'Guided Mode',
            subtitle: 'Full Control',
            description: 'Review and verify each step. See exactly what we parse from your resume before the final evaluation.',
            icon: FileText,
            gradient: 'from-[var(--color-primary-500)] to-[var(--color-primary-600)]',
            bgLight: 'bg-[var(--color-primary-50)]',
            borderColor: 'border-[var(--color-primary-500)]',
            textColor: 'text-[var(--color-primary-600)]',
            badge: 'Recommended',
            badgeColor: 'bg-[var(--color-primary-100)] text-[var(--color-primary-700)]',
            features: [
                { icon: Eye, text: 'Preview parsed data' },
                { icon: Check, text: 'Verify before analysis' },
                { icon: Clock, text: '~2 min process' },
            ]
        },
        {
            id: 'assisted' as AnalysisMode,
            title: 'Quick Mode',
            subtitle: 'Speed First',
            description: 'Skip the review steps. Upload your files and get instant results with AI-powered parsing.',
            icon: Wand2,
            gradient: 'from-[var(--color-accent-500)] to-[var(--color-accent-600)]',
            bgLight: 'bg-[var(--color-accent-50)]',
            borderColor: 'border-[var(--color-accent-500)]',
            textColor: 'text-[var(--color-accent-600)]',
            badge: 'Fastest',
            badgeColor: 'bg-[var(--color-accent-100)] text-[var(--color-accent-700)]',
            features: [
                { icon: Zap, text: 'Instant results' },
                { icon: Sparkles, text: 'AI auto-parsing' },
                { icon: Clock, text: '<30 seconds' },
            ]
        }
    ];

    return (
        <div className="max-w-5xl mx-auto py-16 px-6 animate-fade-in">
            {/* Header */}
            <div className="text-center mb-16">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-[var(--color-neutral-200)] shadow-sm mb-6">
                    <Sparkles className="w-4 h-4 text-[var(--color-accent-500)]" />
                    <span className="text-sm font-semibold text-[var(--color-neutral-600)]">Step 1 of 5</span>
                </div>
                <h1 className="text-4xl md:text-5xl font-bold text-[var(--color-neutral-900)] mb-4">
                    How would you like to analyze?
                </h1>
                <p className="text-lg text-[var(--color-neutral-500)] max-w-xl mx-auto">
                    Both modes deliver the same powerful insights. Choose based on your preference.
                </p>
            </div>

            {/* Mode Cards */}
            <div className="grid md:grid-cols-2 gap-6 mb-12 max-w-4xl mx-auto">
                {modes.map((mode) => {
                    const isSelected = selected === mode.id;
                    const isHovering = hovering === mode.id;
                    const Icon = mode.icon;

                    return (
                        <button
                            key={mode.id}
                            onClick={() => setSelected(mode.id)}
                            onMouseEnter={() => setHovering(mode.id)}
                            onMouseLeave={() => setHovering(null)}
                            className={`
                                relative text-left p-8 rounded-3xl border-2 transition-all duration-300 overflow-hidden
                                ${isSelected
                                    ? `${mode.borderColor} bg-white shadow-2xl scale-[1.02]`
                                    : 'border-[var(--color-neutral-200)] bg-white hover:shadow-xl hover:border-[var(--color-neutral-300)]'}
                            `}
                        >
                            {/* Selection Checkmark */}
                            {isSelected && (
                                <div className={`absolute top-4 right-4 w-8 h-8 rounded-full bg-gradient-to-br ${mode.gradient} flex items-center justify-center animate-fade-in shadow-lg`}>
                                    <Check className="w-5 h-5 text-white" strokeWidth={3} />
                                </div>
                            )}

                            {/* Badge */}
                            <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${mode.badgeColor} mb-6`}>
                                {mode.badge}
                            </div>

                            {/* Icon */}
                            <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${mode.gradient} flex items-center justify-center mb-6 shadow-lg transition-transform duration-300 ${isHovering || isSelected ? 'scale-110' : ''}`}>
                                <Icon className="w-8 h-8 text-white" />
                            </div>

                            {/* Title & Subtitle */}
                            <div className="mb-4">
                                <h3 className="text-2xl font-bold text-[var(--color-neutral-900)]">{mode.title}</h3>
                                <span className={`text-sm font-medium ${mode.textColor}`}>{mode.subtitle}</span>
                            </div>

                            {/* Description */}
                            <p className="text-[var(--color-neutral-500)] mb-6 leading-relaxed">
                                {mode.description}
                            </p>

                            {/* Features */}
                            <div className="space-y-3">
                                {mode.features.map((feature, idx) => (
                                    <div key={idx} className="flex items-center gap-3 text-sm text-[var(--color-neutral-600)]">
                                        <div className={`w-6 h-6 rounded-lg ${mode.bgLight} flex items-center justify-center`}>
                                            <feature.icon className={`w-3.5 h-3.5 ${mode.textColor}`} />
                                        </div>
                                        <span>{feature.text}</span>
                                    </div>
                                ))}
                            </div>

                            {/* Hover Gradient Effect */}
                            <div className={`absolute inset-0 bg-gradient-to-br ${mode.gradient} opacity-0 transition-opacity duration-300 ${isSelected ? 'opacity-[0.03]' : ''}`}></div>
                        </button>
                    );
                })}
            </div>

            {/* Action Button */}
            <div className="flex flex-col items-center gap-4">
                <button
                    onClick={() => selected && onModeSelect(selected)}
                    disabled={!selected}
                    className={`
                        group flex items-center gap-2 px-10 h-14 rounded-2xl font-bold text-lg transition-all duration-300
                        ${selected
                            ? 'bg-gradient-to-r from-[var(--color-primary-600)] to-[var(--color-primary-500)] text-white shadow-xl shadow-[var(--color-primary-500)]/30 hover:shadow-[var(--color-primary-500)]/50 hover:scale-105'
                            : 'bg-[var(--color-neutral-100)] text-[var(--color-neutral-400)] cursor-not-allowed'}
                    `}
                >
                    <span>Continue</span>
                    <ArrowRight className={`w-5 h-5 transition-transform ${selected ? 'group-hover:translate-x-1' : ''}`} />
                </button>

                {!selected && (
                    <p className="text-sm text-[var(--color-neutral-400)]">
                        Select a mode to continue
                    </p>
                )}
            </div>
        </div>
    );
}
