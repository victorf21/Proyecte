from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client 
router = APIRouter(prefix="/cursar", tags=["Cursar"])

# Modelo para la respuesta
class Cursar(BaseModel):
    Uid_usuarios: str
    Nombre_uf: str
    Codigo_aula: int

# Obtener todos los registros de cursar
@router.get("/list", response_model=List[Cursar])
def list_cursar():
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        cursor.execute("SELECT Uid_usuarios, Codigo_aula, Nombre_uf FROM cursar")
        cursar = cursor.fetchall()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return cursar

# Crear un nuevo registro de cursar
@router.post("/add")
def create_cursar(cursar: Cursar):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        query = """
            INSERT INTO cursar (Uid_usuarios, Nombre_uf, Codigo_aula)
            VALUES (%s, %s, %s)
        """
        values = (cursar.Uid_usuarios, cursar.Nombre_uf, cursar.Codigo_aula)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": "Registro de cursar creado correctamente"}
