import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, BookOpen, Target, FileText, Scale, Info } from 'lucide-react';
import './ExplainWhyPanel.css';

// Explanations for RTI questions and structure
const RTI_EXPLANATIONS = {
  en: {
    addressee: {
      title: 'Public Information Officer (PIO)',
      icon: Target,
      why: 'Under Section 5 of RTI Act, every public authority must designate a PIO. Your application must be addressed to the correct PIO.',
      what: 'The PIO is responsible for receiving your application, collecting information from various units, and providing the response within 30 days.',
      tip: 'If unsure about the PIO, address to "The Public Information Officer" of the concerned department.'
    },
    subject: {
      title: 'Subject Line',
      icon: FileText,
      why: 'A clear subject helps the PIO understand your request quickly and route it to the correct section.',
      what: 'The subject should briefly state what information you are seeking and the relevant time period.',
      tip: 'Keep it under 15 words. Example: "RTI Application - Road Construction Details for FY 2023-24"'
    },
    citizenship: {
      title: 'Citizenship Declaration',
      icon: Scale,
      why: 'Section 3 of RTI Act grants the right to information only to citizens of India. This declaration is legally mandatory.',
      what: 'By stating "I am a citizen of India", you confirm your eligibility to file RTI.',
      tip: 'This statement cannot be removed - it is legally required.'
    },
    section6: {
      title: 'Section 6(1) Reference',
      icon: BookOpen,
      why: 'Section 6(1) of the RTI Act allows any citizen to request information from any public authority.',
      what: 'Citing this section establishes the legal basis for your request and reminds the PIO of their legal obligation.',
      tip: 'Keep this reference - it strengthens your application legally.'
    },
    information_sought: {
      title: 'Information Sought',
      icon: HelpCircle,
      why: 'This is the core of your RTI. Clear, specific questions get better responses.',
      what: 'List each piece of information you need as a separate numbered point.',
      tip: 'Ask "what, when, who, how much" questions. Avoid vague terms like "all related documents".'
    },
    time_period: {
      title: 'Time Period',
      icon: FileText,
      why: 'Without a time period, your request may be rejected as too broad (Section 7).',
      what: 'Specifies the date range for which you need information.',
      tip: 'Be specific: "FY 2023-24" or "January 2023 to December 2023" instead of "recent years".'
    },
    fee: {
      title: 'RTI Fee',
      icon: Scale,
      why: 'Section 7 requires a fee of ₹10 for RTI applications (waived for BPL applicants).',
      what: 'The fee can be paid via IPO, DD, or online (where available).',
      tip: 'Mention the payment mode and details. Keep proof of payment.'
    },
    declaration: {
      title: 'Final Declaration',
      icon: BookOpen,
      why: 'Confirms your request is in good faith and you will pay additional copying charges if needed.',
      what: 'Standard closing statement acknowledging RTI rules and your commitment to pay fees.',
      tip: 'This is a standard clause - no changes needed.'
    }
  },
  hi: {
    addressee: {
      title: 'लोक सूचना अधिकारी (PIO)',
      icon: Target,
      why: 'RTI अधिनियम की धारा 5 के तहत, प्रत्येक लोक प्राधिकरण को एक PIO नामित करना होता है। आपका आवेदन सही PIO को संबोधित होना चाहिए।',
      what: 'PIO आपका आवेदन प्राप्त करने, विभिन्न इकाइयों से जानकारी एकत्र करने और 30 दिनों के भीतर जवाब देने के लिए जिम्मेदार है।',
      tip: 'यदि PIO के बारे में अनिश्चित हैं, तो संबंधित विभाग के "लोक सूचना अधिकारी" को संबोधित करें।'
    },
    subject: {
      title: 'विषय पंक्ति',
      icon: FileText,
      why: 'एक स्पष्ट विषय PIO को आपके अनुरोध को जल्दी समझने और सही अनुभाग में भेजने में मदद करता है।',
      what: 'विषय में संक्षेप में बताएं कि आप कौन सी जानकारी मांग रहे हैं और संबंधित समय अवधि।',
      tip: '15 शब्दों से कम रखें। उदाहरण: "RTI आवेदन - वित्त वर्ष 2023-24 के लिए सड़क निर्माण विवरण"'
    },
    citizenship: {
      title: 'नागरिकता घोषणा',
      icon: Scale,
      why: 'RTI अधिनियम की धारा 3 केवल भारत के नागरिकों को सूचना का अधिकार देती है। यह घोषणा कानूनी रूप से अनिवार्य है।',
      what: '"मैं भारत का नागरिक हूं" कहकर, आप RTI दाखिल करने की अपनी पात्रता की पुष्टि करते हैं।',
      tip: 'यह कथन नहीं हटाया जा सकता - यह कानूनी रूप से आवश्यक है।'
    },
    section6: {
      title: 'धारा 6(1) संदर्भ',
      icon: BookOpen,
      why: 'RTI अधिनियम की धारा 6(1) किसी भी नागरिक को किसी भी लोक प्राधिकरण से जानकारी का अनुरोध करने की अनुमति देती है।',
      what: 'इस धारा का उल्लेख आपके अनुरोध का कानूनी आधार स्थापित करता है।',
      tip: 'इस संदर्भ को रखें - यह कानूनी रूप से आपके आवेदन को मजबूत करता है।'
    },
    information_sought: {
      title: 'मांगी गई जानकारी',
      icon: HelpCircle,
      why: 'यह आपके RTI का मूल है। स्पष्ट, विशिष्ट प्रश्न बेहतर प्रतिक्रिया प्राप्त करते हैं।',
      what: 'प्रत्येक जानकारी को अलग क्रमांकित बिंदु के रूप में सूचीबद्ध करें।',
      tip: '"क्या, कब, कौन, कितना" जैसे प्रश्न पूछें। "सभी संबंधित दस्तावेज" जैसे अस्पष्ट शब्दों से बचें।'
    },
    time_period: {
      title: 'समय अवधि',
      icon: FileText,
      why: 'बिना समय अवधि के, आपका अनुरोध बहुत व्यापक होने के कारण अस्वीकार किया जा सकता है (धारा 7)।',
      what: 'उस तारीख सीमा को निर्दिष्ट करता है जिसके लिए आपको जानकारी चाहिए।',
      tip: 'विशिष्ट रहें: "हाल के वर्षों" के बजाय "वित्त वर्ष 2023-24" या "जनवरी 2023 से दिसंबर 2023"।'
    },
    fee: {
      title: 'RTI शुल्क',
      icon: Scale,
      why: 'धारा 7 के तहत RTI आवेदन के लिए ₹10 का शुल्क आवश्यक है (BPL आवेदकों के लिए छूट)।',
      what: 'शुल्क IPO, DD या ऑनलाइन (जहां उपलब्ध हो) के माध्यम से भुगतान किया जा सकता है।',
      tip: 'भुगतान मोड और विवरण का उल्लेख करें। भुगतान का प्रमाण रखें।'
    },
    declaration: {
      title: 'अंतिम घोषणा',
      icon: BookOpen,
      why: 'पुष्टि करता है कि आपका अनुरोध सद्भाव में है और आप आवश्यकता पड़ने पर अतिरिक्त प्रतिलिपि शुल्क का भुगतान करेंगे।',
      what: 'RTI नियमों को स्वीकार करने वाला मानक समापन कथन।',
      tip: 'यह एक मानक खंड है - किसी बदलाव की आवश्यकता नहीं।'
    }
  }
};

const ExplainWhyPanel = ({ language = 'english', draftType = 'rti', activeSections = [] }) => {
  const [expandedSection, setExpandedSection] = useState(null);
  const isHindi = language === 'hindi';
  const explanations = isHindi ? RTI_EXPLANATIONS.hi : RTI_EXPLANATIONS.en;

  const toggleSection = (sectionKey) => {
    setExpandedSection(expandedSection === sectionKey ? null : sectionKey);
  };

  // Filter to show only relevant sections
  const sectionsToShow = activeSections.length > 0 
    ? activeSections 
    : Object.keys(explanations);

  return (
    <div className="explain-why-panel">
      <div className="panel-header">
        <BookOpen size={18} />
        <h3>{isHindi ? 'प्रत्येक भाग क्यों महत्वपूर्ण है' : 'Why Each Section Matters'}</h3>
      </div>

      <p className="panel-intro">
        {isHindi 
          ? 'RTI के प्रत्येक भाग का एक विशिष्ट कानूनी उद्देश्य है। समझें कि प्रत्येक अनुभाग क्या करता है।'
          : 'Each part of your RTI has a specific legal purpose. Understand what each section does.'}
      </p>

      <div className="explanations-list">
        {sectionsToShow.map((sectionKey) => {
          const section = explanations[sectionKey];
          if (!section) return null;
          
          const Icon = section.icon;
          const isExpanded = expandedSection === sectionKey;

          return (
            <div key={sectionKey} className={`explanation-item ${isExpanded ? 'expanded' : ''}`}>
              <button 
                className="explanation-header"
                onClick={() => toggleSection(sectionKey)}
              >
                <div className="header-left">
                  <Icon size={16} className="section-icon" />
                  <span className="section-title">{section.title}</span>
                </div>
                {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </button>

              {isExpanded && (
                <div className="explanation-content">
                  <div className="explanation-block">
                    <div className="block-label">
                      <HelpCircle size={14} />
                      {isHindi ? 'यह क्यों है?' : 'Why is this here?'}
                    </div>
                    <p>{section.why}</p>
                  </div>

                  <div className="explanation-block">
                    <div className="block-label">
                      <FileText size={14} />
                      {isHindi ? 'यह क्या करता है?' : 'What does it do?'}
                    </div>
                    <p>{section.what}</p>
                  </div>

                  <div className="explanation-tip">
                    <Info size={14} />
                    <span><strong>{isHindi ? 'सुझाव:' : 'Tip:'}</strong> {section.tip}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="legal-note">
        <Scale size={14} />
        <span>
          {isHindi 
            ? 'RTI अधिनियम 2005 के तहत, आपको 30 दिनों के भीतर जवाब पाने का अधिकार है।'
            : 'Under RTI Act 2005, you have the right to receive a response within 30 days.'}
        </span>
      </div>
    </div>
  );
};

export default ExplainWhyPanel;
