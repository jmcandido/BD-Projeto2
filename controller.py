# controller.py
from dao import ProdutoDAO
from models import Compra

def processar_compra(compra: Compra) -> bool:
    produtoDAO = ProdutoDAO()
    # Verificar se há estoque suficiente para cada item da compra
    for item in compra.itens:
        # Buscar o produto pelo nome (ou de outra forma)
        produtos = produtoDAO.search_produtos(nome=item.produto.nome)
        if not produtos:
            print(f"Produto {item.produto.nome} não encontrado!")
            return False
        produto_in_db = produtos[0]
        if produto_in_db.estoque < item.quantidade:
            print(f"Estoque insuficiente para o produto {produto_in_db.nome} (Disponível: {produto_in_db.estoque})")
            return False
        # Deduzir a quantidade do estoque
        produto_in_db.estoque -= item.quantidade
        produtoDAO.update_produto(produto_in_db)
    
    # Processar pagamento e aplicar desconto se o cliente for elegível
    desconto = 0.0
    if (compra.cliente.torce_flamengo or 
        compra.cliente.assiste_one_piece or 
        compra.cliente.e_de_sousa):
        desconto = 0.1  # Exemplo: 10% de desconto
    
    total = sum(item.produto.preco * item.quantidade for item in compra.itens)
    total_com_desconto = total * (1 - desconto)
    
    print(f"Total da compra: R$ {total:.2f}")
    if desconto > 0:
        print(f"Desconto aplicado: {desconto*100:.0f}%")
        print(f"Total com desconto: R$ {total_com_desconto:.2f}")
    else:
        print("Nenhum desconto aplicado.")
    
    # Aqui, insira a lógica para gravar a compra no banco de dados.
    # Exemplo: inserir registro na tabela 'compra' e 'itens_compra'.
    
    return True

