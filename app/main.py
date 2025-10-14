from fastapi import FastAPI, Query, Depends, HTTPException
from datetime import datetime, time as dt_time
from app.database import SessionLocal, engine
from app import models
from app.middleware import TimingMiddleware
import app.logger_config  # initializes logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Fetch API")
app.add_middleware(TimingMiddleware)

def get_db():
    db = SessionLocal()
    try:
        yield db # database connection remains open indefinitely after each request if we use return here
    finally:
        db.close()

# http://127.0.0.1:8000/news?date=2025-10-12
@app.get("/news")
def get_news(date: str, db=Depends(get_db)):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    start = datetime.combine(dt, dt_time.min)
    end = datetime.combine(dt, dt_time.max)
    articles = db.query(models.Article).filter(models.Article.publishedAt.between(start, end)).all()
    print("title ",articles[0].title)
    return [
        {
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "publishedAt": a.publishedAt.isoformat() if a.publishedAt else None,
            "url": a.url,
        } for a in articles
    ]
