from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/pasar_lista", tags=["Pasar Lista"])

# Modelo para la respuesta
class PasarLista(BaseModel):
    fecha_id: int
    aula_codigo: int

# Obtener todos los registros de pasar lista
@router.get("/list", response_model=List[PasarLista])
def list_pasar_lista():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasar_lista")
        pasar_lista = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return pasar_lista

# Crear un nuevo registro de pasar lista
@router.post("/add")
def create_pasar_lista(pasar_lista: PasarLista):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO pasar_lista (fecha_id, aula_codigo)
            VALUES (%s, %s)
        """
        values = (pasar_lista.fecha_id, pasar_lista.aula_codigo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Registro de pasar lista creado correctamente"}
