# CIVISIM ML/AI Module

Machine Learning and AI components for policy analysis and simulation intelligence.

## Setup

1. Create virtual environment:
```bash
python -m venv civisim_env
```

2. Activate environment:
```bash
# Windows
civisim_env\Scripts\activate

# Linux/Mac
source civisim_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Project Structure

```
ml/
├── models/              # ML models and processors
├── data/               # Input and output data
│   ├── policy_samples/  # Input policy documents
│   ├── extracted_text/  # Processed text
│   └── results/         # Analysis results
├── config/             # Configuration files
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Usage

See individual model files for usage examples.
