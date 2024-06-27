import os
from datetime import datetime
from controllers import (
    cadastrar_fornecedor,
    lista_de_fornecedores_controller,
    pesquisar_dados_fornecedor,
    atualizar_dados_fornecedor,
    deletar_fornecedor,
    adicionar_produto_fornecedor,
    lista_produtos_fornecedor,
    lista_produtos,
    pesquisar_produto,
    atualizar_dados_produto,
    deletar_produto,
    entrada_produto,
    exibir_entradas,
    saida_produto,
    alertar_baixo_estoque,
    alertar_alto_estoque,
    exibir_saida_terminal,
)
from cliente_controller import (
    cadastrar_cliente,
    listar_clientes_controller,
    buscar_cliente,
    atualizar_cliente_controller,
    excluir_cliente_controller,
)



def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_menu_cliente():
    while True:
        print("\nMENU DE CLIENTES:")
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes Cadastrados")
        print("3. Buscar Cliente por CPF")
        print("4. Atualizar Cliente")
        print("5. Excluir Cliente")
        print("0. Voltar para o Menu Principal")
        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes_controller()
        elif opcao == "3":
            buscar_cliente()
        elif opcao == "4":
           atualizar_cliente_controller()
        elif opcao == "5":
          excluir_cliente_controller()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
            

def exibir_menu_fornecedor():
    while True:
        print("\nMENU DE FORNECEDORES:")
        print("1. Cadastrar Fornecedor")
        print("2. Listar Fornecedores")
        print("3. Buscar Fornecedor por CNPJ")
        print("4. Atualizar Fornecedor")
        print("5. Deletar Fornecedor")
        print("0. Voltar para o Menu Principal")
        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            cadastrar_fornecedor()
        elif opcao == "2":
            lista_de_fornecedores_controller()
        elif opcao == "3":
            pesquisar_dados_fornecedor()
        elif opcao == "4":
            atualizar_dados_fornecedor()
        elif opcao == "5":
            deletar_fornecedor()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")


def exibir_menu_cadastro_produto():
    while True:
        print("\nMENU CADASTRAR PRODUTOS:")
        print("1. Adicionar Produto a Fornecedor")
        print("2. Listar Produtos de Fornecedor")
        print("3. Listar Todos os Produtos")
        print("4. Buscar Produto")
        print("5. Atualizar Produto")
        print("6. Excluir Produto")        
        print("0. Voltar para o Menu Principal")
        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == "1":
            adicionar_produto_fornecedor()
        elif opcao == "2":
            lista_produtos_fornecedor()
        elif opcao == "3":
            lista_produtos()
        elif opcao == "4":
            pesquisar_produto()
        elif opcao == "5":
            atualizar_dados_produto()
        elif opcao == "6":
            deletar_produto()        
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def exibir_menu_entrada_produto():
    while True:
        print("\nMENU REGISTRAR PRODUTOS:")
        print("1. Registrar entrada de produto")
        print("2. Listar entradas de produto registradas")        
        print("0. Voltar para o Menu Principal")
        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == "1":
            entrada_produto()
        elif opcao == "2":
            exibir_entradas()        
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
            
def exibir_menu_saida_produto():
    while True:
        print("\nMENU SAIDA PRODUTOS:")
        print("1. Registrar saida de produto")
        print("2. Alerta de baixo estoque")  
        print("3. Verificar produtos com alto estoque")
        print("4. Verificar nota da saida de produto")   
        print("0. Voltar para o Menu Principal")
        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == "1":
            saida_produto()
        elif opcao == "2":
            alertar_baixo_estoque()    
        elif opcao == "3":
            alertar_alto_estoque() 
        elif opcao == "4":    
            exibir_saida_terminal()     
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    while True:
        print("\nMENU PRINCIPAL:")
        print("1. Menu de Clientes")
        print("2. Menu de Fornecedores")
        print("3. Menu Cadastro de Produtos")
        print("4. Menu Registrar Entradas de Produtos")
        print("5. Menu Registrar Saídas de Produtos")
        print("0. Sair do Programa")
        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            exibir_menu_cliente()            
        elif opcao == "2":
            exibir_menu_fornecedor()            
        elif opcao == "3":
            exibir_menu_cadastro_produto()
        elif opcao == "4":
            exibir_menu_entrada_produto()
        elif opcao == "5":
           exibir_menu_saida_produto()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
    
