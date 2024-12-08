from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/ciclos", tags=["Ciclos"])

# Modelo para la respuesta
class Ciclo(BaseModel):
    codigo: int
    nombre: str
    grado: str

# Obtener todos los ciclos
@router.get("/list", response_model=List[Ciclo])
def list_ciclos():
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ciclo")
        ciclos = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
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
            INSERT INTO ciclo (codigo, nombre, grado)
            VALUES (%s, %s, %s)
        """
        values = (ciclo.codigo, ciclo.nombre, ciclo.grado)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Ciclo creado correctamente", "codigo": ciclo.codigo}

# Obtener un ciclo específico por código
@router.get("/show/{codigo}", response_model=Ciclo)
def get_ciclo(codigo: int):
    try:
        conn = db_client()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ciclo WHERE codigo = %s", (codigo,))
        ciclo = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not ciclo:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")

    return ciclo
