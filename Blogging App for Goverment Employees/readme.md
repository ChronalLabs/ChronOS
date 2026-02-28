# Gov-Gazette 📰

A government-focused blogging platform built with **FastAPI** backend and **HTML/CSS** frontend. Government employees can post official gazette notifications, while normal users can only comment and engage.

[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-brightgreen)](https://gov-gazette.onrender.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20Fast%20API-blue)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-orange)](https://www.python.org/)

## ✨ Features

- **Role-based Access Control**
  - Government employees: Create, edit, delete posts
  - Normal users: View posts and comment only
- **Blog Management System** for official government notifications
- **Responsive HTML/CSS** frontend
- **FastAPI** RESTful backend APIs
- **Real-time** comment system
- **Secure** authentication system

## 🚀 Live Demo

[https://gov-gazette.onrender.com/](https://gov-gazette.onrender.com/)

## 🛠 Tech Stack

Backend: FastAPI, Python
Frontend: HTML5, CSS3, Vanilla JavaScript
Database: SQLite (Development) / PostgreSQL (Production)
Deployment: Render
Authentication: JWT/Session-based

text

## 📋 Quick Start

### Prerequisites
- Python 3.9+
- Git

### Clone & Run Locally

```bash
git clone [https://github.com/yourusername/gov-gazette.git](https://github.com/ananyascodes/Gov-Gazette/tree/main)
cd gov-gazette
pip install -r requirements.txt
cp .env.example .env
# Update .env with your configuration
uvicorn main:app --reload --port 8000
Visit http://localhost:8000

Environment Variables
text
DATABASE_URL=sqlite:///./gov_gazette.db
SECRET_KEY=your-secret-key-here
DEBUG=True
👥 User Roles & Permissions
Role	Can Post Blogs	Can Comment	Can Edit Posts	Can Delete Posts
Gov Employee	✅ Yes	✅ Yes	✅ Yes	✅ Yes
Normal User	❌ No	✅ Yes	❌ No	❌ No


📖 API Endpoints
Method	Endpoint	Description	Auth Required
POST	/api/posts/	Create new blog post	Gov Employee
GET	/api/posts/	List all posts	No
GET	/api/posts/{id}	Get single post	No
POST	/api/posts/{id}/comments	Add comment	User
PUT	/api/posts/{id}	Update post	Gov Employee



🏗 Project Structure
text
gov-gazette/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API routes
│   ├── static/              # CSS, JS, images
│   └── templates/           # HTML templates
├── requirements.txt
├── .env.example
└── README.md



🔐 Authentication
Gov Employees: Register/Login with government credentials

Normal Users: Register/Login as regular users

Role-based permissions enforced at API level

🚀 Deployment
Render (Recommended)
Fork this repo

Connect to Render

Set build command: pip install -r requirements.txt

Set start command: uvicorn main:app --host 0.0.0.0 --port $PORT

Other Platforms
Railway, Heroku, Fly.io, DigitalOcean


📄 License
This project is open source and available under the MIT License.

🙏 Acknowledgments
FastAPI - Amazing Python web framework

Render - Lightning-fast deployment platform

All contributors and government employees using the platform!
