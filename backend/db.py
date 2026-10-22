import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./smartshop.db')
connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class PriceSnapshot(Base):
    __tablename__ = 'price_snapshots'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True, nullable=False)
    store = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class PriceAlert(Base):
    __tablename__ = 'price_alerts'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True, nullable=False)
    target_price = Column(Float, nullable=False)
    email = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class SearchLog(Base):
    __tablename__ = 'search_logs'
    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
