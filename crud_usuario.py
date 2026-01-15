from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Usuario, UsuarioCreate, UsuarioUpdate
from typing import List
from auth import require_admin

router = APIRouter()

@router.post("/usuarios/", response_model=dict)
async def create_usuario(usuario: UsuarioCreate, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO usuario (nome, senha, tipo_usuario, email) VALUES (%s, %s, %s, %s)",
            (usuario.nome, usuario.senha, usuario.tipo_usuario, usuario.email)
        )
        conn.commit()
        return {"message": "Usuário criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/usuarios/", response_model=List[dict])
async def get_usuarios(current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM usuario")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/usuarios/{id_usuario}", response_model=dict)
async def get_usuario(id_usuario: int, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/usuarios/{id_usuario}", response_model=dict)
async def update_usuario(id_usuario: int, usuario: UsuarioUpdate, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if usuario.nome is not None:
            updates.append("nome = %s")
            values.append(usuario.nome)
        if usuario.senha is not None:
            updates.append("senha = %s")
            values.append(usuario.senha)
        if usuario.tipo_usuario is not None:
            updates.append("tipo_usuario = %s")
            values.append(usuario.tipo_usuario)
        if usuario.email is not None:
            updates.append("email = %s")
            values.append(usuario.email)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_usuario)
        query = f"UPDATE usuario SET {', '.join(updates)} WHERE id_usuario = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/usuarios/{id_usuario}", response_model=dict)
async def delete_usuario(id_usuario: int, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        return {"message": "Usuário deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
