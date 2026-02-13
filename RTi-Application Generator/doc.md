# AI-Powered Public Complaint & RTI Generator

## Project Documentation

**Author:** Anurag Mishra  
**Date:** February 2, 2026  
**Project:** GSoC - AI-Powered Public Complaint and RTI Generator

---

## Progress Tracker

### Latest Session: February 2, 2026 - Final Testing & Documentation

#### System Integration Testing ✅

**Backend FastAPI Server:**
- ✅ Successfully running on port 8000
- ✅ Health endpoint responding correctly
- ✅ Draft generation API working perfectly
- ✅ Template system functioning (RTI & complaints)
- ✅ OpenAI integration configured

**Frontend React Application:**
- ✅ Successfully running on port 3000
- ✅ All pages updated with institutional civic design
- ✅ Complete component redesign implemented
- ✅ Responsive design working across devices

**API Testing Results:**
```bash
# Health Check - WORKING
GET http://localhost:8000/health
Response: {"status": "healthy", "version": "1.0.0"}

# Draft Generation - WORKING
POST http://localhost:8000/api/draft
Response: Generated 235-word RTI application successfully

# Document Templates - WORKING
- RTI Information Request: ✅
- RTI Records Request: ✅ 
- Complaint/Grievance: ✅
- Escalation: ✅
```

**Design System Overhaul:**
- Replaced "AI-first startup" messaging with "institutional civic infrastructure"
- Updated color scheme to orange (#EA580C) and navy (#0F172A)
- Implemented consistent component styling
- Added page headers with badges and back links
- Updated all CSS to use proper design tokens

### Session: February 1, 2026 - Initial Development

---

### 1. Environment Setup & Python Compatibility Fix

**Problem:** Python 3.14 was incompatible with spaCy due to pydantic v1 dependency issues.

**Solution:**
- Discovered Python 3.13.6 was available on the system
- Created new virtual environment with Python 3.13.6:
  ```bash
  py -3.13 -m venv .venv
  ```
- Activated and installed all dependencies

**Status:** ✅ Completed

---

### 2. Dependency Installation

Installed all required packages:
- `spacy` 3.8.11 with `en_core_web_sm` model
- `transformers` + `torch` for DistilBERT
- `fastapi` + `uvicorn` for API server
- `python-docx`, `reportlab`, `openpyxl` for document generation
- `email-validator` for pydantic EmailStr validation
- `pytest` for testing

**Command:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Status:** ✅ Completed

---

### 3. Code Fixes

#### 3.1 Fixed `confidence_gate.py`
- **Issue:** Missing `Tuple` import from typing
- **File:** `backend/app/services/nlp/confidence_gate.py`
- **Fix:** Added `Tuple` to imports

#### 3.2 Fixed `services/__init__.py`
- **Issue:** Trying to import non-existent classes (`InferenceOrchestrator`, `AuthorityResolver`)
- **File:** `backend/app/services/__init__.py`
- **Fix:** Updated exports to match actual functions/classes

#### 3.3 Enabled Swagger Docs
- **Issue:** Swagger UI was disabled (DEBUG=False)
- **File:** `backend/app/main.py`
- **Fix:** Changed `docs_url` and `redoc_url` to always be enabled

**Status:** ✅ Completed

---

### 4. Unit Tests

Created comprehensive test suite with **130 tests** covering:

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_text_sanitizer.py` | 15 | PII detection, input cleaning |
| `test_language_normalizer.py` | 12 | Language normalization |
| `test_tone.py` | 8 | Tone analysis |
| `test_intent_rules.py` | 20 | Intent classification rules |
| `test_issue_rules.py` | 18 | Issue categorization |
| `test_legal_triggers.py` | 15 | Legal citation detection |
| `test_confidence_gate.py` | 12 | Confidence thresholds |
| `test_spacy_engine.py` | 10 | NER entity extraction |
| `test_distilbert_semantic.py` | 10 | Semantic similarity |
| `test_schemas.py` | 10 | Pydantic validation |

**Command:**
```bash
pytest tests/ -v --tb=short
```

**Result:** All 130 tests passed ✅

---

### 5. ML Components Verification

#### 5.1 spaCy NLP Engine
```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp("I filed a complaint with Delhi Police on January 15")
# Entities: Delhi (GPE), January 15 (DATE)
```
**Status:** ✅ Working

#### 5.2 Rule Engine - Intent Classification
```python
from app.services.rule_engine.intent_rules import classify_intent
result = classify_intent("I want to file an RTI application")
# Result: intent=rti, confidence=0.72
```
**Status:** ✅ Working

#### 5.3 Rule Engine - Issue Mapping
```python
from app.services.rule_engine.issue_rules import map_issue_to_department
result = map_issue_to_department("road construction problem")
# Result: category=roads, departments=[PWD, NHAI, ...], confidence=0.95
```
**Status:** ✅ Working

#### 5.4 Legal Triggers Detection
```python
from app.services.rule_engine.legal_triggers import detect_legal_triggers
result = detect_legal_triggers("Under Section 6 of RTI Act")
# Detects RTI Act Section 6 citation
```
**Status:** ✅ Working

#### 5.5 DistilBERT Semantic Similarity
```python
from app.services.nlp.distilbert_semantic import rank_by_similarity
result = rank_by_similarity("road construction", candidates, top_k=4)
# Returns ranked candidates with similarity scores
```
**Model:** `distilbert-base-uncased` (268MB, cached after first download)  
**Status:** ✅ Working

---

### 6. Backend API Server

Started FastAPI server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Server URL:** http://127.0.0.1:8000  
**Swagger UI:** http://127.0.0.1:8000/docs  
**ReDoc:** http://127.0.0.1:8000/redoc

**Status:** ✅ Running

---

### 7. API Endpoint Testing

#### 7.1 POST `/api/infer` - Intent Classification

**Test 1: RTI Request**
```json
{
  "text": "I want information about road construction expenses in my district under RTI Act",
  "language": "english"
}
```
**Response:**
- Intent: `rti`
- Document Type: `information_request`
- Confidence: 95% (High) - No confirmation needed
- Department: PWD, Municipal Corporation, NHAI
- Processing Time: ~760ms

**Test 2: Complaint**
```json
{
  "text": "The water supply has been irregular for the past 3 weeks in Sector 15",
  "language": "english"
}
```
**Response:**
- Intent: `complaint`
- Document Type: `grievance`
- Confidence: 64% (Low) - Requires confirmation
- DistilBERT boosted to 80%
- Department: Water Supply, Jal Board, PHED (94% confidence)

**Status:** ✅ Working

---

#### 7.2 POST `/api/draft` - Document Generation

**Test: RTI Information Request**
```json
{
  "document_type": "information_request",
  "applicant": {
    "name": "Rahul Sharma",
    "address": "123, Gandhi Nagar, Jaipur",
    "state": "Rajasthan"
  },
  "issue": {
    "description": "Road construction expenditure details",
    "specific_request": "Itemized expenditure and contractor details",
    "time_period": "Jan-Dec 2024"
  },
  "authority": {
    "department_name": "PWD",
    "designation": "PIO"
  }
}
```

**Generated Document:**
- Proper RTI format with legal citations (Section 6, 7, 8, 9)
- Fee information (Rs. 10)
- 30-day response timeline
- Word count: 225 words
- Template: `rti/information_request.txt`

**Status:** ✅ Working

---

#### 7.3 POST `/api/download` - Document Export

| Format | Status | File Size | Notes |
|--------|--------|-----------|-------|
| **PDF** | ✅ Working | 3,558 bytes | Official submission format |
| **DOCX** | ✅ Working | 37,713 bytes | Editable Word document |
| **XLSX** | ✅ Working | 7,438 bytes | Tracking spreadsheet |

**Privacy Feature:** Documents streamed directly, NOT stored on server.

**Status:** ✅ Working

---

### 8. Complete System Summary

#### Backend API Endpoints
| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/health` | GET | Health check | ✅ |
| `/api/infer` | POST | Classify intent & extract entities | ✅ |
| `/api/draft` | POST | Generate document from template | ✅ |
| `/api/download` | POST | Export as PDF/DOCX/XLSX | ✅ |
| `/api/authority` | GET | Get department info | ✅ |
| `/docs` | GET | Swagger UI | ✅ |

#### ML/NLP Components
| Component | Model/Library | Status |
|-----------|---------------|--------|
| NER Engine | spaCy 3.8.11 (`en_core_web_sm`) | ✅ |
| Intent Rules | Custom rule engine | ✅ |
| Issue Mapping | Custom rule engine | ✅ |
| Legal Triggers | Regex-based detection | ✅ |
| Semantic Similarity | DistilBERT (`distilbert-base-uncased`) | ✅ |
| Confidence Gate | Threshold-based gating | ✅ |

#### Design Principles Implemented
1. ✅ **Rules decide, AI assists** - Rule engine is primary, NLP only assists
2. ✅ **Human confirmation mandatory** - Low confidence requires user verification
3. ✅ **Privacy-first** - No database, stateless, nothing stored
4. ✅ **No AI-generated legal text** - Templates pre-written, AI fills placeholders

---

### 9. Project Structure

```
AI-Powered-Public-Complaint-and-RTI-Generat/
├── .venv/                      # Python 3.13 virtual environment
├── backend/
│   ├── app/
│   │   ├── api/                # FastAPI routers
│   │   │   ├── infer.py        # Intent classification
│   │   │   ├── draft.py        # Document generation
│   │   │   ├── download.py     # PDF/DOCX/XLSX export
│   │   │   └── authority.py    # Department info
│   │   ├── services/
│   │   │   ├── nlp/            # NLP components
│   │   │   │   ├── spacy_engine.py
│   │   │   │   ├── distilbert_semantic.py
│   │   │   │   └── confidence_gate.py
│   │   │   ├── rule_engine/    # Rule-based classification
│   │   │   │   ├── intent_rules.py
│   │   │   │   ├── issue_rules.py
│   │   │   │   └── legal_triggers.py
│   │   │   ├── draft_assembler.py
│   │   │   ├── document_generator.py
│   │   │   └── inference_orchestrator.py
│   │   ├── templates/          # Pre-written legal templates
│   │   │   ├── rti/
│   │   │   └── complaint/
│   │   ├── utils/
│   │   ├── schemas/
│   │   ├── config.py
│   │   └── main.py
│   ├── tests/                  # 130 unit tests
│   └── requirements.txt
├── frontend/                   # (To be built)
├── ml/
├── docs/
└── doc.md                      # This file
```

---

### 10. Frontend Implementation (React 19)

#### 10.1 Complete Component Structure (15 Components)

| Component | Purpose | Features |
|-----------|---------|----------|
| **ApplicantForm** | User details & issue input | Form validation, state selection |
| **CharacterLimitIndicator** | Character count display | Real-time tracking, visual warnings |
| **ConfidenceNotice** | AI confidence display | Semantic highlighting, manual override |
| **ConstrainedDraftEditor** | Template-aware editing | Placeholder protection, validation |
| **DownloadPanel** | Document export | PDF/DOCX/XLSX options |
| **DraftHistoryPanel** | Version tracking | Undo/redo, restore snapshots |
| **DraftPreview** | Live document preview | Editable, syntax highlighting |
| **ExplainWhyPanel** | AI decision transparency | Rule breakdown, confidence sources |
| **LoadingState** | Loading indicators | Skeleton loaders, progress bars |
| **PIIWarning** | Privacy alerts | Sensitive data detection |
| **PrivacyControls** | Data management | Clear data, no-storage info |
| **QualityScore** | Draft quality metrics | Scoring, improvement suggestions |
| **StructuredRTIForm** | RTI-specific form | Section-wise input |
| **SubmissionGuidancePanel** | Filing instructions | Department addresses, fees |
| **ValidatedInput** | Input validation | Real-time feedback, constraints |

#### 10.2 Service Layer (6 Services)

| Service | Purpose |
|---------|---------|
| `apiClient.js` | Centralized HTTP client with retry, timeout, error handling |
| `authorityService.js` | Authority lookup API |
| `draftHistoryService.js` | Local storage history management |
| `draftService.js` | Draft generation API |
| `inferenceService.js` | Intent classification API |
| `validationService.js` | Draft validation API |

#### 10.3 Pages (3 Main Modes)

1. **Home** - Landing page with mode selection
2. **GuidedMode** - Step-by-step wizard for beginners
3. **AssistedMode** - Free-form input with AI assistance

**Status:** ✅ Completed

---

### 11. Hindi Language Support

#### 11.1 Backend Hindi Templates
```
backend/app/templates/
├── rti/
│   ├── information_request_hindi.txt
│   └── records_request_hindi.txt
└── complaint/
    ├── grievance_hindi.txt
    └── escalation_hindi.txt
```

#### 11.2 Language Detection & Processing
- Automatic Hindi text detection using `langdetect`
- Indic NLP Library for preprocessing
- Hindi-specific keyword matching in rule engine
- Bilingual output generation

**Status:** ✅ Completed

---

### 12. Reliability & UX Features

#### 12.1 API Client Improvements
- **Retry Logic**: 3 attempts with exponential backoff (1s, 2s, 4s)
- **Request Timeout**: 30 seconds default
- **Error Handling**: Graceful degradation with user-friendly messages
- **Request Debouncing**: Prevents API flooding

#### 12.2 Draft Quality Features
- **Character Limit Indicator**: Real-time character counting
- **PII Warning**: Detects sensitive data (Aadhaar, phone, email)
- **Quality Score**: Grades drafts A-F with improvement suggestions
- **Validated Input**: Real-time constraint checking

#### 12.3 History & Versioning
- **Draft History Panel**: Tracks all draft versions
- **Undo/Redo**: Navigate through changes
- **Restore**: Return to any previous version
- **Local Storage**: Privacy-first, no server storage

#### 12.4 Accessibility
- **WCAG 2.1 AA Compliant**
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: ARIA labels and live regions
- **Print Styles**: Optimized print layout

**Status:** ✅ Completed

---

### 13. API Integration Tests (12 Tests)

Created comprehensive API test suite covering all endpoints:

```python
# Test Results (All Passed)
✅ Health Check - Status: healthy
✅ RTI Intent Classification - Intent: rti, Confidence: 0.95
✅ Complaint Intent Classification - Intent: complaint, Confidence: 0.65
✅ Hindi Language Inference - Intent: rti
✅ RTI Draft Generation - Template: rti/information_request.txt, Words: 219
✅ Complaint Draft Generation - Template: complaint/grievance.txt, Words: 229
✅ PDF Download - Size: 3732 bytes
✅ DOCX Download - Size: 37647 bytes
✅ XLSX Download - Size: 7038 bytes
✅ Authority Lookup - Found 3 authorities for Delhi electricity
✅ RTI Validation - Score: 84, Grade: B
✅ Edit Validation - Valid: true
```

**Status:** ✅ All 12 Tests Passed

---

### 14. Complete Test Summary

| Test Category | Tests | Status |
|---------------|-------|--------|
| **Unit Tests** | 130 | ✅ All Passed |
| **API Integration Tests** | 12 | ✅ All Passed |
| **Frontend Build** | - | ✅ Successful |
| **Total** | 142 | ✅ All Passed |

---

### 15. Final Project Structure

```
AI-Powered-Public-Complaint-and-RTI-Generat/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── authority.py
│   │   │   ├── download.py
│   │   │   ├── draft.py
│   │   │   └── infer.py
│   │   ├── services/
│   │   │   ├── nlp/
│   │   │   │   ├── confidence_gate.py
│   │   │   │   ├── distilbert_semantic.py
│   │   │   │   └── spacy_engine.py
│   │   │   ├── rule_engine/
│   │   │   │   ├── intent_rules.py
│   │   │   │   ├── issue_rules.py
│   │   │   │   └── legal_triggers.py
│   │   │   ├── authority_resolver.py
│   │   │   ├── document_generator.py
│   │   │   ├── draft_assembler.py
│   │   │   └── inference_orchestrator.py
│   │   ├── templates/
│   │   │   ├── rti/
│   │   │   │   ├── information_request.txt
│   │   │   │   ├── information_request_hindi.txt
│   │   │   │   ├── records_request.txt
│   │   │   │   ├── records_request_hindi.txt
│   │   │   │   └── inspection_request.txt
│   │   │   └── complaint/
│   │   │       ├── grievance.txt
│   │   │       ├── grievance_hindi.txt
│   │   │       ├── escalation.txt
│   │   │       ├── escalation_hindi.txt
│   │   │       └── follow_up.txt
│   │   ├── schemas/
│   │   ├── utils/
│   │   ├── config.py
│   │   ├── main.py
│   │   └── middleware.py
│   ├── tests/ (130 unit tests)
│   ├── test_api.py (12 integration tests)
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/ (15 components)
│   │   │   ├── ApplicantForm/
│   │   │   ├── CharacterLimitIndicator/
│   │   │   ├── ConfidenceNotice/
│   │   │   ├── ConstrainedDraftEditor/
│   │   │   ├── DownloadPanel/
│   │   │   ├── DraftHistoryPanel/
│   │   │   ├── DraftPreview/
│   │   │   ├── ExplainWhyPanel/
│   │   │   ├── LoadingState/
│   │   │   ├── PIIWarning/
│   │   │   ├── PrivacyControls/
│   │   │   ├── QualityScore/
│   │   │   ├── StructuredRTIForm/
│   │   │   ├── SubmissionGuidancePanel/
│   │   │   └── ValidatedInput/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   │   ├── Home/
│   │   │   ├── GuidedMode/
│   │   │   └── AssistedMode/
│   │   ├── services/ (6 services)
│   │   │   ├── apiClient.js
│   │   │   ├── authorityService.js
│   │   │   ├── draftHistoryService.js
│   │   │   ├── draftService.js
│   │   │   ├── inferenceService.js
│   │   │   └── validationService.js
│   │   ├── utils/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── ml/
│   ├── model_manager.py
│   ├── MODEL_USAGE_POLICY.md
│   └── requirements.txt
│
├── docs/
│   ├── architecture.md
│   ├── decision_flow.md
│   ├── ai_safety_notes.md
│   ├── privacy_policy.md
│   └── future_scope.md
│
├── doc.md (This file)
├── README.md
└── pyrightconfig.json
```

---

### 16. Project Milestones Completed

- [x] Environment setup (Python 3.13.6)
- [x] Backend API implementation (FastAPI)
- [x] Rule engine implementation
- [x] NLP components (spaCy, DistilBERT)
- [x] Document generation (PDF, DOCX, XLSX)
- [x] Unit test suite (130 tests)
- [x] Frontend implementation (React 19)
- [x] 15 React components
- [x] Hindi language support
- [x] Reliability features (retry, timeout, error handling)
- [x] UX improvements (history, validation, quality score)
- [x] Accessibility features (WCAG 2.1 AA)
- [x] API integration tests (12 tests)
- [x] Documentation updates

---

### 17. Future Enhancements

- [ ] Regional language UI (Tamil, Telugu, Bengali, etc.)
- [ ] Voice input support
- [ ] Mobile app (React Native)
- [ ] Integration with government portals
- [ ] Appeal tracking system
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment

---

## Quick Start Commands

```bash
# Backend Setup
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run Backend Server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run Backend Tests
pytest tests/ -v  # 130 unit tests
python test_api.py  # 12 API integration tests

# Frontend Setup
cd frontend
npm install
npm start  # Development server
npm run build  # Production build

# Access Points
# Backend API: http://127.0.0.1:8000
# Swagger UI: http://127.0.0.1:8000/docs
# Frontend: http://localhost:3000
```

---

**Last Updated:** February 1, 2026  
**Author:** Anurag Mishra  
**Project:** GSoC - AI-Powered Public Complaint and RTI Generator  
**Status:** ✅ Feature Complete
