-- Script completo para criação do banco de dados arena_pinheiro
-- Execute no PostgreSQL como usuário com privilégios

-- Criar banco de dados (se não existir)
-- CREATE DATABASE arena_pinheiro;
-- \c arena_pinheiro

-- =============================================================================
-- 1. TABELA USUARIO
-- =============================================================================
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

-- =============================================================================
-- 2. TABELA CLIENTE
-- =============================================================================
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    cpf VARCHAR(11) UNIQUE,
    nome VARCHAR(100),
    email VARCHAR(100),
    tipo VARCHAR(50),
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- =============================================================================
-- 3. TABELA PRODUTO
-- =============================================================================
CREATE TABLE IF NOT EXISTS produto (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    preco NUMERIC(10, 2),
    validade DATE,
    quant_min_estoque INTEGER,
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- =============================================================================
-- 4. TABELA ESTOQUE
-- =============================================================================
CREATE TABLE IF NOT EXISTS estoque (
    id_estoque SERIAL PRIMARY KEY,
    id_produto INTEGER UNIQUE REFERENCES produto(id_produto) ON DELETE CASCADE,
    quant_present INTEGER DEFAULT 0
);

-- =============================================================================
-- 5. TABELA MOVIMENTA (Movimentação de Estoque)
-- =============================================================================
CREATE TABLE IF NOT EXISTS movimenta (
    id_movimenta SERIAL PRIMARY KEY,
    id_estoque INTEGER REFERENCES estoque(id_estoque) ON DELETE CASCADE,
    tipo VARCHAR(50), -- 'entrada' ou 'saida'
    quantidade INTEGER,
    data DATE
);

-- =============================================================================
-- 6. TABELA MESA
-- =============================================================================
CREATE TABLE IF NOT EXISTS mesa (
    id_mesa SERIAL PRIMARY KEY,
    numero INTEGER UNIQUE NOT NULL,
    status VARCHAR(50) -- 'disponivel', 'ocupada', 'reservada'
);

-- =============================================================================
-- 7. TABELA COMANDA
-- =============================================================================
CREATE TABLE IF NOT EXISTS comanda (
    id_comanda SERIAL PRIMARY KEY,
    data DATE,
    status VARCHAR(50), -- 'aberta', 'fechada', 'paga'
    numero_mesa INTEGER REFERENCES mesa(numero) ON DELETE SET NULL,
    cpf_cliente VARCHAR(11) REFERENCES cliente(cpf) ON DELETE SET NULL,
    id_usuario_responsavel INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- =============================================================================
-- 8. TABELA ITEM_COMANDA
-- =============================================================================
CREATE TABLE IF NOT EXISTS item_comanda (
    id_item_comanda SERIAL PRIMARY KEY,
    id_comanda INTEGER REFERENCES comanda(id_comanda) ON DELETE CASCADE,
    id_produto INTEGER REFERENCES produto(id_produto) ON DELETE SET NULL,
    quantidade INTEGER
);

-- =============================================================================
-- 9. TABELA CAMPO
-- =============================================================================
CREATE TABLE IF NOT EXISTS campo (
    id_campo SERIAL PRIMARY KEY,
    numero INTEGER UNIQUE,
    status VARCHAR(50) -- 'disponivel', 'ocupado', 'manutencao'
);

-- =============================================================================
-- 10. TABELA RESERVA
-- =============================================================================
CREATE TABLE IF NOT EXISTS reserva (
    id_reserva SERIAL PRIMARY KEY,
    data DATE,
    quant_horas INTEGER,
    status VARCHAR(50), -- 'confirmada', 'cancelada', 'realizada'
    cpf_cliente VARCHAR(11) REFERENCES cliente(cpf) ON DELETE SET NULL,
    id_campo INTEGER REFERENCES campo(id_campo) ON DELETE SET NULL,
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- =============================================================================
-- 11. TABELA COMPRA
-- =============================================================================
CREATE TABLE IF NOT EXISTS compra (
    id_compra SERIAL PRIMARY KEY,
    data DATE,
    valor_total NUMERIC(10, 2),
    cpf_cliente VARCHAR(11) REFERENCES cliente(cpf) ON DELETE SET NULL,
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- =============================================================================
-- 12. TABELA ITEM_COMPRA
-- =============================================================================
CREATE TABLE IF NOT EXISTS item_compra (
    id_item_compra SERIAL PRIMARY KEY,
    id_compra INTEGER REFERENCES compra(id_compra) ON DELETE CASCADE,
    id_produto INTEGER REFERENCES produto(id_produto) ON DELETE SET NULL,
    quantidade INTEGER
);

-- =============================================================================
-- 13. TABELA PAGAMENTO
-- =============================================================================
CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    valor NUMERIC(10, 2),
    forma VARCHAR(50), -- 'dinheiro', 'cartao_credito', 'cartao_debito', 'pix'
    tipo_pagamento VARCHAR(50), -- 'comanda', 'compra', 'reserva'
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- =============================================================================
-- 14. TABELA PAG_COMANDA (Relacionamento Pagamento-Comanda)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pag_comanda (
    id_pag_comanda SERIAL PRIMARY KEY,
    id_pagamento INTEGER NOT NULL REFERENCES pagamento(id_pagamento) ON DELETE CASCADE,
    id_comanda INTEGER NOT NULL REFERENCES comanda(id_comanda) ON DELETE CASCADE,
    UNIQUE(id_pagamento, id_comanda)
);

-- =============================================================================
-- 15. TABELA PAG_COMPRA (Relacionamento Pagamento-Compra)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pag_compra (
    id_pag_compra SERIAL PRIMARY KEY,
    id_pagamento INTEGER NOT NULL REFERENCES pagamento(id_pagamento) ON DELETE CASCADE,
    id_compra INTEGER NOT NULL REFERENCES compra(id_compra) ON DELETE CASCADE,
    UNIQUE(id_pagamento, id_compra)
);

-- =============================================================================
-- 16. TABELA PAG_RESERVA (Relacionamento Pagamento-Reserva)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pag_reserva (
    id_pag_reserva SERIAL PRIMARY KEY,
    id_pagamento INTEGER NOT NULL REFERENCES pagamento(id_pagamento) ON DELETE CASCADE,
    id_reserva INTEGER NOT NULL REFERENCES reserva(id_reserva) ON DELETE CASCADE,
    porcentagem NUMERIC(5, 2), -- Para pagamentos parciais
    UNIQUE(id_pagamento, id_reserva)
);

-- =============================================================================
-- VIEWS PARA CONSULTAS OTIMIZADAS
-- =============================================================================

-- View: Item Comanda com Preço do Produto
CREATE OR REPLACE VIEW vw_item_comanda_completo AS
SELECT 
    ic.id_item_comanda,
    ic.id_comanda,
    ic.id_produto,
    ic.quantidade,
    p.preco as preco_unitario,
    (ic.quantidade * p.preco) as subtotal,
    p.nome as produto_nome
FROM item_comanda ic
INNER JOIN produto p ON ic.id_produto = p.id_produto;

-- View: Item Compra com Preço do Produto
CREATE OR REPLACE VIEW vw_item_compra_completo AS
SELECT 
    ic.id_item_compra,
    ic.id_compra,
    ic.id_produto,
    ic.quantidade,
    p.preco as preco_unitario,
    (ic.quantidade * p.preco) as subtotal,
    p.nome as produto_nome
FROM item_compra ic
INNER JOIN produto p ON ic.id_produto = p.id_produto;

-- View: Clientes Públicos (sem dados sensíveis)
CREATE OR REPLACE VIEW vw_clientes_publicos AS
SELECT id_cliente, nome, email, tipo, cpf
FROM cliente;

-- View: Produtos com Estoque
CREATE OR REPLACE VIEW vw_produtos_estoque AS
SELECT p.id_produto, p.nome, p.preco, e.quant_present
FROM produto p
LEFT JOIN estoque e ON e.id_produto = p.id_produto;

-- View: Reservas Detalhadas
CREATE OR REPLACE VIEW vw_reservas_detalhe AS
SELECT r.id_reserva, r.data, r.quant_horas, r.status, r.cpf_cliente, r.id_campo
FROM reserva r;

-- =============================================================================
-- ÍNDICES PARA MELHORAR PERFORMANCE
-- =============================================================================

-- Índices de Cliente
CREATE INDEX IF NOT EXISTS idx_cliente_cpf ON cliente(cpf);
CREATE INDEX IF NOT EXISTS idx_cliente_email ON cliente(email);

-- Índices de Produto
CREATE INDEX IF NOT EXISTS idx_produto_nome ON produto(nome);

-- Índices de Comanda
CREATE INDEX IF NOT EXISTS idx_comanda_cpf_cliente ON comanda(cpf_cliente);
CREATE INDEX IF NOT EXISTS idx_comanda_numero_mesa ON comanda(numero_mesa);
CREATE INDEX IF NOT EXISTS idx_comanda_status ON comanda(status);

-- Índices de Item Comanda
CREATE INDEX IF NOT EXISTS idx_item_comanda_comanda ON item_comanda(id_comanda);
CREATE INDEX IF NOT EXISTS idx_item_comanda_produto ON item_comanda(id_produto);

-- Índices de Reserva
CREATE INDEX IF NOT EXISTS idx_reserva_cpf_cliente ON reserva(cpf_cliente);
CREATE INDEX IF NOT EXISTS idx_reserva_campo ON reserva(id_campo);
CREATE INDEX IF NOT EXISTS idx_reserva_status ON reserva(status);

-- Índices de Compra
CREATE INDEX IF NOT EXISTS idx_compra_cpf_cliente ON compra(cpf_cliente);

-- Índices de Item Compra
CREATE INDEX IF NOT EXISTS idx_item_compra_compra ON item_compra(id_compra);
CREATE INDEX IF NOT EXISTS idx_item_compra_produto ON item_compra(id_produto);

-- Índices de Estoque
CREATE INDEX IF NOT EXISTS idx_estoque_produto ON estoque(id_produto);

-- Índices de Movimentação
CREATE INDEX IF NOT EXISTS idx_movimenta_estoque ON movimenta(id_estoque);

-- Índices de Pagamento
CREATE INDEX IF NOT EXISTS idx_pag_comanda_pagamento ON pag_comanda(id_pagamento);
CREATE INDEX IF NOT EXISTS idx_pag_comanda_comanda ON pag_comanda(id_comanda);
CREATE INDEX IF NOT EXISTS idx_pag_compra_pagamento ON pag_compra(id_pagamento);
CREATE INDEX IF NOT EXISTS idx_pag_compra_compra ON pag_compra(id_compra);
CREATE INDEX IF NOT EXISTS idx_pag_reserva_pagamento ON pag_reserva(id_pagamento);
CREATE INDEX IF NOT EXISTS idx_pag_reserva_reserva ON pag_reserva(id_reserva);

-- =============================================================================
-- DADOS DE EXEMPLO (OPCIONAL)
-- =============================================================================

-- Usuários iniciais da aplicação para autenticação HTTP Basic
INSERT INTO usuario (nome, email, senha, tipo_usuario) 
VALUES ('Administrador', 'admin@pinheiro.com', 'admin123', 'admin')
ON CONFLICT (email) DO UPDATE SET 
    nome = EXCLUDED.nome,
    tipo_usuario = EXCLUDED.tipo_usuario;

INSERT INTO usuario (nome, email, senha, tipo_usuario) 
VALUES ('Funcionário', 'funcionario@pinheiro.com', 'func123', 'funcionario')
ON CONFLICT (email) DO UPDATE SET 
    nome = EXCLUDED.nome,
    tipo_usuario = EXCLUDED.tipo_usuario;

-- Mesas exemplo
INSERT INTO mesa (numero, status) VALUES 
(1, 'disponivel'),
(2, 'disponivel'),
(3, 'disponivel'),
(4, 'disponivel'),
(5, 'disponivel')
ON CONFLICT (numero) DO NOTHING;

-- Campos exemplo
INSERT INTO campo (numero, status) VALUES 
(1, 'disponivel'),
(2, 'disponivel'),
(3, 'disponivel')
ON CONFLICT (numero) DO NOTHING;

-- =============================================================================
-- CONFIRMAÇÃO
-- =============================================================================
SELECT 'Banco de dados arena_pinheiro criado com sucesso!' as status;

-- =============================================================================
-- COMO USAR ESTE SCRIPT
-- =============================================================================
-- 1. Conecte ao PostgreSQL:
--    psql -U postgres
--
-- 2. Crie o banco (se ainda não existe):
--    CREATE DATABASE arena_pinheiro;
--
-- 3. Execute este script:
--    psql -U postgres -d arena_pinheiro -f sql/create_database_complete.sql
--
-- 4. Ou execute linha por linha no psql após conectar ao banco:
--    \c arena_pinheiro
--    \i sql/create_database_complete.sql
-- =============================================================================
