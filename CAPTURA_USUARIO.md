# Captura Automática de ID de Usuário

## 📋 Descrição

Alguns cadastros na API capturam automaticamente o ID do usuário logado (extraído das credenciais HTTP Basic). Você **não precisa** enviar `id_usuario_cadastrou` no request body.

## 🎯 Endpoints que Usam Captura Automática

### 1. **POST /api/produtos/** - Criar Produto
O campo `id_usuario_cadastrou` é extraído do usuário autenticado.

**Antes (sem captura automática):**
```json
{
  "nome": "Bebida",
  "preco": 5.50,
  "validade": "2026-12-31",
  "quant_min_estoque": 10,
  "id_usuario_cadastrou": 1
}
```

**Depois (com captura automática):**
```json
{
  "nome": "Bebida",
  "preco": 5.50,
  "validade": "2026-12-31",
  "quant_min_estoque": 10
}
```

### 2. **POST /api/reservas/** - Criar Reserva
O campo `id_usuario_cadastrou` é extraído do usuário autenticado.

**Request Body:**
```json
{
  "data": "2026-01-20",
  "quant_horas": 2,
  "status": "confirmada",
  "cpf_cliente": "12345678901",
  "id_campo": 1
}
```

### 3. **POST /api/compras/** - Criar Compra
O campo `id_usuario_cadastrou` é extraído do usuário autenticado.

**Request Body:**
```json
{
  "data": "2026-01-15",
  "valor_total": 150.00,
  "cpf_cliente": "12345678901"
}
```

### 4. **POST /api/pagamentos/** - Criar Pagamento
O campo `id_usuario_cadastrou` é extraído do usuário autenticado.

**Request Body:**
```json
{
  "valor": 100.00,
  "forma": "dinheiro",
  "tipo_pagamento": "venda"
}
```

## 🔐 Como Funciona

1. **Usuário se autentica** via HTTP Basic com email e senha
2. **Credenciais são verificadas** no banco de dados
3. **ID do usuário é extraído** das credenciais autenticadas
4. **ID é inserido automaticamente** no campo `id_usuario_cadastrou`

## 💡 Exemplo Prático

### Via cURL

```bash
# Criar produto como admin@pinheiro.com
curl -X POST "http://127.0.0.1:5000/api/produtos/" \
  -H "Content-Type: application/json" \
  -u "admin@pinheiro.com:admin123" \
  -d '{
    "nome": "Refrigerante",
    "preco": 3.50,
    "validade": "2027-01-01",
    "quant_min_estoque": 20
  }'

# Resposta:
# {"message": "Produto criado com sucesso"}
# 
# No banco de dados, o registro terá:
# - id_usuario_cadastrou = 1 (id do admin@pinheiro.com)
```

### Via Swagger UI

1. Acesse http://127.0.0.1:5000/docs
2. Clique em "Authorize" e autentique como admin@pinheiro.com / admin123
3. Abra o endpoint **POST /api/produtos/**
4. Clique em "Try it out"
5. Preencha apenas os campos (sem `id_usuario_cadastrou`):
   ```json
   {
     "nome": "Água",
     "preco": 2.00,
     "validade": "2027-06-01",
     "quant_min_estoque": 50
   }
   ```
6. Clique em "Execute"
7. O sistema automaticamente usará o ID do usuário logado!

## ✅ Vantagens

- ✔️ Segurança: Impossível falsificar quem cadastrou o item
- ✔️ Simplicidade: Menos campos no request body
- ✔️ Integridade: ID sempre corresponde ao usuário autenticado
- ✔️ Rastreabilidade: Sempre sabe quem fez cada cadastro

## ⚠️ Importante

Se tentar enviar `id_usuario_cadastrou` no request body, ele será **ignorado** e o do usuário autenticado será usado.

```bash
# Mesmo que você envie:
curl -X POST "http://127.0.0.1:5000/api/produtos/" \
  -H "Content-Type: application/json" \
  -u "admin@pinheiro.com:admin123" \
  -d '{
    "nome": "Produto",
    "preco": 10.00,
    "id_usuario_cadastrou": 999  # ❌ Será IGNORADO
  }'

# O registro será criado com:
# id_usuario_cadastrou = 1 (do admin@pinheiro.com)
# NÃO 999
```
