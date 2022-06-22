import csv
from curses.ascii import isalnum, isalpha
import itertools
from math import comb
from pathlib import Path
from os import remove

def inicializar_base():
    '''Função para inicializar a base com o header.'''
    with open('database_projeto2.csv','w',encoding='utf-8') as database:
        escritor = csv.writer(database)
        header = ['nome','email','instrumentos','generos']
        escritor.writerow(header)

def conferir_base():
    '''Caso o arquivo da base não exista ainda, cria o arquivo.'''
    path = Path('database_projeto2.csv')
    if not path.is_file():
        inicializar_base()

def validar_nome(nome:str):
    '''Testa se o nome fornecido tem apenas caracteres alfabéticos.'''
    for char in nome:
        if not isalpha(char):
            return False 
    return True

def validar_email(email:str):
    '''Valida o email, considerando apenas caracteres alfanuméricos e um @.'''
    for char in email:
        if not (isalnum(char) or char=='_' or char=='.' or char=='@'):
            return False
    if not ('@' in email): 
        return False
    return True

def email_encontrado(email,dados ='database_projeto2.csv'):
    '''Confere se o email já existe na base, devolvendo um bool.'''
    with open(dados,'r',encoding='utf-8') as database:
        leitor = csv.reader(database, delimiter=',', lineterminator='\n')
        for linha in leitor:
            if linha[1]==email:
                return True
        return False

def validar_cadastro(nome:str,email:str,instrumentos:list,generos:list,dados ='database_projeto2.csv'):
    '''Executa toda a validação da função de cadastro, printando os erros e levantando exceções.'''
    conferir_base()
    if not validar_nome(nome):
        print('Nome inválido!')
        raise Exception('Nome inválido!')
    if not validar_email(email):
        print('Email inválido!')
        raise Exception('Email inválido!')
    if email_encontrado(email,dados):
        print('Cadastro já encontrado!')
        raise Exception('Cadastro já encontrado!')
    if instrumentos==['']:
        print('Digite ao menos um instrumento!')
        raise Exception('instrumentos')
    if generos==['']:
        print('Digite ao menos um gênero!')
        raise Exception('generos')

def input_cadastro():
    '''Pega os dados necessários para o cadastro a partir do usuário.'''
    print('Digite nome, email, instrumentos e gêneros')
    nome = input('Nome: ')
    email = input('Email: ')
    instrumentos = input('Instrumento (digite separado por vírgulas caso sejam mais de um): ').split(sep=',')
    generos = input('Gênero (digite separado por vírgulas caso sejam mais de um): ').split(sep=',')
    return nome,email,instrumentos,generos

def cadastrar(nome:str,email:str,instrumentos:list,generos:list,dados ='database_projeto2.csv'):
    '''Realiza o cadastro no arquivo.'''
    validar_cadastro(nome,email,instrumentos,generos)

    with open(dados,'a',encoding='utf-8') as database:
        novo_musico=[nome,email,instrumentos,generos]
        escritor = csv.writer(database, delimiter=',', lineterminator='\n')
        escritor.writerow(novo_musico)

def input_busca():
    '''Pega os dados para a busca.'''
    print('Selecione os parâmetros da busca (todos são opcionais, mas ao menos um deve ser escolhido) ')
    nome = input('Nome: ')
    email = input('Email: ')
    instrumento = input('Instrumento: ')
    genero = input('Gênero: ')

    return nome,email,instrumento,genero

def chave_busca(nome:str,email:str,instrumento:list,genero:list):
    '''Cria uma lista legível de busca, e identifica quantos parâmetros estão sendo buscados.'''
    chave = [nome,email,instrumento,genero]
    num_campos = sum([1 if x!=None else 0 for x in chave])
    chave = [x if x!=None else 'vazio' for x in chave]
    return chave,num_campos

def comparacao(linha:list,chave:list,num_campos:int,restrito:bool):
    '''Compara a linha analisada com a chave, já considerando se a comparação é restrita (exige todos os campos) ou não.'''
    comp = [int(linha[i]==chave[i]) for i in range(2)]
    comp += [int(chave[i] in linha[i]) for i in [2,3]]
    if restrito:
        checar = sum(comp)
        if checar>=num_campos:
            return True
        else:
            return False
    else:
        checar = sum(comp) 
        if checar>0:
            return True
        else:
            return False

def buscar(nome:str = None, email:str = None, instrumento:str = None,genero:str = None,restrito=False,dados ='database_projeto2.csv'):
    '''Busca ao longo da base as entradas que correspondem aos parâmetros da busca. Todos os parâmetros são opcionais, mas ao menos um deve ser passado. O bool restrito define se a busca é satisfeita com todos os campos corretos, ou se apenas um campo é suficiente.'''
    conferir_base()
    if not (nome or email or genero or instrumento):
        print('Busca inválida, digite algum dos campos.')
        raise Exception('Busca inválida, nenhum campo selecionado.')

    with open(dados,'r',encoding='utf-8') as database:
        out = []
        chave,num_campos = chave_busca(nome,email,instrumento,genero)
        leitor = csv.reader(database, delimiter=',', lineterminator='\n')
        for linha in leitor:
            if comparacao(linha,chave,num_campos,restrito):
                out.append(linha)
    return out

def print_busca(busca):
    '''Printa a busca de forma mais adequada.'''
    for linha in busca:
        print(f'Nome: {linha[0]} Email: {linha[1]} Instrumentos: {linha[2]}  Gêneros: {linha[3]}')

def dados_para_lista(dados='database_projeto2.csv'):
    '''Simplesmente carrega os dados do arquivo em uma lista.'''
    with open(dados,'r',encoding='utf-8') as database:
        leitor = list(csv.reader(database, delimiter=',', lineterminator='\n'))
        lista = [linha for linha in leitor]
        return lista

def str_pra_lista(string):
    '''Adequa as strings do csv para listas por simplicidade.'''
    string = string[1:-1]
    string=string.replace("'",'')
    lista = string.split(sep=',')
    return lista

def formatar_musico(musico):
    '''Adequa as linhas do csv aos tipos de dados utilizados no programa.'''
    musico[2]=str_pra_lista(musico[2])
    musico[3]=str_pra_lista(musico[3])
    return musico

def find_musico(email,leitor):
    '''Retorna o índice de um certo músico na base de dados.'''
    for i in range(len(leitor)):
        if leitor[i][1]==email:
            return i

def modificar(email:str,dados ='database_projeto2.csv'):
    '''Modifica uma das entradas do arquivo.'''
    conferir_base()
    if not email_encontrado(email,dados):
        print('Email não encontrado!')
        raise Exception('Email não encontrado!')

    with open(dados,'r+',encoding='utf-8') as database:
        leitor = dados_para_lista()
        musico = leitor[find_musico(email,leitor)]
        musico = formatar_musico(musico)
        opcao = input('Deseja adicionar algo? (i para instrumento, g para gênero, n para não)')
        if opcao == 'i' or opcao =='g':
            modificacao = input('Insira o novo termo: ')
            musico[2].append(modificacao) if opcao == 'i' else musico[3].append(modificacao)
        opcao = input('Deseja remover algo? (i para instrumento, g para gênero, n para não)')
        if opcao == 'i' or opcao =='g':
            modificacao = input('Insira o novo termo: ')
            musico[2].remove(modificacao) if opcao == 'i' else musico[3].remove(modificacao)
        leitor[find_musico(email,leitor)]=musico
        escritor = csv.writer(database)
        escritor.writerows(leitor)

def musicos_possiveis(num_musicos, instrumentos, genero):
    '''Lista todos os músicos possíveis para a busca das bandas, devolvendo uma lista de listas, com cada entrada sendo uma lista de tuplas dos músicos adequados à posição.'''
    musicos_possiveis = []
    for i in range(num_musicos):
        musicos_possiveis.append([(musico[1],instrumentos[i]) for musico in buscar(instrumento=instrumentos[i]) if genero in musico[3]])
    return musicos_possiveis

def comb_facil(lista_listas):
    '''Versão simples da combinação caso a outra dê erro.'''
    return list(itertools.product(*lista_listas))

def lista_pura(lista):
    '''Torna uma lista unidimensional.'''
    lista_nova=[]
    for item in lista:
        if type(item)==list:
            lista_nova+=lista_pura(item)
    else:
        lista_nova+=item
    return lista_nova

def comb_minha(lista_de_listas):
    '''Minha versão da combinação, utilizando recursão.'''
    if len(lista_de_listas)==1:
        return lista_de_listas
    if len(lista_de_listas)==2:
        out=[]
        for a in lista_de_listas[0]:
            for b in lista_de_listas[1]:
                out.append(lista_pura([a,b]))
        return out
    else:
        lista_de_listas[0]=comb_minha(lista_de_listas[0:2])
        lista_de_listas.pop(1)
        return comb_minha(lista_de_listas)
    
def remover_reps(combs):
    '''Remove combinações que consideram o mesmo músico em duas posições.'''
    combs_copia=combs.copy()
    for comb in combs_copia:
        emails = [email for (email,x) in comb]
        if len(emails)!=len(set(emails)):
            combs.remove(comb)
    return combs

def input_banda():
    '''Pega os inputs do usuário para montar_banda.'''
    print('Selecione o número de músicos, os instrumentos (separados por vírgulas) e o gênero')
    num_musicos = int(input('Número de músicos: '))
    instrumentos = input('Instrumentos: ').split(sep=',')
    genero = input('Gênero: ')
    return num_musicos,instrumentos,genero

def validar_banda(num_musicos, instrumentos, genero):
    '''Valida as entradas da função montar_bandas'''
    conferir_base()
    if len(instrumentos)!=num_musicos:
        print('O número de instrumentos é inválido!')
        raise Exception('O número de instrumentos é inválido!')
    if num_musicos==0:
        print('O número de músicos é inválido!')
        raise Exception('O número de músicos é inválido!')

def montar_banda(num_musicos, instrumentos, genero):
    '''Monta as bandas, baseada na quantidade de músicos, uma lista de instrumentos, e o gênero.'''
    validar_banda(num_musicos, instrumentos, genero)
    mus_possiveis = musicos_possiveis(num_musicos, instrumentos, genero)
    combinacoes = comb_facil(mus_possiveis)
    combinacoes = remover_reps(combinacoes)
    return combinacoes

def print_bandas(combinacoes):
    '''Função para printar de forma adequada a montagem das bandas.'''
    for comb in combinacoes:
        string=''
        for x in comb:
            string+=str(x)+'+'
        string=string[:-1]
        string+='\n'
    print(string)

def menu():
    '''Função do menu para acesso das outras funções.'''
    opcao=-1
    while opcao!=0:
        print('\n 1 - Cadastrar músicos\n','2 - Buscar músicos\n','3 - Modificar músicos\n','4 - Montar bandas\n','0 - Sair\n')
        opcao = int(input('Digite a opção desejada: '))
        if opcao == 1:
            nome,email,instrumentos,generos=input_cadastro()
            try:
                cadastrar(nome,email,instrumentos,generos)
            except:
                continue
        elif opcao == 2:
            nome,email,instrumento,genero=input_busca()
            try:
                print_busca(buscar(nome,email,instrumento,genero))
            except:
                continue
        elif opcao == 3:
            email=input('Digite o email a ser modificado: ')
            try:
                modificar(email)
            except:
                continue
        elif opcao == 4:
            num_musicos,instrumentos,genero=input_banda()
            try:
                print_bandas(montar_banda(num_musicos,instrumentos,genero))
            except:
                continue

menu()