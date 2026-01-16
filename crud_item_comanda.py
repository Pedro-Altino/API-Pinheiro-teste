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
        # Verifica se comanda existe
        cursor.execute("SELECT 1 FROM comanda WHERE id_comanda = %s", (item.id_comanda,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
            
        # Verifica se produto existe
        cursor.execute("SELECT 1 FROM produto WHERE id_produto = %s", (item.id_produto,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        cursor.execute(
            """INSERT INTO item_comanda (id_comanda, id_produto, quantidade) 
               VALUES (%s, %s, %s)""",
            (item.id_comanda, item.id_produto, item.quantidade)
        )
        conn.commit()
        return {"message": "Item da comanda criado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar item da comanda: {e}")
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
        
        # preco_unitario removido pois nao consta na tabela item_comanda

        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização")
        
        values.append(id_item_comanda)
        query = f"UPDATE item_comanda SET {', '.join(updates)} WHERE id_item_comanda = %s"
        cursor.execute(query, values)
        
        if cursor.rowcount == 0:
            # Verifica se item existe
            cursor.execute("SELECT 1 FROM item_comanda WHERE id_item_comanda = %s", (id_item_comanda,))
            if not cursor.fetchone():
               raise HTTPException(status_code=404, detail=f"Item da comanda com ID {id_item_comanda} não encontrado")
        
        conn.commit()
        return {"message": "Item da comanda atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar item da comanda: {e}")
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

