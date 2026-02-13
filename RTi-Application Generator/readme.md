# AI-Powered Public Complaint & RTI Generator

A civic tech application that helps Indian citizens draft Right to Information (RTI) applications and public complaints with AI assistance while maintaining human control.

## 🎯 Purpose

This tool addresses the cognitive, structural, and procedural gaps citizens face when filing:
- **RTI Applications** (Right to Information Act, 2005)
- **Public Complaints** to government departments

### Key Features
- ✅ **Dual-Mode Interaction**: Guided mode for beginners, Assisted mode for power users
- ✅ **Live Draft Projection**: See your document form in real-time with debounced updates
- ✅ **Rule-Based Structure**: Deterministic document formatting per legal standards
- ✅ **AI Intent Inference**: Smart detection of document type and requirements
- ✅ **Authority Suggestions**: Get recommendations for the right government office
- ✅ **Bilingual Support**: English and Hindi (with Hindi templates)
- ✅ **Tone Selection**: Neutral, Formal, or Strict but Polite
- ✅ **Editable Preview**: Full control over final document
- ✅ **Submission Guidance**: Step-by-step instructions for filing
- ✅ **Multi-format Export**: PDF, DOCX, and XLSX download options
- ✅ **Draft Quality Score**: Grade your draft with improvement suggestions
- ✅ **PII Detection**: Warns about sensitive data in your input
- ✅ **Draft History**: Undo/redo with version tracking
- ✅ **Accessibility**: WCAG 2.1 AA compliant

## 🏗️ Architecture

### Design Philosophy
- **Rules decide what is allowed** (structure, mandatory fields, legal format)
- **AI infers what the user means** (intent, document type, authority)
- **Users retain final control** (editable preview, manual overrides)
- **No database storage** – Privacy-first, stateless design

### Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, React Router DOM 7, Axios, Lucide Icons |
| **Backend** | FastAPI, Uvicorn, Pydantic v2, Loguru |
| **NLP/AI** | spaCy 3.8.11, DistilBERT (Transformers), scikit-learn |
| **Document Generation** | ReportLab (PDF), python-docx (DOCX), openpyxl (XLSX) |
| **Language Support** | langdetect, regex, unidecode |

---

## 📂 Project Structure

```
AI-Powered-Public-Complaint-RTI-Generator/
│
├── frontend/                                   # React 19 Frontend
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── components/                        # 15 Reusable Components
│   │   │   ├── ApplicantForm/                 # User details + issue input
│   │   │   ├── CharacterLimitIndicator/       # Real-time character count
│   │   │   ├── ConfidenceNotice/              # AI confidence + user confirmation
│   │   │   ├── ConstrainedDraftEditor/        # Template-aware editing
│   │   │   ├── DownloadPanel/                 # PDF / DOCX / XLSX download
│   │   │   ├── DraftHistoryPanel/             # Version history & undo/redo
│   │   │   ├── DraftPreview/                  # Shows generated RTI / Complaint
│   │   │   ├── ExplainWhyPanel/               # AI decision transparency
│   │   │   ├── LoadingState/                  # Loading indicators
│   │   │   ├── PIIWarning/                    # Sensitive data alerts
│   │   │   ├── PrivacyControls/               # Data management options
│   │   │   ├── QualityScore/                  # Draft quality grading
│   │   │   ├── StructuredRTIForm/             # RTI-specific form
│   │   │   ├── SubmissionGuidancePanel/       # How & where to submit
│   │   │   └── ValidatedInput/                # Input with validation
│   │   │
│   │   ├── layouts/
│   │   │   └── MainLayout/                    # Header, footer, container
│   │   │
│   │   ├── pages/
│   │   │   ├── Home/                          # Landing + explanation
│   │   │   ├── GuidedMode/                    # Rule-first (minimal AI)
│   │   │   └── AssistedMode/                  # NLP-assisted mode
│   │   │
│   │   ├── services/                          # 6 API Services
│   │   │   ├── apiClient.js                   # Centralized HTTP client
│   │   │   ├── inferenceService.js            # Calls /infer API
│   │   │   ├── draftService.js                # Calls /draft API
│   │   │   ├── authorityService.js            # Calls /authority API
│   │   │   ├── validationService.js           # Calls /validate API
│   │   │   └── draftHistoryService.js         # Local storage history
│   │   │
│   │   ├── hooks/
│   │   │   └── useDebounce.js
│   │   │
│   │   ├── utils/
│   │   │   └── fileDownload.js                # Blob → file logic
│   │   │
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── accessibility.css                  # WCAG 2.1 AA styles
│   │   └── print.css                          # Print-optimized styles
│   │
│   ├── package.json
│   └── README.md
│
├── backend/                                    # Python Backend (FastAPI)
│   ├── app/
│   │   ├── main.py                            # FastAPI entry point
│   │   ├── middleware.py                      # Request logging middleware
│   │   ├── config.py                          # Environment configuration
│   │   │
│   │   ├── api/                               # HTTP routes
│   │   │   ├── infer.py                       # Intent + NLP inference
│   │   │   ├── draft.py                       # Draft generation
│   │   │   ├── authority.py                   # Authority suggestion
│   │   │   └── download.py                    # PDF / DOCX / XLSX export
│   │   │
│   │   ├── services/                          # Core business logic
│   │   │   ├── rule_engine/                   # 🔒 PRIMARY DECISION LAYER
│   │   │   │   ├── intent_rules.py            # RTI vs Complaint vs Appeal
│   │   │   │   ├── legal_triggers.py          # RTI sections, grievance markers
│   │   │   │   └── issue_rules.py             # Issue → department mapping
│   │   │   │
│   │   │   ├── nlp/                           # 🔒 STRICTLY BOUNDED AI
│   │   │   │   ├── spacy_engine.py            # NER + phrase rules (CORE)
│   │   │   │   ├── distilbert_semantic.py     # Similarity / ranking ONLY
│   │   │   │   └── confidence_gate.py         # Confidence thresholds & fallback
│   │   │   │
│   │   │   ├── authority_resolver.py          # Deterministic authority logic
│   │   │   ├── draft_assembler.py             # Fills legal templates
│   │   │   ├── document_generator.py          # PDF / DOCX / XLSX creation
│   │   │   └── inference_orchestrator.py      # Orchestrates NLP pipeline
│   │   │
│   │   ├── schemas/                           # Pydantic request/response
│   │   │   ├── applicant.py
│   │   │   ├── issue.py
│   │   │   ├── inference.py
│   │   │   └── draft.py
│   │   │
│   │   ├── templates/                         # NON-AI legal content
│   │   │   ├── rti/
│   │   │   │   ├── information_request.txt
│   │   │   │   ├── information_request_hindi.txt
│   │   │   │   ├── records_request.txt
│   │   │   │   ├── records_request_hindi.txt
│   │   │   │   └── inspection_request.txt
│   │   │   │
│   │   │   └── complaint/
│   │   │       ├── grievance.txt
│   │   │       ├── grievance_hindi.txt
│   │   │       ├── escalation.txt
│   │   │       ├── escalation_hindi.txt
│   │   │       └── follow_up.txt
│   │   │
│   │   └── utils/
│   │       ├── language_normalizer.py
│   │       ├── text_sanitizer.py
│   │       └── tone.py
│   │
│   ├── tests/                                 # 130 Unit Tests
│   │   ├── test_confidence_gate.py            # 26 tests
│   │   ├── test_distilbert_semantic.py        # 20 tests
│   │   ├── test_intent_rules.py               # 20 tests
│   │   ├── test_issue_rules.py                # 18 tests
│   │   ├── test_legal_triggers.py             # 22 tests
│   │   ├── test_spacy_engine.py               # 24 tests
│   │   └── conftest.py
│   │
│   ├── test_api.py                            # 12 API Integration Tests
│   ├── requirements.txt
│   ├── pytest.ini
│   └── README.md
│
├── ml/                                        # 🔒 MODEL ASSETS ONLY
│   ├── model_manager.py
│   ├── MODEL_USAGE_POLICY.md
│   └── requirements.txt
│
├── docs/                                      # Documentation
│   ├── architecture.md
│   ├── decision_flow.md
│   ├── ai_safety_notes.md
│   ├── privacy_policy.md
│   └── future_scope.md
│
├── doc.md                                     # Development log
├── README.md                                  # This file
├── pyrightconfig.json
└── LICENSE
```

---

## 📦 Requirements

### Backend (Python 3.10+)

```txt
# Core Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.0.0
python-dotenv
loguru

# NLP & AI
spacy>=3.8.0
transformers>=4.35.0
torch>=2.1.0
numpy
scikit-learn

# Language Support
langdetect
regex
unidecode
python-dateutil

# Document Generation
reportlab>=4.0.0
python-docx>=1.1.0
openpyxl>=3.1.0
aiofiles

# Testing
pytest>=8.0.0
httpx  # For FastAPI TestClient
```

### Frontend (Node.js 18+)

```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.1.0",
    "axios": "^1.7.9",
    "lucide-react": "^0.473.0",
    "file-saver": "^2.0.5"
  }
}
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** v18+ (for frontend)
- **Python** 3.10+ (3.13 recommended)
- **pip** for Python packages

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Windows)
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Create virtual environment (Linux/Mac)
python3.13 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start the server
uvicorn app.main:app --reload --port 8000

# Run unit tests (130 tests)
pytest tests/ -v

# Run API integration tests (12 tests)
python test_api.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Access Points
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📖 How to Use

### Guided Mode (For Beginners)
1. Select **Guided Mode** from the home screen
2. Fill in your personal details
3. Answer simple questions about your issue
4. Choose language and tone preferences
5. Review the generated document
6. Download as PDF/DOCX/XLSX
7. Get submission instructions

### Assisted Mode (For Advanced Users)
1. Select **Assisted Mode** from the home screen
2. Fill in your personal details
3. Write freely in the issue description box
4. Watch the live draft update on the right panel
5. Enable/disable auto-draft as needed
6. Finalize and edit the document
7. Download in your preferred format
8. Get submission instructions

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/infer` | POST | Analyze text and infer intent/document type |
| `/api/draft` | POST | Generate draft document |
| `/api/authority` | POST | Get authority suggestions |
| `/api/download` | POST | Export as PDF/DOCX/XLSX |
| `/api/validate/rti` | POST | Validate RTI draft quality |
| `/api/validate/edit` | POST | Validate edit suggestions |

---

## 🧪 Testing

### Unit Tests (130 tests)
```bash
cd backend
pytest tests/ -v --tb=short
```

### API Integration Tests (12 tests)
```bash
cd backend
python test_api.py
```

### Test Coverage
| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_confidence_gate.py` | 26 | Confidence thresholds |
| `test_distilbert_semantic.py` | 20 | Semantic similarity |
| `test_intent_rules.py` | 20 | Intent classification |
| `test_issue_rules.py` | 18 | Issue categorization |
| `test_legal_triggers.py` | 22 | Legal citation detection |
| `test_spacy_engine.py` | 24 | NER entity extraction |

---

## 🔒 AI Safety & Boundaries

This project follows strict AI boundaries:

1. **Rule Engine is Primary** – All structural decisions are rule-based
2. **AI is Advisory Only** – NLP assists but doesn't decide
3. **Confidence Gating** – Low-confidence results require user confirmation
4. **No Hallucination Risk** – Templates are human-written, AI only fills placeholders
5. **Full Transparency** – Users see confidence scores and can override

See [docs/ai_safety_notes.md](docs/ai_safety_notes.md) for detailed policy.

---

## 🌐 Supported States

All Indian states and union territories are supported:
- 28 States
- 8 Union Territories

---

## ⚠️ Disclaimer

**This tool provides drafting assistance only.** All generated content is advisory. Users must:
- Review all content carefully
- Edit as needed
- Verify authority addresses
- Submit as per applicable laws

This tool does NOT provide legal advice or guarantees.

---

## 🤝 Contributing

Contributions are welcome! This project aims to make civic participation more accessible.

### Areas for Contribution
- UI/UX improvements
- Additional language support (regional Indian languages)
- Better NER training for Indian government entities
- State-specific portal integrations
- Accessibility enhancements
- Test coverage

---

## 📝 License

This project is created for educational and civic purposes.

---

## 🔮 Future Enhancements

- [ ] Regional language UI (Tamil, Telugu, Bengali, etc.)
- [ ] Voice input support
- [ ] Mobile app (React Native)
- [ ] Integration with government portals
- [ ] Appeal tracking system
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment

---

## 📊 Project Status

| Feature | Status |
|---------|--------|
| Backend API | ✅ Complete |
| Frontend UI | ✅ Complete |
| Unit Tests (130) | ✅ Passing |
| API Tests (12) | ✅ Passing |
| Hindi Support | ✅ Complete |
| Accessibility | ✅ WCAG 2.1 AA |
| Documentation | ✅ Complete |

---

**Built with ❤️ for the citizens of India**

**Last Updated:** February 2, 2026  
**Author:** Anurag Mishra  
**Project:** GSoC - AI-Powered Public Complaint and RTI Generator

---

## ✅ Current Test Results (February 2, 2026)

### Backend API Functionality
- ✅ **Health Check Endpoint**: `GET /health` - Working
- ✅ **Draft Generation API**: `POST /api/draft` - Working (RTI & Complaints)
- ✅ **Document Templates**: All RTI and complaint templates functional
- ✅ **OpenAI Integration**: Configured and ready
- ⚠️  **ML Inference API**: `POST /api/infer` - Minor enum sync issue
- ✅ **Document Download**: Backend endpoints available

### Frontend Application
- ✅ **React App**: Running successfully on localhost:3000
- ✅ **Responsive Design**: Institutional civic design implemented
- ✅ **Page Components**: Home, Templates, GuidedMode, AssistedMode
- ✅ **Component Library**: All 15+ components styled consistently

### Integration Status
- ✅ **Frontend ↔ Backend**: Communication established
- ✅ **Template System**: Legal documents generating correctly
- ✅ **Real-time Preview**: Draft updates working
- ✅ **File Export**: PDF/DOCX/XLSX capabilities available
