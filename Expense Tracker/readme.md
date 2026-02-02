# 💸 ExpenseTracker Pro

A sleek, lightweight **Personal Finance Dashboard** built with Python and Flask. This application allows users to track their daily spending, set monthly budgets, and visualize their financial habits through an intuitive web interface.

---

## 🚀 Features

* **User Authentication**: Secure Signup and Login system powered by `Flask-Login` with hashed passwords.
* **Monthly Budgeting**: Set a financial ceiling and monitor your remaining balance in real-time.
* **Expense Management**: Categorize and log daily expenses with timestamps and custom notes.
* **Dynamic Analytics**: Generates category-wise breakdowns (`JSON` ready) for front-end chart integration.
* **Persistent Storage**: Utilizes SQLAlchemy with SQLite for reliable, local data management.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.x, Flask |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Authentication** | Flask-Login, Werkzeug |
| **Frontend** | Jinja2 Templates, HTML5, CSS3 |

---

## 📂 Project Structure

```text
.
├── main.py              # Application entry point & route handlers
├── models.py            # Database schema (User, Expense, Budget)
├── static/              # CSS, JavaScript, and Images
├── templates/           # HTML Jinja2 templates
│   ├── index.html       # Main dashboard
│   ├── login.html       # Login page
│   └── signup.html      # Registration page
└── instance/
    └── database.db      # SQLite Database (generated automatically)



## Installation & Setup
Clone the repository

Bash
git clone [https://github.com/yourusername/expense-tracker.git](https://github.com/yourusername/expense-tracker.git)
cd expense-tracker
Create a virtual environment

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

Bash
pip install flask flask-sqlalchemy flask-login
Run the application

Bash
python main.py
The app will initialize the database and start at http://127.0.0.1:5000/.

🔐 Security Note
For production environments, ensure you change the SECRET_KEY in main.py:

Python
app.config['SECRET_KEY'] = 'your-secure-random-string-here'
📊 Database Logic
The application follows a relational structure:

User Model: Handles profile data and password hashing.

Expense Model: Tracks individual transactions linked to a User ID.

Budget Model: Stores a one-to-one relationship for the user's monthly spending limit.

📝 Roadmap & Future Enhancements
[ ] Data Visualization: Integrate Chart.js to render the chart_data dictionary.

[ ] Date Filters: View expenses from previous months or specific date ranges.

[ ] Export Data: Download expense reports in CSV or PDF format.

[ ] UI/UX: Transition to a Tailwind CSS or Bootstrap 5 framework for better responsiveness.

🤝 Contributing
Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Developed with ❤️ by Ananaya Sharma and Ananya Tiwari

Linkedin urls :-
a. Ananya Sharma ---> https://www.linkedin.com/in/ananya-sharma-dev/
b. Ananya Tiwari ---> https://www.linkedin.com/in/ananya-tiwari-devs/
