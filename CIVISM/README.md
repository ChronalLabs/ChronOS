# 🏛️ CIVISIM - Civic Policy Intelligence Platform

> **Before any policy affects citizens, decision-makers should see its impact.**

A comprehensive **multi-domain civic policy simulation platform** that helps governments visualize the real-world impact of policy decisions on **citizens, resources, and public welfare** — before those decisions are implemented.

---

## 🌍 Vision

CIVISIM aims to be the **universal policy simulation engine** for all civic domains — enabling data-driven governance across every sector that affects citizens' lives.

---

## 🎯 The Problem We Solve

### The Challenge
Policy decisions across government sectors are made under intense pressure:
- ⏱️ Political deadlines and election cycles
- 💰 Budget constraints and resource limitations
- 👥 Public demands and stakeholder conflicts
- 📊 Lack of predictive tools for impact assessment

**The blind spot?** There's no practical way to simulate policy consequences *before execution*.

### The Cost
This results in:
- 📉 Policies that don't achieve intended outcomes
- 💔 Unintended negative effects on citizens
- 😤 Public dissatisfaction and erosion of trust
- 💸 Wasted resources on ineffective measures
- ⚠️ Safety and welfare compromises

### Our Solution
**CIVISIM** = A decision-support platform where policymakers can test *what-if* scenarios across multiple domains and clearly understand their consequences before implementation.

---

## 🏗️ Supported Policy Domains

| Domain | Status | Description |
|--------|--------|-------------|
| 🏗️ **Construction & Infrastructure** | ✅ Active | Urban development, building permits, safety regulations |
| ❤️ **Healthcare & Public Health** | 🔜 Coming Soon | Medical policies, hospital regulations, health emergencies |
| 🎓 **Education & Academia** | 🔜 Coming Soon | School policies, curriculum changes, funding allocation |
| 🚗 **Transportation & Mobility** | 🔜 Coming Soon | Traffic policies, public transit, road safety |
| 🌱 **Environment & Sustainability** | 🔜 Coming Soon | Green policies, pollution control, conservation |
| ⚖️ **Legal & Governance** | 🔜 Coming Soon | Civil laws, regulatory compliance, citizen rights |
| 💼 **Employment & Labor** | 🔜 Coming Soon | Labor laws, workplace safety, employment policies |
| ⚡ **Energy & Utilities** | 🔜 Coming Soon | Power policies, utility regulations, renewables |

---

## ✨ What CIVISIM Does

### ✅ Core Features
| Feature | Impact |
|---------|--------|
| 🧠 **ML Policy Analysis** | AI-powered extraction of intent, entities, and risks |
| 📋 **Policy Simulator** | Test different strategies before execution |
| 🔄 **Baseline Comparison** | See how alternatives perform vs. current approach |
| 📊 **Trade-off Visualization** | Multiple metrics — all visible and comparable |
| ⚠️ **Risk Detection** | Automatic flagging of dangerous policy combinations |
| 📈 **Impact Dashboard** | Track metrics relevant to each domain |
| 💡 **Explainable AI** | Understand *why* outcomes happen (not just *what*) |

### ❌ What We Don't Do
- ❌ Predict the future with certainty
- ❌ Automatically approve policies  
- ❌ Replace planners, experts, or officials
- ❌ Optimize blindly for single metrics

**Why?** Because humans must remain in control of decisions that affect real lives.

---

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **React Router** for navigation

### Backend
- **FastAPI** (Python)
- **Modular architecture** (routes, services, schemas)
- **CORS-enabled** API

### ML Pipeline
- **PyTorch** & **Transformers** (Hugging Face)
- **spaCy** for NER
- **DistilBERT** for intent extraction
- **BART** for zero-shot classification
- Custom models for:
  - Ambiguity detection
  - Risk assessment
  - Parameter mapping
  - Impact explanation

---

## 📁 Project Structure

```
civisim/
├── frontend/                 # React + TypeScript UI
│   └── src/
│       ├── pages/           # Route pages
│       │   ├── LandingPage.tsx
│       │   ├── MLAnalysisPage.tsx
│       │   ├── SimulationEnginePage.tsx
│       │   ├── PolicyConfigurationPage.tsx
│       │   └── ImpactAnalysisPage.tsx
│       └── components/      # Reusable components
│
├── backend/                  # FastAPI Backend
│   ├── main.py              # App entry point
│   ├── simulation.py        # Simulation engine
│   ├── routes/              # API route handlers
│   │   ├── simulation.py    # /simulate endpoints
│   │   └── ml.py            # /ml/* endpoints
│   ├── services/            # Business logic
│   │   └── ml_service.py    # ML model management
│   └── schemas/             # Pydantic models
│       └── models.py        # Request/response schemas
│
└── ml/                       # ML Pipeline
    ├── main.py              # Full pipeline runner
    ├── models/              # ML model implementations
    │   ├── document_parser.py
    │   ├── intent_extractor.py
    │   ├── policy_ner.py
    │   ├── ambiguity_detector.py
    │   ├── policy_classifier.py
    │   ├── policy_mapper.py
    │   ├── impact_explainer.py
    │   └── risk_detector.py
    └── .venv/               # Python virtual environment
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.12+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/civisim.git
cd civisim
```

2. **Setup ML Environment**
```bash
cd ml
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Setup Frontend**
```bash
cd frontend
npm install
```

4. **Install Backend Dependencies**
```bash
cd backend
pip install fastapi uvicorn pydantic
```

### Running the Application

1. **Start Backend** (Port 8000)
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

2. **Start Frontend** (Port 3000)
```bash
cd frontend
npm run dev
```

3. **Access the Application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 🔌 API Endpoints

### Simulation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/simulate` | Run policy simulation |

### ML Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ml/status` | Check ML models status |
| POST | `/ml/analyze` | Full ML pipeline analysis |
| POST | `/ml/extract-intent` | Extract policy intent |
| POST | `/ml/extract-entities` | Extract named entities |
| POST | `/ml/analyze-ambiguity` | Analyze text ambiguity |
| POST | `/ml/classify` | Classify policy focus |

---

## 🎨 Screenshots

### Landing Page
- Multi-domain selector with 8 policy sectors
- Active domain highlighted (Construction)
- Coming soon badges for future domains

### ML Analysis Page
- Policy text input with sample loader
- Real-time AI analysis
- Visual charts for ambiguity and entities
- Risk assessment with recommendations

### Simulation Engine
- Interactive parameter configuration
- Baseline vs. policy comparison
- Impact metrics visualization

---

## 🔮 Roadmap

### Phase 1: Foundation ✅
- [x] Construction domain implementation
- [x] ML pipeline (8 models)
- [x] Frontend with React/TypeScript
- [x] Backend with FastAPI

### Phase 2: Expansion 🔄
- [ ] Healthcare domain
- [ ] Transportation domain
- [ ] Enhanced visualizations
- [ ] PDF policy upload

### Phase 3: Intelligence 📋
- [ ] Cross-domain impact analysis
- [ ] Historical policy learning
- [ ] Recommendation engine
- [ ] Multi-language support

---

## 👥 Contributing

We welcome contributions! Please read our contributing guidelines before submitting PRs.

---

## 🤝 Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Chronallabs

---

## 🙏 Acknowledgments

- Built for data-driven governance
- Inspired by the need for transparent policy-making
- Designed for citizens, by citizens

---

<div align="center">

**🏛️ CIVISIM**

*Empowering data-driven governance across all civic domains*

[Demo](http://localhost:3000) · [API Docs](http://localhost:8000/docs) · [Report Bug](https://github.com/issues)

<br />
<small>Maintained by <a href="https://github.com/Chronallabs">Chronallabs</a></small>

</div>
