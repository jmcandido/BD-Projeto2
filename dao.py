from db import get_connection
from models import Cliente, Produto

class ClienteDAO:
    def create_cliente(self, cliente: Cliente) -> Cliente:
        conn = get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        # Atualize o INSERT para incluir cpf e vendedor
        sql = ("INSERT INTO cliente (nome, cpf, vendedor, torce_flamengo, assiste_one_piece, e_de_sousa) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (cliente.nome, cliente.cpf, cliente.vendedor,
                             cliente.torce_flamengo, cliente.assiste_one_piece, cliente.e_de_sousa))
        conn.commit()
        cliente.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return cliente


    def get_cliente(self, cliente_id: int) -> Cliente:
        conn = get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        sql = ("SELECT id, nome, cpf, vendedor, torce_flamengo, assiste_one_piece, e_de_sousa "
               "FROM cliente WHERE id = %s")
        cursor.execute(sql, (cliente_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Cliente(
                id=row[0],
                nome=row[1],
                cpf=row[2],
                vendedor=row[3],
                torce_flamengo=row[4],
                assiste_one_piece=row[5],
                e_de_sousa=row[6]
            )
        return None
    
    def get_cliente_by_nome_cpf(self, nome: str, cpf: str) -> Cliente:
        conn = get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        sql = ("SELECT id, nome, cpf, vendedor, torce_flamengo, assiste_one_piece, e_de_sousa "
               "FROM cliente WHERE nome = %s AND cpf = %s")
        cursor.execute(sql, (nome, cpf))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Cliente(
                id=row[0],
                nome=row[1],
                cpf=row[2],
                vendedor=row[3],
                torce_flamengo=row[4],
                assiste_one_piece=row[5],
                e_de_sousa=row[6]
            )
        return None


class ProdutoDAO:
    def create_produto(self, produto: Produto) -> Produto:
        conn = get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        sql = ("INSERT INTO produto (nome, preco, categoria, fabricado_em_mari, estoque) "
               "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(sql, (
            produto.nome, 
            produto.preco, 
            produto.categoria, 
            produto.fabricado_em_mari, 
            produto.estoque
        ))
        conn.commit()
        produto.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return produto

    def update_produto(self, produto: Produto):
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        sql = "UPDATE produto SET estoque = %s WHERE id = %s"
        cursor.execute(sql, (produto.estoque, produto.id))
        conn.commit()
        cursor.close()
        conn.close()

    def search_produtos(self, nome=None, faixa_preco=None, categoria=None, fabricado_em_mari=None, estoque_limite=None):
        conn = get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        sql = ("SELECT id, nome, preco, categoria, fabricado_em_mari, estoque FROM produto WHERE 1=1")
        params = []
        if nome:
            sql += " AND nome LIKE %s"
            params.append('%'+nome+'%')
        if faixa_preco:
            # faixa_preco é uma tupla (min, max)
            sql += " AND preco BETWEEN %s AND %s"
            params.extend(faixa_preco)
        if categoria:
            sql += " AND categoria = %s"
            params.append(categoria)
        if fabricado_em_mari is not None:
            sql += " AND fabricado_em_mari = %s"
            params.append(fabricado_em_mari)
        if estoque_limite is not None:
            sql += " AND estoque < %s"
            params.append(estoque_limite)
        cursor.execute(sql, tuple(params))
        produtos = []
        for row in cursor.fetchall():
            produtos.append(Produto(
                id=row[0],
                nome=row[1],
                preco=row[2],
                categoria=row[3],
                fabricado_em_mari=row[4],
                estoque=row[5]
            ))
        cursor.close()
        conn.close()
        return produtos

class RelatorioDAO:
    def get_vendas_mensais(self):
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            # Supõe que exista uma stored procedure chamada "relatorio_vendas_mensal"
            cursor.callproc('relatorio_vendas_mensal')
            for result in cursor.stored_results():
                rows = result.fetchall()
                print("Relatório de Vendas Mensal:")
                for row in rows:
                    print(row)
        except Exception as e:
            print("Erro ao executar o relatório:", e)
        finally:
            cursor.close()
            conn.close()
