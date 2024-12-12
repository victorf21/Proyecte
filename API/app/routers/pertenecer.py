from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/pertenecer", tags=["Pertenecer"])

# Modelo para la respuesta
class Pertenecer(BaseModel):
    Codigo_ciclo: int
    Nombre_modulo: str

# Obtener todos los registros de pertenecer
@router.get("/list", response_model=List[Pertenecer])
def list_pertenecer():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Codigo_ciclo, Nombre_modulo FROM pertenecer")
        pertenecer = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return pertenecer

# Crear un nuevo registro de pertenecer
@router.post("/add")
def create_pertenecer(pertenecer: Pertenecer):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO pertenecer (Codigo_ciclo, Nombre_modulo)
            VALUES (%s, %s)
        """
        values = (pertenecer.Codigo_ciclo, pertenecer.Nombre_modulo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Registro creado correctamente"}

# Obtener un registro de pertenecer específico por código de ciclo y nombre de módulo
@router.get("/show/{Codigo_ciclo}/{Nombre_modulo}", response_model=Pertenecer)
def get_pertenecer(Codigo_ciclo: int, Nombre_modulo: str):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Codigo_ciclo, Nombre_modulo FROM pertenecer WHERE Codigo_ciclo = %s AND Nombre_modulo = %s", (Codigo_ciclo, Nombre_modulo))
        pertenecer = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not pertenecer:
        raise HTTPException(status_code=404, detail="Registro de pertenecer no encontrado")

    return pertenecer