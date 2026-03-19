"""
CivicFix - Complaint Text Generator
Generates formatted complaint text from report data
"""
from datetime import datetime, timezone


def generate_complaint_text(
    issue_type: str,
    description: str,
    address: str,
    latitude: float,
    longitude: float,
    report_date: datetime | None = None,
) -> str:
    """Generate a formatted complaint text for a report."""
    if report_date is None:
        report_date = datetime.now(timezone.utc)

    date_str = report_date.strftime("%d %b %Y")
    maps_link = f"https://maps.google.com/?q={latitude},{longitude}"

    complaint = (
        f"🚨 Civic Issue Report\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 Issue Type: {issue_type}\n"
        f"📝 Description: {description}\n"
        f"📍 Location: {address}\n"
        f"🗺️ Coordinates: {latitude},{longitude}\n"
        f"🔗 Map: {maps_link}\n"
        f"📅 Date: {date_str}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Reported via CivicFix"
    )
    return complaint


def generate_tweet_text(
    issue_type: str,
    description: str,
    address: str,
    latitude: float,
    longitude: float,
) -> str:
    """Generate a tweet-length complaint text (max 280 chars)."""
    maps_link = f"https://maps.google.com/?q={latitude},{longitude}"

    # Truncate description to fit tweet limit
    max_desc_len = 100
    short_desc = description[:max_desc_len] + "..." if len(description) > max_desc_len else description

    tweet = (
        f"🚨 {issue_type} reported!\n"
        f"{short_desc}\n"
        f"📍 {address[:80]}\n"
        f"🔗 {maps_link}\n"
        f"#CivicFix #CitizenReport"
    )

    # Ensure tweet fits limit
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return tweet


# --- Gwalior area-to-authority mapping ---
GWALIOR_AUTHORITY_MAP = {
    "lashkar": "@GwaliorMC",
    "morar": "@GwaliorMC",
    "thatipur": "@GwaliorMC",
    "city center": "@GwaliorMC",
    "hazira": "@GwaliorMC",
    "bahodapur": "@GwaliorMC",
    "dabra": "@DabraMC",
    "gird": "@GwaliorMC",
    "phool bagh": "@GwaliorMC",
    "jayendraganj": "@GwaliorMC",
    "kampoo": "@GwaliorMC",
    "padav": "@GwaliorMC",
    "birla nagar": "@GwaliorMC",
    "university": "@GwaliorMC",
}
DEFAULT_AUTHORITY = "@GwaliorMC"


def get_authority_tag(address: str) -> str:
    """Get the relevant authority X handle based on the area in the address."""
    if not address:
        return DEFAULT_AUTHORITY
    address_lower = address.lower()
    for area, handle in GWALIOR_AUTHORITY_MAP.items():
        if area in address_lower:
            return handle
    return DEFAULT_AUTHORITY


def generate_resolved_tweet_text(
    issue_type: str,
    address: str,
    user_twitter_handle: str | None = None,
    authority_tag: str | None = None,
) -> str:
    """Generate a tweet for a resolved report with user and authority tags."""
    if not authority_tag:
        authority_tag = get_authority_tag(address)

    location = address[:80] if address else "Gwalior"

    user_mention = f"\n{user_twitter_handle}" if user_twitter_handle else ""

    tweet = (
        f"✅ Issue Resolved!\n\n"
        f"📍 Location: {location}\n"
        f"📝 The reported {issue_type.lower()} has been successfully resolved.\n\n"
        f"Thanks for reporting 🙏"
        f"{user_mention} {authority_tag} #CivicFix #Gwalior"
    )

    # Ensure tweet fits limit
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return tweet


def generate_declined_tweet_text(
    issue_type: str,
    address: str,
    decline_reason: str = "Invalid report",
    user_twitter_handle: str | None = None,
    authority_tag: str | None = None,
) -> str:
    """Generate a tweet for a declined/fake report with user and authority tags."""
    if not authority_tag:
        authority_tag = get_authority_tag(address)

    location = address[:80] if address else "Gwalior"

    user_mention = f"\n{user_twitter_handle}" if user_twitter_handle else ""

    tweet = (
        f"❌ Report Declined\n\n"
        f"📍 Location: {location}\n"
        f"📝 This report has been marked as fake / invalid.\n\n"
        f"Reason: {decline_reason}\n"
        f"Thanks for helping keep CivicFix clean 🙏"
        f"{user_mention} {authority_tag} #CivicFix #Gwalior"
    )

    # Ensure tweet fits limit
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return tweet

