from sqlalchemy import Column, Integer, String, Text
from project.database import Base, get_db


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
        self.save()

    def __repr__(self):
        return self.title

    def save(self):
        db = get_db()
        db.add(self)
        db.commit()
