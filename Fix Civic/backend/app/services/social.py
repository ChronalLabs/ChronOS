"""
CivicFix - Social Posting Service (X / Twitter)
Posts reports to X with retry/backoff. Simulates if keys missing.
"""
import uuid
import logging
from app.config import settings

logger = logging.getLogger("civicfix.social")


async def post_to_x(
    complaint_text: str,
    tweet_text: str,
    image_url: str | None = None,
    image_bytes: bytes | None = None,
) -> dict:
    """
    Post a report to X (Twitter).
    Returns dict with posted_status, tweet_id/mock_id, message.
    """
    has_keys = all([
        settings.X_API_KEY,
        settings.X_API_SECRET,
        settings.X_ACCESS_TOKEN,
        settings.X_ACCESS_TOKEN_SECRET,
    ])

    if settings.MOCK_MODE or not has_keys:
        return _simulate_post(tweet_text, image_url)

    return await _real_post(tweet_text, image_bytes)


def _simulate_post(tweet_text: str, image_url: str | None) -> dict:
    """Simulate posting to X when keys are not configured."""
    mock_id = f"mock_{uuid.uuid4().hex[:12]}"
    logger.info(
        f"[MOCK] SIMULATED X POST\n"
        f"  Mock ID: {mock_id}\n"
        f"  Text: {tweet_text}\n"
        f"  Image: {image_url or 'none'}"
    )
    return {
        "posted_status": "simulated",
        "tweet_id": None,
        "mock_id": mock_id,
        "message": "SIMULATED_POST — X API keys not configured. Post logged to console.",
    }


async def _real_post(tweet_text: str, image_bytes: bytes | None) -> dict:
    """Post to X using Tweepy with retry."""
    try:
        import tweepy

        auth = tweepy.OAuth1UserHandler(
            settings.X_API_KEY,
            settings.X_API_SECRET,
            settings.X_ACCESS_TOKEN,
            settings.X_ACCESS_TOKEN_SECRET,
        )

        api = tweepy.API(auth, retry_count=3, retry_delay=5, wait_on_rate_limit=True)

        client = tweepy.Client(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
        )

        # Upload image if available
        media_ids = []
        if image_bytes:
            try:
                from io import BytesIO
                media = api.media_upload(
                    filename="upload.jpg", 
                    file=BytesIO(image_bytes),
                    chunked=True,
                    media_category="tweet_image"
                )
                media_ids = [media.media_id]
            except Exception as e:
                logger.warning(f"Image upload to X failed: {e}")

        # Post tweet
        if media_ids:
            response = client.create_tweet(text=tweet_text, media_ids=media_ids)
        else:
            response = client.create_tweet(text=tweet_text)

        tweet_id = str(response.data['id'])
        logger.info(f"Posted to X successfully. Tweet ID: {tweet_id}")

        return {
            "posted_status": "posted",
            "tweet_id": tweet_id,
            "mock_id": None,
            "message": f"Successfully posted to X. Tweet ID: {tweet_id}",
        }

    except Exception as e:
        logger.error(f"Failed to post to X: {e}")
        return {
            "posted_status": "failed",
            "tweet_id": None,
            "mock_id": None,
            "message": f"Failed to post to X: {str(e)}",
        }
