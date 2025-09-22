from .config import Config
from .logger_config import setup_logging

# Get the logger instance
logger = setup_logging()

def start_service():
    """
    Starts the user service and logs a startup message.
    """
    # Use the logger to log a message in JSON format
    logger.info("Starting user service...", extra={'service_name': 'user-service'})
    
    # Access and log configuration values to verify they loaded correctly
    logger.info(
        "Configuration loaded",
        extra={
            'database_url': Config.DATABASE_URL,
            'service_port': Config.SERVICE_PORT,
            'log_level': Config.LOG_LEVEL
        }
    )
    
    # Main service logic would go here (e.g., a web server)
    # ...

if __name__ == "__main__":
    start_service()