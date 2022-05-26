import json
import os.path
import sys

def obter_dados():
    '''
    Essa função carrega os dados dos produtos e retorna uma lista de dicionários, onde cada dicionário representa um produto.
    NÃO MODIFIQUE essa função.
    '''
    with open(os.path.join(sys.path[0], 'dados.json'), 'r') as arq:
        dados = json.loads(arq.read())
    return dados

def listar_categorias(dados:list) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista contendo todas as categorias dos diferentes produtos.
    Cuidado para não retornar categorias repetidas.    
    '''
    categorias = [] 
    [categorias.append(produto['categoria']) for produto in dados if produto['categoria'] not in categorias] 

    return categorias

def validar_categoria(dados:list,categoria:str) -> bool:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    A função valida que a categoria aparece dentro dos dados.  
    '''
    if categoria in listar_categorias(dados):
        return True
    else:
        return False

def listar_por_categoria(dados:list,categoria:str) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar uma lista contendo todos os produtos pertencentes à categoria dada.
    '''
    produtos_categoria = [produto for produto in dados if produto['categoria']==categoria]
    
    return produtos_categoria
    
def produto_mais_caro(dados:list,categoria:str) -> dict:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar um dicionário representando o produto mais caro da categoria dada.
    '''
    produtos_categoria = listar_por_categoria(dados, categoria)

    return sorted(produtos_categoria,key= lambda x: float(x['preco']),reverse = True)[0] 

def produto_mais_barato(dados:list,categoria:str) -> dict:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar um dicionário representando o produto mais caro da categoria dada.
    '''
    produtos_categoria = listar_por_categoria(dados, categoria)

    return sorted(produtos_categoria,key= lambda x: float(x['preco']))[0] 

def top_10_caros(dados:list) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista de dicionários representando os 10 produtos mais caros.
    '''
    return sorted(dados,key = lambda x: float(x['preco']),reverse=True)[:10]

def top_10_baratos(dados:list) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista de dicionários representando os 10 produtos mais baratos.
    '''
    return sorted(dados,key = lambda x: float(x['preco']))[:10]

def print_lista_dicts(lista:list) -> None:
    '''
    O parâmetro lista é uma lista de dicionários, printados de forma mais amigável.
    '''
    if type(lista)==list:
        lista.sort(key = lambda x: float(x['preco']))
        for item in lista:
            print('Identificador: ',item['id'])
            print('preço = ',item['preco'],'   ','categoria = ',item['categoria'])
    else:
        item = lista
        print('Identificador: ',item['id'])
        print('preço = ',item['preco'],'   ','categoria = ',item['categoria'])

def print_lista(lista:list) -> None:
    '''
    O parâmetro lista recebe uma lista a ser colocada de forma mais bonita no output.
    A lista apenas é exibida com cada item em uma linha.
    '''
    lista.sort()    
    for item in lista:
        print(item)

def menu(dados:list) -> None:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá, em loop, realizar as seguintes ações:
    - Exibir as seguintes opções:
        1. Listar categorias
        2. Listar produtos de uma categoria
        3. Produto mais caro por categoria
        4. Produto mais barato por categoria
        5. Top 10 produtos mais caros
        6. Top 10 produtos mais baratos
        0. Sair
    - Ler a opção do usuário.
    - No caso de opção inválida, imprima uma mensagem de erro.
    - No caso das opções 2, 3 ou 4, pedir para o usuário digitar a categoria desejada.
    - Chamar a função adequada para tratar o pedido do usuário e salvar seu retorno.
    - Imprimir o retorno salvo. 
    O loop encerra quando a opção do usuário for 0.
    '''
    
    opcao = -1

    lista_menu = ['0. Sair','1. Listar categorias','2. Listar produtos de uma categoria',
                    '3. Produto mais caro por categoria','4. Produto mais barato por categoria',
                    '5. Top 10 produtos mais caros','6. Top 10 produtos mais baratos']

    while opcao != 0:
        print_lista(lista_menu)
        opcao = int(input('Digite a opção desejada: '))

        if opcao in [2,3,4]:
            categoria = input('Selecione a categoria: ')
            if not validar_categoria(dados,categoria):
                print('A categoria é inválida!')
                continue

        if opcao == 1:
            print_lista(listar_categorias(dados))
        elif opcao == 2:
            print_lista_dicts(listar_por_categoria(dados,categoria))
        elif opcao == 3:
            print_lista_dicts(produto_mais_caro(dados,categoria))
        elif opcao == 4:
            print_lista_dicts(produto_mais_barato(dados,categoria))
        elif opcao == 5:
            print_lista_dicts(top_10_caros(dados))
        elif opcao == 6:
            print_lista_dicts(top_10_baratos(dados))
        elif opcao == 0:
            print('Adeus!')
        else:
            print('Entrada inválida!')

# Programa Principal - não modificar!
dados = obter_dados()
menu(dados)
