from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/consulta", tags=["Consulta"])


class Consulta(BaseModel):
    usuario_uid: str
    fecha_id: int


# Ruta para registrar una consulta
@router.post("/add")
def add_consulta(consulta: Consulta):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            INSERT INTO consultar (usuario_uid, fecha_id)
            VALUES (%s, %s)
        """
        values = (consulta.usuario_uid, consulta.fecha_id)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Consulta registrada correctamente"}


# Ruta para listar todas las consultas de un usuario
@router.get("/list/{usuario_uid}", response_model=List[Consulta])
def list_consultas(usuario_uid: str):
    try:
        conn = db_client()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT usuario_uid, fecha_id 
            FROM consultar 
            WHERE usuario_uid = %s
        """, (usuario_uid,))
        result = cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="No se encontraron consultas para este usuario")

    return result


# Ruta para actualizar una consulta
@router.put("/update/{usuario_uid}/{fecha_id}")
def update_consulta(usuario_uid: str, fecha_id: int, new_fecha_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE consultar
            SET fecha_id = %s
            WHERE usuario_uid = %s AND fecha_id = %s
        """
        values = (new_fecha_id, usuario_uid, fecha_id)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Consulta no encontrada para actualizar")

    return {"message": "Consulta actualizada correctamente"}


# Ruta para eliminar una consulta
@router.delete("/delete/{usuario_uid}/{fecha_id}")
def delete_consulta(usuario_uid: str, fecha_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            DELETE FROM consultar 
            WHERE usuario_uid = %s AND fecha_id = %s
        """
        cur.execute(query, (usuario_uid, fecha_id))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Consulta no encontrada para eliminar")

    return {"message": "Consulta eliminada correctamente"}
