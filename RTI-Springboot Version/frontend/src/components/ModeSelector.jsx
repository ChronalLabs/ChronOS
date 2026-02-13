import React from 'react';

const ModeSelector = ({ currentMode, onModeChange }) => {
    return (
        <div className="flex bg-gray-100 p-1 rounded-lg mb-6">
            <button
                onClick={() => onModeChange('assisted')}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all duration-200 ${currentMode === 'assisted'
                        ? 'bg-white text-indigo-deep shadow-sm ring-1 ring-black/5'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
            >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                Assisted Mode
            </button>
            <button
                onClick={() => onModeChange('ai')}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all duration-200 ${currentMode === 'ai'
                        ? 'bg-indigo-deep text-white shadow-sm'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
            >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                AI Mode
            </button>
        </div>
    );
};

export default ModeSelector;
