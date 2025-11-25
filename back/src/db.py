import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Ruta ABSOLUTA al .env
ENV_PATH = "/home/laraO/TPG-IDS/TPG-IDS/.env"

# Cargar variables
load_dotenv(ENV_PATH)

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except Error as e:
        print("❌ Error conectando a MySQL:", e)
        return None
