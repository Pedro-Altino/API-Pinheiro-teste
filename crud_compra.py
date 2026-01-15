from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Compra, CompraCreate, CompraUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/compras/", response_model=dict)
async def create_compra(compra: CompraCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            """INSERT INTO compra (data, valor_total, cpf_cliente, id_usuario_cadastrou) 
               VALUES (%s, %s, %s, %s)""",
            (compra.data, compra.valor_total, compra.cpf_cliente, current_user['id_usuario'])
        )
        conn.commit()
        return {"message": "Compra criada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/compras/", response_model=List[dict])
async def get_compras(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT c.*, cl.nome as cliente_nome, u.nome as usuario_nome
            FROM compra c
            LEFT JOIN cliente cl ON c.cpf_cliente = cl.cpf
            LEFT JOIN usuario u ON c.id_usuario_cadastrou = u.id_usuario
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/compras/{id_compra}", response_model=dict)
async def get_compra(id_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT c.*, cl.nome as cliente_nome, u.nome as usuario_nome
            FROM compra c
            LEFT JOIN cliente cl ON c.cpf_cliente = cl.cpf
            LEFT JOIN usuario u ON c.id_usuario_cadastrou = u.id_usuario
            WHERE c.id_compra = %s
        """, (id_compra,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/compras/{id_compra}", response_model=dict)
async def update_compra(id_compra: int, compra: CompraUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if compra.data is not None:
            updates.append("data = %s")
            values.append(compra.data)
        if compra.valor_total is not None:
            updates.append("valor_total = %s")
            values.append(compra.valor_total)
        if compra.cpf_cliente is not None:
            updates.append("cpf_cliente = %s")
            values.append(compra.cpf_cliente)
        if compra.id_usuario_cadastrou is not None:
            updates.append("id_usuario_cadastrou = %s")
            values.append(compra.id_usuario_cadastrou)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_compra)
        query = f"UPDATE compra SET {', '.join(updates)} WHERE id_compra = %s"
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        return {"message": "Compra atualizada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/compras/{id_compra}", response_model=dict)
async def delete_compra(id_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM compra WHERE id_compra = %s", (id_compra,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        return {"message": "Compra deletada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()
