# Smart Resume Analyzer - Backend

This directory contains the FastAPI-based backend for the Smart Resume & Job Fit Analyzer.

## Directory Structure

This project follows a standardized FastAPI service architecture:

- **`api/`**: API routes and Pydantic schemas (Interface Layer).
- **`parsers/`**: Core logic for PDF/text parsing and extraction (Deep Learning & Regex).
- **`rules/`**: Rule-based evaluation engine and scoring logic (Business Logic).
- **`services/`**: Infrastructure services like session management (Data Layer).
- **`tests/`**: Unit, integration, and robustness tests.
- **`uploads/`**: Temporary storage for uploaded resumes.
- **`sessions/`**: JSON-based file persistence for user sessions.

## Key Components

- **`main.py`**: Application entry point. Configures CORS and loads the Spacy NLP model on startup.
- **`parsers/jd_parser.py`**: Extracts skills and requirements from Job Descriptions.
- **`parsers/resume_parser.py`**: Parse PDFs and extracts structured resume data.
- **`rules/engine.py`**: The "brain" of the fit analysis.
  - Deterministic evaluation (rule-based).
  - Domain-specific logic (Finance, Healthcare, Tech).
  - Gap Analysis and Logic.

## Setup & Running

1.  **Environment**: Ensure Python 3.10+ is installed.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```
    *Note: If you encounter Pydantic/Spacy conflicts, ensure `pydantic<2.0.0` is installed.*

3.  **Run Server**:
    ```bash
    python -m uvicorn main:app --reload
    ```
    Server runs at `http://localhost:8000`.

## Testing

Run the full test suite using pytest:

```bash
python -m pytest tests/
```
