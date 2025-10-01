# src/config.py
import os

class Config:
    def __init__(self):
        """
        Lee las variables de entorno en el momento de la instanciación.
        """
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        # El , 8000 es el valor por defecto si la variable no está
        self.SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000)) 
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "un_secreto")