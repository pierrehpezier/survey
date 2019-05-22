import sqlalchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, LargeBinary, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

BASE = declarative_base()
BASEPATH = 'sqlite:///{}/database.db'.format(os.path.dirname(os.path.realpath(__file__)))

class USERS(BASE):
    __tablename__ = 'USERS'
    id = Column(Integer, primary_key=True)
    IP = Column(String(4096), nullable=False)
    USER_AGENT = Column(String(4096), nullable=False)
    DATE = Column(Date())

class QUESTIONS(BASE):
    __tablename__ = 'QUESTIONS'
    id = Column(Integer, primary_key=True)
    QUESTION = Column(Text(convert_unicode=True), nullable=False)
    DATE = Column(Date())

class VOTES(BASE):
    __tablename__ = 'VOTES'
    id = Column(Integer, primary_key=True)
    USER = Column(Integer, ForeignKey('USERS.id'))
    QUESTION = Column(Integer, ForeignKey('QUESTIONS.id'))
    SCORE = Column(Integer, nullable=False)
    DATE = Column(Date())

try:
    BASE.metadata.create_all(create_engine(BASEPATH))
    del BASE
    ENGINE = create_engine(BASEPATH, encoding='utf8', convert_unicode=True)
    DBSession = sessionmaker(bind=ENGINE)
    SESSION = scoped_session(DBSession)
except sqlalchemy.exc.OperationalError:
    sys.exit(-1)
