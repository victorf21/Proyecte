from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from datetime import datetime
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/pasar_llista", tags=["Pasar Lista"])

# Modelo para la respuesta
class PasarLista(BaseModel):
    uid_usuarios: str
    fecha_hora: datetime

# Obtener todos los registros de pasar lista
@router.get("/list", response_model=List[PasarLista])
def list_pasar_llista():
    try:
        conn = db_client()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT uid_usuarios, fecha_hora 
            FROM pasar_llista
            """)
        pasar_llista = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return pasar_llista

# Crear un nuevo registro de pasar lista
@router.post("/add")
def create_pasar_llista(pasar_llista: PasarLista):
    try:
        conn = db_client()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Verificar si la fecha existe en la tabla FECHA
        cursor.execute("SELECT 1 FROM FECHA WHERE fecha_hora = %s", (pasar_llista.fecha_hora,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=400, detail="La fecha proporcionada no existe en la tabla FECHA.")

        # Insertar el nuevo registro en pasar_llista
        query = """
            INSERT INTO pasar_llista (uid_usuarios, fecha_hora)
            VALUES (%s, %s)
        """
        values = (pasar_llista.uid_usuarios, pasar_llista.fecha_hora)
        cursor.execute(query, values)
        conn.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Registro de pasar lista creado correctamente"}

# Eliminar un registro de pasar lista
@router.delete("/delete/{uid_usuarios}/{fecha_hora}")
def delete_pasar_llista(uid_usuarios: str, fecha_hora: datetime):
    try:
        conn = db_client()
        cursor = conn.cursor()

        # Eliminar el registro correspondiente
        query = """
            DELETE FROM pasar_llista
            WHERE uid_usuarios = %s AND fecha_hora = %s
        """
        cursor.execute(query, (uid_usuarios, fecha_hora))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": f"Registro de {uid_usuarios} en {fecha_hora} eliminado correctamente"}

# Actualizar un registro de pasar lista
@router.put("/update/{uid_usuarios}/{fecha_hora}")
def update_pasar_llista(uid_usuarios: str, fecha_hora: datetime, pasar_llista: PasarLista):
    try:
        conn = db_client()
        cursor = conn.cursor()

        # Verificar si la fecha existe en la tabla FECHA
        cursor.execute("SELECT 1 FROM FECHA WHERE fecha_hora = %s", (pasar_llista.fecha_hora,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=400, detail="La fecha proporcionada no existe en la tabla FECHA.")

        # Actualizar el registro de pasar_llista
        query = """
            UPDATE pasar_llista
            SET uid_usuarios = %s, fecha_hora = %s
            WHERE uid_usuarios = %s AND fecha_hora = %s
        """
        values = (pasar_llista.uid_usuarios, pasar_llista.fecha_hora, uid_usuarios, fecha_hora)
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": f"Registro de {uid_usuarios} en {fecha_hora} actualizado correctamente"}
