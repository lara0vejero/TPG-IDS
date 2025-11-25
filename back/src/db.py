import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "libroxlibro_db",
}

def get_connection():
    """Devuelve una conexión nueva a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)
