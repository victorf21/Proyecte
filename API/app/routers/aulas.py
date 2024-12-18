from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client  
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/aulas", tags=["Aulas"])

# Definición del modelo de aula
class Aula(BaseModel):
    codigo_aula: int
    nombre: str

# Ruta para obtener todas las aulas
@router.get("/list", response_model=List[Aula])
def get_aulas():
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM AULA")
        aulas = cursor.fetchall()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    if not aulas:
        raise HTTPException(status_code=404, detail="No se encontraron aulas")

    return aulas  # FastAPI ahora podrá serializar correctamente

# Ruta para obtener una aula específica por su código
@router.get("/show/{codigo_aula}", response_model=Aula)
def get_aula(codigo_aula: int):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT Codigo_aula AS codigo_aula, Nombre AS nombre FROM AULA WHERE Codigo_aula = %s",
            (codigo_aula,)
        )
        aula = cursor.fetchone()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return aula  # FastAPI ahora podrá serializar correctamente

# Ruta para crear una nueva aula
@router.post("/add")
def add_aula(aula: Aula):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        query = "INSERT INTO AULA (Codigo_aula, Nombre) VALUES (%s, %s)"
        values = (aula.codigo_aula, aula.nombre)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": "Aula creada correctamente", "codigo_aula": aula.codigo_aula}

# Ruta para actualizar una aula existente
@router.put("/update/{codigo_aula}")
def update_aula(codigo_aula: int, aula: Aula):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        cursor = conn.cursor()
        query = "UPDATE AULA SET Nombre = %s WHERE Codigo_aula = %s"
        values = (aula.nombre, codigo_aula)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return {"message": "Aula actualizada correctamente", "codigo_aula": codigo_aula}

# Ruta para eliminar una aula
@router.delete("/delete/{codigo_aula}")
def delete_aula(codigo_aula: int):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        # Consulta para eliminar el aula por su código
        query = "DELETE FROM AULA WHERE Codigo_aula = %s"
        cursor.execute(query, (codigo_aula,))
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        if conn:
            conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return {"message": "Aula eliminada correctamente", "codigo_aula": codigo_aula}
