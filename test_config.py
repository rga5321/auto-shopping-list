import pytest
import os
from config import AppConfig

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to set all required environment variables for testing."""
    monkeypatch.setenv("KEEP_EMAIL", "test@example.com")
    monkeypatch.setenv("KEEP_TOKEN", "secret_token")
    monkeypatch.setenv("KEEP_NOTE_ID", "keep_note_abc123")
    monkeypatch.setenv("TODOIST_API_KEY", "todoist_key_xyz987")
    monkeypatch.setenv("TODOIST_PROJECT_ID", "todoist_proj_12345")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini_key_abcxyz")

def test_config_loads_all_required_variables(mock_env):
    """Test standard case where all environment variables are present."""
    config = AppConfig()
    
    assert config.keep_email == "test@example.com"
    assert config.keep_token == "secret_token"
    assert config.keep_note_id == "keep_note_abc123"
    assert config.todoist_api_key == "todoist_key_xyz987"
    assert config.todoist_project_id == "todoist_proj_12345"
    assert config.gemini_api_key == "gemini_key_abcxyz"
    assert config.mode == "simulation"  # The default when not specified

def test_config_execution_mode(mock_env, monkeypatch):
    """Test EXECUTION_MODE loading and validation."""
    monkeypatch.setenv("EXECUTION_MODE", "real")
    config = AppConfig()
    assert config.mode == "real"

    monkeypatch.setenv("EXECUTION_MODE", "simULATION") # Test case insensitivity 
    config = AppConfig()
    assert config.mode == "simulation"

    monkeypatch.setenv("EXECUTION_MODE", "invalid_mode")
    with pytest.raises(ValueError, match="EXECUTION_MODE must be either 'simulation' or 'real'"):
        AppConfig()

def test_missing_required_variable(monkeypatch):
    """Test that AppConfig raises a ValueError if a required environment variable is missing."""
    # Ensure nothing is set 
    monkeypatch.delenv("KEEP_EMAIL", raising=False)
    
    with pytest.raises(ValueError, match="Missing required environment variable: KEEP_EMAIL"):
        AppConfig()

def test_empty_required_variable(mock_env, monkeypatch):
     """Test that AppConfig raises a ValueError if a required environment variable is empty."""
     monkeypatch.setenv("KEEP_EMAIL", "")
    
     with pytest.raises(ValueError, match="Missing required environment variable: KEEP_EMAIL"):
        AppConfig()
