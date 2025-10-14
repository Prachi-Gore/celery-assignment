import os
import logging
import requests
from datetime import datetime
from app.celery_app import celery
from app.database import SessionLocal
from app.models import Article
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
logger = logging.getLogger(__name__)

@celery.task(name="app.tasks.fetch_and_store_news",bind=True, max_retries=3)
def fetch_and_store_news(self):
    db = SessionLocal()
    try:
        logger.info("Fetching news from NewsAPI...")

        params = {
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 50,
            "country": "us",
        }

        response = requests.get(
            "https://newsapi.org/v2/top-headlines", params=params, timeout=10
        )
        response.raise_for_status()

        articles = response.json().get("articles", [])
        count = 0

        for a in articles:
            # Skip if no URL or already exists in DB
            if not a.get("url") or db.query(Article).filter_by(url=a["url"]).first():
                continue

            # Convert publishedAt string → datetime object
            published_at_str = a.get("publishedAt")
            published_at = None
            if published_at_str:
                try:
                    # Convert ISO format to datetime with timezone
                    published_at = datetime.fromisoformat(
                        published_at_str.replace("Z", "+00:00")
                    )
                except ValueError:
                    logger.warning(f"Invalid publishedAt format: {published_at_str}")

            # Create Article object
            article_obj = Article(
                source=a.get("source", {}).get("name"),
                author=a.get("author"),
                title=a.get("title"),
                description=a.get("description"),
                url=a.get("url"),
                urlToImage=a.get("urlToImage"),
                publishedAt=published_at,
                content=a.get("content"),
            )

            db.add(article_obj)
            count += 1

        db.commit()
        logger.info(f"Stored {count} new articles.")

    except requests.RequestException as e:
        logger.error(f"News API error: {e}")
        raise self.retry(exc=e, countdown=60)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
    except Exception as e:
        logger.exception("Unexpected error in Celery task")
        db.rollback()
    finally:
        db.close()
