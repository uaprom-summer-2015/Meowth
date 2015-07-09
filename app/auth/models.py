from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from hashlib import sha256
from app import app

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    password = Column(String(100))
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30), unique=True)
    role = Column(Boolean) #False for staff, True for superuser

    def __init__(self, login, password, name=None, surname=None, email=None, role = False):
        self.name = name
        self.email = email
        self.login = login
        password = (password + app.config['SALT']).encode('utf-8')
        self.password = sha256(password).hexdigest()
        self.surname = surname
        self.role = role

    def __repr__(self):
        return '<User %r>' % (self.name + ' ' + self.surname)

    def is_superuser(self):
        return self.role

