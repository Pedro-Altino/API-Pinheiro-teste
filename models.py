from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class Usuario(BaseModel):
    id_usuario: int
    nome: str
    senha: str
    tipo_usuario: str
    email: str

class UsuarioCreate(BaseModel):
    nome: str
    senha: str
    tipo_usuario: str
    email: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    senha: Optional[str] = None
    tipo_usuario: Optional[str] = None
    email: Optional[str] = None

class Cliente(BaseModel):
    id_cliente: int
    cpf: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    tipo: Optional[str] = None
    id_usuario_cadastrou: Optional[int] = None

class ClienteCreate(BaseModel):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    tipo: Optional[str] = None
    id_usuario_cadastrou: Optional[int] = None

class ClienteUpdate(BaseModel):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    tipo: Optional[str] = None
    id_usuario_cadastrou: Optional[int] = None

class Produto(BaseModel):
    id_produto: int
    nome: Optional[str] = None
    preco: Optional[Decimal] = None
    validade: Optional[date] = None
    quant_min_estoque: Optional[int] = None
    id_usuario_cadastrou: Optional[int] = None

class ProdutoCreate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[Decimal] = None
    validade: Optional[date] = None
    quant_min_estoque: Optional[int] = None

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[Decimal] = None
    validade: Optional[date] = None
    quant_min_estoque: Optional[int] = None

class ItemComanda(BaseModel):
    id_item_comanda: int
    id_comanda: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[Decimal] = None

class ItemComandaCreate(BaseModel):
    id_comanda: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[Decimal] = None

class ItemComandaUpdate(BaseModel):
    id_comanda: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[Decimal] = None

class Comanda(BaseModel):
    id_comanda: int
    data: Optional[date] = None
    status: Optional[str] = None
    numero_mesa: Optional[int] = None
    cpf_cliente: Optional[str] = None
    id_usuario_responsavel: Optional[int] = None

class ComandaCreate(BaseModel):
    data: Optional[date] = None
    status: Optional[str] = None
    numero_mesa: Optional[int] = None
    cpf_cliente: Optional[str] = None
    id_usuario_responsavel: Optional[int] = None

class ComandaUpdate(BaseModel):
    data: Optional[date] = None
    status: Optional[str] = None
    numero_mesa: Optional[int] = None
    cpf_cliente: Optional[str] = None
    id_usuario_responsavel: Optional[int] = None

class PagComanda(BaseModel):
    id_pag_comanda: int
    id_pagamento: int
    id_comanda: int

class PagComandaCreate(BaseModel):
    id_pagamento: int
    id_comanda: int

class PagComandaUpdate(BaseModel):
    id_pagamento: Optional[int] = None
    id_comanda: Optional[int] = None

class Pagamento(BaseModel):
    id_pagamento: int
    valor: Optional[Decimal] = None
    forma: Optional[str] = None
    tipo_pagamento: Optional[str] = None
    id_usuario_cadastrou: Optional[int] = None

class PagamentoCreate(BaseModel):
    valor: Optional[Decimal] = None
    forma: Optional[str] = None
    tipo_pagamento: Optional[str] = None

class PagamentoUpdate(BaseModel):
    valor: Optional[Decimal] = None
    forma: Optional[str] = None
    tipo_pagamento: Optional[str] = None

class Reserva(BaseModel):
    id_reserva: int
    data: Optional[date] = None
    quant_horas: Optional[int] = None
    status: Optional[str] = None
    cpf_cliente: Optional[str] = None
    id_campo: Optional[int] = None
    id_usuario_cadastrou: Optional[int] = None

class ReservaCreate(BaseModel):
    data: Optional[date] = None
    quant_horas: Optional[int] = None
    status: Optional[str] = None
    cpf_cliente: Optional[str] = None
    id_campo: Optional[int] = None

class ReservaUpdate(BaseModel):
    data: Optional[date] = None
    quant_horas: Optional[int] = None
    status: Optional[str] = None
    cpf_cliente: Optional[str] = None
    id_campo: Optional[int] = None

class Campo(BaseModel):
    id_campo: int
    numero: Optional[int] = None
    status: Optional[str] = None

class CampoCreate(BaseModel):
    numero: Optional[int] = None
    status: Optional[str] = None

class CampoUpdate(BaseModel):
    numero: Optional[int] = None
    status: Optional[str] = None

class PagCompra(BaseModel):
    id_pag_compra: int
    id_pagamento: Optional[int] = None
    id_compra: Optional[int] = None

class PagCompraCreate(BaseModel):
    id_pagamento: Optional[int] = None
    id_compra: Optional[int] = None

class PagCompraUpdate(BaseModel):
    id_pagamento: Optional[int] = None
    id_compra: Optional[int] = None

class Compra(BaseModel):
    id_compra: int
    data: Optional[date] = None
    valor_total: Optional[Decimal] = None
    cpf_cliente: Optional[str] = None
    id_usuario_cadastrou: Optional[int] = None

class CompraCreate(BaseModel):
    data: Optional[date] = None
    valor_total: Optional[Decimal] = None
    cpf_cliente: Optional[str] = None

class CompraUpdate(BaseModel):
    data: Optional[date] = None
    valor_total: Optional[Decimal] = None
    cpf_cliente: Optional[str] = None

class PagReserva(BaseModel):
    id_pag_reserva: int
    id_pagamento: Optional[int] = None
    id_reserva: Optional[int] = None
    porcentagem: Optional[float] = None

class PagReservaCreate(BaseModel):
    id_pagamento: Optional[int] = None
    id_reserva: Optional[int] = None
    porcentagem: Optional[float] = None

class PagReservaUpdate(BaseModel):
    id_pagamento: Optional[int] = None
    id_reserva: Optional[int] = None
    porcentagem: Optional[float] = None

class Mesa(BaseModel):
    id_mesa: int
    numero: int
    status: Optional[str] = None

class MesaCreate(BaseModel):
    numero: int
    status: Optional[str] = None

class MesaUpdate(BaseModel):
    numero: Optional[int] = None
    status: Optional[str] = None

class ItemCompra(BaseModel):
    id_item_compra: int
    id_compra: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[Decimal] = None

class ItemCompraCreate(BaseModel):
    id_compra: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[Decimal] = None

class ItemCompraUpdate(BaseModel):
    id_compra: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[Decimal] = None

class Estoque(BaseModel):
    id_estoque: int
    id_produto: int
    quant_present: Optional[int] = None
    
class EstoqueCreate(BaseModel):
    id_produto: int
    quant_present: Optional[int] = None

class EstoqueUpdate(BaseModel):
    id_produto: Optional[int] = None
    quant_present: Optional[int] = None

class Movimenta(BaseModel):
    id_movimenta: int
    id_estoque: Optional[int] = None
    tipo: Optional[str] = None
    quantidade: Optional[int] = None
    data: Optional[date] = None

class MovimentaCreate(BaseModel):
    id_estoque: Optional[int] = None
    tipo: Optional[str] = None
    quantidade: Optional[int] = None
    data: Optional[date] = None

class MovimentaUpdate(BaseModel):
    id_estoque: Optional[int] = None
    tipo: Optional[str] = None
    quantidade: Optional[int] = None
    data: Optional[date] = None
