import os
from dotenv import load_dotenv

# Loads environment variables from the .env file
load_dotenv()

class Config:
    """
    Configuration class for the user service.
    Loads settings from environment variables.
    """
    # Database URL for connecting to MySQL
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Port where the service runs, default is 8000
    SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000))
    
    # Logging level, default is 'INFO'
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# You can import and use this Config class in other parts of your application.