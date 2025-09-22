import logging
import sys
from pythonjsonlogger import jsonlogger
from .config import Config

def setup_logging():
    """
    Sets up JSON logging format for the service.
    """
    # Create the root logger
    logger = logging.getLogger()
    
    # Set the logging level from configuration
    logger.setLevel(Config.LOG_LEVEL)

    # Create a handler to display logs to standard output
    handler = logging.StreamHandler(sys.stdout)
    
    # Define the JSON format with required fields
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Return the configured logger instance
    return logger

# Example usage:
# logger = setup_logging()
# logger.info("Service started successfully", extra={'service_name': 'user-service'})