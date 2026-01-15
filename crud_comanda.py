from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Comanda, ComandaCreate, ComandaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/comandas/", response_model=dict)
async def create_comanda(comanda: ComandaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO comanda (data, status, numero_mesa, cpf_cliente, id_usuario_responsavel) VALUES (%s, %s, %s, %s, %s)",
            (comanda.data, comanda.status, comanda.numero_mesa, comanda.cpf_cliente, comanda.id_usuario_responsavel)
        )
        conn.commit()
        return {"message": "Comanda criada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar comanda: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/comandas/", response_model=List[dict])
async def get_comandas(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM comanda")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/comandas/{id_comanda}", response_model=dict)
async def get_comanda(id_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM comanda WHERE id_comanda = %s", (id_comanda,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/comandas/{id_comanda}", response_model=dict)
async def update_comanda(id_comanda: int, comanda: ComandaUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if comanda.data is not None:
            updates.append("data = %s")
            values.append(comanda.data)
        if comanda.status is not None:
            updates.append("status = %s")
            values.append(comanda.status)
        if comanda.numero_mesa is not None:
            updates.append("numero_mesa = %s")
            values.append(comanda.numero_mesa)
        if comanda.cpf_cliente is not None:
            updates.append("cpf_cliente = %s")
            values.append(comanda.cpf_cliente)
        if comanda.id_usuario_responsavel is not None:
            updates.append("id_usuario_responsavel = %s")
            values.append(comanda.id_usuario_responsavel)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_comanda)
        query = f"UPDATE comanda SET {', '.join(updates)} WHERE id_comanda = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Comanda atualizada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/comandas/{id_comanda}", response_model=dict)
async def delete_comanda(id_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM comanda WHERE id_comanda = %s", (id_comanda,))
        conn.commit()
        return {"message": "Comanda deletada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

