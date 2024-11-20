from fastapi import APIRouter, Depends
from typing import List
from app.models import Marcatge, MarcatgeCreate
from app.database import db_client

router = APIRouter()

@router.get("/marcatges", response_model=List[Marcatge])
def get_marcatges():
    conn = db_client()
    if conn is None:
        return {"error": "Error de connexió a la base de dades"}
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marcatges")
    result = cursor.fetchall()
    conn.close()
    return result

@router.get("/marcatges/{usuari_id}", response_model=List[Marcatge])
def get_marcatges_usuari(usuari_id: int):
    conn = db_client()
    if conn is None:
        return {"error": "Error de connexió a la base de dades"}
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marcatges WHERE usuari_id = %s", (usuari_id,))
    result = cursor.fetchall()
    conn.close()
    return result

@router.post("/marcatges")
def create_marcatge(marcatge: MarcatgeCreate):
    conn = db_client()
    if conn is None:
        return {"error": "Error de connexió a la base de dades"}
    
    cursor = conn.cursor()
    query = """
        INSERT INTO marcatges (usuari_id, data_entrada, espai_id, estat) 
        VALUES (%s, %s, %s, %s)
    """
    values = (marcatge.usuari_id, marcatge.data_entrada, marcatge.espai_id, marcatge.estat)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return {"message": "Marcatge creat correctament"}
