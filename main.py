from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from crud_usuario import router as usuario_router
from crud_cliente import router as cliente_router
from crud_produto import router as produto_router
from crud_comanda import router as comanda_router
from crud_mesa import router as mesa_router
from crud_campo import router as campo_router
from crud_reserva import router as reserva_router
from crud_pagamento import router as pagamento_router
from crud_pag_comanda import router as pag_comanda_router
from crud_pag_compra import router as pag_compra_router
from crud_pag_reserva import router as pag_reserva_router
from crud_estoque import router as estoque_router
from crud_movimenta import router as movimenta_router
from crud_compra import router as compra_router
from crud_item_comanda import router as item_comanda_router
from crud_item_compra import router as item_compra_router
from crud_views import router as views_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("\n" + "="*60)
    print("🚀 Pinheiro API iniciada com sucesso!")
    print("="*60)
    print("📍 Acesse em: http://127.0.0.1:5000")
    print("📚 Documentação: http://127.0.0.1:5000/docs")
    print("="*60 + "\n")
    yield
    # Shutdown (se necessário)
    print("\n" + "="*60)
    print("🛑 Pinheiro API encerrada")
    print("="*60 + "\n")

app = FastAPI(
    title="Pinheiro API",
    description="API para gerenciamento da arena pinheiro",
    lifespan=lifespan
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router, prefix="/api", tags=["Usuario"])
app.include_router(cliente_router, prefix="/api", tags=["Cliente"])
app.include_router(produto_router, prefix="/api", tags=["Produto"])
app.include_router(comanda_router, prefix="/api", tags=["Comanda"])
app.include_router(mesa_router, prefix="/api", tags=["Mesa"])
app.include_router(campo_router, prefix="/api", tags=["Campo"])
app.include_router(reserva_router, prefix="/api", tags=["Reserva"])
app.include_router(pagamento_router, prefix="/api", tags=["Pagamento"])
app.include_router(pag_comanda_router, prefix="/api", tags=["Pagamento Comanda"])
app.include_router(pag_compra_router, prefix="/api", tags=["Pagamento Compra"])
app.include_router(pag_reserva_router, prefix="/api", tags=["Pagamento Reserva"])
app.include_router(estoque_router, prefix="/api", tags=["Estoque"])
app.include_router(movimenta_router, prefix="/api", tags=["Movimenta"])
app.include_router(compra_router, prefix="/api", tags=["Compra"])
app.include_router(item_comanda_router, prefix="/api", tags=["Item Comanda"])
app.include_router(item_compra_router, prefix="/api", tags=["Item Compra"])
app.include_router(views_router, prefix="/api", tags=["Views (Visões Complexas)"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
