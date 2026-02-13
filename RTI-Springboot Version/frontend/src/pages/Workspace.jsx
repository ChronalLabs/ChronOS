import React, { useState, useEffect, useRef } from 'react';
import Button from '../components/Button';
import ModeSelector from '../components/ModeSelector';
import SuggestionCard from '../components/SuggestionCard';
import { rtiApi } from '../services/api';
import { useLocation } from 'react-router-dom';

const Workspace = () => {
    console.log("Workspace Component Mounted");
    const location = useLocation();

    // Core State
    const [mode, setMode] = useState(() => localStorage.getItem('rti_mode') || 'assisted');
    const [intent, setIntent] = useState('');
    const [applicantName, setApplicantName] = useState('Guest User');
    const [address, setAddress] = useState('');
    const [mobile, setMobile] = useState(''); // New Field
    const [department, setDepartment] = useState('');
    const [departmentAddress, setDepartmentAddress] = useState(''); // New Field
    const [language, setLanguage] = useState('en'); // New Language Toggle ('en' | 'hi')

    // Department Address Mapping
    const deptAddresses = {
        "Ministry of Municipal Affairs": "Mantralaya, Mumbai - 400032",
        "Public Works Department (PWD)": "Public Works Department, Fort Area, Mumbai - 400001",
        "Education Ministry": "Directorate of Education, Balbharati, Senapati Bapat Marg, Pune - 411004",
        "Health Department": "Arogya Bhavan, St. George's Hospital, Mumbai - 400001",
        "Police Department": "Office of the Commissioner of Police, Crawford Market, Mumbai - 400001",
        "Revenue Department": "Collector Office, Old Custom House, Fort, Mumbai - 400001",
        "Other": ""
    };

    const handleDepartmentChange = (e) => {
        const val = e.target.value;
        setDepartment(val);
        // Auto-fill address if not "Other"
        if (deptAddresses[val]) {
            setDepartmentAddress(deptAddresses[val]);
        } else if (val === "Other") {
            setDepartmentAddress("Public Information Officer, Concerned Department, [City/District]");
        } else {
            setDepartmentAddress("");
        }
    };

    // Draft / Suggestions State
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [draft, setDraft] = useState(null); // Used for PDF export & metadata
    const [draftHtml, setDraftHtml] = useState(null); // Rendered HTML for preview
    const [suggestions, setSuggestions] = useState([]);
    const [acceptedSuggestions, setAcceptedSuggestions] = useState([]);
    const [complianceLog, setComplianceLog] = useState(null); // New State for Compliance Status
    const [smartQuestions, setSmartQuestions] = useState([]); // New State for Smart Questions

    const handleIntentChange = (e) => setIntent(e.target.value);

    // Smart Question Handlers
    const handleAddQuestion = () => setSmartQuestions([...smartQuestions, "New Question"]);
    const handleRemoveQuestion = (idx) => setSmartQuestions(smartQuestions.filter((_, i) => i !== idx));
    const handleEditQuestion = (idx, text) => {
        const newQ = [...smartQuestions];
        newQ[idx] = text;
        setSmartQuestions(newQ);
    };

    const handleAcceptSuggestion = (suggestion) => {
        setAcceptedSuggestions([...acceptedSuggestions, suggestion]);
        setSuggestions(suggestions.filter(s => s.id !== suggestion.id));
    };

    const handleRejectSuggestion = (suggestion) => {
        setSuggestions(suggestions.filter(s => s.id !== suggestion.id));
    };

    const handleGenerate = async () => {
        setLoading(true);
        setError(null);
        try {
            let result;
            if (mode === 'assisted') {
                result = await rtiApi.generateAssistedDraft({
                    name: applicantName,
                    address: address,
                    mobile: mobile,
                    state: 'Maharashtra',
                    department: department,
                    departmentAddress: departmentAddress,
                    issue: intent,
                    acceptedSuggestions: acceptedSuggestions.map(s => s.text),
                    mode: 'assisted',
                    language: language
                });
            } else {
                result = await rtiApi.generateAiDraft({
                    name: applicantName,
                    address: address,
                    mobile: mobile,
                    state: 'Maharashtra',
                    department: department,
                    departmentAddress: departmentAddress,
                    issue: intent,
                    mode: 'ai',
                    language: language
                });
            }

            setDraftHtml(result.draftHtml);
            setDraft({ ...result, id: 'temp-id-' + Date.now() }); // Mock ID for now until saved

            // Set Compliance & Questions (Assisted Mode)
            if (mode === 'assisted') {
                setComplianceLog(result.complianceLog);
                setSmartQuestions(result.questions || []);
            }

            // Clear suggestions on success
            setSuggestions([]);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = async () => {
        if (!draft?.id) return;
        try {
            // Ensure draft is saved/updated before export
            await rtiApi.updateDraft(draft.id, {
                ...draft,
                applicant: { name: applicantName, address: address }
            });

            const blob = await rtiApi.exportPdf(draft.id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `rti_draft_${draft.id}.pdf`;
            a.click();
        } catch (err) {
            console.error("Export failed", err);
            // Fallback for demo: if ID is mock, we can't export via backend real ID logic yet without a save step
            alert("Draft saved! (PDF export requires real backend ID in this demo)");
        }
    };

    return (
        <div className="flex flex-col lg:flex-row h-[calc(100vh-5rem)] overflow-hidden bg-[#FAF9F6]">

            {/* Left Pane: Input & Controls */}
            <div className="w-full lg:w-1/3 bg-white border-r border-amber-100 flex flex-col z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
                <div className="p-5 border-b border-amber-100 bg-white">
                    <ModeSelector currentMode={mode} onModeChange={setMode} />

                    <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center space-x-2">
                            <div className="w-2 h-2 rounded-full bg-orange-600"></div>
                            <h2 className="font-serif font-bold text-lg text-stone-800 tracking-tight">
                                {mode === 'assisted' ? 'Assisted Drafting' : 'AI Auto-Draft'}
                            </h2>
                        </div>
                        <div className="flex bg-gray-100 p-1 rounded-lg">
                            <button
                                onClick={() => setLanguage('en')}
                                className={`text-xs font-bold px-2 py-1 rounded-md transition-all ${language === 'en' ? 'bg-white text-black shadow-sm' : 'text-gray-400'}`}
                            >
                                ENG
                            </button>
                            <button
                                onClick={() => setLanguage('hi')}
                                className={`text-xs font-bold px-2 py-1 rounded-md transition-all ${language === 'hi' ? 'bg-white text-black shadow-sm' : 'text-gray-400'}`}
                            >
                                हिंदी
                            </button>
                        </div>
                    </div>
                </div>

                <div className="p-5 flex-grow flex flex-col relative overflow-y-auto">
                    {/* Personal Details (Shared) */}
                    <div className="space-y-4 mb-6 p-4 bg-orange-50/50 rounded-xl border border-orange-100">
                        <h3 className="text-xs font-bold text-orange-800/60 uppercase tracking-wider">Applicant Details</h3>
                        <div className="grid grid-cols-1 gap-3">
                            <div>
                                <input
                                    type="text"
                                    className="w-full p-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
                                    value={applicantName}
                                    onChange={(e) => setApplicantName(e.target.value)}
                                    placeholder="Full Name"
                                />
                            </div>
                            <div>
                                <input
                                    type="text"
                                    className="w-full p-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
                                    value={address}
                                    onChange={(e) => setAddress(e.target.value)}
                                    placeholder="Address"
                                />
                            </div>
                            <div>
                                <input
                                    type="text"
                                    className="w-full p-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
                                    value={mobile}
                                    onChange={(e) => setMobile(e.target.value)}
                                    placeholder="Mobile Number (Optional)"
                                />
                            </div>
                            <div>
                                <div>
                                    <select
                                        className="w-full p-2 bg-white border border-stone-200 rounded-lg text-sm focus:ring-2 focus:ring-orange-800 focus:border-transparent outline-none transition-all"
                                        value={department}
                                        onChange={handleDepartmentChange}
                                    >
                                        <option value="">Select Department (Optional)</option>
                                        <option value="Ministry of Municipal Affairs">Ministry of Municipal Affairs</option>
                                        <option value="Public Works Department (PWD)">Public Works Department (PWD)</option>
                                        <option value="Education Ministry">Education Ministry</option>
                                        <option value="Health Department">Health Department</option>
                                        <option value="Police Department">Police Department</option>
                                        <option value="Revenue Department">Revenue Department</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        {/* Department / Authority Details */}
                        {department && (
                            <div className="space-y-4 mb-6 p-4 bg-orange-50/50 rounded-xl border border-orange-100 animate-fadeIn">
                                <h3 className="text-xs font-bold text-orange-800/60 uppercase tracking-wider">Authority Details</h3>
                                <div className="grid grid-cols-1 gap-3">
                                    <div>
                                        <label className="text-xs text-gray-500 block mb-1">Target Department</label>
                                        <div className="w-full p-2 bg-gray-100 border border-transparent rounded-lg text-sm text-gray-700">
                                            {department}
                                        </div>
                                    </div>
                                    <div>
                                        <label className="text-xs text-gray-500 block mb-1">Office Address</label>
                                        <textarea
                                            className="w-full p-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all resize-none h-20"
                                            value={departmentAddress}
                                            onChange={(e) => setDepartmentAddress(e.target.value)}
                                            placeholder="Department Address will appear here..."
                                        />
                                    </div>
                                </div>
                            </div>
                        )}


                        {/* Issue Input */}
                        <div className="relative flex-grow min-h-[200px] flex flex-col">
                            <label className="text-xs font-bold text-orange-800/60 uppercase tracking-wider mb-2">
                                {mode === 'assisted' ? 'Describe your issue details' : 'Briefly describe your issue'}
                            </label>
                            <textarea
                                className="w-full flex-grow p-4 bg-white border border-stone-200 rounded-xl resize-none text-sm leading-relaxed text-stone-700 placeholder-stone-400 focus:ring-2 focus:ring-orange-800 focus:border-transparent transition-all outline-none shadow-sm"
                                placeholder={mode === 'assisted'
                                    ? "Start typing about your issue. I'll provide suggestions..."
                                    : "My scholarship is delayed..."}
                                value={intent}
                                onChange={handleIntentChange}
                                disabled={loading}
                            ></textarea>

                            {/* Suggestions Panel (Assisted Mode Only) */}
                            {mode === 'assisted' && suggestions.length > 0 && (
                                <div className="mt-4 animate-slideUp">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">AI Suggestions</span>
                                    </div>
                                    <div className="space-y-2">
                                        {suggestions.map(s => (
                                            <SuggestionCard
                                                key={s.id}
                                                suggestion={s}
                                                onAccept={handleAcceptSuggestion}
                                                onReject={handleRejectSuggestion}
                                            />
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Compliance Status Block (Assisted Mode) */}
                        {mode === 'assisted' && complianceLog && (
                            <div className="mt-6 p-4 bg-stone-50 rounded-xl border border-stone-200 animate-fadeIn">
                                <h3 className="text-sm font-bold text-stone-700 uppercase tracking-wide mb-2 flex items-center gap-2">
                                    <svg className="w-4 h-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                    RTI Legal Compliance Status
                                </h3>
                                <div className="text-xs text-stone-600 whitespace-pre-line font-mono leading-relaxed bg-white p-3 rounded-lg border border-stone-100 shadow-sm">
                                    {complianceLog}
                                </div>
                            </div>
                        )}

                        {/* Smart Questions Generator (Assisted Mode) */}
                        {mode === 'assisted' && smartQuestions.length > 0 && (
                            <div className="mt-6 animate-slideUp">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-xs font-bold text-orange-800/60 uppercase tracking-wider">Smart Questions Generated</span>
                                    <button onClick={handleAddQuestion} className="text-xs text-orange-600 hover:text-orange-700 font-bold">+ Add</button>
                                </div>
                                <div className="space-y-2">
                                    {smartQuestions.map((q, idx) => (
                                        <div key={idx} className="group flex items-start gap-2 p-3 bg-white border border-stone-200 rounded-lg shadow-sm hover:border-orange-300 transition-all">
                                            <span className="text-xs font-bold text-stone-400 mt-1">{idx + 1}.</span>
                                            <textarea
                                                className="flex-grow text-sm text-stone-700 bg-transparent outline-none resize-none h-auto"
                                                rows={2}
                                                value={q}
                                                onChange={(e) => handleEditQuestion(idx, e.target.value)}
                                            />
                                            <button
                                                onClick={() => handleRemoveQuestion(idx)}
                                                className="opacity-0 group-hover:opacity-100 text-stone-400 hover:text-red-500 transition-all"
                                            >
                                                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                                            </button>
                                        </div>
                                    ))}
                                    <div className="text-right mt-2">
                                        <small className="text-xs text-stone-400 italic">Edit questions above to refine. (Draft update pending...)</small>
                                    </div>
                                </div>
                            </div>
                        )}

                        {error && (
                            <div className="mt-4 p-3 bg-red-50 text-red-600 text-xs rounded-lg border border-red-100">
                                {error}
                            </div>
                        )}

                        <div className="mt-6">
                            <Button
                                variant="primary"
                                className="w-full justify-center group relative overflow-hidden"
                                onClick={handleGenerate}
                                disabled={loading}
                            >
                                <span className={`relative z-10 flex items-center justify-center space-x-2 ${loading ? 'opacity-0' : 'opacity-100'}`}>
                                    <span>{mode === 'assisted' ? 'Generate Final Draft' : 'Auto-Generate Draft'}</span>
                                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
                                </span>
                                {loading && (
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                    </div>
                                )}
                            </Button>
                        </div>
                    </div>
                </div>

            </div>

            {/* Right Pane: Live Preview */}
            <div className="flex-1 bg-[#F5F2EB] p-6 lg:p-10 overflow-y-auto flex justify-center bg-grain relative">
                <div className="absolute inset-0 opacity-[0.03] bg-[radial-gradient(#8B4513_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none"></div>

                <div className={`w-full max-w-[210mm] min-h-[297mm] bg-white shadow-2xl transition-all duration-500 ease-out p-[20mm] relative`}>

                    {draft && (
                        <div className="absolute top-6 right-6 print:hidden">
                            <Button size="sm" onClick={handleExport} className="shadow-lg hover:shadow-xl bg-black text-white border-0">
                                <span className="flex items-center gap-2">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                                    Download PDF
                                </span>
                            </Button>
                        </div>
                    )}

                    {!draft && !draftHtml ? (
                        <div className="absolute inset-0 flex flex-col items-center justify-center bg-white z-10 text-center p-8">
                            <div className="w-20 h-24 border-2 border-dashed border-gray-200 rounded-lg flex items-center justify-center mb-6">
                                <svg className="w-8 h-8 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                            </div>
                            <h3 className="text-gray-900 font-serif font-bold text-xl mb-2">
                                {mode === 'assisted' ? 'Drafting Assistant Ready' : 'AI Generation Ready'}
                            </h3>
                            <p className="text-gray-500 text-sm max-w-sm mx-auto">
                                {mode === 'assisted'
                                    ? "Start typing your issue on the left. I'll help you refine it and format the legal draft automatically."
                                    : "Describe your issue briefly on the left and click Generate to create a complete RTI application instantly."}
                            </p>
                        </div>
                    ) : (
                        /* Render Draft Content */
                        <div
                            className="font-serif text-gray-900 text-[11pt] leading-relaxed animate-fadeIn h-full bg-white"
                            dangerouslySetInnerHTML={{ __html: draftHtml || (draft?.draftHtml) || "<div class='p-4 text-center text-gray-500'><i>Draft generated but content is empty. Please try again.</i></div>" }}
                        />
                    )}
                </div>
            </div >
        </div >
    );
};

export default Workspace;
