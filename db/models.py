
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

from db.database import engine, Session

Base = declarative_base()

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())

class TestStep(Base):
    __tablename__ = 'test_steps'
    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"))
    step_order = Column(Integer)
    action = Column(Text, nullable=False)
    expected_result = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    test_step_id = Column(Integer, ForeignKey("test_steps.id"))
    log_type = Column(String)
    message = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())

Base.metadata.create_all(engine)
