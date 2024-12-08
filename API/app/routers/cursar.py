from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/cursar", tags=["Cursar"])

# Modelo para la respuesta
class Cursar(BaseModel):
    usuario_uid: str
    aula_codigo: int
    grupo: str

# Obtener todos los registros de cursar
@router.get("/list", response_model=List[Cursar])
def list_cursar():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cursar")
        cursar = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return cursar

# Crear un nuevo registro de cursar
@router.post("/add")
def create_cursar(cursar: Cursar):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO cursar (usuario_uid, aula_codigo, grupo)
            VALUES (%s, %s, %s)
        """
        values = (cursar.usuario_uid, cursar.aula_codigo, cursar.grupo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Registro de cursar creado correctamente"}
