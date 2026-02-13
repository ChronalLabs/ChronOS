import React from 'react';

const SuggestionCard = ({ suggestion, onAccept, onReject }) => {
    return (
        <div className="bg-white border border-indigo-100 rounded-xl p-4 shadow-sm hover:shadow-md transition-all animate-fadeIn mb-3">
            <div className="flex items-start gap-3">
                <div className={`mt-1 w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${suggestion.type === 'clarify' ? 'bg-amber-100 text-amber-600' : 'bg-indigo-100 text-indigo-600'
                    }`}>
                    {suggestion.type === 'clarify' ? (
                        <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    ) : (
                        <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                    )}
                </div>
                <div className="flex-grow">
                    <p className="text-sm text-gray-700 leading-snug mb-3">{suggestion.text}</p>
                    <div className="flex gap-2">
                        <button
                            onClick={() => onAccept(suggestion)}
                            className="text-xs font-medium px-3 py-1.5 bg-indigo-50 text-indigo-700 rounded-md hover:bg-indigo-100 transition-colors"
                        >
                            {suggestion.type === 'clarify' ? 'Answer' : 'Accept'}
                        </button>
                        <button
                            onClick={() => onReject(suggestion)}
                            className="text-xs font-medium px-3 py-1.5 text-gray-400 hover:text-gray-600 transition-colors"
                        >
                            Dismiss
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SuggestionCard;
