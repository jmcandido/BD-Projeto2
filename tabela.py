-- Crie o banco de dados e selecione-o (caso ainda não exista)
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

-- ========================================
-- Tabela Cliente
-- ========================================
CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    torce_flamengo BOOLEAN NOT NULL DEFAULT FALSE,
    assiste_one_piece BOOLEAN NOT NULL DEFAULT FALSE,
    e_de_sousa BOOLEAN NOT NULL DEFAULT FALSE,
    email VARCHAR(255),
    telefone VARCHAR(50)
) ENGINE=InnoDB;

-- ========================================
-- Tabela Produto
-- ========================================
CREATE TABLE IF NOT EXISTS produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(100),
    fabricado_em_mari BOOLEAN NOT NULL DEFAULT FALSE,
    estoque INT NOT NULL,
    CONSTRAINT chk_estoque CHECK (estoque >= 0)
) ENGINE=InnoDB;

-- Índices para facilitar buscas por nome e categoria
CREATE INDEX idx_produto_nome ON produto(nome);
CREATE INDEX idx_produto_categoria ON produto(categoria);
CREATE INDEX idx_produto_fabricado ON produto(fabricado_em_mari);

-- ========================================
-- Tabela Vendedor
-- ========================================
CREATE TABLE IF NOT EXISTS vendedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- ========================================
-- Tabela Compra
-- ========================================
CREATE TABLE IF NOT EXISTS compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    vendedor_id INT NOT NULL,
    data_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    forma_pagamento VARCHAR(50) NOT NULL,
    status_pagamento VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE CASCADE,
    FOREIGN KEY (vendedor_id) REFERENCES vendedor(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ========================================
-- Tabela Item da Compra
-- ========================================
CREATE TABLE IF NOT EXISTS item_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compra(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produto(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ========================================
-- View para Vendas por Vendedor (Mensal)
-- ========================================
DROP VIEW IF EXISTS vw_vendas_vendedor;
CREATE VIEW vw_vendas_vendedor AS 
SELECT 
    v.nome AS vendedor,
    MONTH(c.data_compra) AS mes,
    SUM(c.total) AS total_vendas
FROM compra c
JOIN vendedor v ON c.vendedor_id = v.id
GROUP BY v.nome, mes;

-- ========================================
-- Stored Procedure para Relatório Mensal de Vendas
-- ========================================
DELIMITER //

DROP PROCEDURE IF EXISTS relatorio_vendas_mensal;
CREATE PROCEDURE relatorio_vendas_mensal()
BEGIN
    SELECT 
        v.nome AS vendedor,
        MONTH(c.data_compra) AS mes,
        SUM(c.total) AS total_vendas
    FROM compra c 
    JOIN vendedor v ON c.vendedor_id = v.id
    WHERE MONTH(c.data_compra) = MONTH(CURRENT_DATE())
    GROUP BY v.nome;
END //

DELIMITER ;
