import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    "host": "laru.mysql.pythonanywhere-services.com",
    "user": "laru",
    "password": "lara23120412",
    "database": "laru$default"
}

def execute_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        cursor.close()
        conn.close()
        print("Base de datos inicializada correctamente.")

    except Error as e:
        print(f"Error al ejecutar SQL: {e}")


if __name__ == "__main__":
    execute_sql_file("init_db.sql")
