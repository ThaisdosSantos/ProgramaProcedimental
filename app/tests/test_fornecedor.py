import pytest
from unittest.mock import patch, MagicMock
from repository import criar_fornecedor, buscar_fornecedor, excluir_fornecedor, atualizar_fornecedor
from controllers import cadastrar_fornecedor, pesquisar_dados_fornecedor, atualizar_dados_fornecedor, deletar_fornecedor

@pytest.fixture
def fornecedores_lista():
    return [
        {"cnpj": "765456789", "nome": "Alexandre", "telefone": "938854321", "email": "fornecedorum@teste.com"},
        {"cnpj": "987654321", "nome": "Neto", "telefone": "187656789", "email": "fornecedordois@teste.com"},
        {"cnpj": "496839458", "nome": "Felipe", "telefone": "968324321", "email": "fornecedortres@teste.com"},
        {"cnpj": "907673361", "nome": "Clarissa", "telefone": "999436789", "email": "fornecedorquatro@teste.com"}
    ]

@pytest.fixture
def fornecedor():
    return {"cnpj": "173486759", "nome": "João Aleatório", "telefone": "987654321", "email": "fornecedoraleatorio@teste.com"}


def test_criar_fornecedor(mocker, fornecedor):
    # Mock das funções ler_fornecedores() e salvar_fornecedores()
    fornecedores_existente = [{"cnpj": "987654321", "nome": "Daniel Existente", "telefone": "39598123", "email": "fornecedorexistente@teste.com"}]
    mock_ler_fornecedores = mocker.patch("repository.ler_fornecedores", return_value=fornecedores_existente)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Chama a função criar_fornecedor() com um novo fornecedor
    criar_fornecedor(**fornecedor)

    # Verifica se ler_fornecedores() foi chamado
    mock_ler_fornecedores.assert_called_once()

    # Verifica se salvar_fornecedores() foi chamado com a lista atualizada de fornecedores
    fornecedores_existente.append(fornecedor)
    mock_salvar_fornecedores.assert_called_once_with(fornecedores_existente)

def test_buscar_fornecedor_encontra_pelo_nome(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)

    # Testa se o fornecedor é encontrado pelo nome
    assert buscar_fornecedor("Alexandre") == True

def test_buscar_fornecedor_encontra_pelo_cnpj(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)

    # Testa se o fornecedor é encontrado pelo CNPJ
    assert buscar_fornecedor("496839458") == True

def test_buscar_fornecedor_nao_encontra(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)

    # Testa quando o fornecedor não é encontrado
    assert buscar_fornecedor("Jóencio") == False
    assert buscar_fornecedor("556345782") == False

def test_atualizar_fornecedor_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores() e salvar_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Atualiza um fornecedor existente
    assert atualizar_fornecedor("765456789", "Alexandre Costa", "935654321", "novoemail@teste.com") == True

    # Verifica se o fornecedor foi atualizado corretamente
    assert fornecedores_lista[0]["nome"] == "Alexandre Costa"
    assert fornecedores_lista[0]["telefone"] == "935654321"
    assert fornecedores_lista[0]["email"] == "novoemail@teste.com"

    # Verifica se salvar_fornecedores() foi chamado com a lista atualizada de fornecedores
    mock_salvar_fornecedores.assert_called_once_with(fornecedores_lista)

def test_atualizar_fornecedor_nao_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Tenta atualizar um fornecedor que não existe
    assert atualizar_fornecedor("Jailson", "Jailson Junior", "366532257", "novoemail@teste.com") == False

    # Verifica se salvar_fornecedores() não foi chamado
    mock_salvar_fornecedores.assert_not_called()

def test_excluir_fornecedor_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores() e salvar_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Exclui um fornecedor existente
    excluir_fornecedor("765456789")

    # Verifica se o fornecedor foi excluído corretamente
    assert len(fornecedores_lista) == 4
    assert fornecedores_lista[0]["cnpj"] == "987654321"

    # Verifica se salvar_fornecedores() foi chamado com a lista atualizada de fornecedores
    mock_salvar_fornecedores.assert_called_once_with(fornecedores_lista)

def test_excluir_fornecedor_nao_existente(fornecedores_lista, mocker):
    # Mock da função ler_fornecedores()
    mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    # Tenta excluir um fornecedor que não existe
    excluir_fornecedor("Junior")

    # Verifica se salvar_fornecedores() não foi chamado
    mock_salvar_fornecedores.assert_not_called()


def test_cadastrar_fornecedor(fornecedores_lista, mocker):
    mock_ler_fornecedores = mocker.patch("repository.ler_fornecedores", return_value=fornecedores_lista)
    mock_salvar_fornecedores = mocker.patch("repository.salvar_fornecedores")

    entrada_usuario = [
        "39574385",  
        "João Aldo",  
        "1258794830",  
        "testecadastro@example.com"  
    ]
    # Simula o input do usuário
    with patch('builtins.input', side_effect=entrada_usuario):
        # Chama a função testada
        cadastrar_fornecedor()

    # Verifica se a função criar_fornecedor foi chamada com os argumentos corretos
    mock_salvar_fornecedores.assert_called_once()

    # Verifica se todos os dados foram salvos corretamente na lista
    assert fornecedores_lista[4]["cnpj"] == entrada_usuario[0]
    assert fornecedores_lista[4]["nome"] == entrada_usuario[1]
    assert fornecedores_lista[4]["telefone"] == entrada_usuario[2]
    assert fornecedores_lista[4]["email"] == entrada_usuario[3] 

    # Verifica se a função ler_fornecedores foi chamada
    assert mock_ler_fornecedores.called

# Simula a entrada do usuário e a função buscar_fornecedor
@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
def test_pesquisar_dados_fornecedor_encontrado(mock_buscar_fornecedor, mock_input):
    # Configura o mock da entrada do usuário para simular um CNPJ válido
    mock_input.return_value = "123456789"

    # Configura o mock da função buscar_fornecedor para simular que o fornecedor foi encontrado
    mock_buscar_fornecedor.return_value = True

    # Chama a função testada
    pesquisar_dados_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("123456789")

# Simula a entrada do usuário e a função buscar_fornecedor
@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
def test_pesquisar_dados_fornecedor_nao_encontrado(mock_buscar_fornecedor, mock_input):
    # Configura o mock da entrada do usuário para simular um nome de fornecedor inexistente
    mock_input.return_value = "Fornecedor Inexistente"

    # Configura o mock da função buscar_fornecedor para simular que o fornecedor não foi encontrado
    mock_buscar_fornecedor.return_value = False

    # Chama a função testada
    pesquisar_dados_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("Fornecedor Inexistente")

@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
@patch('controllers.atualizar_fornecedor')
def test_atualizar_dados_fornecedor_encontrado(mock_atualizar_fornecedor, mock_buscar_fornecedor, mock_input):
    # Simula a entrada do usuário para fornecedor existente
    mock_input.side_effect = ["486749672", "Lucas Rios", "9958435672", "novo@email.com"]

    # Simula que o fornecedor foi encontrado
    mock_buscar_fornecedor.return_value = True

    # Chama a função testada
    atualizar_dados_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("486749672")
    
    # Verifica se a função atualizar_fornecedor foi chamada com os argumentos corretos
    mock_atualizar_fornecedor.assert_called_once_with("486749672", "Lucas Rios", "9958435672", "novo@email.com")

@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
@patch('controllers.atualizar_fornecedor')
def test_atualizar_dados_fornecedor_nao_encontrado(mock_atualizar_fornecedor, mock_buscar_fornecedor, mock_input):
    # Simula a entrada do usuário para fornecedor não existente
    mock_input.return_value = "Fornecedor Inexistente"

    # Simula que o fornecedor não foi encontrado
    mock_buscar_fornecedor.return_value = False

    # Chama a função testada
    atualizar_dados_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("Fornecedor Inexistente")

    # Verifica se a função atualizar_fornecedor não foi chamada
    assert not mock_atualizar_fornecedor.called

@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
@patch('controllers.excluir_fornecedor')
def test_deletar_fornecedor_confirmado(mock_excluir_fornecedor, mock_buscar_fornecedor, mock_input):
    # Simula a entrada do usuário para um fornecedor existente e confirmação de exclusão
    mock_input.side_effect = ["45782475", "s"]

    # Simula que o fornecedor foi encontrado
    mock_buscar_fornecedor.return_value = True

    # Chama a função testada
    deletar_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("45782475")

    # Verifica se a função excluir_fornecedor foi chamada com o argumento correto
    mock_excluir_fornecedor.assert_called_once_with("45782475")

@patch('builtins.input')
@patch('controllers.buscar_fornecedor')
@patch('controllers.excluir_fornecedor')
def test_deletar_fornecedor_nao_encontrado(mock_excluir_fornecedor, mock_buscar_fornecedor, mock_input):
    # Simula a entrada do usuário para um fornecedor não existente
    mock_input.return_value = "Fornecedor Inexistente"

    # Simula que o fornecedor não foi encontrado
    mock_buscar_fornecedor.return_value = False

    # Chama a função testada
    deletar_fornecedor()

    # Verifica se a função buscar_fornecedor foi chamada com o argumento correto
    mock_buscar_fornecedor.assert_called_once_with("Fornecedor Inexistente")

    # Verifica se a função excluir_fornecedor não foi chamada
    assert not mock_excluir_fornecedor.called