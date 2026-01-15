from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from auth import require_auth

router = APIRouter()

@router.get("/views/item-comanda-completo")
async def get_itens_comanda_completo(id_comanda: int = None, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        if id_comanda:
            cursor.execute(
                """
                SELECT 
                    id_item_comanda,
                    id_comanda,
                    id_produto,
                    produto_nome,
                    quantidade,
                    preco_unitario,
                    subtotal
                FROM vw_item_comanda_completo 
                WHERE id_comanda = %s
                ORDER BY id_item_comanda
                """,
                (id_comanda,)
            )
        else:
            cursor.execute(
                """
                SELECT 
                    id_item_comanda,
                    id_comanda,
                    id_produto,
                    produto_nome,
                    quantidade,
                    preco_unitario,
                    subtotal
                FROM vw_item_comanda_completo 
                ORDER BY id_comanda, id_item_comanda
                LIMIT 100
                """
            )
        
        items = cursor.fetchall()
        return [dict(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/views/item-compra-completo")
async def get_itens_compra_completo(id_compra: int = None, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        if id_compra:
            cursor.execute(
                """
                SELECT 
                    id_item_compra,
                    id_compra,
                    id_produto,
                    produto_nome,
                    quantidade,
                    preco_unitario,
                    subtotal
                FROM vw_item_compra_completo 
                WHERE id_compra = %s
                ORDER BY id_item_compra
                """,
                (id_compra,)
            )
        else:
            cursor.execute(
                """
                SELECT 
                    id_item_compra,
                    id_compra,
                    id_produto,
                    produto_nome,
                    quantidade,
                    preco_unitario,
                    subtotal
                FROM vw_item_compra_completo 
                ORDER BY id_compra, id_item_compra
                LIMIT 100
                """
            )
        
        items = cursor.fetchall()
        return [dict(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/views/produtos-estoque")
async def get_produtos_estoque(em_estoque: bool = None, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        if em_estoque:
            cursor.execute(
                """
                SELECT id_produto, nome, preco, quant_present
                FROM vw_produtos_estoque 
                WHERE quant_present > 0
                ORDER BY nome
                """
            )
        else:
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

@router.get("/views/clientes-publicos")
async def get_clientes_publicos(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        cursor.execute(
            """
            SELECT id_cliente, nome, email, tipo, cpf
            FROM vw_clientes_publicos 
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
