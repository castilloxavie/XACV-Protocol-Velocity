import os
from dotenv import load_dotenv

class Config:
    """
    Se utiliza una clase Singleton para cargar las variables del entorno
    de forma segura.
    evita el hardcode de credenciales
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Config, cls).__new__(cls)
            cls._instancia._cargar_variables()
        return cls._instancia

    def _cargar_variables(self):
        load_dotenv()

        self.DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
        self.DB_PORT = os.getenv("DB_PORT", "3306")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

        if not self.DB_USER or not self.DB_PASSWORD:
            raise ValueError("Credenciales e la base d edatos no encontrada em (.env)")
