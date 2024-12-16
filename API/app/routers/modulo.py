from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/modulos", tags=["Módulos"])

# Modelo para la respuesta
class Modulo(BaseModel):
    nombre_modulo: str  
    nombre_uf: str  

# Obtener todos los módulos
@router.get("/list", response_model=List[Modulo])
def list_modulos():
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM modulo")
        modulos = cursor.fetchall()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return modulos

# Crear un nuevo módulo
@router.post("/add")
def create_modulo(modulo: Modulo):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO modulo (nombre_modulo, nombre_uf)
            VALUES (%s, %s)
        """
        values = (modulo.nombre_modulo, modulo.nombre_uf)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": "Módulo creado correctamente", "nombre_modulo": modulo.nombre_modulo}

# Obtener un módulo específico por nombre del módulo
@router.get("/show/{nombre_modulo}", response_model=Modulo)
def get_modulo(nombre_modulo: str):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT nombre_modulo, nombre_uf FROM modulo WHERE nombre_modulo = %s", (nombre_modulo,))
        modulo = cursor.fetchone()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")

    return modulo
