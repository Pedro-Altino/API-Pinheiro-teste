from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import PagComanda, PagComandaCreate, PagComandaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/pag_comanda/", response_model=dict)
async def create_pag_comanda(pag: PagComandaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        # Verifica se o pagamento existe
        cursor.execute("SELECT id_pagamento FROM pagamento WHERE id_pagamento = %s", (pag.id_pagamento,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        # Verifica se a comanda existe
        cursor.execute("SELECT id_comanda FROM comanda WHERE id_comanda = %s", (pag.id_comanda,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        
        cursor.execute(
            """INSERT INTO pag_comanda (id_pagamento, id_comanda) 
               VALUES (%s, %s)""",
            (pag.id_pagamento, pag.id_comanda)
        )
        conn.commit()
        return {"message": "Pagamento de comanda criado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pagamento de comanda: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_comanda/", response_model=List[dict])
async def get_pag_comandas(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pc.*, p.valor, p.forma, p.tipo_pagamento, c.numero_mesa, c.cpf_cliente
            FROM pag_comanda pc
            LEFT JOIN pagamento p ON pc.id_pagamento = p.id_pagamento
            LEFT JOIN comanda c ON pc.id_comanda = c.id_comanda
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_comanda/{id_pag_comanda}", response_model=dict)
async def get_pag_comanda(id_pag_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pc.*, p.valor, p.forma, p.tipo_pagamento, c.numero_mesa, c.cpf_cliente
            FROM pag_comanda pc
            LEFT JOIN pagamento p ON pc.id_pagamento = p.id_pagamento
            LEFT JOIN comanda c ON pc.id_comanda = c.id_comanda
            WHERE pc.id_pag_comanda = %s
        """, (id_pag_comanda,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pagamento de comanda não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_comanda/comanda/{id_comanda}", response_model=List[dict])
async def get_pag_by_comanda(id_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pc.*, p.valor, p.forma, p.tipo_pagamento
            FROM pag_comanda pc
            LEFT JOIN pagamento p ON pc.id_pagamento = p.id_pagamento
            WHERE pc.id_comanda = %s
        """, (id_comanda,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/pag_comanda/{id_pag_comanda}", response_model=dict)
async def delete_pag_comanda(id_pag_comanda: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM pag_comanda WHERE id_pag_comanda = %s", (id_pag_comanda,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pagamento de comanda não encontrado")
        
        return {"message": "Pagamento de comanda deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pagamento de comanda: {str(e)}")
    finally:
        cursor.close()
        conn.close()

