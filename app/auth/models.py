from sqlalchemy import Column, Integer, String
from app.database import Base
from hashlib import sha256
from app import app

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    password = Column(String(50))
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30), unique=True)

    def __init__(self, login, password, name, surname, email):
        self.name = name
        self.email = email
        self.login = login
        self.password = sha256(password + app.config['SALT']).hexdigest()
        self.surname = surname

    def __repr__(self):
        return '<User %r>' % (self.name + self.surname)