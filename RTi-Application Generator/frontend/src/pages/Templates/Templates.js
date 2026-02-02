import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FileText, Search, Copy, ArrowRight, Building2, Zap, Droplets, MapPin, Shield, HeartPulse, GraduationCap, Train, Globe, ArrowLeft, BookOpen, Scale, CheckCircle2 } from 'lucide-react';
import { toast } from 'react-toastify';
import './Templates.css';

// Sample templates organized by department
const SAMPLE_TEMPLATES = [
  {
    id: 'rti-pwd-roads',
    category: 'RTI',
    department: 'Public Works Department (PWD)',
    icon: MapPin,
    title: 'Road Construction Expenditure',
    description: 'Request details about road construction costs, contractor information, and project timelines.',
    sampleText: `I want to know the complete details of the road construction/repair work carried out in [YOUR AREA] during [TIME PERIOD]. Please provide:

1. Total budget sanctioned for the project
2. Name and address of the contractor awarded the work
3. Date of commencement and completion of work
4. Itemized expenditure details
5. Quality inspection reports, if any
6. Copies of work completion certificates`,
    tags: ['roads', 'construction', 'budget', 'contractor']
  },
  {
    id: 'rti-electricity-bills',
    category: 'RTI',
    department: 'Electricity Department',
    icon: Zap,
    title: 'Electricity Connection & Bills',
    description: 'Request information about electricity connections, meter readings, and billing details.',
    sampleText: `I request the following information regarding electricity supply in [YOUR AREA/CONSUMER NUMBER]:

1. Details of electricity tariff applicable to domestic/commercial consumers
2. Criteria for load sanctioning and connection approval
3. Details of power outages in the last 6 months with reasons
4. Subsidy amount, if any, provided to consumers
5. Procedure for filing complaints and average resolution time`,
    tags: ['electricity', 'bills', 'power', 'tariff']
  },
  {
    id: 'rti-water-supply',
    category: 'RTI',
    department: 'Water Supply Department',
    icon: Droplets,
    title: 'Water Supply & Quality',
    description: 'Request information about water supply schedules, quality reports, and infrastructure.',
    sampleText: `I request the following information regarding water supply in [YOUR LOCALITY]:

1. Daily water supply schedule and duration
2. Water quality test reports for the last 12 months
3. Details of water treatment plants serving this area
4. Number of complaints received and resolved in the last year
5. Future plans for improving water supply infrastructure
6. Per capita water availability as per government norms`,
    tags: ['water', 'supply', 'quality', 'municipal']
  },
  {
    id: 'complaint-police',
    category: 'Complaint',
    department: 'Police Department',
    icon: Shield,
    title: 'Law & Order Issue',
    description: 'File a complaint about law and order issues, nuisance, or security concerns.',
    sampleText: `I wish to bring to your notice a serious law and order issue in [YOUR AREA]:

Nature of Problem:
[Describe the issue - e.g., illegal parking, noise pollution, suspicious activities, eve-teasing, etc.]

Location: [Exact address/landmark]
Time of Occurrence: [When does this usually happen]
Duration: This has been going on since [DATE]

Impact:
- [How it affects you and the community]
- [Any safety concerns]

I request immediate patrolling and necessary action to resolve this issue. I am willing to provide any additional information required.`,
    tags: ['police', 'security', 'law', 'complaint']
  },
  {
    id: 'complaint-hospital',
    category: 'Complaint',
    department: 'Health Department',
    icon: HeartPulse,
    title: 'Government Hospital Services',
    description: 'File a complaint about hospital services, staff behavior, or medical facilities.',
    sampleText: `I wish to file a complaint regarding the services at [HOSPITAL NAME]:

Date of Visit: [DATE]
OPD/Ward Number: [IF APPLICABLE]

Issues Faced:
1. [Describe issue - e.g., long waiting time, unavailability of medicines, staff behavior]
2. [Any other issues]

Details:
[Provide specific details of the incident including names of staff if known]

Expected Resolution:
- Improvement in services
- Disciplinary action against concerned staff (if applicable)
- Written explanation

I request your immediate intervention to ensure patients receive proper care and treatment.`,
    tags: ['hospital', 'health', 'medical', 'services']
  },
  {
    id: 'rti-education',
    category: 'RTI',
    department: 'Education Department',
    icon: GraduationCap,
    title: 'School Infrastructure & Funds',
    description: 'Request information about school funds, teacher appointments, and infrastructure.',
    sampleText: `I request the following information regarding [SCHOOL NAME / DISTRICT SCHOOLS]:

1. Total funds allocated under Sarva Shiksha Abhiyan / Samagra Shiksha for the year [YEAR]
2. Number of sanctioned vs. working teachers
3. Details of Mid-Day Meal scheme implementation and funds utilized
4. Infrastructure development works undertaken in the last 2 years
5. Student enrollment and dropout rates for the last 3 years
6. Availability of basic amenities (toilets, drinking water, library)`,
    tags: ['education', 'school', 'teachers', 'funds']
  },
  {
    id: 'complaint-municipal',
    category: 'Complaint',
    department: 'Municipal Corporation',
    icon: Building2,
    title: 'Garbage & Sanitation',
    description: 'File a complaint about garbage collection, drainage, or sanitation issues.',
    sampleText: `I wish to bring to your urgent attention a sanitation issue in [YOUR LOCALITY]:

Problem: [Irregular garbage collection / Overflowing drain / Open dumping]

Location: [Complete address with landmarks]

Details:
- Garbage has not been collected since [DATE/DAYS]
- [Describe the current condition]
- [Health hazards being faced]

Impact on Residents:
- Foul smell making it difficult to live
- Breeding of mosquitoes and flies
- Risk of diseases

I request immediate action to:
1. Clear the accumulated garbage/unclog the drain
2. Ensure regular collection/maintenance going forward
3. Take action against those responsible for the lapse`,
    tags: ['garbage', 'sanitation', 'municipal', 'drainage']
  },
  {
    id: 'rti-railway',
    category: 'RTI',
    department: 'Indian Railways',
    icon: Train,
    title: 'Railway Services & Projects',
    description: 'Request information about railway projects, services, and facilities.',
    sampleText: `I request the following information regarding [STATION NAME / RAILWAY ZONE]:

1. Details of pending railway projects in the region with expected completion dates
2. Revenue generated from [STATION] in the last financial year
3. Number of complaints received regarding cleanliness/services and action taken
4. Plans for new trains or increased frequency on [ROUTE]
5. Details of passenger amenities available and planned improvements
6. Criteria for ticket reservation quota allocation`,
    tags: ['railway', 'trains', 'station', 'transport']
  },
  // Hindi Templates
  {
    id: 'rti-pwd-roads-hindi',
    category: 'RTI',
    department: 'लोक निर्माण विभाग (PWD)',
    icon: MapPin,
    title: 'सड़क निर्माण व्यय - हिंदी',
    description: 'सड़क निर्माण लागत, ठेकेदार जानकारी और परियोजना समयसीमा के बारे में विवरण का अनुरोध करें।',
    language: 'hindi',
    sampleText: `मैं [आपका क्षेत्र] में [समय अवधि] के दौरान किए गए सड़क निर्माण/मरम्मत कार्य का पूर्ण विवरण जानना चाहता/चाहती हूं। कृपया निम्नलिखित जानकारी प्रदान करें:

1. परियोजना के लिए स्वीकृत कुल बजट
2. कार्य प्रदान किए गए ठेकेदार का नाम और पता
3. कार्य प्रारंभ और समाप्ति की तिथि
4. मदवार व्यय विवरण
5. गुणवत्ता निरीक्षण रिपोर्ट, यदि कोई हो
6. कार्य पूर्णता प्रमाण पत्र की प्रतियां`,
    tags: ['सड़क', 'निर्माण', 'बजट', 'ठेकेदार', 'hindi']
  },
  {
    id: 'rti-electricity-hindi',
    category: 'RTI',
    department: 'विद्युत विभाग',
    icon: Zap,
    title: 'बिजली कनेक्शन और बिल - हिंदी',
    description: 'बिजली कनेक्शन, मीटर रीडिंग और बिलिंग विवरण के बारे में जानकारी का अनुरोध करें।',
    language: 'hindi',
    sampleText: `मैं [आपका क्षेत्र/उपभोक्ता संख्या] में बिजली आपूर्ति के संबंध में निम्नलिखित जानकारी का अनुरोध करता/करती हूं:

1. घरेलू/वाणिज्यिक उपभोक्ताओं पर लागू बिजली टैरिफ का विवरण
2. लोड स्वीकृति और कनेक्शन अनुमोदन के मानदंड
3. पिछले 6 महीनों में बिजली कटौती का विवरण कारणों सहित
4. उपभोक्ताओं को प्रदान की गई सब्सिडी राशि, यदि कोई हो
5. शिकायत दर्ज करने की प्रक्रिया और औसत समाधान समय`,
    tags: ['बिजली', 'बिल', 'विद्युत', 'टैरिफ', 'hindi']
  },
  {
    id: 'rti-water-hindi',
    category: 'RTI',
    department: 'जल आपूर्ति विभाग',
    icon: Droplets,
    title: 'पानी आपूर्ति और गुणवत्ता - हिंदी',
    description: 'पानी आपूर्ति समय-सारणी, गुणवत्ता रिपोर्ट और बुनियादी ढांचे के बारे में जानकारी का अनुरोध करें।',
    language: 'hindi',
    sampleText: `मैं [आपका मोहल्ला/क्षेत्र] में जल आपूर्ति के संबंध में निम्नलिखित जानकारी का अनुरोध करता/करती हूं:

1. दैनिक जल आपूर्ति समय-सारणी और अवधि
2. पिछले 12 महीनों की पानी गुणवत्ता परीक्षण रिपोर्ट
3. इस क्षेत्र को सेवा देने वाले जल शोधन संयंत्रों का विवरण
4. पिछले वर्ष में प्राप्त और निपटाई गई शिकायतों की संख्या
5. जल आपूर्ति बुनियादी ढांचे में सुधार की भविष्य की योजनाएं
6. सरकारी मानकों के अनुसार प्रति व्यक्ति पानी उपलब्धता`,
    tags: ['पानी', 'आपूर्ति', 'जल', 'नगरपालिका', 'hindi']
  },
  {
    id: 'complaint-police-hindi',
    category: 'Complaint',
    department: 'पुलिस विभाग',
    icon: Shield,
    title: 'कानून व्यवस्था समस्या - हिंदी',
    description: 'कानून व्यवस्था, उपद्रव या सुरक्षा संबंधी मुद्दों के बारे में शिकायत दर्ज करें।',
    language: 'hindi',
    sampleText: `मैं [आपका क्षेत्र] में एक गंभीर कानून व्यवस्था समस्या के बारे में आपका ध्यान आकर्षित करना चाहता/चाहती हूं:

समस्या का स्वरूप:
[समस्या का वर्णन करें - जैसे अवैध पार्किंग, शोर प्रदूषण, संदिग्ध गतिविधियां, छेड़छाड़ आदि]

स्थान: [पूर्ण पता/लैंडमार्क]
घटना का समय: [यह आमतौर पर कब होता है]
अवधि: यह [तारीख] से चल रहा है

प्रभाव:
- [यह आपको और समुदाय को कैसे प्रभावित करता है]
- [कोई सुरक्षा चिंता]

मैं इस समस्या के समाधान के लिए तत्काल गश्त और आवश्यक कार्रवाई का अनुरोध करता/करती हूं। मैं किसी भी अतिरिक्त जानकारी प्रदान करने को तैयार हूं।`,
    tags: ['पुलिस', 'सुरक्षा', 'कानून', 'शिकायत', 'hindi']
  },
  {
    id: 'complaint-hospital-hindi',
    category: 'Complaint',
    department: 'स्वास्थ्य विभाग',
    icon: HeartPulse,
    title: 'सरकारी अस्पताल सेवाएं - हिंदी',
    description: 'अस्पताल सेवाओं, कर्मचारी व्यवहार या चिकित्सा सुविधाओं के बारे में शिकायत दर्ज करें।',
    language: 'hindi',
    sampleText: `मैं [अस्पताल का नाम] की सेवाओं के संबंध में शिकायत दर्ज करना चाहता/चाहती हूं:

भेंट की तारीख: [तारीख]
OPD/वार्ड नंबर: [यदि लागू हो]

सामना की गई समस्याएं:
1. [समस्या का वर्णन करें - जैसे लंबा प्रतीक्षा समय, दवाओं की अनुपलब्धता, कर्मचारी व्यवहार]
2. [अन्य समस्याएं]

विवरण:
[घटना का विशिष्ट विवरण प्रदान करें, यदि ज्ञात हो तो कर्मचारियों के नाम सहित]

अपेक्षित समाधान:
- सेवाओं में सुधार
- संबंधित कर्मचारियों के खिलाफ अनुशासनात्मक कार्रवाई (यदि लागू हो)
- लिखित स्पष्टीकरण

मैं आपसे तत्काल हस्तक्षेप का अनुरोध करता/करती हूं ताकि मरीजों को उचित देखभाल और उपचार मिल सके।`,
    tags: ['अस्पताल', 'स्वास्थ्य', 'चिकित्सा', 'सेवाएं', 'hindi']
  },
  {
    id: 'complaint-municipal-hindi',
    category: 'Complaint',
    department: 'नगर निगम',
    icon: Building2,
    title: 'कचरा और स्वच्छता - हिंदी',
    description: 'कचरा संग्रह, नाली या स्वच्छता संबंधी मुद्दों के बारे में शिकायत दर्ज करें।',
    language: 'hindi',
    sampleText: `मैं [आपका मोहल्ला] में एक स्वच्छता समस्या की ओर आपका तत्काल ध्यान आकर्षित करना चाहता/चाहती हूं:

समस्या: [अनियमित कचरा संग्रह / उफनती नाली / खुले में कचरा फेंकना]

स्थान: [लैंडमार्क के साथ पूर्ण पता]

विवरण:
- [तारीख/दिनों] से कचरा नहीं उठाया गया है
- [वर्तमान स्थिति का वर्णन करें]
- [स्वास्थ्य संबंधी खतरे]

निवासियों पर प्रभाव:
- दुर्गंध के कारण रहना मुश्किल हो रहा है
- मच्छरों और मक्खियों का प्रजनन
- बीमारियों का खतरा

मैं तत्काल कार्रवाई का अनुरोध करता/करती हूं:
1. जमा कचरा साफ करें/नाली खोलें
2. आगे नियमित संग्रह/रखरखाव सुनिश्चित करें
3. चूक के लिए जिम्मेदार लोगों के खिलाफ कार्रवाई करें`,
    tags: ['कचरा', 'स्वच्छता', 'नगरपालिका', 'नाली', 'hindi']
  }
];

const CATEGORIES = ['All', 'RTI', 'Complaint'];
const LANGUAGES = ['All', 'English', 'Hindi'];

const Templates = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedLanguage, setSelectedLanguage] = useState('All');
  const [expandedTemplate, setExpandedTemplate] = useState(null);

  const filteredTemplates = SAMPLE_TEMPLATES.filter(template => {
    const matchesCategory = selectedCategory === 'All' || template.category === selectedCategory;
    const matchesLanguage = selectedLanguage === 'All' || 
      (selectedLanguage === 'Hindi' && template.language === 'hindi') ||
      (selectedLanguage === 'English' && !template.language);
    const matchesSearch = searchQuery === '' || 
      template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.department.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesLanguage && matchesSearch;
  });

  const handleCopyText = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Template copied to clipboard!');
  };

  const handleUseTemplate = (template) => {
    // Navigate to appropriate mode with pre-filled data
    const route = template.category === 'RTI' ? '/assisted' : '/assisted';
    navigate(route, { 
      state: { 
        prefillDescription: template.sampleText,
        documentType: template.category === 'RTI' ? 'information_request' : 'grievance',
        language: template.language || 'english'
      } 
    });
  };

  return (
    <div className="templates-page">
      {/* Page Header */}
      <div className="templates-page-header">
        <div className="container">
          <Link to="/" className="back-link">
            <ArrowLeft size={16} />
            <span>Back to Home</span>
          </Link>
          
          <div className="page-header-content">
            <div className="page-header-icon">
              <BookOpen size={24} />
            </div>
            <div className="page-header-text">
              <h1>RTI & Complaint Templates</h1>
              <p>
                Pre-validated templates following Section 6(1) of the RTI Act, 2005. 
                These are starting points — customize with your specific details.
              </p>
            </div>
          </div>

          <div className="page-header-badges">
            <div className="header-badge">
              <Scale size={14} />
              <span>Legally Structured</span>
            </div>
            <div className="header-badge">
              <CheckCircle2 size={14} />
              <span>Rule-Validated</span>
            </div>
          </div>
        </div>
      </div>

      <div className="container templates-content">
        {/* Search and Filter Bar */}
        <div className="templates-toolbar">
          <div className="search-box">
            <Search size={18} className="search-icon" />
            <input
              type="text"
              placeholder="Search by department, keyword..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="category-filters">
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                className={`filter-btn ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
            <span className="filter-divider">|</span>
            {LANGUAGES.map(lang => (
              <button
                key={lang}
                className={`filter-btn lang-btn ${selectedLanguage === lang ? 'active' : ''}`}
                onClick={() => setSelectedLanguage(lang)}
              >
                {lang === 'Hindi' && <Globe size={14} />}
                {lang}
              </button>
            ))}
          </div>
        </div>

        {/* Results Count */}
        <div className="results-summary">
          <span className="results-count">{filteredTemplates.length} templates</span>
          {(selectedCategory !== 'All' || selectedLanguage !== 'All' || searchQuery) && (
            <button 
              className="clear-filters"
              onClick={() => {
                setSelectedCategory('All');
                setSelectedLanguage('All');
                setSearchQuery('');
              }}
            >
              Clear filters
            </button>
          )}
        </div>

        {/* Templates Grid */}
        <div className="templates-grid">
          {filteredTemplates.map(template => {
            const Icon = template.icon;
            const isExpanded = expandedTemplate === template.id;

          return (
            <div key={template.id} className={`template-card ${isExpanded ? 'expanded' : ''}`}>
              <div className="template-card-header">
                <div className="template-icon">
                  <Icon size={20} />
                </div>
                <div className="template-meta">
                  <span className={`category-badge ${template.category.toLowerCase()}`}>
                    {template.category}
                  </span>
                  <span className="department-name">{template.department}</span>
                </div>
              </div>

              <h3 className="template-title">{template.title}</h3>
              <p className="template-description">{template.description}</p>

              <div className="template-tags">
                {template.tags.map(tag => (
                  <span key={tag} className="tag">#{tag}</span>
                ))}
              </div>

              {/* Expandable Sample Text */}
              <div className="template-preview">
                <button 
                  className="preview-toggle"
                  onClick={() => setExpandedTemplate(isExpanded ? null : template.id)}
                >
                  <FileText size={16} />
                  {isExpanded ? 'Hide Sample Text' : 'View Sample Text'}
                </button>

                {isExpanded && (
                  <div className="sample-text-container">
                    <pre className="sample-text">{template.sampleText}</pre>
                    <button 
                      className="copy-btn"
                      onClick={() => handleCopyText(template.sampleText)}
                    >
                      <Copy size={14} /> Copy Text
                    </button>
                  </div>
                )}
              </div>

              <div className="template-actions">
                <button 
                  className="btn btn-primary use-btn"
                  onClick={() => handleUseTemplate(template)}
                >
                  Use This Template <ArrowRight size={16} />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {filteredTemplates.length === 0 && (
        <div className="no-results">
          <FileText size={48} strokeWidth={1} />
          <h3>No templates found</h3>
          <p>Try adjusting your search or filter criteria.</p>
        </div>
      )}

      {/* Info Section */}
      <div className="templates-info">
        <div className="info-header">
          <h3>How to Use These Templates</h3>
          <p className="info-subtitle">Follow these steps to create a compliant application</p>
        </div>
        <div className="info-steps">
          <div className="info-step">
            <div className="info-step-number">1</div>
            <div className="info-step-content">
              <strong>Browse</strong>
              <p>Find a template that matches your requirement by department or category.</p>
            </div>
          </div>
          <div className="info-step">
            <div className="info-step-number">2</div>
            <div className="info-step-content">
              <strong>View</strong>
              <p>Click "View Sample Text" to see the full template structure.</p>
            </div>
          </div>
          <div className="info-step">
            <div className="info-step-number">3</div>
            <div className="info-step-content">
              <strong>Customize</strong>
              <p>Replace placeholders [IN BRACKETS] with your specific details.</p>
            </div>
          </div>
          <div className="info-step">
            <div className="info-step-number">4</div>
            <div className="info-step-content">
              <strong>Generate</strong>
              <p>Click "Use This Template" to auto-fill the drafting form.</p>
            </div>
          </div>
        </div>
        <div className="info-disclaimer">
          <strong>Note:</strong> These templates are starting points for guidance. The rule engine will 
          validate and format your input to ensure compliance with RTI Act requirements.
        </div>
      </div>
      </div>
    </div>
  );
};

export default Templates;
