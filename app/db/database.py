"""
Database Configuration Module

This module handles database connection and configuration using SQLAlchemy.
It provides the database engine and session management functionality.

Key components:
- SQLAlchemy engine configuration
- Session management
- Base model class for ORM
- Database URL configuration
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment or use default SQLite
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./transcription_app.db"
)

# Create SQLAlchemy engine with SQLite-specific configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Note:
        This function is used as a FastAPI dependency to manage database sessions.
        It ensures proper session cleanup after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 