import pytest
from unittest.mock import patch
from app.repository import adicionar_produto, excluir_produto, buscar_produto, atualizar_produto
from controllers import adicionar_produto_fornecedor, pesquisar_produto, atualizar_dados_produto, deletar_produto

@pytest.fixture
def fornecedores_lista():
    return [
        {"cnpj": "765456789", "nome": "Alexandre", "produtos": [
            {"codigo_id": "100000", "nome": "Produto Um", "descricao": "Descrição do Produto Um"},
            {"codigo_id": "100001", "nome": "Produto Dois", "descricao": "Descrição do Produto Dois"}
        ]},
        {"cnpj": "987654321", "nome": "Neto", "produtos": [
            {"codigo_id": "100002", "nome": "Produto Três", "descricao": "Descrição do Produto Três"}
        ]}
    ]

def test_adicionar_produto_para_fornecedor_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores() e salvar_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Adiciona um produto para um fornecedor existente
    adicionar_produto("765456789", "100001", "Produto Teste", "Descrição do Produto Teste", 10)

    # Verifica se o produto foi adicionado corretamente
    for fornecedor in fornecedores_lista:
        if fornecedor["cnpj"] == "765456789":
            assert len(fornecedor["produtos"]) == 3
            assert fornecedor["produtos"][2]["codigo_id"] == "100001"
            assert fornecedor["produtos"][2]["nome"] == "Produto Teste"
            assert fornecedor["produtos"][2]["descricao"] == "Descrição do Produto Teste"
            assert fornecedor["produtos"][2]["preco_aquisicao"] == 10

    # Verifica se salvar_fornecedores() foi chamado com a lista atualizada de fornecedores
    mock_salvar_fornecedores.assert_called_once_with(fornecedores_lista)

def test_adicionar_produto_para_fornecedor_inexistente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Tenta adicionar um produto para um fornecedor que não existe
    adicionar_produto("900003061", "100000", "Produto Dois", "Descrição do Produto Dois", 10)

    # Verifica se salvar_fornecedores() não foi chamado
    mock_salvar_fornecedores.assert_not_called()

def test_excluir_produto_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores() e salvar_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Exclui um produto existente
    assert excluir_produto("100001") == True

    # Verifica se o produto foi excluído corretamente
    for fornecedor in fornecedores_lista:
        for produto in fornecedor.get("produtos", []):
            assert produto["codigo_id"] != "100001"

    # Verifica se salvar_fornecedores() foi chamado com a lista atualizada de fornecedores
    mock_salvar_fornecedores.assert_called_once_with(fornecedores_lista)

def test_excluir_produto_nao_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Tenta excluir um produto que não existe
    assert excluir_produto("100049") == False

    # Verifica se salvar_fornecedores() não foi chamado
    mock_salvar_fornecedores.assert_not_called()

def test_buscar_produto_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)

    # Testa se o produto é encontrado pelo código ID
    assert buscar_produto("100001") == True

    # Testa se o produto é encontrado pelo nome
    assert buscar_produto("Produto Dois") == True

def test_buscar_produto_inexistente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)

    # Testa quando o produto não é encontrado
    assert buscar_produto("100006") == False
    assert buscar_produto("Produto Seis") == False

def test_atualizar_produto_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores() e salvar_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Atualiza um produto existente
    assert atualizar_produto("100000", "Produto Novo", "Nova Descrição", 40) == True

    # Verifica se o produto foi atualizado corretamente
    for fornecedor in fornecedores_lista:
        for produto in fornecedor.get("produtos", []):
            if produto["nome"] == "Produto Novo":
                assert produto["descricao"] == "Nova Descrição"
                assert produto["preco_aquisicao"] == 40

    # Verifica se salvar_fornecedores() foi chamado com a lista atualizada de fornecedores
    mock_salvar_fornecedores.assert_called_once_with(fornecedores_lista)

def test_atualizar_produto_nao_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Tenta atualizar um produto que não existe
    assert atualizar_produto("100059", "Produto Inexistente", "Nova Descrição", 50) == False

    # Verifica se salvar_fornecedores() não foi chamado
    mock_salvar_fornecedores.assert_not_called()

@patch('builtins.input')
@patch('controllers.ler_codigo_id_base')
@patch('controllers.buscar_fornecedor')
@patch('controllers.salvar_codigo_id_base')
@patch('controllers.adicionar_produto')
def test_adicionar_produto_fornecedor_encontrado(mock_adicionar_produto, mock_salvar_codigo_id_base, mock_buscar_fornecedor, mock_ler_codigo_id_base, mock_input):
    # Simula a entrada do usuário para um fornecedor existente
    mock_input.side_effect = ["765456789", "Produto Novo", "Descrição do Produto novo", "10.0"]

    # Simula que o fornecedor foi encontrado
    mock_buscar_fornecedor.return_value = True

    # Simula o retorno do código base
    mock_ler_codigo_id_base.return_value = 100000

    # Chama a função testada
    adicionar_produto_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("765456789")

    # Verifica se a função ler_codigo_id_base foi chamada
    assert mock_ler_codigo_id_base.called

    # Verifica se a função adicionar_produto foi chamada com os argumentos corretos
    mock_adicionar_produto.assert_called_once_with("765456789", 100000, "Produto Novo", "Descrição do Produto novo", 10.0)

    # Verifica se a função salvar_codigo_id_base foi chamada
    mock_salvar_codigo_id_base.assert_called_once_with(100001)

@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
def test_adicionar_produto_fornecedor_nao_encontrado(mock_buscar_fornecedor, mock_input):
    # Simula a entrada do usuário para um fornecedor não existente
    mock_input.return_value = "Fornecedor Inexistente"

    # Simula que o fornecedor não foi encontrado
    mock_buscar_fornecedor.return_value = False

    # Chama a função testada
    adicionar_produto_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("Fornecedor Inexistente")

@patch('builtins.input')
@patch('controllers.buscar_produto')
def test_pesquisar_produto_encontrado(mock_buscar_produto, mock_input):
    # Simula a entrada do usuário para um produto existente
    mock_input.return_value = "Produto Buscado"

    # Simula que o produto foi encontrado
    mock_buscar_produto.return_value = True

    # Chama a função testada
    pesquisar_produto()

    # Verifica se a função buscar_produto foi chamada com o argumento correto
    mock_buscar_produto.assert_called_once_with("Produto Buscado")

@patch('builtins.input')
@patch('controllers.buscar_produto')
def test_pesquisar_produto_nao_encontrado(mock_buscar_produto, mock_input):
    # Simula a entrada do usuário para um produto não existente
    mock_input.return_value = "Produto Inexistente"

    # Simula que o produto não foi encontrado
    mock_buscar_produto.return_value = False

    # Chama a função testada
    pesquisar_produto()

    # Verifica se a função buscar_produto foi chamada com o argumento correto
    mock_buscar_produto.assert_called_once_with("Produto Inexistente")

@patch('builtins.input')
@patch('controllers.buscar_produto')
@patch('controllers.atualizar_produto')
def test_atualizar_dados_produto_encontrado(mock_atualizar_produto, mock_buscar_produto, mock_input):
    # Simula a entrada do usuário para um produto existente
    mock_input.side_effect = ["100001", "Produto Dois Alterado", "Produto Dois nova Descrição", "20.0"]

    # Simula que o produto foi encontrado
    mock_buscar_produto.return_value = True

    # Chama a função testada
    atualizar_dados_produto()

    # Verifica se a função buscar_produto foi chamada com o argumento correto
    mock_buscar_produto.assert_called_once_with("100001")

    # Verifica se a função atualizar_produto foi chamada com os argumentos corretos
    mock_atualizar_produto.assert_called_once_with("100001", "Produto Dois Alterado", "Produto Dois nova Descrição", 20.0)

@patch('builtins.input')
@patch('controllers.buscar_produto')
def test_atualizar_dados_produto_nao_encontrado(mock_buscar_produto, mock_input):
    # Simula a entrada do usuário para um produto não existente
    mock_input.return_value = "Produto Inexistente"

    # Simula que o produto não foi encontrado
    mock_buscar_produto.return_value = False

    # Chama a função testada
    atualizar_dados_produto()

    # Verifica se a função buscar_produto foi chamada com o argumento correto
    mock_buscar_produto.assert_called_once_with("Produto Inexistente")
