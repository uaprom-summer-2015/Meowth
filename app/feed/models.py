from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    title = Column(String(300))
    text = Column(Text())
    category = Column(String(50))

    def __init__(self, title, text, category):
        self.title = title
        self.text = text
        self.category = category

    def __str__(self):
        return self.title
