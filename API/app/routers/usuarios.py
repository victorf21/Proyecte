from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class Usuario(BaseModel):
    uid: str
    email: str
    nombre: str
    contraseña: str
    rol: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Ruta para listar todos los usuarios
@router.get("/list", response_model=List[Usuario])
def list_usuarios():
    try:
        conn = db_client()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT uid, email, nombre, contraseña, rol FROM usuarios")
        result = cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return result


# Ruta para obtener un usuario por UID
@router.get("/show/{uid}", response_model=Usuario)
def get_usuario(uid: str):
    try:
        conn = db_client()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT uid, email, nombre, contraseña, rol FROM usuarios WHERE uid = %s", (uid,))
        result = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return result


# Ruta para crear un usuario
@router.post("/add")
def create_usuario(usuario: Usuario):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            INSERT INTO usuarios (uid, email, nombre, contraseña, rol)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (usuario.uid, usuario.email, usuario.nombre, usuario.contraseña, usuario.rol)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    return {"message": "Usuario creado correctamente", "uid": usuario.uid}


# Ruta para iniciar sesión
@router.post("/login")
def login(credentials: LoginRequest):
    email = credentials.email
    password = credentials.password
    try:
        conn = db_client()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if password != user['contraseña']:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso", "role": user["rol"], "id": user["uid"], "name": user["nombre"]}


# Ruta para actualizar un usuario
@router.put("/update/{uid}")
def update_usuario(uid: str, usuario: Usuario):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE usuarios 
            SET email = %s, nombre = %s, contraseña = %s, rol = %s
            WHERE uid = %s
        """
        values = (usuario.email, usuario.nombre, usuario.contraseña, usuario.rol, uid)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario actualizado correctamente", "uid": uid}


# Ruta para eliminar un usuario
@router.delete("/delete/{uid}")
def delete_usuario(uid: str):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM usuarios WHERE uid = %s"
        cur.execute(query, (uid,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario eliminado correctamente", "uid": uid}
