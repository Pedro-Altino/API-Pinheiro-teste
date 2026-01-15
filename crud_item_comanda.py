from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import ItemComanda, ItemComandaCreate, ItemComandaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/item_comanda/", response_model=dict)
async def create_item_comanda(item: ItemComandaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            """INSERT INTO item_comanda (id_comanda, id_produto, quantidade, preco_unitario) 
               VALUES (%s, %s, %s, %s)""",
            (item.id_comanda, item.id_produto, item.quantidade, item.preco_unitario)
        )
        conn.commit()
        return {"message": "Item da comanda criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar item da comanda: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/item_comanda/", response_model=List[dict])
async def get_itens_comanda(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM item_comanda")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/item_comanda/{id_item_comanda}", response_model=dict)
async def get_item_comanda(id_item_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM item_comanda WHERE id_item_comanda = %s", (id_item_comanda,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item da comanda não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/item_comanda/comanda/{id_comanda}", response_model=List[dict])
async def get_itens_by_comanda(id_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT ic.*, p.nome as produto_nome 
            FROM item_comanda ic
            LEFT JOIN produto p ON ic.id_produto = p.id_produto
            WHERE ic.id_comanda = %s
        """, (id_comanda,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/item_comanda/{id_item_comanda}", response_model=dict)
async def update_item_comanda(id_item_comanda: int, item: ItemComandaUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if item.id_comanda is not None:
            updates.append("id_comanda = %s")
            values.append(item.id_comanda)
        if item.id_produto is not None:
            updates.append("id_produto = %s")
            values.append(item.id_produto)
        if item.quantidade is not None:
            updates.append("quantidade = %s")
            values.append(item.quantidade)
        if item.preco_unitario is not None:
            updates.append("preco_unitario = %s")
            values.append(item.preco_unitario)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_item_comanda)
        query = f"UPDATE item_comanda SET {', '.join(updates)} WHERE id_item_comanda = %s"
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item da comanda não encontrado")
        
        return {"message": "Item da comanda atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar item da comanda: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/item_comanda/{id_item_comanda}", response_model=dict)
async def delete_item_comanda(id_item_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM item_comanda WHERE id_item_comanda = %s", (id_item_comanda,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item da comanda não encontrado")
        
        return {"message": "Item da comanda deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar item da comanda: {str(e)}")
    finally:
        cursor.close()
        conn.close()

