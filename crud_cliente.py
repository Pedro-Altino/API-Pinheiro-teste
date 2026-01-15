from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Cliente, ClienteCreate, ClienteUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/clientes/", response_model=dict)
async def create_cliente(cliente: ClienteCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO cliente (cpf, nome, email, tipo, id_usuario_cadastrou) VALUES (%s, %s, %s, %s, %s)",
            (cliente.cpf, cliente.nome, cliente.email, cliente.tipo, cliente.id_usuario_cadastrou)
        )
        conn.commit()
        return {"message": "Cliente criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/clientes/", response_model=List[dict])
async def get_clientes(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM cliente")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/clientes/{id_cliente}", response_model=dict)
async def get_cliente(id_cliente: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/clientes/{id_cliente}", response_model=dict)
async def update_cliente(id_cliente: int, cliente: ClienteUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if cliente.cpf is not None:
            updates.append("cpf = %s")
            values.append(cliente.cpf)
        if cliente.nome is not None:
            updates.append("nome = %s")
            values.append(cliente.nome)
        if cliente.email is not None:
            updates.append("email = %s")
            values.append(cliente.email)
        if cliente.tipo is not None:
            updates.append("tipo = %s")
            values.append(cliente.tipo)
        if cliente.id_usuario_cadastrou is not None:
            updates.append("id_usuario_cadastrou = %s")
            values.append(cliente.id_usuario_cadastrou)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_cliente)
        query = f"UPDATE cliente SET {', '.join(updates)} WHERE id_cliente = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Cliente atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/clientes/{id_cliente}", response_model=dict)
async def delete_cliente(id_cliente: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        return {"message": "Cliente deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
