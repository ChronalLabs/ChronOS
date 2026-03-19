"""
CivicFix Database Models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    display_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    provider = Column(String(50), default="local")  # local, firebase
    role = Column(String(20), default="user")  # user, admin
    created_at = Column(DateTime(timezone=True), default=utcnow)

    reports = relationship("Report", back_populates="user")


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    issue_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text, nullable=True)
    incident_date = Column(DateTime(timezone=True), nullable=True)
    image_url = Column(Text, nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    status = Column(String(20), default="pending")  # pending, approved, resolved, rejected
    complaint_text = Column(Text, nullable=True)
    admin_note = Column(Text, nullable=True)
    posted_to_x = Column(Boolean, default=False)
    x_post_id = Column(String(100), nullable=True)
    device_id = Column(String(100), nullable=True)
    resolved_image_url = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(String(255), nullable=True)
    resolved_note = Column(Text, nullable=True)
    declined_at = Column(DateTime(timezone=True), nullable=True)
    declined_by = Column(String(255), nullable=True)
    decline_reason = Column(Text, nullable=True)
    is_fake = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="reports")
    audit_logs = relationship("AuditLog", back_populates="report")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("reports.id"), nullable=True)
    action = Column(String(100), nullable=False)
    actor = Column(String(255), nullable=True)
    note = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=utcnow)

    report = relationship("Report", back_populates="audit_logs")
