from app.database import Base
from sqlalchemy import Column,Integer,String,Text,DateTime


class Article(Base):
    __tablename__="articles"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(255))
    author = Column(String(255))
    title = Column(String(512))
    description = Column(Text)
    url = Column(String(255), unique=True)
    urlToImage = Column(String(1024))
    publishedAt = Column(DateTime, index=True)
    content = Column(Text)