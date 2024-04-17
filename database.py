from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Double
from datetime import datetime

Base = declarative_base()

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    size = Column(Double(precision=2))
    path = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    path = Column(String(255))
    size = Column(Double(precision=2))
    created_at = Column(DateTime, default=datetime.now)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    message = Column(String(255))
    status = Column(String(10))
    created_at = Column(DateTime, default=datetime.now)
    
# Utility functions

def get_db_session():
    engine = create_engine('sqlite:///CQUK.db')
    Session = sessionmaker(bind=engine)
    return Session()

def save_to_db(obj):
    session = get_db_session()
    session.add(obj)
    session.commit()
    session.close()

# Create database
if __name__ == "__main__":
    engine = create_engine('sqlite:///CQUK.db')
    Base.metadata.create_all(engine)



