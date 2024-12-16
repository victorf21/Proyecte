from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client  
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/uf", tags=["UF"])

class UF(BaseModel):
    nombre_uf: str

# Ruta para obtener todas las UF
@router.get("/list", response_model=List[UF])
def get_ufs():
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM UF")
        ufs = cursor.fetchall()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    if not ufs:
        raise HTTPException(status_code=404, detail="No se encontraron UF")

    return ufs 

# Ruta para obtener una UF por su nombre
@router.get("/show/{nombre_uf}", response_model=UF)
def get_uf(nombre_uf: str):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT Nombre_uf AS nombre_uf FROM UF WHERE Nombre_uf = %s",
            (nombre_uf,)
        )
        uf = cursor.fetchone()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    if not uf:
        raise HTTPException(status_code=404, detail="UF no encontrada")

    return uf

# Ruta para crear una nueva UF
@router.post("/add")
def add_uf(uf: UF):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        query = "INSERT INTO UF (Nombre_uf) VALUES (%s)"
        values = (uf.nombre_uf,)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": "UF creada correctamente", "nombre_uf": uf.nombre_uf}

# Ruta para eliminar una UF por su nombre
@router.delete("/delete/{nombre_uf}")
def delete_uf(nombre_uf: str):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        query = "DELETE FROM UF WHERE Nombre_uf = %s"
        cursor.execute(query, (nombre_uf,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="UF no encontrada")

        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": f"UF con nombre {nombre_uf} eliminada correctamente"}
