from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from datetime import datetime, timedelta, time

router = APIRouter(prefix="/fechas", tags=["Fechas"])

# Modelo para la respuesta
class Fecha(BaseModel):
    id: int = None  # El ID es autoincremental, no es necesario al crear
    fecha: datetime
    hora: time

# Obtener todas las fechas
@router.get("/list", response_model=List[Fecha])
def list_fechas():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fecha")
        fechas = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    # Convertir la hora a tipo `time` si es necesario
    for fecha in fechas:
        if isinstance(fecha["hora"], timedelta):  # En caso de que sea timedelta
            fecha["hora"] = (datetime.min + fecha["hora"]).time()
        else:
            fecha["hora"] = fecha["hora"].strftime("%H:%M:%S")  # Formato a string "HH:MM:SS"

    return fechas

# Crear una nueva fecha
@router.post("/add")
def create_fecha(fecha: Fecha):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO fecha (fecha, hora)
            VALUES (%s, %s)
        """
        values = (fecha.fecha, fecha.hora)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Fecha creada correctamente", "fecha": fecha.fecha, "hora": fecha.hora}

# Obtener una fecha específica por ID
@router.get("/show/{fecha_id}", response_model=Fecha)
def get_fecha(fecha_id: int):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fecha WHERE id = %s", (fecha_id,))
        fecha = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not fecha:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")

    # Convertir la hora a tipo `time` si es necesario
    if isinstance(fecha["hora"], timedelta):  # En caso de que sea timedelta
        fecha["hora"] = (datetime.min + fecha["hora"]).time()
    else:
        fecha["hora"] = fecha["hora"].strftime("%H:%M:%S")  # Formato a string "HH:MM:SS"

    return fecha
