import csv

def inicializar_base():
    with open('database_projeto2.csv','w',encoding='utf-8') as database:
        escritor = csv.writer(database)
        header = ['nome','email','instrumentos','generos']
        escritor.writerow(header)

def cadastrar(nome:str,email:str,instrumentos:list,generos:list):
    with open('database_projeto2.csv','a',encoding='utf-8') as database:
        novo_musico=[nome,email,instrumentos,generos]
        escritor = csv.writer(database, delimiter=',', lineterminator='\n')
        escritor.writerow(novo_musico)

def buscar(nome:str = None, email:str = None, instrumento:str = None,genero:str = None):
    if not (nome or email or genero or instrumento):
        print('Busca inválida, digite algum dos campos.')
        raise Exception('Busca inválida, nenhum campo selecionado.')

    with open('database_projeto2.csv','r',encoding='utf-8') as database:
        out = []
        leitor = csv.reader(database, delimiter=',', lineterminator='\n')
        if nome:
            [out.append(linha) for linha in leitor if linha[0]==nome]
        elif email:
            [out.append(linha) for linha in leitor if linha[1]==email]
        elif instrumento:
            [out.append(linha) for linha in leitor if instrumento in linha[2]]
        elif genero:
            [out.append(linha) for linha in leitor if genero in linha[3]]

    return out

def modificar(email):
    with open('database_projeto2.csv','a+',encoding='utf-8') as database:
        leitor = csv.reader(database, delimiter=',', lineterminator='\n')
        musico = [linha for linha in leitor if linha[1]==email]
        opcao = input('Deseja adicionar algo? (i para instrumento, g para gênero, n para não)')
        if opcao == 'i' or opcao =='g':
            modificacao = input('Insira o novo termo: ')
            musico[2].append(modicacao) if opcao == 'i'  else musico[3].append(modicacao)
        opcao = input('Deseja remover algo? (i para instrumento, g para gênero, n para não)')
        if opcao == 'i' or opcao =='g':
            modificacao = input('Insira o novo termo: ')
            musico[2].remove(modicacao) if opcao == 'i' else musico[3].remove(modicacao)
        [linha for linha in leitor if linha[1]==email][0]=musico

def montar_banda(num_musicos,instrumentos,gênero):
    buscar()

def menu():
    print('1 - Cadastrar músicos\n','2 - Buscar músicos\n','3 - Modificar músicos\n','4 - Montar bandas\n','0 - Sair\n')
    opcao = int(input('Digite a opção desejada: '))

    if opcao == 1:
        print('Digite , email, instrumentos e gêneros')
        nome = input('Nome: ')
        email = input('Email: ')
        instrumentos = input('Instrumento (digite separado por vírgulas caso sejam mais de um): ').split(sep=',')
        generos = input('Gênero (digite separado por vírgulas caso sejam mais de um): ').split(sep=',')
        cadastrar(nome,email,instrumentos,generos)
    elif opcao == 2:
        print('Selecione os parâmetros da busca (todos são opcionais, mas ao menos um deve ser escolhido) ')
        nome = input('Nome: ')
        email = input('Email: ')
        instrumento = input('Instrumento: ')
        genero = input('Gênero: ')
        print(buscar(nome,email,instrumento,genero))
    elif opcao == 3:
        email=input('Digite o email a ser modificado: ')
        modificar(email)

#menu()