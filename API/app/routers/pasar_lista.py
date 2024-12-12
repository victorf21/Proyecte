from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from datetime import datetime

router = APIRouter(prefix="/pasar_llista", tags=["Pasar Lista"])

# Modelo para la respuesta
class PasarLista(BaseModel):
    Uid_usuarios: str  # Referencia al ID del usuario
    Fecha_hora: datetime

# Obtener todos los registros de pasar lista
@router.get("/list", response_model=List[PasarLista])
def list_pasar_llista():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Uid_usuarios, Fecha_hora FROM pasar_llista")
        pasar_llista = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return pasar_llista

# Crear un nuevo registro de pasar lista
@router.post("/add")
def create_pasar_llista(pasar_llista: PasarLista):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO pasar_llista (Uid_usuarios, Fecha_hora)
            VALUES (%s, %s)
        """
        values = (pasar_llista.Uid_usuarios, pasar_llista.Fecha_hora)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Registro de pasar lista creado correctamente"}