from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Movimenta, MovimentaCreate, MovimentaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/movimentas/", response_model=dict)
async def create_movimenta(movimenta: MovimentaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO movimenta (id_estoque, tipo, quantidade, data) VALUES (%s, %s, %s, %s)",
            (movimenta.id_estoque, movimenta.tipo, movimenta.quantidade, movimenta.data)
        )
        conn.commit()
        return {"message": "Movimentação criada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar movimentação: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/movimentas/", response_model=List[dict])
async def get_movimentas(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM movimenta")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/movimentas/{id_movimenta}", response_model=dict)
async def get_movimenta(id_movimenta: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM movimenta WHERE id_movimenta = %s", (id_movimenta,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Movimentação não encontrada")
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/movimentas/{id_movimenta}", response_model=dict)
async def update_movimenta(id_movimenta: int, movimenta: MovimentaUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        updates = []
        values = []
        if movimenta.id_estoque is not None:
            updates.append("id_estoque = %s")
            values.append(movimenta.id_estoque)
        if movimenta.tipo is not None:
            updates.append("tipo = %s")
            values.append(movimenta.tipo)
        if movimenta.quantidade is not None:
            updates.append("quantidade = %s")
            values.append(movimenta.quantidade)
        if movimenta.data is not None:
            updates.append("data = %s")
            values.append(movimenta.data)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_movimenta)
        query = f"UPDATE movimenta SET {', '.join(updates)} WHERE id_movimenta = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Movimentação atualizada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/movimentas/{id_movimenta}", response_model=dict)
async def delete_movimenta(id_movimenta: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM movimenta WHERE id_movimenta = %s", (id_movimenta,))
        conn.commit()
        return {"message": "Movimentação deletada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

