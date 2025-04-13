# main.py
from dao import ClienteDAO, ProdutoDAO
from models import Cliente, Produto, Compra, ItemCompra, Vendedor
from controller import processar_compra

def menu():
    while True:
        print("\n=== Sistema de Vendas ===")
        print("1. Cadastrar Cliente")
        print("2. Consultar Produtos")
        print("3. Fazer Compra")
        print("4. Gerar Relatório de Vendas Mensal")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            consultar_produtos()
        elif opcao == "3":
            fazer_compra()
        elif opcao == "4":
            gerar_relatorio()
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    torce = input("O cliente torce Flamengo? (s/n): ").strip().lower() == 's'
    one_piece = input("O cliente assiste One Piece? (s/n): ").strip().lower() == 's'
    de_sousa = input("O cliente é de Sousa? (s/n): ").strip().lower() == 's'
    
    cliente = Cliente(nome=nome, torce_flamengo=torce, assiste_one_piece=one_piece, e_de_sousa=de_sousa)
    dao = ClienteDAO()
    dao.create_cliente(cliente)
    print(f"Cliente {cliente.nome} cadastrado com sucesso com ID: {cliente.id}")

def consultar_produtos():
    nome = input("Nome do produto (ou pressione Enter para pular): ")
    preco_min = input("Preço mínimo (ou pressione Enter): ")
    preco_max = input("Preço máximo (ou pressione Enter): ")
    categoria = input("Categoria (ou pressione Enter): ")
    fabricado = input("Fabricado em Mari? (s/n ou Enter para qualquer): ").strip().lower()
    
    estoque_limite = None
    func = input("Você é funcionário? (s/n): ").strip().lower()
    if func == 's':
        estoque_limite = 5  # Filtrar produtos com estoque abaixo de 5
    
    faixa_preco = None
    if preco_min and preco_max:
        faixa_preco = (float(preco_min), float(preco_max))
    
    fabricado_em_mari = None
    if fabricado == 's':
        fabricado_em_mari = True
    elif fabricado == 'n':
        fabricado_em_mari = False

    dao = ProdutoDAO()
    produtos = dao.search_produtos(nome if nome else None, faixa_preco, categoria if categoria else None, fabricado_em_mari, estoque_limite)
    
    print("\n=== Produtos Encontrados ===")
    for p in produtos:
        print(f"ID: {p.id} | Nome: {p.nome} | Preço: {p.preco} | Estoque: {p.estoque}")

def fazer_compra():
    try:
        cliente_id = int(input("Digite o ID do cliente: "))
    except ValueError:
        print("ID inválido!")
        return

    from dao import ClienteDAO  # Import local para evitar dependência circular, se necessário
    clienteDAO = ClienteDAO()
    cliente = clienteDAO.get_cliente(cliente_id)
    if not cliente:
        print("Cliente não encontrado!")
        return

    # Para este exemplo, simulamos um vendedor fixo
    vendedor = Vendedor(id=1, nome="Vendedor 1")
    compra = Compra(cliente=cliente, vendedor=vendedor, forma_pagamento="Cartão")
    
    try:
        num_itens = int(input("Quantos produtos deseja comprar? "))
    except ValueError:
        print("Número inválido!")
        return

    produtoDAO = ProdutoDAO()
    for i in range(num_itens):
        try:
            produto_id = int(input("Digite o ID do produto: "))
            quantidade = int(input("Digite a quantidade: "))
        except ValueError:
            print("Entrada inválida, abortando a compra.")
            return

        # Buscar o produto pelo ID (aqui, uma busca simples; você pode criar um método específico)
        produtos = produtoDAO.search_produtos()
        produto_selecionado = next((p for p in produtos if p.id == produto_id), None)
        if not produto_selecionado:
            print("Produto não encontrado!")
            return
        item = ItemCompra(produto=produto_selecionado, quantidade=quantidade)
        compra.itens.append(item)
    
    if processar_compra(compra):
        print("Compra processada com sucesso!")
    else:
        print("Erro ao processar a compra.")

def gerar_relatorio():
    from dao import RelatorioDAO
    relatorio = RelatorioDAO()
    relatorio.get_vendas_mensais()

if __name__ == "__main__":
    menu()
