from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field
from app.database import db_client
from datetime import datetime
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/fecha", tags=["Fecha"])

# Modelo para la respuesta
class Fecha(BaseModel):
    fecha_hora: datetime 
    estado: str 
    uid_usuarios: str 

# Obtener todos los registros de la tabla FECHA
@router.get("/list", response_model=List[Fecha])
def list_fecha():
    try:
        conn = db_client()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT fecha_hora, estado, uid_usuarios FROM FECHA")
        fechas = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return fechas

# Crear un nuevo registro en la tabla FECHA
@router.post("/add")
def create_fecha(fecha: Fecha):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO FECHA (fecha_hora, estado, uid_usuarios)
            VALUES (%s, %s, %s)
        """
        values = (fecha.fecha_hora, fecha.estado, fecha.uid_usuarios)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Registro creado correctamente en la tabla FECHA"}

# Eliminar un registro de la tabla FECHA
@router.delete("/delete/{fecha_hora}")
def delete_fecha(fecha_hora: datetime):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = "DELETE FROM FECHA WHERE fecha_hora = %s"
        cursor.execute(query, (fecha_hora,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": f"Registro con fecha {fecha_hora} eliminado correctamente"}

# Actualizar un registro en la tabla FECHA
@router.put("/update/{fecha_hora}")
def update_fecha(fecha_hora: datetime, fecha: Fecha):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            UPDATE FECHA
            SET estado = %s, uid_usuarios = %s
            WHERE fecha_hora = %s
        """
        values = (fecha.estado, fecha.uid_usuarios, fecha_hora)
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": f"Registro con fecha {fecha_hora} actualizado correctamente"}