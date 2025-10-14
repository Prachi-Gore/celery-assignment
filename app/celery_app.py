import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

celery = Celery("news_tasks", broker=REDIS_URL, backend=REDIS_URL)

celery.conf.beat_schedule = {
    "fetch-news-every-minute": {
        "task": "app.tasks.fetch_and_store_news",
        "schedule": 60.0,
    },
}
celery.conf.timezone = "UTC"

celery.autodiscover_tasks(["app"])

if __name__ == "__main__":
    celery.start()
