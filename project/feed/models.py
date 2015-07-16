# from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
# from sqlalchemy.orm import relationship, backref
# from project.database import Base, db_session
#
#
# class Category(Base):
#     __tablename__ = 'category'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return self.name
#
#     def __repr__(self):
#         return "[{}] {}".format(self.__class__.__name__, self.name)
#
#     def save(self):
#         db_session.add(self)
#         db_session.commit()
