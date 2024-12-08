from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/modulos", tags=["Módulos"])

# Modelo para la respuesta
class Modulo(BaseModel):
    codigo: int
    nombre: str
    ufs: int

# Obtener todos los módulos
@router.get("/list", response_model=List[Modulo])
def list_modulos():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM modulo")
        modulos = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return modulos

# Crear un nuevo módulo
@router.post("/add")
def create_modulo(modulo: Modulo):
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
            INSERT INTO modulo (codigo, nombre, ufs)
            VALUES (%s, %s, %s)
        """
        values = (modulo.codigo, modulo.nombre, modulo.ufs)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Módulo creado correctamente", "codigo": modulo.codigo}

# Obtener un módulo específico por código
@router.get("/show/{codigo}", response_model=Modulo)
def get_modulo(codigo: int):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM modulo WHERE codigo = %s", (codigo,))
        modulo = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")

    return modulo
