from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.database import db_client
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class Usuario(BaseModel):
    Uid_usuarios: str
    email: str
    nombre: str
    contraseña: str
    rol: str

class LoginRequest(BaseModel):
    email: str
    contraseña: str

# Ruta para listar todos los usuarios
@router.get("/list", response_model=List[Usuario])
def list_usuarios():
    try:
        conn = db_client()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT Uid_usuarios, email, nombre, contraseña, rol FROM usuarios")
        result = cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cur.close()
        conn.close()

    return result


# Ruta para obtener un usuario por Uid_usuarios
@router.get("/show/{Uid_usuarios}", response_model=Usuario)
def get_usuario(Uid_usuarios: str):
    try:
        conn = db_client()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT Uid_usuarios, email, nombre, contraseña, rol FROM usuarios WHERE Uid_usuarios = %s", (Uid_usuarios,))
        result = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cur.close()
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
            INSERT INTO usuarios (Uid_usuarios, email, nombre, contraseña, rol)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (usuario.Uid_usuarios, usuario.email, usuario.nombre, usuario.contraseña, usuario.rol)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cur.close()
        conn.close()

    return {"message": "Usuario creado correctamente", "Uid_usuarios": usuario.Uid_usuarios}


# Ruta para iniciar sesión
@router.post("/login")
def login(credentials: LoginRequest):
    email = credentials.email
    contraseña = credentials.contraseña
    try:
        conn = db_client()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    finally:
        cur.close()
        conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if contraseña != user['contraseña']:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso", "role": user["rol"], "id": user["Uid_usuarios"], "name": user["nombre"]}


# Ruta para actualizar un usuario
@router.put("/update/{Uid_usuarios}")
def update_usuario(Uid_usuarios: str, usuario: Usuario):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE usuarios 
            SET email = %s, nombre = %s, contraseña = %s, rol = %s
            WHERE Uid_usuarios = %s
        """
        values = (usuario.email, usuario.nombre, usuario.contraseña, usuario.rol, Uid_usuarios)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cur.close()
        conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario actualizado correctamente", "Uid_usuarios": Uid_usuarios}


# Ruta para eliminar un usuario
@router.delete("/delete/{Uid_usuarios}")
def delete_usuario(Uid_usuarios: str):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM usuarios WHERE Uid_usuarios = %s"
        cur.execute(query, (Uid_usuarios,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
    finally:
        cur.close()
        conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario eliminado correctamente", "Uid_usuarios": Uid_usuarios}