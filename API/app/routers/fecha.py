from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from datetime import datetime

router = APIRouter(prefix="/fechas", tags=["Fechas"])

# Modelo para la respuesta
class Fecha(BaseModel):
    Fecha_hora: datetime
    Estado: str  # 'presente', 'retardo', o 'falta'
    Uid_usuarios: str

# Obtener todas las fechas
@router.get("/list", response_model=List[Fecha])
def list_fechas():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Fecha_hora, Estado, Uid_usuarios FROM FECHA")
        fechas = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return fechas

# Crear una nueva fecha
@router.post("/add")
def create_fecha(fecha: Fecha):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO FECHA (Fecha_hora, Estado, Uid_usuarios)
            VALUES (%s, %s, %s)
        """
        values = (fecha.Fecha_hora, fecha.Estado, fecha.Uid_usuarios)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Fecha creada correctamente", "Fecha_hora": fecha.Fecha_hora, "Estado": fecha.Estado}

# Obtener una fecha específica por Fecha_hora
@router.get("/show/{Fecha_hora}", response_model=Fecha)
def get_fecha(Fecha_hora: datetime):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM FECHA WHERE Fecha_hora = %s", (Fecha_hora,))
        fecha = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not fecha:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")

    return fecha
