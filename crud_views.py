from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from auth import require_auth

router = APIRouter()

@router.get("/views/produtos-estoque")
async def get_produtos_estoque(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        cursor.execute(
            """
            SELECT id_produto, nome, preco, quant_present
            FROM vw_produtos_estoque 
            ORDER BY nome
            """
        )
        
        items = cursor.fetchall()
        return [dict(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/views/reservas-detalhe")
async def get_reservas_detalhe(status: str = None, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        if status:
            cursor.execute(
                """
                SELECT id_reserva, data, quant_horas, status, cpf_cliente, id_campo
                FROM vw_reservas_detalhe 
                WHERE status = %s
                ORDER BY data DESC
                """,
                (status,)
            )
        else:
            cursor.execute(
                """
                SELECT id_reserva, data, quant_horas, status, cpf_cliente, id_campo
                FROM vw_reservas_detalhe 
                ORDER BY data DESC
                """
            )
        
        items = cursor.fetchall()
        return [dict(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
