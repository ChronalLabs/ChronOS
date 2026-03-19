"""
CivicFix - Auth Router
Signup, Login, and user profile endpoints
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import random
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, TokenResponse, UserResponse, OTPRequest, OTPVerify, FirebaseLoginRequest
from app.config import settings
from app.middleware.auth import (
    hash_password, verify_password, create_access_token, require_user
)

logger = logging.getLogger("civicfix.auth")
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        display_name=data.display_name,
        provider="local",
        role="user",
    )
    db.add(user)
    await db.flush()

    token = create_access_token(user.id, user.role)
    logger.info(f"New user registered: {user.email}")

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        display_name=user.display_name,
        role=user.role,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.role)
    logger.info(f"User logged in: {user.email}")

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        display_name=user.display_name,
        role=user.role,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(require_user)):
    """Get current user profile."""
    return user


@router.post("/firebase-login", response_model=TokenResponse)
async def firebase_login(data: FirebaseLoginRequest, db: AsyncSession = Depends(get_db)):
    """Login/register via Firebase ID token."""
    try:
        # Decode the Google ID token to extract user info
        # In production, verify with Firebase Admin SDK
        from jose import jwt as jose_jwt
        claims = jose_jwt.get_unverified_claims(data.firebase_token)
        email = claims.get("email")
        name = claims.get("name") or claims.get("email", "").split("@")[0]

        if not email:
            raise HTTPException(status_code=400, detail="Could not extract email from token")
    except Exception as e:
        logger.error(f"Firebase token decode failed: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")

    email_lower = email.lower()

    # Check if user exists
    result = await db.execute(select(User).where(User.email == email_lower))
    user = result.scalar_one_or_none()

    if not user:
        # Create new user from Google sign-in
        user = User(
            email=email_lower,
            password_hash=None,
            display_name=name,
            provider="firebase",
            role="user",
        )
        db.add(user)
        await db.flush()
        logger.info(f"New user registered via Firebase: {user.email}")
    else:
        logger.info(f"Existing user logged in via Firebase: {user.email}")

    token = create_access_token(user.id, user.role)
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        display_name=user.display_name,
        role=user.role,
    )


# --- OTP System ---
otp_store = {}  # Format: {email: {"code": "123456", "expires": datetime}}

def send_otp_email(recipient_email: str, code: str):
    if not settings.SMTP_SERVER or not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning(f"SMTP not configured. Skipping email send. Code for {recipient_email} is: {code}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your CivicFix Login Code"
    msg["From"] = settings.SMTP_USERNAME or "noreply@civicfix.com"
    msg["To"] = recipient_email

    text = f"Your CivicFix login code is: {code}\n\nIt expires in 10 minutes."
    html = f"<html><body><h3>CivicFix Login</h3><p>Your one-time login code is: <strong>{code}</strong></p><p>It expires in 10 minutes.</p></body></html>"
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(msg["From"], [recipient_email], msg.as_string())
        server.quit()
        logger.info(f"OTP email sent to {recipient_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")

@router.post("/request-otp")
async def request_otp(data: OTPRequest, background_tasks: BackgroundTasks):
    code = f"{random.randint(100000, 999999)}"
    expires = datetime.utcnow() + timedelta(minutes=10)
    email_lower = data.email.lower()
    
    otp_store[email_lower] = {"code": code, "expires": expires}
    logger.info(f"Generated OTP for {email_lower}")
    
    background_tasks.add_task(send_otp_email, email_lower, code)
    return {"message": "OTP sent if email is valid", "expires_in": 600}

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(data: OTPVerify, db: AsyncSession = Depends(get_db)):
    email_lower = data.email.lower()
    store = otp_store.get(email_lower)
    
    if not store:
        raise HTTPException(status_code=400, detail="OTP expired or invalid")
        
    if store["code"] != data.code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")
        
    if datetime.utcnow() > store["expires"]:
        del otp_store[email_lower]
        raise HTTPException(status_code=400, detail="OTP expired")
        
    # Valid OTP! Remove it
    del otp_store[email_lower]
    
    # Sign up user
    result = await db.execute(select(User).where(User.email == email_lower))
    user = result.scalar_one_or_none()
    
    if user:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
        
    user = User(
        email=email_lower,
        password_hash=hash_password(data.password),
        display_name=data.display_name or email_lower.split('@')[0],
        provider="local",
        role="user",
    )
    db.add(user)
    await db.flush()
    logger.info(f"New user registered via OTP: {user.email}")
        
    token = create_access_token(user.id, user.role)
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        display_name=user.display_name,
        role=user.role,
    )
