# RefineX - AI Data Intelligence Platform

RefineX is a comprehensive AI-powered dataset cleaning and intelligence analysis system. It empowers businesses and researchers by automating the tedious processes of spreadsheet/CSV parsing, missing values detection, duplicate removal, and generating rich statistical visualization dashboards seamlessly.

## 🚀 Features

*   **Intelligent Dataset Parsing**: Drag and drop CSV uploads that auto-map data columns accurately.
*   **Automated Diagnostics**: Instantly detect missing entries and duplicates without writing any python scripts.
*   **Deep Statistical Analysis**: View rich visual correlation graphs, status breakdowns, and monthly trends.
*   **Data Export Pipeline**: Generate and export diagnostic analysis reports in PDF and CSV variants.
*   **Premium Modern UX**: Fully responsive glassmorphism UI built specifically for seamless data management workflows.

## 🛠 Tech Stack

*   **Frontend**: React 18, Next.js (App Router), TypeScript, Tailwind CSS, Recharts for dynamic visual mapping.
*   **Backend**: Python, FastAPI, Pydantic (currently mocked schema validation logic built for fast ML integration).
*   **Client Connection**: Axios integration across all endpoints fetching structured mock intelligence arrays.

## 💻 Running the Project Locally

The project consists of decoupled frontend and backend services logic to mimic real-world scalable MLOps environments.

### 1. Start the Backend API (FastAPI)
Open a terminal inside the backend directory:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
You can access the backend Swagger OpenAPI playground at `http://localhost:8000/docs`.

### 2. Start the Frontend (Next.js)
Open a separate terminal inside the frontend directory:
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:3000` to interact with the responsive dashboard!

## 🧩 Future Roadmap (Machine Learning Integrations)
This repository contains the completed UI frameworks and server schema mappings. Next architectural steps involve embedding actual `pandas`, `NumPy`, and `scikit-learn` algorithms into the backend `app/routes/analysis.py` files to replace the mock response engines with real statistical processing. 
