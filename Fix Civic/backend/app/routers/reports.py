"""
CivicFix - Reports Router
Core API endpoints for report CRUD and social posting
"""
import logging
from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.database import get_db
from app.models import Report, User
from app.schemas import (
    ReportResponse, ReportCreateResponse, ReportListResponse,
    PostToXResponse, AdminUpdateReport, IssueType
)
from app.middleware.auth import get_current_user, require_admin
from app.middleware.rate_limit import check_rate_limit
from app.services.storage import upload_image, validate_image
from app.services.geocoding import reverse_geocode
from app.services.social import post_to_x
from app.services.complaint import generate_complaint_text, generate_tweet_text, generate_resolved_tweet_text, generate_declined_tweet_text
from app.routers.settings import is_auto_post_enabled
from app.utils.audit import log_action

logger = logging.getLogger("civicfix.reports")
router = APIRouter(prefix="/api/v1", tags=["Reports"])


@router.post("/report", response_model=ReportCreateResponse, status_code=201)
async def create_report(
    image: UploadFile = File(...),
    issue_type: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    timestamp: Optional[str] = Form(None),
    device_id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """
    Submit a new civic issue report.
    Accepts multipart/form-data with image, issue data, and GPS coordinates.
    """
    # Rate limiting
    identifier = user.id if user else (device_id or "anonymous")
    await check_rate_limit(identifier)

    # Validate issue_type
    allowed_types = [e.value for e in IssueType]
    if issue_type not in allowed_types:
        raise HTTPException(400, f"issue_type must be one of: {', '.join(allowed_types)}")

    # Validate description
    if not description or len(description) > 500:
        raise HTTPException(400, "Description is required (max 500 chars)")

    # Validate coordinates
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise HTTPException(400, "Invalid coordinates")

    # Validate & upload image
    file_bytes = await image.read()
    validation_error = await validate_image(
        image.content_type or "", len(file_bytes), image.filename or "upload.jpg"
    )
    if validation_error:
        raise HTTPException(400, validation_error)

    # Upload to storage
    storage_result = await upload_image(file_bytes, image.filename or "upload.jpg")

    # Reverse geocode
    address = await reverse_geocode(latitude, longitude)

    # Generate complaint text
    complaint_text = generate_complaint_text(
        issue_type=issue_type,
        description=description,
        address=address,
        latitude=latitude,
        longitude=longitude,
    )

    incident_date = None
    if timestamp:
        try:
            # Handle standard ISO format strings ending in Z or with timezone offset
            incident_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            logger.warning(f"Failed to parse timestamp: {timestamp}")

    # Create report record
    report = Report(
        user_id=user.id if user else None,
        issue_type=issue_type,
        description=description,
        latitude=latitude,
        longitude=longitude,
        address=address,
        incident_date=incident_date,
        image_url=storage_result["image_url"],
        thumbnail_url=storage_result.get("thumbnail_url"),
        complaint_text=complaint_text,
        device_id=device_id,
        status="pending",
    )
    db.add(report)
    await db.flush()

    # Audit log
    await log_action(db, "report_created", actor=identifier, report_id=report.id)
    logger.info(f"Report created: {report.id} by {identifier}")

    # Auto-post to X if enabled
    if is_auto_post_enabled():
        try:
            tweet_text = generate_tweet_text(
                issue_type=issue_type,
                description=description,
                address=address or "",
                latitude=latitude,
                longitude=longitude,
            )
            x_result = await post_to_x(
                complaint_text=complaint_text,
                tweet_text=tweet_text,
                image_url=storage_result["image_url"],
                image_bytes=file_bytes,
            )
            if x_result["posted_status"] == "posted":
                report.posted_to_x = True
                report.x_post_id = x_result["tweet_id"]
            elif x_result["posted_status"] == "simulated":
                report.posted_to_x = False
                report.x_post_id = x_result["mock_id"]
            await db.flush()
            await log_action(
                db, "auto_posted_to_x", actor="system",
                report_id=report.id, note=x_result["message"]
            )
            logger.info(f"Auto-posted report {report.id} to X: {x_result['posted_status']}")
        except Exception as e:
            logger.warning(f"Auto-post to X failed for report {report.id}: {e}")

    return ReportCreateResponse(
        report_id=report.id,
        complaint_text=complaint_text,
        image_url=storage_result["image_url"],
        address=address,
    )


@router.get("/reports", response_model=ReportListResponse)
async def list_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    issue_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """
    List reports. Admin sees all; regular user sees own reports.
    Supports pagination and filtering.
    """
    query = select(Report)

    # Filter by user unless admin
    if user and user.role != "admin":
        query = query.where(Report.user_id == user.id)
    elif not user:
        raise HTTPException(401, "Authentication required")

    # Apply filters
    if issue_type:
        query = query.where(Report.issue_type == issue_type)
    if status:
        query = query.where(Report.status == status)

    # Count total
    count_q = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_q)
    total = total_result.scalar() or 0

    # Paginate
    query = query.order_by(desc(Report.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    reports = result.scalars().all()

    return ReportListResponse(
        reports=[ReportResponse.model_validate(r) for r in reports],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """Get a single report by ID."""
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(404, "Report not found")

    # Check access
    if user and user.role != "admin" and report.user_id != user.id:
        raise HTTPException(403, "Access denied")

    return ReportResponse.model_validate(report)


@router.put("/reports/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: str,
    data: AdminUpdateReport,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Admin: update report status or add admin note."""
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(404, "Report not found")

    if data.status:
        report.status = data.status.value
    if data.admin_note is not None:
        report.admin_note = data.admin_note

    await db.flush()
    await log_action(
        db, "report_updated", actor=admin.email,
        report_id=report_id, note=f"status={data.status}, note={data.admin_note}"
    )

    return ReportResponse.model_validate(report)


@router.post("/reports/{report_id}/post-to-x", response_model=PostToXResponse)
async def post_report_to_x(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Post a report to X (Twitter). Simulates if API keys are not configured."""
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(404, "Report not found")

    if report.posted_to_x:
        raise HTTPException(400, "Report already posted to X")

    # Generate tweet text
    tweet_text = generate_tweet_text(
        issue_type=report.issue_type,
        description=report.description,
        address=report.address or "",
        latitude=report.latitude,
        longitude=report.longitude,
    )

    # Fetch image bytes if available so manual posts include media
    image_bytes = None
    if report.image_url:
        try:
            if report.image_url.startswith("/mock_uploads"):
                import os
                file_path = f".{report.image_url}"
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        image_bytes = f.read()
            elif report.image_url.startswith("http"):
                import httpx
                async with httpx.AsyncClient() as client:
                    resp = await client.get(report.image_url)
                    if resp.status_code == 200:
                        image_bytes = resp.content
        except Exception as e:
            logger.warning(f"Failed to fetch image bytes for manual X post: {e}")

    # Post to X
    x_result = await post_to_x(
        complaint_text=report.complaint_text or "",
        tweet_text=tweet_text,
        image_url=report.image_url,
        image_bytes=image_bytes,
    )

    # Update report
    if x_result["posted_status"] == "posted":
        report.posted_to_x = True
        report.x_post_id = x_result["tweet_id"]
    elif x_result["posted_status"] == "simulated":
        report.posted_to_x = False
        report.x_post_id = x_result["mock_id"]

    await db.flush()
    await log_action(
        db, "posted_to_x", actor=admin.email,
        report_id=report_id, note=x_result["message"]
    )

    return PostToXResponse(**x_result)


@router.post("/reports/{report_id}/resolve")
async def resolve_report(
    report_id: str,
    image: UploadFile = File(...),
    resolved_note: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Admin: resolve a report with a resolution photo.
    Uploads the resolution image, marks the report as resolved,
    and generates a resolved tweet text for the admin to post.
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(404, "Report not found")

    # Validate & upload resolution image
    file_bytes = await image.read()
    validation_error = await validate_image(
        image.content_type or "", len(file_bytes), image.filename or "upload.jpg"
    )
    if validation_error:
        raise HTTPException(400, validation_error)

    storage_result = await upload_image(file_bytes, image.filename or "resolved.jpg")

    # Update report
    report.status = "resolved"
    report.resolved_image_url = storage_result["image_url"]
    report.resolved_at = datetime.now(timezone.utc)
    report.resolved_by = admin.email
    if resolved_note:
        report.resolved_note = resolved_note
        report.admin_note = resolved_note  # Also update admin_note for consistency

    await db.flush()

    # Audit log
    await log_action(
        db, "report_resolved", actor=admin.email,
        report_id=report_id, note=f"Resolved with image: {storage_result['image_url']}"
    )
    logger.info(f"Report {report_id} resolved by {admin.email}")

    # Generate resolved tweet text
    resolved_tweet = generate_resolved_tweet_text(
        issue_type=report.issue_type,
        address=report.address or "",
        user_twitter_handle=None,  # Can be extended later
    )

    return JSONResponse(content={
        "report": ReportResponse.model_validate(report).model_dump(mode="json"),
        "resolved_tweet": resolved_tweet,
        "message": "Report resolved successfully",
    })


@router.post("/reports/{report_id}/decline")
async def decline_report(
    report_id: str,
    decline_reason: str = Form("Fake report"),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Admin: decline a report and mark it as fake/invalid.
    Generates a declined tweet text for the admin to post.
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(404, "Report not found")

    # Update report
    report.status = "declined"
    report.is_fake = True
    report.declined_at = datetime.now(timezone.utc)
    report.declined_by = admin.email
    report.decline_reason = decline_reason
    report.admin_note = f"Declined: {decline_reason}"

    await db.flush()

    # Audit log
    await log_action(
        db, "report_declined", actor=admin.email,
        report_id=report_id, note=f"Declined: {decline_reason}"
    )
    logger.info(f"Report {report_id} declined by {admin.email}: {decline_reason}")

    # Generate declined tweet text
    declined_tweet = generate_declined_tweet_text(
        issue_type=report.issue_type,
        address=report.address or "",
        decline_reason=decline_reason,
        user_twitter_handle=None,
    )

    return JSONResponse(content={
        "report": ReportResponse.model_validate(report).model_dump(mode="json"),
        "declined_tweet": declined_tweet,
        "message": "Report declined successfully",
    })
