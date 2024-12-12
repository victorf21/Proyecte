from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from fastapi import Query

router = APIRouter(prefix="/ciclos", tags=["Ciclos"])


# Modelo para la respuesta
class Ciclo(BaseModel):
    Codigo_ciclo: int
    Nombre_ciclo: str
    Grado: int = Query(..., ge=1, le=2, description="El grado debe estar entre 1 y 2")


# Obtener todos los ciclos
@router.get("/list", response_model=List[Ciclo])
def list_ciclos():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ciclo")
        ciclos = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()
    return ciclos


# Crear un nuevo ciclo
@router.post("/add")
def create_ciclo(ciclo: Ciclo):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO ciclo (Codigo_ciclo, Nombre_ciclo, Grado)
            VALUES (%s, %s, %s)
        """
        values = (ciclo.Codigo_ciclo, ciclo.Nombre_ciclo, ciclo.Grado)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    return {"message": "Ciclo creado correctamente", "Codigo_ciclo": ciclo.Codigo_ciclo}


# Obtener un ciclo específico por código
@router.get("/show/{Codigo_ciclo}", response_model=Ciclo)
def get_ciclo(Codigo_ciclo: int):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ciclo WHERE Codigo_ciclo = %s", (Codigo_ciclo,))
        ciclo = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if not ciclo:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")

    return ciclo


# Actualizar un ciclo existente
@router.put("/update/{Codigo_ciclo}")
def update_ciclo(Codigo_ciclo: int, ciclo: Ciclo):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            UPDATE ciclo
            SET Nombre_ciclo = %s, Grado = %s
            WHERE Codigo_ciclo = %s
        """
        values = (ciclo.Nombre_ciclo, ciclo.Grado, Codigo_ciclo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")

    return {"message": "Ciclo actualizado correctamente", "Codigo_ciclo": Codigo_ciclo}