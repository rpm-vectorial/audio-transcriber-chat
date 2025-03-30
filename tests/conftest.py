import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from app.main import app
from app.models.models import Transcription, ChatMessage  # Import models to ensure they are registered
from unittest.mock import patch, MagicMock

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def db_engine():
    """Create all tables in the test database."""
    Base.metadata.drop_all(bind=engine)  # Clean up any existing tables
    Base.metadata.create_all(bind=engine)  # Create fresh tables
    yield engine
    Base.metadata.drop_all(bind=engine)  # Clean up after all tests

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a fresh database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def mock_openai():
    """Mock OpenAI client for testing."""
    mock_response = MagicMock()
    mock_response.text = "This is a test transcription."
    
    mock_client = MagicMock()
    mock_client.audio.transcriptions.create.return_value = mock_response
    
    with patch('app.services.transcription_service.client', mock_client):
        yield mock_client

@pytest.fixture
def client(db_engine, db_session, mock_openai):
    """Test client fixture."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear() 