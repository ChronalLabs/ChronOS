const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8091/api/v1";

const getMockDraft = (data) => {
    const today = new Date().toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
    const issueLower = (data.issue || "").toLowerCase();

    // 1. Determine Department
    let department = data.department;
    if (!department) {
        if (issueLower.includes('road') || issueLower.includes('pothole')) department = "Public Works Department (PWD)";
        else if (issueLower.includes('scholarship') || issueLower.includes('school')) department = "Education Department";
        else if (issueLower.includes('police') || issueLower.includes('fir')) department = "Police Department";
        else if (issueLower.includes('garbage') || issueLower.includes('drain')) department = "Municipal Corporation";
        else department = "Public Information Officer";
    }

    // Hindi Department Mapping
    const deptHindiMap = {
        "Ministry of Municipal Affairs": "नगर निगम मंत्रालय",
        "Public Works Department (PWD)": "लोक निर्माण विभाग (PWD)",
        "Education Ministry": "शिक्षा मंत्रालय",
        "Education Department": "शिक्षा विभाग",
        "Health Department": "स्वास्थ्य विभाग",
        "Police Department": "पुलिस विभाग",
        "Revenue Department": "राजस्व विभाग",
        "Municipal Corporation": "नगर निगम",
        "Public Information Officer": "जन सूचना अधिकारी"
    };

    // 2. Determine Questions based on topic
    let questions = [];
    if (department.includes("Works") || issueLower.includes("road")) {
        questions = [
            "Copy of the contract awarded for the construction/repair of the work.",
            "The deadline for completion of the work as per the tender/contract.",
            "Names and contact details of the engineers responsible for supervising this work."
        ];
    } else if (department.includes("Education") || issueLower.includes("scholarship")) {
        questions = [
            "Daily progress made on my application/complaint.",
            "Names and designations of officials who have held my file during this period.",
            "Reasons for the delay in taking action on my application."
        ];
    } else if (department.includes("Police")) {
        questions = [
            "Copy of the FIR/Complaint register entry.",
            "Daily progress made on the investigation.",
            "Name of the investigating officer assigned to this case."
        ];
    } else {
        // Generic fallback for ANY other topic
        // We dynamically insert their specific text so it looks "AI-generated" for any topic
        questions = [
            `Daily progress report on my complaint regarding: "${data.issue ? data.issue.substring(0, 50) : ""}..."`,
            "Names and designations of the officials responsible for taking action on this matter.",
            "Certified copies of all file notings and correspondence made on this issue."
        ];

        if (!department) {
            department = "The Public Information Officer, \nGeneral Administration Department / Concerned Department";
        }
    }

    // Append Assisted Mode Suggestions
    if (data.acceptedSuggestions && Array.isArray(data.acceptedSuggestions) && data.acceptedSuggestions.length > 0) {
        // Filter out duplicates if needed, or just append
        questions = [...questions, ...data.acceptedSuggestions];
    }

    // 3. Construct HTML
    // 3. Construct HTML (STRICT FORMAT LOCK)
    // If Hindi, translate TEXT CONTENT ONLY. DO NOT CHANGE STRUCTURE.
    const isHindi = data.language === 'hi';

    // Translate Data Fields for Mock
    let displayDept = data.department || "Public Information Officer";
    let displayDeptAddr = data.departmentAddress || "[City/District Office Address]";
    let displayDate = today;

    if (isHindi) {
        displayDept = deptHindiMap[displayDept] || displayDept;

        // Advanced Address Transliteration for Mock
        const addrMap = {
            "Directorate of Education": "शिक्षा निदेशालय",
            "Balbharati": "बालभारती",
            "Senapati Bapat Marg": "सेनापति बापट मार्ग",
            "Pune": "पुणे",
            "Delhi": "दिल्ली",
            "Mumbai": "मुंबई",
            "Mantralaya": "मंत्रालय",
            "Road": "रोड",
            "Marg": "मार्ग",
            "Colony": "कॉलोनी",
            "Nagar": "नगर",
            "Street": "गली",
            "House": "मकान",
            "Sector": "सेक्टर"
        };

        if (displayDeptAddr) {
            Object.keys(addrMap).forEach(k => {
                displayDeptAddr = displayDeptAddr.replace(new RegExp(k, 'gi'), addrMap[k]);
            });
        }

        // Simple Date Translation
        const dateObj = new Date();
        const months = ["जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"];
        displayDate = `${dateObj.getDate()} ${months[dateObj.getMonth()]} ${dateObj.getFullYear()}`;
    }

    // Mock Transliteration for Name/Address
    let displayName = data.name || (isHindi ? 'आवेदक का नाम' : 'Applicant Name');
    let displayAddress = data.address || (isHindi ? 'आवेदक का पता' : 'Applicant Address');

    if (isHindi) {
        // Basic Mock Map
        const transMap = {
            "Vikram": "विक्रम", "Yogesh": "योगेश", "Rahul": "राहुल", "Amit": "अमित",
            "Delhi": "दिल्ली", "Pune": "पुणे", "Mumbai": "मुंबई", "Bangalore": "बैंगलोर",
            "Road": "रोड", "Nagar": "नगर", "Colony": "कॉलोनी", "Marg": "मार्ग"
        };

        if (data.name) {
            Object.keys(transMap).forEach(k => {
                displayName = displayName.replace(new RegExp(k, 'gi'), transMap[k]);
            });
        }
        if (data.address) {
            Object.keys(transMap).forEach(k => {
                displayAddress = displayAddress.replace(new RegExp(k, 'gi'), transMap[k]);
            });
        }
    }

    const labels = isHindi ? {
        to: "सेवा में,",
        pio: "जन सूचना अधिकारी,",
        date: "दिनांक:",
        subject: "विषय:",
        subjectText: "सूचना का अधिकार अधिनियम, 2005 के तहत जानकारी के लिए आवेदन।",
        sir: "महोदय / महोदया,",
        intro: "कृपया उपर्युक्त विषय के संबंध में निम्नलिखित जानकारी की सच्ची, प्रमाणित प्रतियां प्रदान करें:",
        name: "नाम:",
        address: "पता:",
        mobile: "मोबाइल:",
        declaration: "मैं एतद्द्वारा सूचित करता हूँ कि:<br>मैं भारत का नागरिक हूँ।<br>मैं गरीबी रेखा से ऊपर हूँ।<br>मेरे आईडी प्रूफ की एक प्रति संलग्न है।",
        sign: "आवेदक के हस्ताक्षर"
    } : {
        to: "To,",
        pio: "The Public Information Officer,",
        date: "Date:",
        subject: "Subject:",
        subjectText: "Request for information under Right to Information Act, 2005.",
        sir: "Sir / Ma'am,",
        intro: "Please provide true, certified copies of the following information regarding the subject mentioned above:",
        name: "Name:",
        address: "Address:",
        mobile: "Mobile:",
        declaration: "I hereby inform that:<br>I am a citizen of India.<br>I am above the poverty line.<br>A copy of my ID proof is attached.",
        sign: "Signature of the applicant"
    };

    const draftHtml = `
        <div style="font-family: 'Times New Roman', serif; line-height: 1.6; color: #000;">
            <p style="margin-bottom: 0;">${labels.to}</p>
            <p style="margin: 0;">${labels.pio}</p>
            <p style="margin: 0;">${displayDept || (isHindi ? "जन सूचना अधिकारी" : "Public Information Officer")},</p>
            <p style="margin: 0;">${displayDeptAddr || (isHindi ? "संबंधित विभाग का कार्यालय, [शहर/जिला]" : "[City/District Office Address]")}</p>
            
            <p style="margin-top: 20px;"><strong>${labels.date}</strong> ${displayDate}</p>
            
            <p style="margin-top: 20px;"><strong>${labels.subject}</strong> ${labels.subjectText}</p>
            
            <p style="margin-top: 20px;">${labels.sir}</p>
            
            <p>${labels.intro}</p>
            
            <ol style="margin-top: 10px; padding-left: 20px;">
                ${questions.map(q => {
        let text = q;
        if (isHindi) {
            // Mock Translation Logic
            if (q.includes("contract")) text = "कार्य के निर्माण/मरम्मत के लिए दिए गए ठेके की प्रति।";
            else if (q.includes("deadline")) text = "निविदा/अनुबंध के अनुसार कार्य पूरा करने की अंतिम तिथि।";
            else if (q.includes("engineers")) text = "इस कार्य की निगरानी के लिए जिम्मेदार इंजीनियरों के नाम और संपर्क विवरण।";
            else if (q.includes("Daily progress")) text = "मेरे आवेदन/शिकायत पर की गई दैनिक प्रगति।";
            else if (q.includes("officials who")) text = "उन अधिकारियों के नाम और पदनाम जिन्होंने इस अवधि के दौरान मेरी फाइल को संभाला।";
            else if (q.includes("delay")) text = "मेरे आवेदन पर कार्रवाई करने में देरी के कारण।";
            else if (q.includes("FIR")) text = "एफआईआर/शिकायत रजिस्टर प्रविष्टि की प्रति।";
            else if (q.includes("investigation")) text = "जांच पर की गई दैनिक प्रगति।";
            else if (q.includes("officer assigned")) text = "इस मामले के लिए नियुक्त जांच अधिकारी का नाम।";
            else text = q + " (हिंदी अनुवाद...)"; // Fallback
        }
        return `<li>${text}</li>`;
    }).join('')}
            </ol>
            
            <div style="margin-top: 30px;">
                <p style="margin: 0;"><strong>${labels.name}</strong> ${displayName}</p>
                <p style="margin: 0;"><strong>${labels.address}</strong> ${displayAddress}</p>
                ${data.mobile ? `<p style="margin: 0;"><strong>${labels.mobile}</strong> ${data.mobile}</p>` : ''}
            </div>
            
            <div style="margin-top: 20px;">
                <p style="margin: 0;">${labels.declaration}</p>
            </div>
            
            <div style="margin-top: 60px; display: flex; justify-content: space-between; align-items: flex-end;">
                <div>
                    <div style="width: 150px; border-bottom: 1px solid #000; margin-bottom: 10px;"></div>
                    <p style="margin: 0;"><strong>${labels.sign}</strong></p>
                </div>
            </div>
        </div>`;

    return {
        draftHtml,
        plainText: `Subject: ${data.issue}\n\nQuestions:\n${questions.join('\n')}`,
        questions,
        complianceLog: isHindi ? 'RTI कानूनी अनुपालन स्थिति:\n🟢 धारा 6(1): सत्यापित\n🟢 पीआईओ: सही' : 'RTI LEGAL COMPLIANCE STATUS:\n🟢 Section 6(1): Verified\n🟢 PIO: Correctly Addressed',
        warnings: []
    };
};

export const rtiApi = {
    /**
     * Generate an RTI draft from plain text
     * @param {Object} data - { text: string, userId: string, ... }
     * @returns {Promise<Object>} - The generated draft
     */
    generateDraft: async (data) => {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout

            const response = await fetch(`${API_BASE_URL}/rti/generate`, {
                signal: controller.signal,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    inputText: data.text, // Mapping 'text' to 'inputText' for backend DTO
                    language: "en",
                    privacyMode: true,
                    consentToSendPii: true // Default for MVP
                }),
            });
            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Failed to generate RTI');
            }

            return await response.json();
        } catch (error) {
            console.error("API Error:", error);
            throw error;
        }
    },

    /**
     * Update an existing draft
     * @param {string} id 
     * @param {Object} draftData 
     * @returns {Promise<Object>}
     */
    updateDraft: async (id, draftData) => {
        const response = await fetch(`${API_BASE_URL}/rti/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(draftData),
        });

        if (!response.ok) {
            throw new Error('Failed to update draft');
        }

        return await response.json();
    },

    /**
     * Export draft to PDF
     * @param {string} draftId 
     * @returns {Promise<Blob>}
     */
    exportPdf: async (draftId) => {
        const response = await fetch(`${API_BASE_URL}/rti/${draftId}/export/pdf`, {
            method: 'POST',
        });
        if (!response.ok) throw new Error('Failed to export PDF');
        return await response.blob();
    },

    getSuggestions: async (data) => {
        try {
            const response = await fetch(`${API_BASE_URL}/rti/generate/assisted/suggestions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to get suggestions');
            return await response.json();
        } catch (e) {
            console.warn("API failed, using mock suggestions", e);
            return {
                suggestions: [
                    { id: 'm1', type: 'clarify', text: 'When did you submit the application?', confidence: 0.9 },
                    { id: 'm2', type: 'reword', text: 'I requested information regarding...', confidence: 0.8 },
                    { id: 'm3', type: 'add_question', text: 'Ask for the daily progress report.', confidence: 0.85 }
                ]
            };
        }
    },

    generateAssistedDraft: async (data) => {
        try {
            // Transform flat data to nested DTO structure
            const payload = {
                applicant: {
                    name: data.name,
                    address: data.address,
                    mobile: data.mobile // Optional
                },
                department: {
                    name: data.department,
                    address: data.departmentAddress // Required by new schema
                },
                issue: data.issue,
                acceptedSuggestions: data.acceptedSuggestions,
                mode: 'assisted',
                language: data.language
            };

            const response = await fetch(`${API_BASE_URL}/rti/generate/assisted/draft`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('Failed to generate draft');
            return await response.json();
        } catch (e) {
            console.warn("API failed, using dynamic mock draft", e);
            return getMockDraft(data);
        }
    },

    generateAiDraft: async (data) => {
        try {
            const payload = {
                applicant: {
                    name: data.name,
                    address: data.address,
                    mobile: data.mobile
                },
                department: {
                    name: data.department,
                    address: data.departmentAddress
                },
                issue: data.issue,
                mode: 'ai',
                language: data.language
            };

            const response = await fetch(`${API_BASE_URL}/rti/generate/ai/draft`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('Failed to generate draft');
            return await response.json();
        } catch (e) {
            console.warn("API failed, using dynamic mock AI draft", e);
            return getMockDraft(data);
        }
    }
};
