from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/aulas", tags=["Aulas"])


class Aula(BaseModel):
    codigo: int
    nombre: str


# Ruta para obtener todas las aulas
@router.get("/list", response_model=List[Aula])
def get_aulas():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT codigo, nombre FROM aula")
        aulas = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if not aulas:
        raise HTTPException(status_code=404, detail="No se encontraron aulas")

    return aulas


# Ruta para obtener una aula específica por su código
@router.get("/show/{codigo}", response_model=Aula)
def get_aula(codigo: int):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT codigo, nombre FROM aula WHERE codigo = %s", (codigo,))
        aula = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return aula


# Ruta para crear una nueva aula
@router.post("/add")
def add_aula(aula: Aula):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = "INSERT INTO aula (codigo, nombre) VALUES (%s, %s)"
        values = (aula.codigo, aula.nombre)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    return {"message": "Aula creada correctamente", "codigo": aula.codigo}


# Ruta para actualizar una aula existente
@router.put("/update/{codigo}")
def update_aula(codigo: int, aula: Aula):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = "UPDATE aula SET nombre = %s WHERE codigo = %s"
        values = (aula.nombre, codigo)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return {"message": "Aula actualizada correctamente", "codigo": codigo}


# Ruta para eliminar una aula
@router.delete("/delete/{codigo}")
def delete_aula(codigo: int):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = "DELETE FROM aula WHERE codigo = %s"
        cursor.execute(query, (codigo,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return {"message": "Aula eliminada correctamente", "codigo": codigo}
