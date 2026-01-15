from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Reserva, ReservaCreate, ReservaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/reservas/", response_model=dict)
async def create_reserva(reserva: ReservaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO reserva (data, quant_horas, status, cpf_cliente, id_campo, id_usuario_cadastrou) VALUES (%s, %s, %s, %s, %s, %s)",
            (reserva.data, reserva.quant_horas, reserva.status, reserva.cpf_cliente, reserva.id_campo, current_user['id_usuario'])
        )
        conn.commit()
        return {"message": "Reserva criada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar reserva: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/reservas/", response_model=List[dict])
async def get_reservas(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM reserva")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/reservas/{id_reserva}", response_model=dict)
async def get_reserva(id_reserva: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/reservas/{id_reserva}", response_model=dict)
async def update_reserva(id_reserva: int, reserva: ReservaUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if reserva.data is not None:
            updates.append("data = %s")
            values.append(reserva.data)
        if reserva.quant_horas is not None:
            updates.append("quant_horas = %s")
            values.append(reserva.quant_horas)
        if reserva.status is not None:
            updates.append("status = %s")
            values.append(reserva.status)
        if reserva.cpf_cliente is not None:
            updates.append("cpf_cliente = %s")
            values.append(reserva.cpf_cliente)
        if reserva.id_campo is not None:
            updates.append("id_campo = %s")
            values.append(reserva.id_campo)
        if reserva.id_usuario_cadastrou is not None:
            updates.append("id_usuario_cadastrou = %s")
            values.append(reserva.id_usuario_cadastrou)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_reserva)
        query = f"UPDATE reserva SET {', '.join(updates)} WHERE id_reserva = %s"
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        return {"message": "Reserva atualizada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/reservas/{id_reserva}", response_model=dict)
async def delete_reserva(id_reserva: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        return {"message": "Reserva deletada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        conn.close()
