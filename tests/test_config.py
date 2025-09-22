# tests/test_config.py
import os
import pytest
from src.config import Config

@pytest.fixture
def set_env_vars():
    """
    A pytest fixture to temporarily set environment variables for the test.
    This ensures the test is isolated and repeatable.
    """
    original_env = dict(os.environ)
    os.environ['DATABASE_URL'] = 'mysql://test_user:test_pass@localhost:3306/test_db'
    os.environ['SERVICE_PORT'] = '8000'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    yield
    # Clean up by restoring the original environment variables
    os.environ.clear()
    os.environ.update(original_env)

def test_config_loading(set_env_vars):
    """
    Test that the Config class correctly loads environment variables.
    """
    # Create an instance of the Config class
    config = Config()
    
    # Assert that the attributes are loaded with the expected values
    assert config.DATABASE_URL == 'mysql://test_user:test_pass@localhost:3306/test_db'
    assert config.SERVICE_PORT == 8000
    assert config.LOG_LEVEL == 'DEBUG'

def test_config_default_values():
    """
    Test that the Config class uses default values when variables are not set.
    """
    # Unset the environment variables to test default behavior
    if 'SERVICE_PORT' in os.environ:
        del os.environ['SERVICE_PORT']
    if 'LOG_LEVEL' in os.environ:
        del os.environ['LOG_LEVEL']
    
    # Create an instance of the Config class
    config = Config()
    
    # Assert that the attributes fall back to their default values
    assert config.SERVICE_PORT == 8000
    assert config.LOG_LEVEL == 'INFO'