from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client 

router = APIRouter(prefix="/pertenecer", tags=["Pertenecer"])

# Modelo para la respuesta
class Pertenecer(BaseModel):
    codigo_ciclo: int
    nombre_modulo: str

# Obtener todos los registros de pertenecer
@router.get("/list", response_model=List[Pertenecer])
def list_pertenecer():
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        cursor.execute("SELECT Codigo_ciclo, Nombre_modulo FROM pertenecer")
        pertenecer = cursor.fetchall()

        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return pertenecer

# Crear un nuevo registro de pertenecer
@router.post("/add")
def create_pertenecer(pertenecer: Pertenecer):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        query = """
            INSERT INTO pertenecer (Codigo_ciclo, Nombre_modulo)
            VALUES (%s, %s)
        """
        values = (pertenecer.codigo_ciclo, pertenecer.nombre_modulo)
        cursor.execute(query, values)
        conn.commit()

        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": "Registro creado correctamente"}

# Obtener un registro de pertenecer específico por código de ciclo y nombre de módulo
@router.get("/show/{codigo_ciclo}/{nombre_modulo}", response_model=Pertenecer)
def get_pertenecer(codigo_ciclo: int, nombre_modulo: str):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        cursor.execute("SELECT Codigo_ciclo, Nombre_modulo FROM pertenecer WHERE Codigo_ciclo = %s AND Nombre_modulo = %s", (codigo_ciclo, nombre_modulo))
        pertenecer = cursor.fetchone()

        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    if not pertenecer:
        raise HTTPException(status_code=404, detail="Registro de pertenecer no encontrado")

    return pertenecer
