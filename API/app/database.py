import psycopg2
from psycopg2 import sql

def db_client():
    try:
        dbname = "sistema_ciclos"
        user = "web"
        password = "admin"
        host = "192.168.34.100"
        port = "5432"

        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname
        )
        print("Conexió exitosa a la base de dades")
        return conn

    except Exception as e:
        print(f"Error de connexió a la base de dades: {e}")
        return None  # Retornar None si hi ha un error