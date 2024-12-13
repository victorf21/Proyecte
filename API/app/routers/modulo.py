from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/modulos", tags=["Módulos"])

# Modelo para la respuesta
class Modulo(BaseModel):
    Nombre_modulo: str  
    Nombre_uf: str  

# Obtener todos los módulos
@router.get("/list", response_model=List[Modulo])
def list_modulos():
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        cursor.execute("SELECT Nombre_modulo, Nombre_uf FROM modulo")
        modulos = cursor.fetchall()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return modulos

# Crear un nuevo módulo
@router.post("/add")
def create_modulo(modulo: Modulo):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        query = """
            INSERT INTO modulo (Nombre_modulo, Nombre_uf)
            VALUES (%s, %s)
        """
        values = (modulo.Nombre_modulo, modulo.Nombre_uf)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    return {"message": "Módulo creado correctamente", "Nombre_modulo": modulo.Nombre_modulo}

# Obtener un módulo específico por nombre del módulo
@router.get("/show/{Nombre_modulo}", response_model=Modulo)
def get_modulo(Nombre_modulo: str):
    try:
        conn = db_client()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = conn.cursor()
        cursor.execute("SELECT Nombre_modulo, Nombre_uf FROM modulo WHERE Nombre_modulo = %s", (Nombre_modulo,))
        modulo = cursor.fetchone()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()

    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")

    return modulo
