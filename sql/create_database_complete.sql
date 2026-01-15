CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    cpf VARCHAR(11) UNIQUE,
    nome VARCHAR(100),
    email VARCHAR(100),
    tipo VARCHAR(50),
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    preco NUMERIC(10, 2),
    validade DATE,
    quant_min_estoque INTEGER,
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS estoque (
    id_estoque SERIAL PRIMARY KEY,
    id_produto INTEGER UNIQUE REFERENCES produto(id_produto) ON DELETE CASCADE,
    quant_present INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS movimenta (
    id_movimenta SERIAL PRIMARY KEY,
    id_estoque INTEGER REFERENCES estoque(id_estoque) ON DELETE CASCADE,
    tipo VARCHAR(50), 
    quantidade INTEGER,
    data DATE
);

CREATE TABLE IF NOT EXISTS mesa (
    id_mesa SERIAL PRIMARY KEY,
    numero INTEGER UNIQUE NOT NULL,
    status VARCHAR(50) 
);

CREATE TABLE IF NOT EXISTS comanda (
    id_comanda SERIAL PRIMARY KEY,
    data DATE,
    status VARCHAR(50), 
    numero_mesa INTEGER REFERENCES mesa(numero) ON DELETE SET NULL,
    cpf_cliente VARCHAR(11) REFERENCES cliente(cpf) ON DELETE SET NULL,
    id_usuario_responsavel INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS item_comanda (
    id_item_comanda SERIAL PRIMARY KEY,
    id_comanda INTEGER REFERENCES comanda(id_comanda) ON DELETE CASCADE,
    id_produto INTEGER REFERENCES produto(id_produto) ON DELETE SET NULL,
    quantidade INTEGER
);

CREATE TABLE IF NOT EXISTS campo (
    id_campo SERIAL PRIMARY KEY,
    numero INTEGER UNIQUE,
    status VARCHAR(50) 
);

CREATE TABLE IF NOT EXISTS reserva (
    id_reserva SERIAL PRIMARY KEY,
    data DATE,
    quant_horas INTEGER,
    status VARCHAR(50), 
    cpf_cliente VARCHAR(11) REFERENCES cliente(cpf) ON DELETE SET NULL,
    id_campo INTEGER REFERENCES campo(id_campo) ON DELETE SET NULL,
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS compra (
    id_compra SERIAL PRIMARY KEY,
    data DATE,
    valor_total NUMERIC(10, 2),
    cpf_cliente VARCHAR(11) REFERENCES cliente(cpf) ON DELETE SET NULL,
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS item_compra (
    id_item_compra SERIAL PRIMARY KEY,
    id_compra INTEGER REFERENCES compra(id_compra) ON DELETE CASCADE,
    id_produto INTEGER REFERENCES produto(id_produto) ON DELETE SET NULL,
    quantidade INTEGER
);

CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    valor NUMERIC(10, 2),
    forma VARCHAR(50), 
    tipo_pagamento VARCHAR(50), 
    id_usuario_cadastrou INTEGER REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS pag_comanda (
    id_pag_comanda SERIAL PRIMARY KEY,
    id_pagamento INTEGER NOT NULL REFERENCES pagamento(id_pagamento) ON DELETE CASCADE,
    id_comanda INTEGER NOT NULL REFERENCES comanda(id_comanda) ON DELETE CASCADE,
    UNIQUE(id_pagamento, id_comanda)
);

CREATE TABLE IF NOT EXISTS pag_compra (
    id_pag_compra SERIAL PRIMARY KEY,
    id_pagamento INTEGER NOT NULL REFERENCES pagamento(id_pagamento) ON DELETE CASCADE,
    id_compra INTEGER NOT NULL REFERENCES compra(id_compra) ON DELETE CASCADE,
    UNIQUE(id_pagamento, id_compra)
);

CREATE TABLE IF NOT EXISTS pag_reserva (
    id_pag_reserva SERIAL PRIMARY KEY,
    id_pagamento INTEGER NOT NULL REFERENCES pagamento(id_pagamento) ON DELETE CASCADE,
    id_reserva INTEGER NOT NULL REFERENCES reserva(id_reserva) ON DELETE CASCADE,
    porcentagem NUMERIC(5, 2), 
    UNIQUE(id_pagamento, id_reserva)
);

CREATE OR REPLACE VIEW vw_item_comanda_completo AS
SELECT
    ic.id_item_comanda,
    ic.id_comanda,
    ic.id_produto,
    ic.quantidade,
    COALESCE(p.preco, 0) AS preco_unitario,
    (COALESCE(ic.quantidade, 0) * COALESCE(p.preco, 0)) AS subtotal,
    COALESCE(p.nome, 'Desconhecido') AS produto_nome
FROM item_comanda ic
LEFT JOIN produto p ON ic.id_produto = p.id_produto;

CREATE OR REPLACE VIEW vw_item_compra_completo AS
SELECT
    ic.id_item_compra,
    ic.id_compra,
    ic.id_produto,
    ic.quantidade,
    COALESCE(p.preco, 0) AS preco_unitario,
    (COALESCE(ic.quantidade, 0) * COALESCE(p.preco, 0)) AS subtotal,
    COALESCE(p.nome, 'Desconhecido') AS produto_nome
FROM item_compra ic
LEFT JOIN produto p ON ic.id_produto = p.id_produto;

CREATE OR REPLACE VIEW vw_produtos_estoque AS
SELECT p.id_produto, p.nome, p.preco, COALESCE(e.quant_present, 0) AS quant_present
FROM produto p
LEFT JOIN estoque e ON e.id_produto = p.id_produto;

CREATE OR REPLACE VIEW vw_reservas_detalhe AS
SELECT
    r.id_reserva,
    r.data,
    r.quant_horas,
    r.status,
    r.cpf_cliente,
    c.nome AS cliente_nome,
    c.email AS cliente_email,
    r.id_campo,
    f.numero AS campo_numero,
    f.status AS campo_status,
    r.id_usuario_cadastrou,
    u.nome AS usuario_cadastrou
FROM reserva r
LEFT JOIN cliente c ON r.cpf_cliente = c.cpf
LEFT JOIN campo f ON r.id_campo = f.id_campo
LEFT JOIN usuario u ON r.id_usuario_cadastrou = u.id_usuario;

CREATE INDEX IF NOT EXISTS idx_cliente_cpf ON cliente(cpf);
CREATE INDEX IF NOT EXISTS idx_cliente_email ON cliente(email);

CREATE INDEX IF NOT EXISTS idx_produto_nome ON produto(nome);

CREATE INDEX IF NOT EXISTS idx_comanda_cpf_cliente ON comanda(cpf_cliente);
CREATE INDEX IF NOT EXISTS idx_comanda_numero_mesa ON comanda(numero_mesa);
CREATE INDEX IF NOT EXISTS idx_comanda_status ON comanda(status);

CREATE INDEX IF NOT EXISTS idx_item_comanda_comanda ON item_comanda(id_comanda);
CREATE INDEX IF NOT EXISTS idx_item_comanda_produto ON item_comanda(id_produto);

CREATE INDEX IF NOT EXISTS idx_reserva_cpf_cliente ON reserva(cpf_cliente);
CREATE INDEX IF NOT EXISTS idx_reserva_campo ON reserva(id_campo);
CREATE INDEX IF NOT EXISTS idx_reserva_status ON reserva(status);

CREATE INDEX IF NOT EXISTS idx_compra_cpf_cliente ON compra(cpf_cliente);

CREATE INDEX IF NOT EXISTS idx_item_compra_compra ON item_compra(id_compra);
CREATE INDEX IF NOT EXISTS idx_item_compra_produto ON item_compra(id_produto);

CREATE INDEX IF NOT EXISTS idx_estoque_produto ON estoque(id_produto);

CREATE INDEX IF NOT EXISTS idx_movimenta_estoque ON movimenta(id_estoque);

CREATE INDEX IF NOT EXISTS idx_pag_comanda_pagamento ON pag_comanda(id_pagamento);
CREATE INDEX IF NOT EXISTS idx_pag_comanda_comanda ON pag_comanda(id_comanda);
CREATE INDEX IF NOT EXISTS idx_pag_compra_pagamento ON pag_compra(id_pagamento);
CREATE INDEX IF NOT EXISTS idx_pag_compra_compra ON pag_compra(id_compra);
CREATE INDEX IF NOT EXISTS idx_pag_reserva_pagamento ON pag_reserva(id_pagamento);
CREATE INDEX IF NOT EXISTS idx_pag_reserva_reserva ON pag_reserva(id_reserva);

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

INSERT INTO mesa (numero, status) VALUES 
(1, 'disponivel'),
(2, 'disponivel'),
(3, 'disponivel'),
(4, 'disponivel'),
(5, 'disponivel')
ON CONFLICT (numero) DO NOTHING;

INSERT INTO campo (numero, status) VALUES 
(1, 'disponivel'),
(2, 'disponivel'),
(3, 'disponivel')
ON CONFLICT (numero) DO NOTHING;

SELECT 'Banco de dados arena_pinheiro criado com sucesso!' as status;