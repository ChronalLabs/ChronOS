# 🌍 Eco-Guard AI  
## Smart Environmental Intelligence & AQI Prediction System

---

## 📌 Abstract

Eco-Guard AI is a Machine Learning powered environmental intelligence platform designed to predict Air Quality Index (AQI) using pollutant concentration data and provide actionable health advisory insights. The system transforms complex environmental data into understandable predictions, visual analytics, and downloadable professional reports through a modern multi-page web application.

This project aims to bridge the gap between environmental data and public awareness by making air quality analytics accessible to common citizens, researchers, and policymakers.

---

# 1️⃣ Problem Statement

Air pollution has emerged as one of the most severe environmental challenges globally. Urban regions frequently experience hazardous AQI levels due to:

- Industrial emissions  
- Vehicular pollution  
- Construction dust  
- Burning of fossil fuels  
- Seasonal environmental factors  

Cities such as Delhi, Ahmedabad, and Lucknow often report AQI values reaching unhealthy or severe levels.

### ❗ Core Issues Identified

1. AQI numbers are not easily interpretable by common users.  
2. People lack real-time understanding of health risks.  
3. Environmental data is complex and scattered.  
4. There is no simplified AI-based prediction interface for the public.  
5. Data-driven environmental awareness tools are limited.  

---

# 2️⃣ Project Objective

The primary objective of Eco-Guard AI is to:

- Predict AQI using pollutant parameters  
- Classify AQI into health risk categories  
- Provide environmental awareness insights  
- Visualize data patterns using interactive charts  
- Generate downloadable professional environmental reports  

---

# 3️⃣ Proposed Solution

Eco-Guard AI provides a web-based intelligent system that:

1. Accepts pollutant values as input  
2. Uses a trained Machine Learning model to predict AQI  
3. Categorizes air quality into standard health buckets  
4. Displays interactive data insights  
5. Generates structured PDF environmental assessment reports  

---

# 4️⃣ System Architecture

```
User Input (Pollutants)
        ↓
Data Preprocessing
        ↓
Machine Learning Model (Random Forest)
        ↓
AQI Prediction
        ↓
Health Risk Classification
        ↓
Visualization & Insights
        ↓
PDF Report Generation
```

---

# 5️⃣ Dataset Description

Dataset Source: Kaggle Air Quality Dataset (India)

Primary file used:
- city_day.csv

### Important Features Used

| Feature | Description |
|----------|-------------|
| PM2.5 | Fine particulate matter (≤2.5µm) |
| PM10 | Coarse particulate matter (≤10µm) |
| NO2 | Nitrogen dioxide |
| CO | Carbon monoxide |
| SO2 | Sulfur dioxide |
| O3 | Ozone |
| AQI | Air Quality Index (Target Variable) |

---

# 6️⃣ Methodology

## Step 1: Data Preprocessing

- Selection of relevant pollutant features  
- Handling missing values  
- Feature-target separation  
- Train-test split (80-20)  

## Step 2: Model Selection

Algorithm Used:
- RandomForestRegressor

Reason:
- Handles nonlinear relationships  
- Works well with tabular environmental data  
- Robust against overfitting  
- Provides feature importance scores  

## Step 3: Model Evaluation

Metrics Used:
- R² Score  
- Mean Squared Error  

## Step 4: Model Persistence

- Model saved using joblib  
- Loaded dynamically in the Streamlit application  

---

# 7️⃣ Application Features

## 🏠 Home Page
- Project overview  
- Environmental awareness section  
- Importance of pollution monitoring  

## 📈 AQI Prediction Page
- Slider-based pollutant input  
- Machine learning-based AQI prediction  
- Color-coded result display  
- Health category classification  

## 📊 Model Insights Page
- R² Accuracy Score  
- Feature Importance Visualization  
- Correlation Heatmap  

## 📥 Report Generation Page
- Professional PDF Environmental Report  
- City name and AQI value  
- Health advisory section  
- Embedded feature importance chart  

---

# 8️⃣ Health Risk Classification Logic

| AQI Range | Category | Health Impact |
|------------|-----------|---------------|
| 0–50 | Good | Minimal impact |
| 51–100 | Moderate | Acceptable |
| 101–200 | Poor | Sensitive groups affected |
| 201–300 | Very Poor | Respiratory discomfort |
| 301+ | Severe | Serious health effects |

---

# 9️⃣ Technologies Used

### Frontend
- Streamlit  
- Plotly  
- Matplotlib  
- Seaborn  

### Backend
- Python  
- Pandas  
- NumPy  
- Scikit-learn  

### Report Generation
- ReportLab  
- Kaleido  

---

# 🔟 Project Structure

```
EcoGuard/
│
├── app.py
├── train_model.py
├── requirements.txt
│
├── data/
│   └── city_day.csv
│
├── model/
│   └── aqi_model.pkl
│
├── assets/
│   └── style.css
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Predict_AQI.py
│   ├── 3_Model_Insights.py
│   └── Report_Download.py
│
└── utils/
    ├── helper.py
    └── report_generator.py
```

---

# 1️⃣1️⃣ How to Run the Project

### Step 1: Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies
```
pip install -r requirements.txt
```

### Step 3: Train the Model
```
python train_model.py
```

### Step 4: Run the Application
```
streamlit run app.py
```

---

# 1️⃣2️⃣ Impact & Use Cases

## For Citizens
- Understand pollution risks  
- Plan outdoor activities  
- Access downloadable environmental reports  

## For Students & Researchers
- Analyze pollutant correlations  
- Study feature importance  
- Understand ML model application in environmental science  

## For Policymakers
- Identify major pollution contributors  
- Support data-driven environmental decisions  

---

# 1️⃣3️⃣ Future Enhancements

- Real-time AQI API integration  
- City-wise historical trend analysis  
- Cloud deployment  
- User authentication system  
- Full production React + FastAPI version  
- Multi-model comparison dashboard  

---

# 1️⃣4️⃣ Conclusion

Eco-Guard AI demonstrates the practical application of Machine Learning in solving real-world environmental problems. By converting raw pollution data into actionable insights and professional reports, the system contributes toward increased environmental awareness and data-driven decision-making.
This project showcases the integration of data science, machine learning, visualization, and web deployment into a single intelligent environmental platform.

---

# 👨‍💻 Author
Developer - Ananya Sharma
linkedin - https://www.linkedin.com/in/ananya-sharma-dev/
Developed as a Machine Learning & Environmental Intelligence Project.
