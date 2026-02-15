# EduGuard – Smart School Complaint & Feedback Portal

EduGuard is a Streamlit-based web application designed to simplify and digitize school complaint and feedback management.

It enables students and guardians to submit structured complaints while allowing administrators to review, track, and update issue statuses efficiently.

---

## 🎯 Problem Statement

Schools often lack a structured, transparent, and accessible grievance redressal system.

Common issues include:

- Informal complaint handling
- Lack of tracking mechanisms
- No structured categorization
- Limited transparency
- No digital status updates

EduGuard solves these issues by providing a simple digital platform for complaint submission and administrative tracking.

---

## 🚀 Features

### 👤 User Features
- Submit structured complaints
- Select complaint category
- Provide detailed issue descriptions
- Anonymous submission option
- Submit general feedback
- Clean and intuitive interface

### 🔐 Admin Features
- Secure admin login (session-based)
- View all complaints
- Expandable complaint view
- Update complaint status:
  - Pending
  - Checked
  - Solved
- View feedback dashboard

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- CSV-based storage
- HTML/CSS (custom styling)

---

## Project Structure
project-folder/
│
├── app.py
├── complaints.csv
├── feedback.csv
├── sikshasuraksha.JPG
└── README.md



---

## 📦 Installation & Setup

1️⃣ Clone the Repository
git clone URL OF THIS REPO
cd your-repo-folder

2️⃣ **Install Dependencies
pip install streamlit pandas pillow

3️⃣ Run the Application
streamlit run app.py



## Admin Credentials (Demo Version)
Admin ID: manan31
Password: byteedu


## 📊 Data Storage
Data is stored locally in:
complaints.csv
feedback.csv

## Each complaint includes:
Student details
Parent details
Complaint category
Complaint description
Status tracking



## UI Customization
Custom CSS styling
Sidebar navigation
Circular logo display
Dark input fields
Wide layout


## Current Limitations
CSV-based storage (not production ready)
Hardcoded admin credentials
No password hashing
No complaint ID system
No search or filtering system
No role-based authentication
No cloud database integration


## Future Improvements
Replace CSV with PostgreSQL or Firebase
Implement hashed password authentication
Add complaint ID tracking
Add email notifications
Add complaint filtering and search
Add analytics dashboard
Role-based access (Principal, Teacher, Admin)
Deployment-ready architecture


## Use Cases
School administration systems
Academic projects
Hackathons
Civic-tech demonstrations
Educational governance experiments



## Vision
**EduGuard aims to promote transparency, accountability, and structured grievance resolution in educational institutions.**
