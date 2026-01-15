from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Pagamento, PagamentoCreate, PagamentoUpdate
from typing import List
from auth import require_admin, require_auth

router = APIRouter()

@router.post("/pagamentos/", response_model=dict)
async def create_pagamento(pagamento: PagamentoCreate, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO pagamento (valor, forma, tipo_pagamento, id_usuario_cadastrou) VALUES (%s, %s, %s, %s)",
            (pagamento.valor, pagamento.forma, pagamento.tipo_pagamento, current_user['id_usuario'])
        )
        conn.commit()
        return {"message": "Pagamento criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pagamento: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/pagamentos/", response_model=List[dict])
async def get_pagamentos(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM pagamento")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/pagamentos/{id_pagamento}", response_model=dict)
async def get_pagamento(id_pagamento: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/pagamentos/{id_pagamento}", response_model=dict)
async def update_pagamento(id_pagamento: int, pagamento: PagamentoUpdate, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if pagamento.valor is not None:
            updates.append("valor = %s")
            values.append(pagamento.valor)
        if pagamento.forma is not None:
            updates.append("forma = %s")
            values.append(pagamento.forma)
        if pagamento.tipo_pagamento is not None:
            updates.append("tipo_pagamento = %s")
            values.append(pagamento.tipo_pagamento)
        if pagamento.id_usuario_cadastrou is not None:
            updates.append("id_usuario_cadastrou = %s")
            values.append(pagamento.id_usuario_cadastrou)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_pagamento)
        query = f"UPDATE pagamento SET {', '.join(updates)} WHERE id_pagamento = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Pagamento atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/pagamentos/{id_pagamento}", response_model=dict)
async def delete_pagamento(id_pagamento: int, current_user: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        return {"message": "Pagamento deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
