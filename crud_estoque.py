from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Estoque, EstoqueCreate, EstoqueUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/estoques/", response_model=dict)
async def create_estoque(estoque: EstoqueCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO estoque (id_produto, quant_present) VALUES (%s, %s)",
            (estoque.id_produto, estoque.quant_present)
        )
        conn.commit()
        return {"message": "Estoque criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar estoque: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/estoques/", response_model=List[dict])
async def get_estoques(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM estoque")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/estoques/{id_estoque}", response_model=dict)
async def get_estoque(id_estoque: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM estoque WHERE id_estoque = %s", (id_estoque,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Estoque não encontrado")
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/estoques/{id_estoque}", response_model=dict)
async def update_estoque(id_estoque: int, estoque: EstoqueUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        updates = []
        values = []
        if estoque.id_produto is not None:
            updates.append("id_produto = %s")
            values.append(estoque.id_produto)
        if estoque.quant_present is not None:
            updates.append("quant_present = %s")
            values.append(estoque.quant_present)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_estoque)
        query = f"UPDATE estoque SET {', '.join(updates)} WHERE id_estoque = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Estoque atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/estoques/{id_estoque}", response_model=dict)
async def delete_estoque(id_estoque: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM estoque WHERE id_estoque = %s", (id_estoque,))
        conn.commit()
        return {"message": "Estoque deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

