from tabulate import tabulate
from cliente_repository import (
    criar_cliente,
    listar_clientes,
    buscar_cliente_por_cpf,
    atualizar_cliente,
    excluir_cliente,
)

#Função geral para mensagem
def solicitar_cpf(mensagem="\nDigite o CPF do cliente: "):
    return input(mensagem)


# Função para cadastrar um novo cliente
def cadastrar_cliente():
    print("\nCadastro de Cliente")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    telefone = input("Número de Telefone: ")
    email = input("E-mail: ")
    
    # Chama a função do repositório para criar o cliente
    sucesso, mensagem = criar_cliente(nome, sobrenome, cpf, endereco, telefone, email)
    if sucesso:
        print(mensagem)
    else:
        print("Erro:", mensagem)

# Função para listar todos os clientes
def listar_clientes_controller():
    clientes = listar_clientes()
    if clientes:
        print("\nLista de Todos os Clientes Cadastrados:")
        for index, cliente in enumerate(clientes, start=1):
            print(f"\nCliente {index}:")
            print("-" * 20)  # Linha de tabela
            for chave, valor in cliente.items():
                print(f"{chave}: {valor}")
            print("-" * 20)  # Linha de tabela
    else:
        print("\nNenhum cliente cadastrado.")



# Função para buscar um cliente pelo CPF
def buscar_cliente():
    cpf = solicitar_cpf()
    cliente = buscar_cliente_por_cpf(cpf)
    if cliente:
        print("\nInformações do Cliente:")
        exibir_resultados_busca([cliente])
    else:
        print("\nCliente não encontrado.")
      


# Função para exibir os resultados da busca por CPF em uma tabela
def exibir_resultados_busca(resultados):
    if resultados:
        headers = resultados[0].keys()
        table_data = [[cliente.get(header, "") for header in headers] for cliente in resultados]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("Nenhum cliente encontrado.")
        
# Função para atualizar os dados de um cliente
def atualizar_cliente_controller():
    cpf = solicitar_cpf()
    cliente = buscar_cliente_por_cpf(cpf)
    if cliente:
        print("Cliente encontrado. \nDigite os novos dados (deixe em branco para manter os dados atuais):")
        novo_nome = input(f"Nome ({cliente['Nome']}): ").strip() or cliente['Nome']
        novo_sobrenome = input(f"Sobrenome ({cliente['Sobrenome']}): ").strip() or cliente['Sobrenome']
        novo_endereco = input(f"Endereço ({cliente['Endereço']}): ").strip() or cliente['Endereço']
        novo_telefone = input(f"Número de Telefone ({cliente['Telefone']}): ").strip() or cliente['Telefone']
        novo_email = input(f"E-mail ({cliente['E-mail']}): ").strip() or cliente['E-mail']

        novos_dados = {}
        
        # Exibir mensagem de confirmação
        confirmacao = input("Deseja salvar as alterações? (sim/não): ").lower()    
        if confirmacao == 'sim':
            # Atualiza os dados do cliente
            novos_dados = {
                'Nome': novo_nome,
                'Sobrenome': novo_sobrenome,
                'Endereço': novo_endereco,
                'Telefone': novo_telefone,
                'E-mail': novo_email
            }

            if atualizar_cliente(cpf, novos_dados):
                print("\nDados do cliente atualizados com sucesso.")
            else:
                print("\nErro ao atualizar os dados do cliente.")
        else:
            print("\nOperação de atualização cancelada.")
    else:
        print("\nCliente não encontrado.")


# Função para excluir um cliente pelo CPF
def excluir_cliente_controller():
    cpf = solicitar_cpf()
    cliente = buscar_cliente_por_cpf(cpf)
    if cliente:
        confirmacao = input("\nDeseja realmente excluir este cliente?(sim/não): ").lower() 
        if confirmacao == "sim":
            excluir_cliente(cpf)
            print("\nCliente excluído com sucesso.")
        else:
            print("\nOperação de exclusão cancelada.")
    else:
        print("\nCliente não encontrado.")

 