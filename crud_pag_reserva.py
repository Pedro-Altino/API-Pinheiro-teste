from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import PagReserva, PagReservaCreate, PagReservaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/pag_reserva/", response_model=dict)
async def create_pag_reserva(pag: PagReservaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        # Verifica se o pagamento existe
        cursor.execute("SELECT id_pagamento FROM pagamento WHERE id_pagamento = %s", (pag.id_pagamento,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        # Verifica se a reserva existe
        cursor.execute("SELECT id_reserva FROM reserva WHERE id_reserva = %s", (pag.id_reserva,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        cursor.execute(
            """INSERT INTO pag_reserva (id_pagamento, id_reserva, porcentagem) 
               VALUES (%s, %s, %s)""",
            (pag.id_pagamento, pag.id_reserva, pag.porcentagem)
        )
        conn.commit()
        return {"message": "Pagamento de reserva criado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pagamento de reserva: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_reserva/", response_model=List[dict])
async def get_pag_reservas(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pr.*, p.valor, p.forma, p.tipo_pagamento, 
                   r.data as data_reserva, r.quant_horas, r.status
            FROM pag_reserva pr
            LEFT JOIN pagamento p ON pr.id_pagamento = p.id_pagamento
            LEFT JOIN reserva r ON pr.id_reserva = r.id_reserva
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_reserva/{id_pag_reserva}", response_model=dict)
async def get_pag_reserva(id_pag_reserva: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pr.*, p.valor, p.forma, p.tipo_pagamento,
                   r.data as data_reserva, r.quant_horas, r.status
            FROM pag_reserva pr
            LEFT JOIN pagamento p ON pr.id_pagamento = p.id_pagamento
            LEFT JOIN reserva r ON pr.id_reserva = r.id_reserva
            WHERE pr.id_pag_reserva = %s
        """, (id_pag_reserva,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pagamento de reserva não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pag_reserva/reserva/{id_reserva}", response_model=List[dict])
async def get_pag_by_reserva(id_reserva: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("""
            SELECT pr.*, p.valor, p.forma, p.tipo_pagamento
            FROM pag_reserva pr
            LEFT JOIN pagamento p ON pr.id_pagamento = p.id_pagamento
            WHERE pr.id_reserva = %s
        """, (id_reserva,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/pag_reserva/{id_pag_reserva}", response_model=dict)
async def update_pag_reserva(id_pag_reserva: int, pag: PagReservaUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        
        if pag.id_pagamento is not None:
            cursor.execute("SELECT id_pagamento FROM pagamento WHERE id_pagamento = %s", (pag.id_pagamento,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Pagamento não encontrado")
            updates.append("id_pagamento = %s")
            values.append(pag.id_pagamento)
        if pag.id_reserva is not None:
            cursor.execute("SELECT id_reserva FROM reserva WHERE id_reserva = %s", (pag.id_reserva,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Reserva não encontrada")
            updates.append("id_reserva = %s")
            values.append(pag.id_reserva)
        if pag.porcentagem is not None:
            updates.append("porcentagem = %s")
            values.append(pag.porcentagem)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_pag_reserva)
        query = f"UPDATE pag_reserva SET {', '.join(updates)} WHERE id_pag_reserva = %s"
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pagamento de reserva não encontrado")
        
        return {"message": "Pagamento de reserva atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar pagamento de reserva: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/pag_reserva/{id_pag_reserva}", response_model=dict)
async def delete_pag_reserva(id_pag_reserva: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM pag_reserva WHERE id_pag_reserva = %s", (id_pag_reserva,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pagamento de reserva não encontrado")
        
        return {"message": "Pagamento de reserva deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pagamento de reserva: {str(e)}")
    finally:
        cursor.close()
        conn.close()

