from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import PagCompra, PagCompraCreate, PagCompraUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/pag_compra/", response_model=dict)
async def create_pag_compra(pag: PagCompraCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        # Verifica se o pagamento existe
        cursor.execute("SELECT id_pagamento FROM pagamento WHERE id_pagamento = %s", (pag.id_pagamento,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        # Verifica se a compra existe
        cursor.execute("SELECT id_compra FROM compra WHERE id_compra = %s", (pag.id_compra,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        cursor.execute(
            """INSERT INTO pag_compra (id_pagamento, id_compra) 
               VALUES (%s, %s)""",
            (pag.id_pagamento, pag.id_compra)
        )
        conn.commit()
        return {"message": "Pagamento de compra criado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pagamento de compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_compra/", response_model=List[dict])
async def get_pag_compras(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pc.*, p.valor, p.forma, p.tipo_pagamento, c.cpf_cliente, c.valor_total
            FROM pag_compra pc
            LEFT JOIN pagamento p ON pc.id_pagamento = p.id_pagamento
            LEFT JOIN compra c ON pc.id_compra = c.id_compra
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_compra/{id_pag_compra}", response_model=dict)
async def get_pag_compra(id_pag_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pc.*, p.valor, p.forma, p.tipo_pagamento, c.cpf_cliente, c.valor_total
            FROM pag_compra pc
            LEFT JOIN pagamento p ON pc.id_pagamento = p.id_pagamento
            LEFT JOIN compra c ON pc.id_compra = c.id_compra
            WHERE pc.id_pag_compra = %s
        """, (id_pag_compra,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pagamento de compra não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_compra/compra/{id_compra}", response_model=List[dict])
async def get_pag_by_compra(id_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pc.*, p.valor, p.forma, p.tipo_pagamento
            FROM pag_compra pc
            LEFT JOIN pagamento p ON pc.id_pagamento = p.id_pagamento
            WHERE pc.id_compra = %s
        """, (id_compra,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/pag_compra/{id_pag_compra}", response_model=dict)
async def delete_pag_compra(id_pag_compra: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM pag_compra WHERE id_pag_compra = %s", (id_pag_compra,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pagamento de compra não encontrado")
        
        return {"message": "Pagamento de compra deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pagamento de compra: {str(e)}")
    finally:
        cursor.close()
        conn.close()

