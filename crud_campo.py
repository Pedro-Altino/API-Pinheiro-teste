from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Campo, CampoCreate, CampoUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/campos/", response_model=dict)
async def create_campo(campo: CampoCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO campo (numero, status) VALUES (%s, %s)",
            (campo.numero, campo.status)
        )
        conn.commit()
        return {"message": "Campo criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar campo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/campos/", response_model=List[dict])
async def get_campos(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM campo")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/campos/{id_campo}", response_model=dict)
async def get_campo(id_campo: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM campo WHERE id_campo = %s", (id_campo,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Campo não encontrado")
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/campos/{id_campo}", response_model=dict)
async def update_campo(id_campo: int, campo: CampoUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if campo.numero is not None:
            updates.append("numero = %s")
            values.append(campo.numero)
        if campo.status is not None:
            updates.append("status = %s")
            values.append(campo.status)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_campo)
        query = f"UPDATE campo SET {', '.join(updates)} WHERE id_campo = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Campo atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/campos/{id_campo}", response_model=dict)
async def delete_campo(id_campo: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM campo WHERE id_campo = %s", (id_campo,))
        conn.commit()
        return {"message": "Campo deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
