from datetime import datetime
from tabulate import tabulate

from repository import (
    criar_fornecedor,
    listar_fornecedores,
    buscar_fornecedor,
    atualizar_fornecedor,
    excluir_fornecedor,
    adicionar_produto,
    ler_codigo_id_base,
    salvar_codigo_id_base,
    listar_produtos_fornecedor,
    listar_produtos,
    buscar_produto,
    atualizar_produto,
    excluir_produto,
    listar_entradas,
    adicionar_estoque,
    produto_existe,
    obter_quantidade_estoque,
    ler_estoque,
    remover_estoque,   
    registrar_saida,
    listar_saida,
)

from cliente_controller import buscar_cliente
# Funções de controle do Fornecedor

#Função geral para mensagem do fornecedor
def solicitar_cnpj(mensagem="\nInforme o CNPJ do fornecedor: "):
    return input(mensagem)

# Create
def cadastrar_fornecedor():
    print("\nCadastro de Fornecedor")
    cnpj = input("CNPJ: ")
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    
    # Chama a função do repositório para criar o fornecedor
    sucesso, mensagem = criar_fornecedor(cnpj, nome, telefone, email)
    if sucesso:
        print(mensagem)
    else:
        print("Erro:", mensagem)

# Read fornecedor
def lista_de_fornecedores_controller():
    fornecedores = listar_fornecedores()
    if fornecedores:
        print("\nLista de Fornecedores:")
        headers = ["CNPJ", "Nome", "Telefone", "Email", "Data de Cadastro"]
        dados_fornecedores = []
        #Trazer os dados do fornecedor dentro da tabela
        for fornecedor in fornecedores:
            dados_fornecedores.append([
                fornecedor.get('cnpj', ''),
                fornecedor.get('nome', ''),
                fornecedor.get('telefone', ''),
                fornecedor.get('email', ''),
                fornecedor.get('Data de Cadastro', '')
            ])
        print(tabulate(dados_fornecedores, headers=headers, tablefmt="grid"))
    else:
        print("\nNenhum fornecedor cadastrado.")


# Buscar fornecedor por cnpj

# Função para buscar fornecedor por CNPJ
def pesquisar_dados_fornecedor():
    id_fornecedor = solicitar_cnpj()
    fornecedor = buscar_fornecedor(id_fornecedor)
    if fornecedor:
        print("\nInformações do Fornecedor:")
        exibir_resultados_busca([fornecedor])
    else:
        print("Fornecedor não encontrado.")

# Função para exibir os resultados da busca por CNPJ na tabela
def exibir_resultados_busca(resultados):
    if resultados:
        headers = list(resultados[0].keys())
        table_data = []
        for fornecedor in resultados:
            data = fornecedor.copy()
            # Remova a chave 'produtos' e obtenha sua lista de valores
            produtos = data.pop('produtos', [])
            # Adicione uma linha apenas com as informações do fornecedor
            table_data.append(list(data.values()))
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    else:
        print("Nenhum fornecedor encontrado.")



# Update fornecedor
def atualizar_dados_fornecedor():
    id_fornecedor = solicitar_cnpj()
    fornecedor_atual = buscar_fornecedor(id_fornecedor)
    
    if fornecedor_atual:
        print("Fornecedor encontrado.\nDigite os novos dados (deixe em branco para manter os dados atuais):")
        
        nome_novo = input(f"Nome ({fornecedor_atual['nome']}): ").strip() or fornecedor_atual['nome']
        telefone_novo = input(f"Telefone ({fornecedor_atual['telefone']}): ").strip() or fornecedor_atual['telefone']
        email_novo = input(f"Email ({fornecedor_atual['email']}): ").strip() or fornecedor_atual['email']

        novos_dados = {}

        # Verificar se os novos dados foram fornecidos e, se não, manter os dados atuais
        if nome_novo != fornecedor_atual['nome']:
            novos_dados['nome'] = nome_novo
        if telefone_novo != fornecedor_atual['telefone']:
            novos_dados['telefone'] = telefone_novo
        if email_novo != fornecedor_atual['email']:
            novos_dados['email'] = email_novo

        # Exibir mensagem de confirmação
        confirmacao = input("\nDeseja salvar as alterações? (sim/não): ").lower()    
        if confirmacao == 'sim':
            if novos_dados:
                # Atualiza os dados do fornecedor apenas se houver alterações
                if atualizar_fornecedor(id_fornecedor, novos_dados):
                    print("\nDados do fornecedor atualizados com sucesso.")
                else:
                    print("\nErro ao atualizar os dados do fornecedor.")
            else:
                print("\nNenhum dado foi alterado.")
        else:
            print("\nOperação de atualização cancelada.")
    else:
        print("\nFornecedor não encontrado.")


# Delete
def deletar_fornecedor():
    id_fornecedor = solicitar_cnpj()
    if buscar_fornecedor(id_fornecedor):
        escolha = input("Deseja mesmo excluir o fornecedor? (sim/não): ").lower()
        if escolha == "sim":
            excluir_fornecedor(id_fornecedor)
            print("Fornecedor excluído com sucesso.")
        else:
            print("Operação cancelada.")
    else:
        print("Fornecedor não encontrado.")


#  Produtos 

#Função geral para mensagem do produto
def solicitar_id(mensagem="\nInforme o código do produto: "):
    return input(mensagem)

# Create produto
def adicionar_produto_fornecedor():
    codigo_id_base = ler_codigo_id_base()
    id_fornecedor = solicitar_cnpj()
    
    if buscar_fornecedor(id_fornecedor):
        nome_produto = input("Digite o nome do produto: ")
        descricao_produto = input("Digite a descrição do produto: ")
        preco_aquisicao = float(input("Digite o preço de aquisição do produto: "))
        
        # Incrementa o código base para o próximo ID de produto
        novo_codigo_id = codigo_id_base + 1
        salvar_codigo_id_base(novo_codigo_id)
        
        # Tenta adicionar o produto
        resultado = adicionar_produto(
            id_fornecedor,
            novo_codigo_id,
            nome_produto,
            descricao_produto,
            preco_aquisicao,
        )
        
        if resultado:
            print("Produto cadastrado com sucesso!")
            
            # Após cadastrar o produto com sucesso, adiciona ao estoque
            qtd_produto = int(input("Digite a quantidade do produto a ser adicionada ao estoque: "))
            resultado_estoque = adicionar_estoque(novo_codigo_id, qtd_produto)
            
            if resultado_estoque:
                print("Produto adicionado ao estoque.")
            else:
                print("Erro ao adicionar o produto ao estoque.")
        else:
            print("Erro ao cadastrar o produto.")
    else:
        print("Fornecedor não encontrado.")



# Read
def lista_produtos_fornecedor():
    id_fornecedor = solicitar_cnpj()
    if buscar_fornecedor(id_fornecedor):
        produtos = listar_produtos_fornecedor(id_fornecedor)
        print("\nDados do produto")

        if produtos:  # Verifica se há produtos cadastrados
            headers = produtos[0].keys()  # Obtém os cabeçalhos da tabela
            table_data = [[produto[header] for header in headers] for produto in produtos]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("O fornecedor não possui produtos cadastrados.")
    else:
        print("Fornecedor não encontrado.")


#listar produto cadastrado
def lista_produtos():
    listar_produtos()
    

#Pesquisar produto
def pesquisar_produto():
    id_produto = solicitar_id()
    produto = buscar_produto(id_produto)
    if produto:
        fornecedor, nome, descricao, preco_aquisicao = produto
        dados_produto = [{"Fornecedor": fornecedor, "Produto": nome, "Descrição": descricao, "Preço": preco_aquisicao}]
        print(tabulate(dados_produto, headers="keys", tablefmt="grid"))
    else:
        print("Produto não encontrado.")



# Update dos dados do produto
def atualizar_dados_produto():
    id_produto = solicitar_id()
    produto = buscar_produto(id_produto)
    if produto:
        fornecedor, nome, descricao, preco_aquisicao = produto
        print("Produto encontrado. \nDigite os novos dados (deixe em branco para manter os dados atuais):")
        novo_nome = input(f"Nome ({nome}): ").strip() or nome
        nova_descricao = input(f"Descrição ({descricao}): ").strip() or descricao
        novo_preco = input(f"Preço ({preco_aquisicao:.2f}): ").strip() or str(preco_aquisicao)

        novos_dados = {}

        # Verificar se os novos dados foram fornecidos e, se não, manter os dados atuais
        if novo_nome:
            novos_dados['nome'] = novo_nome
        if nova_descricao:
            novos_dados['descricao'] = nova_descricao
        if novo_preco:
            novos_dados['preco_aquisicao'] = float(novo_preco)

        # Exibir mensagem de confirmação
        confirmacao = input("Deseja salvar as alterações? (sim/não): ").lower()
        if confirmacao == 'sim':
            # Atualiza os dados do produto
            if atualizar_produto(id_produto, novos_dados):
                print("\nDados do produto atualizados com sucesso.")
            else:
                print("\nErro ao atualizar os dados do produto.")
        else:
            print("\nOperação de atualização cancelada.")
    else:
        print("Produto não encontrado.")

# Delete
def deletar_produto():
    id_produto = solicitar_id()
    if buscar_produto(id_produto):
        escolha = input("Deseja mesmo excluir o produto? (sim/não):").lower()
        if escolha == "sim":
            excluir_produto(id_produto)
            print("Produto excluído com sucesso.")
        else:
            print("Operação cancelada.")
    else:
        print("Produto não encontrado.")
        
 #entrada de produto no estoque        
def entrada_produto():
    valor = solicitar_id()
    if buscar_produto(id_produto=valor):
        entrada_unidade = int(input("Quantas unidades gostaria de adicionar: "))
        adicionar_estoque(id_produto=valor, qtd_produto=entrada_unidade)
        print("\nQuantidade adcionada no estoque")
        cadastrar_opcao = input("Deseja dar entrada em mais produtos? (sim/não): ").lower()
        if cadastrar_opcao == "sim":
            entrada_produto()
        else:
            print('Retornando ao menu anterior...')
    else:
        print('Produto não encontrado')
        cadastrar_produto = input("Deseja cadastrar um novo produto? (sim/não): ").lower()
        if cadastrar_produto == "sim":
            adicionar_produto_fornecedor()
        else:
            print('Retornando ao menu anterior...')


#alerta pra baixo estoque
def alertar_baixo_estoque():
    limiar = 10  # limiar de estoque baixo 
    estoque = ler_estoque()
    produtos_baixo_estoque = [item for item in estoque if item["qtd"] <= limiar]
    if produtos_baixo_estoque:
        dados_tabela = [(produto['id'], produto['qtd']) for produto in produtos_baixo_estoque]
        print("\nOs seguintes produtos estão com estoque baixo do limite de 10 unidades:")
        print(tabulate(dados_tabela, headers=["ID do Produto", "Quantidade em Estoque"], tablefmt="grid"))
    else:
        print("Todos os produtos estão com estoque suficiente.")

#alerta de alto estoque
def alertar_alto_estoque():
    limite = 11  # limite de estoque alto 
    estoque = ler_estoque()
    produtos_alto_estoque = [item for item in estoque if item["qtd"] >= limite]
    if produtos_alto_estoque:
        dados_tabela = [(produto['id'], produto['qtd']) for produto in produtos_alto_estoque]
        print("\nOs seguintes produtos estão com estoque acima do limite de 10 unidades:")
        print(tabulate(dados_tabela, headers=["ID do Produto", "Quantidade em Estoque"], tablefmt="grid"))
    else:
        print("Não há produtos com estoque acima de 10 unidades.")

       
    
 # Exibir Lista geral de produto    
def exibir_entradas():
    listar_entradas()



#Saida de produto do estoque
def saida_produto():
    valor = solicitar_id()
    if produto_existe(valor):
        qtd_atual = obter_quantidade_estoque(valor)
        if qtd_atual > 0:
            saida_unidade = int(input(f"Quantas unidades de {valor} gostaria de remover: "))
            if saida_unidade <= qtd_atual:
                remover_estoque(id_produto=valor, qtd_produto=saida_unidade)
                data_saida = datetime.now()
                registrar_saida(id_produto=valor, quantidade=saida_unidade, data=data_saida)
                print(f"{saida_unidade} unidades do produto com ID: {valor} foram removidas do estoque.")
            else:
                print("Quantidade solicitada excede o estoque disponível.")
        else:
            print("Este produto está fora de estoque.")
    else:
        print('Produto não encontrado')

# Função para exibir os dados de saída do produto
def exibir_saida_terminal():
    dados_saida = listar_saida()
    if isinstance(dados_saida, str):
        print(dados_saida)  # Se não houver saídas registradas, imprime a mensagem
    else:
        print(tabulate(dados_saida, headers="keys", tablefmt="grid"))



