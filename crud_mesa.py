from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Mesa, MesaCreate, MesaUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/mesas/", response_model=dict)
async def create_mesa(mesa: MesaCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO mesa (numero, status) VALUES (%s, %s)",
            (mesa.numero, mesa.status)
        )
        conn.commit()
        return {"message": "Mesa criada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar mesa: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/mesas/", response_model=List[dict])
async def get_mesas(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM mesa")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/mesas/{id_mesa}", response_model=dict)
async def get_mesa(id_mesa: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM mesa WHERE id_mesa = %s", (id_mesa,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/mesas/{id_mesa}", response_model=dict)
async def update_mesa(id_mesa: int, mesa: MesaUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if mesa.numero is not None:
            updates.append("numero = %s")
            values.append(mesa.numero)
        if mesa.status is not None:
            updates.append("status = %s")
            values.append(mesa.status)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_mesa)
        query = f"UPDATE mesa SET {', '.join(updates)} WHERE id_mesa = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Mesa atualizada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/mesas/{id_mesa}", response_model=dict)
async def delete_mesa(id_mesa: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM mesa WHERE id_mesa = %s", (id_mesa,))
        conn.commit()
        return {"message": "Mesa deletada com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

