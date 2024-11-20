import mysql.connector

def db_client():
    try:
        dbname = "proyecte"
        user = "root"
        password = "root"
        host = "localhost"
        port = "3307"
        collation = "utf8mb4_general_ci"

        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            collation=collation
        )
        print("Conexió exitosa a la base de dades")
        return conn

    except Exception as e:
        print(f"Error de connexió a la base de dades: {e}")
        return None  # Retornar None si hi ha un error
