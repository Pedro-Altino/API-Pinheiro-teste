from fastapi import APIRouter, HTTPException, Depends
from db import get_db_connection, get_db_cursor
from models import Produto, ProdutoCreate, ProdutoUpdate
from typing import List
from auth import require_auth

router = APIRouter()

@router.post("/produtos/", response_model=dict)
async def create_produto(produto: ProdutoCreate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO produto (nome, preco, validade, quant_min_estoque, id_usuario_cadastrou) VALUES (%s, %s, %s, %s, %s)",
            (produto.nome, produto.preco, produto.validade, produto.quant_min_estoque, current_user['id_usuario'])
        )
        conn.commit()
        return {"message": "Produto criado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/produtos/", response_model=List[dict])
async def get_produtos(current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM produto")
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/produtos/{id_produto}", response_model=dict)
async def get_produto(id_produto: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("SELECT * FROM produto WHERE id_produto = %s", (id_produto,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/produtos/{id_produto}", response_model=dict)
async def update_produto(id_produto: int, produto: ProdutoUpdate, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        updates = []
        values = []
        if produto.nome is not None:
            updates.append("nome = %s")
            values.append(produto.nome)
        if produto.preco is not None:
            updates.append("preco = %s")
            values.append(produto.preco)
        if produto.validade is not None:
            updates.append("validade = %s")
            values.append(produto.validade)
        if produto.quant_min_estoque is not None:
            updates.append("quant_min_estoque = %s")
            values.append(produto.quant_min_estoque)
        if produto.id_usuario_cadastrou is not None:
            updates.append("id_usuario_cadastrou = %s")
            values.append(produto.id_usuario_cadastrou)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        values.append(id_produto)
        query = f"UPDATE produto SET {', '.join(updates)} WHERE id_produto = %s"
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Produto atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/produtos/{id_produto}", response_model=dict)
async def delete_produto(id_produto: int, current_user: dict = Depends(require_auth)):
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM produto WHERE id_produto = %s", (id_produto,))
        conn.commit()
        return {"message": "Produto deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
