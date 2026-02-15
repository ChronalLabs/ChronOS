# 🌍 Eco-Guard AI

### Smart Environmental Intelligence & AQI Prediction Platform

**Eco-Guard AI** is a Machine Learning--powered environmental
intelligence system that predicts **Air Quality Index (AQI)** using
pollutant concentration data and transforms complex environmental
information into **clear health insights, visual analytics, and
downloadable professional reports** through a modern web application.

Developed as part of the **ChronalLabs open-source ecosystem**, this
project aims to make **air quality awareness accessible to citizens,
researchers, and policymakers**.

------------------------------------------------------------------------

# 📌 Overview

Air pollution is one of the most critical global environmental
challenges.\
Urban regions frequently experience hazardous AQI levels due to:

-   Industrial emissions\
-   Vehicular pollution\
-   Construction dust\
-   Fossil fuel burning\
-   Seasonal environmental factors

Cities like **Delhi, Ahmedabad, and Lucknow** regularly report
**unhealthy to severe AQI levels**, highlighting the urgent need for
**data-driven public awareness tools**.

------------------------------------------------------------------------

# ❗ Core Challenges

-   AQI numbers are difficult for the general public to interpret\
-   Limited real-time understanding of health risks\
-   Environmental datasets are scattered and complex\
-   Lack of simplified AI-based AQI prediction tools\
-   Insufficient accessible environmental analytics platforms

------------------------------------------------------------------------

# 🎯 Project Objectives

Eco-Guard AI is designed to:

-   Predict AQI using pollutant parameters\
-   Classify AQI into **health-risk categories**\
-   Provide **environmental awareness insights**\
-   Visualize pollution trends with **interactive charts**\
-   Generate **downloadable professional PDF reports**

------------------------------------------------------------------------

# 🧠 Solution Architecture

    Pollutant Input
          ↓
    Data Preprocessing
          ↓
    Random Forest ML Model
          ↓
    AQI Prediction
          ↓
    Health Risk Classification
          ↓
    Visual Insights + PDF Report

------------------------------------------------------------------------

# 📊 Dataset

**Source:** Kaggle -- India Air Quality Dataset\
**Primary File:** `city_day.csv`

### Key Features

  Feature   Description
  --------- ------------------------------------
  PM2.5     Fine particulate matter (≤ 2.5µm)
  PM10      Coarse particulate matter (≤ 10µm)
  NO₂       Nitrogen dioxide
  CO        Carbon monoxide
  SO₂       Sulfur dioxide
  O₃        Ozone
  AQI       Target variable

------------------------------------------------------------------------

# ⚙️ Methodology

## 1. Data Preprocessing

-   Feature selection for major pollutants\
-   Missing value handling\
-   Train--test split (**80/20**)

## 2. Model Selection

**Algorithm:** RandomForestRegressor

**Why Random Forest?** - Captures nonlinear relationships\
- Strong performance on tabular environmental data\
- Resistant to overfitting\
- Provides **feature importance insights**

## 3. Evaluation Metrics

-   **R² Score**\
-   **Mean Squared Error (MSE)**

## 4. Model Persistence

-   Saved using **joblib**\
-   Dynamically loaded in the **Streamlit app**

------------------------------------------------------------------------

# 🖥️ Application Features

## 🏠 Home

-   Project introduction\
-   Environmental awareness content\
-   Importance of pollution monitoring

## 📈 AQI Prediction

-   Slider-based pollutant inputs\
-   Real-time ML AQI prediction\
-   Color-coded health category display

## 📊 Model Insights

-   R² performance score\
-   Feature importance visualization\
-   Correlation heatmap

## 📥 Report Generation

-   Downloadable **professional PDF report**\
-   AQI value, city name, and health advisory\
-   Embedded charts and analytics

------------------------------------------------------------------------

# 🚦 Health Risk Classification

  AQI Range   Category    Health Impact
  ----------- ----------- ---------------------------
  0--50       Good        Minimal impact
  51--100     Moderate    Acceptable
  101--200    Poor        Sensitive groups affected
  201--300    Very Poor   Respiratory discomfort
  301+        Severe      Serious health effects

------------------------------------------------------------------------

# 🛠️ Tech Stack

### Frontend

-   Streamlit\
-   Plotly\
-   Matplotlib\
-   Seaborn

### Backend

-   Python\
-   Pandas, NumPy\
-   Scikit-learn

### Reporting

-   ReportLab\
-   Kaleido

------------------------------------------------------------------------

# 📁 Project Structure

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

------------------------------------------------------------------------

# 🚀 Getting Started

### 1️⃣ Create Virtual Environment

``` bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 3️⃣ Train the Model

``` bash
python train_model.py
```

### 4️⃣ Run the App

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

# 🌱 Impact

### Citizens

-   Understand pollution risks\
-   Plan safe outdoor activities\
-   Access downloadable AQI reports

### Students & Researchers

-   Study pollutant correlations\
-   Explore ML feature importance\
-   Learn real-world ML deployment

### Policymakers

-   Identify pollution contributors\
-   Enable **data-driven environmental decisions**

------------------------------------------------------------------------

# 🔮 Future Roadmap

-   Real-time AQI API integration\
-   Historical city-wise trend analytics\
-   Cloud deployment (Docker + CI/CD)\
-   User authentication & dashboards\
-   React + FastAPI production architecture\
-   Multi-model comparison system

------------------------------------------------------------------------

# 🏁 Conclusion

**Eco-Guard AI** demonstrates how Machine Learning, visualization, and
web technologies can combine to solve **real-world environmental
challenges**.\
By converting raw pollution data into **clear insights and professional
reports**, the platform strengthens **environmental awareness and
data-driven decision-making**.

------------------------------------------------------------------------

# 👨‍💻 Author

**Ananya Sharma**\
Machine Learning & Environmental Intelligence Developer

🔗 LinkedIn:\
https://www.linkedin.com/in/ananya-sharma-dev/
