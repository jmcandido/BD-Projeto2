from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, CheckConstraint, Index, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# ========================================
# Configuração do Banco de Dados
# ========================================
engine = create_engine('mysql+mysqlconnector://root@localhost/sales_db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# ========================================
# Modelo Cliente
# ========================================
class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(20), nullable=False)            # Novo: CPF para login (senha)
    vendedor = Column(Boolean, nullable=False, default=False)  # Novo: Indica se é vendedor
    torce_flamengo = Column(Boolean, nullable=False, default=False)
    assiste_one_piece = Column(Boolean, nullable=False, default=False)
    e_de_sousa = Column(Boolean, nullable=False, default=False)
    email = Column(String(255))
    telefone = Column(String(50))
    
    compras = relationship('Compra', back_populates='cliente')

# ========================================
# Modelo Produto
# ========================================
class Produto(Base):
    __tablename__ = 'produto'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    preco = Column(Numeric(10,2), nullable=False)
    categoria = Column(String(100))
    fabricado_em_mari = Column(Boolean, nullable=False, default=False)
    estoque = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint('estoque >= 0', name='chk_estoque'),
        Index('idx_produto_nome', 'nome'),
        Index('idx_produto_categoria', 'categoria'),
        Index('idx_produto_fabricado', 'fabricado_em_mari')
    )
    
    itens_compra = relationship('ItemCompra', back_populates='produto')

# ========================================
# Modelo Vendedor
# ========================================
class Vendedor(Base):
    __tablename__ = 'vendedor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    
    vendas = relationship('Compra', back_populates='vendedor')

# ========================================
# Modelo Compra
# ========================================
class Compra(Base):
    __tablename__ = 'compra'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id', ondelete='CASCADE'), nullable=False)
    vendedor_id = Column(Integer, ForeignKey('vendedor.id', ondelete='CASCADE'), nullable=False)
    data_compra = Column(DateTime, nullable=False, server_default=func.now())
    forma_pagamento = Column(String(50), nullable=False)
    status_pagamento = Column(String(50), nullable=False, default='Pendente')
    total = Column(Numeric(10,2), nullable=False, default=0)
    
    cliente = relationship('Cliente', back_populates='compras')
    vendedor = relationship('Vendedor', back_populates='vendas')
    itens = relationship('ItemCompra', back_populates='compra')

# ========================================
# Modelo ItemCompra
# ========================================
class ItemCompra(Base):
    __tablename__ = 'item_compra'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    compra_id = Column(Integer, ForeignKey('compra.id', ondelete='CASCADE'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id', ondelete='RESTRICT'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10,2), nullable=False)
    
    compra = relationship('Compra', back_populates='itens')
    produto = relationship('Produto', back_populates='itens_compra')

# ========================================
# Criação das Views e Procedures
# ========================================
def create_database_objects():
    # Criação da View
    view_sql = """
    CREATE OR REPLACE VIEW vw_vendas_vendedor AS 
    SELECT 
        v.nome AS vendedor,
        MONTH(c.data_compra) AS mes,
        SUM(c.total) AS total_vendas
    FROM compra c
    JOIN vendedor v ON c.vendedor_id = v.id
    GROUP BY v.nome, mes;
    """
    
    # Criação da Stored Procedure
    procedure_sql = """
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
    END
    """
    
    try:
        # Executa os comandos SQL diretamente
        with engine.connect() as conn:
            conn.execute(text(view_sql))
            conn.execute(text("DROP PROCEDURE IF EXISTS relatorio_vendas_mensal"))
            conn.execute(text(procedure_sql))
        print("Objetos de banco criados com sucesso!")
    except Exception as e:
        print(f"Erro ao criar objetos: {e}")

# ========================================
# Execução Inicial
# ========================================
if __name__ == '__main__':
    # Cria todas as tabelas
    Base.metadata.create_all(engine)
    
    # Cria views e procedures
    create_database_objects()
