from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from starlette.middleware.sessions import SessionMiddleware
import hashlib

# -------------------- APP SETUP --------------------
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this"
)

# -------------------- STATIC & TEMPLATES --------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -------------------- DATABASE --------------------
engine = create_engine(
    "sqlite:///blog.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# -------------------- MODELS --------------------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    position = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author = Column(String, nullable=False)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    blog_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

# -------------------- HELPERS --------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------- ROUTES --------------------

# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    blogs = db.query(Blog).order_by(Blog.created_at.desc()).all()
    employee = request.session.get("employee")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "blogs": blogs,
            "employee": employee
        }
    )

# -------------------- REGISTER --------------------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register_employee(
    request: Request,
    name: str = Form(...),
    contact: str = Form(...),
    sector: str = Form(...),
    position: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    employee = Employee(
        name=name,
        contact=contact,
        sector=sector,
        position=position,
        password=hash_password(password)
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    request.session["employee"] = {
        "id": employee.id,
        "name": employee.name
    }

    return RedirectResponse("/", status_code=302)

# -------------------- LOGIN --------------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_employee(
    request: Request,
    employee_id: int = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee or employee.password != hash_password(password):
        return RedirectResponse("/login", status_code=302)

    request.session["employee"] = {
        "id": employee.id,
        "name": employee.name
    }

    return RedirectResponse("/", status_code=302)

# -------------------- CREATE BLOG --------------------
@app.get("/create-blog", response_class=HTMLResponse)
def create_blog_page(request: Request):
    if not request.session.get("employee"):
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("create_blog.html", {"request": request})


@app.post("/create-blog")
def create_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...)
):
    employee = request.session.get("employee")
    if not employee:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()

    blog = Blog(
        title=title,
        content=content,
        author=employee["name"]
    )

    db.add(blog)
    db.commit()

    return RedirectResponse("/", status_code=302)


# -------------------- EDIT BLOG --------------------
@app.get("/blog/{blog_id}/edit", response_class=HTMLResponse)
def edit_blog_page(request: Request, blog_id: int):
    employee = request.session.get("employee")
    if not employee:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog or blog.author != employee["name"]:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "edit_blog.html",
        {
            "request": request,
            "blog": blog
        }
    )


@app.post("/blog/{blog_id}/edit")
def edit_blog(
    request: Request,
    blog_id: int,
    title: str = Form(...),
    content: str = Form(...)
):
    employee = request.session.get("employee")
    if not employee:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog or blog.author != employee["name"]:
        return RedirectResponse("/", status_code=302)

    blog.title = title
    blog.content = content
    db.commit()

    return RedirectResponse(f"/blog/{blog_id}", status_code=302)


# -------------------- DELETE BLOG --------------------
@app.post("/blog/{blog_id}/delete")
def delete_blog(request: Request, blog_id: int):
    employee = request.session.get("employee")
    if not employee:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog or blog.author != employee["name"]:
        return RedirectResponse("/", status_code=302)

    db.delete(blog)
    db.commit()

    return RedirectResponse("/", status_code=302)

# -------------------- BLOG DETAIL + COMMENTS --------------------
@app.get("/blog/{blog_id}", response_class=HTMLResponse)
def blog_detail(request: Request, blog_id: int):
    db = SessionLocal()

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        return RedirectResponse("/", status_code=302)

    comments = db.query(Comment)\
        .filter(Comment.blog_id == blog_id)\
        .order_by(Comment.created_at.desc())\
        .all()

    employee = request.session.get("employee")

    return templates.TemplateResponse(
        "blog_detail.html",
        {
            "request": request,
            "blog": blog,
            "comments": comments,
            "employee": employee
        }
    )


@app.post("/blog/{blog_id}/comment")
def add_comment(
    request: Request,
    blog_id: int,
    content: str = Form(...)
):
    employee = request.session.get("employee")
    if not employee:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()

    comment = Comment(
        content=content,
        author=employee["name"],
        blog_id=blog_id
    )

    db.add(comment)
    db.commit()

    return RedirectResponse(f"/blog/{blog_id}", status_code=302)

# -------------------- LOGOUT --------------------
@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
