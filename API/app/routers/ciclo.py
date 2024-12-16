from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from fastapi import Query
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/ciclos", tags=["Ciclos"])


# Modelo para la respuesta
class Ciclo(BaseModel):
    codigo_ciclo: int
    nombre_ciclo: str
    grado: int = Query(..., ge=1, le=2, description="El grado debe estar entre 1 y 2")


# Obtener todos los ciclos
@router.get("/list", response_model=List[Ciclo])
def list_ciclos():
    try:
        conn = db_client()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM ciclo")
        ciclos = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()
    return ciclos


# Crear un nuevo ciclo
@router.post("/add")
def create_ciclo(ciclo: Ciclo):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO ciclo (codigo_ciclo, nombre_ciclo, grado)
            VALUES (%s, %s, %s)
        """
        values = (ciclo.codigo_ciclo, ciclo.nombre_ciclo, ciclo.grado)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Ciclo creado correctamente", "codigo_ciclo": ciclo.codigo_ciclo}


# Obtener un ciclo específico por código
@router.get("/show/{codigo_ciclo}", response_model=Ciclo)
def get_ciclo(codigo_ciclo: int):
    try:
        conn = db_client()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM ciclo WHERE codigo_ciclo = %s", (codigo_ciclo,))
        ciclo = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

    if not ciclo:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")

    return ciclo


# Actualizar un ciclo existente
@router.put("/update/{codigo_ciclo}")
def update_ciclo(codigo_ciclo: int, ciclo: Ciclo):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            UPDATE ciclo
            SET nombre_ciclo = %s, grado = %s
            WHERE codigo_ciclo = %s
        """
        values = (ciclo.nombre_ciclo, ciclo.grado, codigo_ciclo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")

    return {"message": "Ciclo actualizado correctamente", "codigo_ciclo": codigo_ciclo}