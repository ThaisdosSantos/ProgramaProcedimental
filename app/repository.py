import json
from tabulate import tabulate
from datetime import datetime
from cliente_repository import validar_email

FORNECEDORES_JSON = "arquivos/fornecedores.json"
PRODUTOS_JSON = "arquivos/produtos.json"
CODIGO_ID_BASE = "arquivos/codigo_id_base.json"
ESTOQUE_JSON = "arquivos/estoque.json"
SAIDA_JSON = "arquivos/saida.json"



# Fornecedor é um dicionário com as chaves nome, telefone e email
# Leitura do arquivo JSON
def ler_fornecedores():
    try:
        with open(FORNECEDORES_JSON, "r") as file:
            fornecedores = json.load(file)
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        fornecedores = []
    return fornecedores


# Escrita no arquivo JSON
def salvar_fornecedores(fornecedores):
    with open(FORNECEDORES_JSON, "w") as file:
        json.dump(fornecedores, file, indent=4)
        
def ler_estoque():
    try:
        with open(ESTOQUE_JSON, "r") as file:
            estoque = json.load(file)
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        estoque = []
    return [item for item in estoque if "id" in item]

               
        # Escrita no arquivo JSON
def salvar_estoque(EstoqueProdutos):
    with open(ESTOQUE_JSON, "w") as file:
        json.dump(EstoqueProdutos, file, indent=4)


# Create
def criar_fornecedor(cnpj, nome, telefone, email):
    # Validação dos campos obrigatórios
    if cnpj and nome and telefone and email:
        # Verificar se já existe um fornecedor com o mesmo CNPJ
        fornecedores = ler_fornecedores()
        if any(fornecedor['cnpj'] == cnpj for fornecedor in fornecedores):
            return False, "O CNPJ fornecido já está cadastrado."
        else:
            # Validar o formato do e-mail
            if not validar_email(email):
                return False, "Formato de e-mail inválido."
            
            # Registro da data e hora do cadastro
            data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fornecedor = {
                'cnpj': cnpj,
                'nome': nome,
                'telefone': telefone,
                'email': email,
                'Data de Cadastro': data_cadastro
            }
            fornecedores.append(fornecedor)
            salvar_fornecedores(fornecedores)
            return True, "Fornecedor cadastrado com sucesso!"
    else:
        return False, "Todos os campos são obrigatórios."
    
# Read fornecedor
def listar_fornecedores():
    fornecedores = ler_fornecedores()
    return fornecedores
    

#buscar fornecedor por cnpj
def buscar_fornecedor(id_fornecedor):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if fornecedor["cnpj"] == id_fornecedor:
            return fornecedor
    return None

def fornecedor_existe(id_fornecedor):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if fornecedor["nome"] == id_fornecedor or fornecedor["cnpj"] == id_fornecedor:
            return True
    return False


# Update fornecedor
def atualizar_fornecedor(id_fornecedor, novos_dados):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if fornecedor["cnpj"] == id_fornecedor:
            fornecedor.update(novos_dados)
            salvar_fornecedores(fornecedores)
            return True
    return False


# Create adcionar produto ao estoque
def adicionar_estoque(id_produto, qtd_produto):
    estoque = ler_estoque()
    produto_encontrado = False
    
    for item in estoque:
        if item["id"] == id_produto:
            item["qtd"] += qtd_produto
            produto_encontrado = True
            break
    
    if not produto_encontrado:
        # Se o produto não estiver presente no estoque, adiciona-o ao estoque com a quantidade especificada
        novo_produto = {"id": id_produto, "qtd": qtd_produto}
        estoque.append(novo_produto)
    
    salvar_estoque(estoque)
    return True

# Read
def listar_entradas():
    entradaProdutos = ler_estoque()
    if not entradaProdutos or len(entradaProdutos) == 0:
        print("Nenhuma entrada de produto registrada.")
    else:
        # Lista de dicionários contendo as informações das entradas de produtos
        dados_entradas = []
        for estoque in entradaProdutos:
            if 'id' in estoque:
                # Adiciona as informações da entrada de produto à lista de dicionários
                dados_entradas.append({"ID": estoque['id'], "Quantidade em estoque": estoque.get('qtd', 'N/A')})
        
        # Imprime a tabela formatada usando tabulate
        print(tabulate(dados_entradas, headers="keys", tablefmt="grid"))


# Delete
def excluir_fornecedor(id_fornecedor):
    fornecedores = ler_fornecedores()
    fornecedores = [
        fornecedor
        for fornecedor in fornecedores
        if fornecedor["cnpj"] != id_fornecedor
    ]
    salvar_fornecedores(fornecedores)


# Funções para leitura e escrita do código base para os produtos
def ler_codigo_id_base():
    try:
        with open(CODIGO_ID_BASE, "r") as file:
            data = json.load(file)
            return data["codigo_id_base"]
    except FileNotFoundError:
        return 100000


def salvar_codigo_id_base(codigo_id_base):
    with open(CODIGO_ID_BASE, "w") as file:
        json.dump({"codigo_id_base": codigo_id_base}, file)


# Produto é um dicionário com as chaves codigo_id, nome, descricao e preco_aquisicao
# Create
def adicionar_produto(cnpj_fornecedor, codigo_id, nome, descricao, preco_aquisicao):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if fornecedor["cnpj"] == cnpj_fornecedor:
            if "produtos" not in fornecedor:
                fornecedor["produtos"] = []
            produto = {
                "codigo_id": codigo_id,
                "nome": nome,
                "descricao": descricao,
                "preco_aquisicao": preco_aquisicao,
            }
            fornecedor["produtos"].append(produto)
            salvar_fornecedores(fornecedores)
            return True  # Indica que o produto foi adicionado com sucesso
    return False  # Indica que o fornecedor não foi encontrado

            
# Adicionando ID do pruduto no estoque            
    estoqueAdd = {"id": codigo_id, "qtd": 0 }
    estoque = ler_estoque()
    estoque.append(estoqueAdd)
    salvar_estoque(estoque)


# Read
def listar_produtos_fornecedor(cnpj_fornecedor):
    produtos_encontrados = []  # Inicializa uma lista para armazenar os produtos encontrados
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if fornecedor["cnpj"] == cnpj_fornecedor and "produtos" in fornecedor:
            for produto in fornecedor["produtos"]:
                # Adiciona os dados do produto à lista de produtos encontrados
                produtos_encontrados.append({
                    "Codigo_id": produto["codigo_id"],
                    "Nome": produto["nome"],
                    "Descrição": produto["descricao"],
                    "Preço R$": produto["preco_aquisicao"]
                })
            return produtos_encontrados  # Retorna a lista de produtos encontrados
    return produtos_encontrados  # Retorna uma lista vazia se nenhum produto for encontrado


# Listar  Todos os produto
def listar_produtos():
    fornecedores = ler_fornecedores()
    dados_produtos = []  # Lista para armazenar os dados dos produtos
    
    for fornecedor in fornecedores:
        if "produtos" in fornecedor:
            for produto in fornecedor["produtos"]:
                # Adiciona as informações do produto à lista de dicionários
                dados_produtos.append({
                    "Fornecedor": fornecedor['nome'],
                    "Produto": produto['nome'],
                    "Descrição": produto['descricao'],
                    "Preço": produto['preco_aquisicao']

                })
    
    # Imprime a tabela formatada usando tabulate
    print(tabulate(dados_produtos, headers="keys", tablefmt="grid"))


#Buscar produto por id
def buscar_produto(id_produto):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if "produtos" in fornecedor:
            for produto in fornecedor["produtos"]:
                if (
                    str(produto["codigo_id"]) == id_produto
                ):
                    return fornecedor['nome'], produto['nome'], produto['descricao'], produto['preco_aquisicao']
    return None

#
def produto_existe(id_produto):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if "produtos" in fornecedor:
            for produto in fornecedor["produtos"]:
                if str(produto["codigo_id"]) == id_produto or produto["nome"] == id_produto:
                    return True
    return False


# Update produto
def atualizar_produto(id_produto, novos_dados):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if "produtos" in fornecedor:
            for produto in fornecedor["produtos"]:
                if str(produto["codigo_id"]) == id_produto:
                    produto.update(novos_dados)
                    salvar_fornecedores(fornecedores)
                    return True
    return False

# Delete
def excluir_produto(id_produto):
    fornecedores = ler_fornecedores()
    for fornecedor in fornecedores:
        if "produtos" in fornecedor:
            produtos_restantes = [
                p for p in fornecedor["produtos"] if str(p["codigo_id"]) != id_produto
            ]
            if len(produtos_restantes) < len(fornecedor["produtos"]):
                fornecedor["produtos"] = produtos_restantes
                salvar_fornecedores(fornecedores)
                return True
    return False

#manipulação de estoque

def obter_quantidade_estoque(id_produto):
    estoque = ler_estoque()
    for item in estoque:
        if item["id"] == id_produto:
            return item["qtd"]
    return 0

def remover_estoque(id_produto, qtd_produto):
    estoque = ler_estoque()
    for item in estoque:
        if item["id"] == id_produto:
            item["qtd"] -= qtd_produto
            salvar_estoque(estoque)
            return True
    return False


# Saida de produto
# Função para ler as saídas de produtos do arquivo JSON
def ler_saida():
    try:
        with open(SAIDA_JSON, "r") as file:
            saida = json.load(file)
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        saida = []
    return saida

# Função para salvar as saídas de produtos no arquivo JSON
def salvar_saida(saida):
    with open(SAIDA_JSON, "w") as file:
        json.dump(saida, file, indent=4)

# Função para registrar uma saída de produto
def registrar_saida(id_produto, quantidade, data):
    saida = ler_saida()
    saida.append({
        "id_produto": id_produto,
        "quantidade": quantidade,
        "data": data.strftime("%Y-%m-%d %H:%M:%S")
    })
    salvar_saida(saida)

# Função para listar todas as saídas de produtos
def listar_saida():
    saida = ler_saida()
    if not saida:
        print("Nenhuma saída de produto registrada.")
    else:
        dados_saida = []
        for item in saida:
            dados_saida.append({
                "ID do Produto": item["id_produto"],
                "Quantidade": item["quantidade"],
                "Data": item["data"]
            })
        print(tabulate(dados_saida, headers="keys", tablefmt="grid"))
        
