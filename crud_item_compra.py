from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import ItemCompra, ItemCompraCreate, ItemCompraUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/item_compra/", response_model=dict)
async def create_item_compra(item: ItemCompraCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            """INSERT INTO item_compra (id_compra, id_produto, quantidade, preco_unitario) 
               VALUES (%s, %s, %s, %s)""",
            (item.id_compra, item.id_produto, item.quantidade, item.preco_unitario)
        )
        conn.commit()
        return {"message": "Item da compra criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar item da compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/item_compra/", response_model=List[dict])
async def get_itens_compra(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM item_compra")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/item_compra/{id_item_compra}", response_model=dict)
async def get_item_compra(id_item_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM item_compra WHERE id_item_compra = %s", (id_item_compra,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item da compra não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/item_compra/compra/{id_compra}", response_model=List[dict])
async def get_itens_by_compra(id_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT ic.*, p.nome as produto_nome 
            FROM item_compra ic
            LEFT JOIN produto p ON ic.id_produto = p.id_produto
            WHERE ic.id_compra = %s
        """, (id_compra,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/item_compra/{id_item_compra}", response_model=dict)
async def update_item_compra(id_item_compra: int, item: ItemCompraUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if item.id_compra is not None:
            updates.append("id_compra = %s")
            values.append(item.id_compra)
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
        
        values.append(id_item_compra)
        query = f"UPDATE item_compra SET {', '.join(updates)} WHERE id_item_compra = %s"
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item da compra não encontrado")
        
        return {"message": "Item da compra atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar item da compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/item_compra/{id_item_compra}", response_model=dict)
async def delete_item_compra(id_item_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM item_compra WHERE id_item_compra = %s", (id_item_compra,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item da compra não encontrado")
        
        return {"message": "Item da compra deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar item da compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

