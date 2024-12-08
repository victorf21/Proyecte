from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/pertenecer", tags=["Pertenecer"])

# Modelo para la respuesta
class Pertenecer(BaseModel):
    usuario_uid: str
    modulo_codigo: int
    ciclo_codigo: int

# Obtener todos los registros de pertenecer
@router.get("/list", response_model=List[Pertenecer])
def list_pertenecer():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pertenecer")
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
            INSERT INTO pertenecer (usuario_uid, modulo_codigo, ciclo_codigo)
            VALUES (%s, %s, %s)
        """
        values = (pertenecer.usuario_uid, pertenecer.modulo_codigo, pertenecer.ciclo_codigo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Registro creado correctamente"}
