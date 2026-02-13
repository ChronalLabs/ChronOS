# CIVISIM ML/AI Setup Instructions

## Quick Setup (5 minutes)

### Step 1: Navigate to ML folder
```bash
cd d:\Hacks-Projects\CIVISM-main\civisim\ml
```

### Step 2: Create Virtual Environment
```bash
python -m venv civisim_env
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
civisim_env\Scripts\activate
```

**Linux/Mac:**
```bash
source civisim_env/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- PyTorch (CPU version)
- Transformers (DistilBERT)
- pdfplumber, python-docx
- NumPy, pandas, scikit-learn
- And other utilities

**Note:** This may take 5-10 minutes depending on your internet connection.

### Step 5: Verify Setup
```bash
python test_setup.py
```

You should see:
```
✅ All required packages installed
✅ Setup complete! Ready to run ML tasks
```

## Quick Start Demo

Run the quick start demo to see Tasks 1 & 2 in action:

```bash
python quick_start.py
```

This will:
1. Extract text from sample policy document (Task 1)
2. Analyze policy intent with DistilBERT (Task 2)
3. Score keyword relevance
4. Save results to `data/results/`

## Individual Task Usage

### Task 1: Document Parser
```bash
python models/document_parser.py
```

### Task 2: Intent Extractor
```bash
python models/intent_extractor.py
```

## Adding Your Own Policies

1. Add PDF or DOCX files to `data/policy_samples/`
2. Run document parser to extract text
3. Run intent extractor to analyze

## Project Structure

```
ml/
├── models/
│   ├── document_parser.py      # Task 1: Text extraction
│   └── intent_extractor.py     # Task 2: Intent analysis
├── data/
│   ├── policy_samples/         # Input documents
│   ├── extracted_text/         # Parsed text
│   └── results/                # Analysis results
├── config/
│   └── parameters.json         # Configuration
├── requirements.txt            # Dependencies
├── test_setup.py              # Setup verification
└── quick_start.py             # Demo script
```

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
civisim_env\Scripts\activate
pip install -r requirements.txt
```

### Issue: PyTorch installation fails
**Solution:** Install CPU version explicitly:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Model download is slow
**Solution:** Models download on first use. Be patient on first run (may take 2-3 minutes).

### Issue: Out of memory
**Solution:** The code uses CPU by default. If issues persist, process smaller text chunks.

## Next Steps

After completing Tasks 1 & 2, you can:
- Implement Task 3: Named Entity Recognition (spaCy)
- Implement Task 4: Ambiguity Detection
- Implement Task 5: Policy Classification
- Continue with remaining tasks from the guide

## Support

For issues, check the main guide: `CIVISIM-ML-Setup-Guide.md`
