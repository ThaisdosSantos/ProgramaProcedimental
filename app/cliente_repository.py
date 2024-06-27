import json
import re
from datetime import datetime


# Função para validar o formato do email
def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Função para validar o CPF
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        print("O CPF deve conter 11 dígitos.")
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        print("CPF inválido.")
        return False

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        print("CPF inválido.")
        return False

    return True

# Função para carregar clientes do arquivo
def carregar_clientes():
    try:
        with open("arquivos/clientes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar clientes no arquivo
def salvar_clientes(clientes):
    with open("arquivos/clientes.json", "w") as file:
        json.dump(clientes, file, indent=4)

# Lista para armazenar os clientes cadastrados
clientes = carregar_clientes()

# Função para cadastrar um novo cliente
def criar_cliente(nome, sobrenome, cpf, endereco, telefone, email):
    # Validação dos campos obrigatórios
    if nome and sobrenome and endereco and telefone and email:
        cpf_valido = validar_cpf(cpf)
        email_valido = validar_email(email)
        if cpf_valido and email_valido:
            # Verificar se já existe um cliente com o mesmo CPF
            if any(cliente['CPF'] == cpf for cliente in clientes):
                return False, "\nO CPF fornecido já está cadastrado."
            else:
                # Registro da data e hora do cadastro
                data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cliente = {
                    'Nome': nome,
                    'Sobrenome': sobrenome,
                    'CPF': cpf,
                    'Endereço': endereco,
                    'Telefone': telefone,
                    'E-mail': email,
                    'Data de Cadastro': data_cadastro
                }
                clientes.append(cliente)
                salvar_clientes(clientes)
                return True, "\nCliente cadastrado com sucesso!"
        else:
            if not cpf_valido and not email_valido:
                return False, "CPF e formato de e-mail inválidos."
            elif not cpf_valido:
                return False, "CPF inválido."
            else:
                return False, "Formato de e-mail inválido."
    else:
        return False, "Todos os campos são obrigatórios."

# Função para listar todos os clientes
def listar_clientes():
    return clientes

# Função para buscar um cliente pelo CPF
def buscar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if cliente['CPF'] == cpf:
            return cliente
    return None

# Função para atualizar os dados de um cliente
def atualizar_cliente(cpf, novos_dados):
    for cliente in clientes:
        if cliente['CPF'] == cpf:
            cliente.update(novos_dados)
            salvar_clientes(clientes)
            return True
    return False

# Função para excluir um cliente pelo CPF
def excluir_cliente(cpf):
    global clientes
    clientes = [cliente for cliente in clientes if cliente['CPF'] != cpf]
    salvar_clientes(clientes)
