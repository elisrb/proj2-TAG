# função importada de biblioteca externa para aleatorizar a ordem de uma lista
from random import shuffle

# INICIALIZAÇÃO DE VARIÁVEIS

# listas:
alunos = []     # códigos dos alunos
projetos = []   # códigos dos projetos

# dicionários:
vagas_projetos = {}     # código do projeto: número de vagas
nota_projetos = {}      # código do projeto: requisito mínimo de notas para vagas
preferencia_alunos = {} # código do aluno: [lista de projetos preferenciais na ordem]
nota_alunos = {}        # código do aluno: nota do aluno

# FUNÇÕES

"""
A função "read_file" lê o arquivo .txt com os dados de entrada do projeto e reúne os seus dados
nas variáveis inicializadas acima.

Argumento: path do arquivo .txt relativa ao diretório que contém este arquivo (código-fonte)
"""
def read_file(path):
    with open(path, "r") as file:
        texto = file.read()  # extrai texto do arquivo

    for linha in texto.split("\n"):
        # as linhas significativas do arquivo de entrada são apenas as linhas que começam em '('
        if(linha and linha[0] == '('):
            if(':' not in linha):  # descreve os projetos
                linha = linha[1:-1]  # tira parênteses
                projeto, vagas, notas = linha.split(", ")

                # armazena os dados referentes aos projetos
                projetos.append(projeto)
                vagas_projetos[projeto] = int(vagas)
                nota_projetos[projeto] = int(notas)

            else:  # descreve os alunos
                aluno, atributos = linha.split(":")
                preferencia, nota = atributos.split(") (")

                # tira os parênteses que restaram
                aluno = aluno[1:-1]
                preferencia = preferencia[1:]
                nota = nota[:-1]

                # armazena os dados referentes aos alunos
                alunos.append(aluno)
                preferencia_alunos[aluno] = []
                for p in preferencia.split(", "):
                    preferencia_alunos[aluno].append(p)
                nota_alunos[aluno] = int(nota)

"""
A função "emparelhamento_estável" usa o algoritmo de Gale-Shapley para gerar um emparelhamento
estável entre alunos e projetos.

Argumento: lista de alunos
A lista de alunos deve ser passada como argumento para esta função porque para encontrar outros
possíveis emparelhamentos ela deve ser reordenada, logo, seu conteúdo será diferente a cada
chamada. Os demais dicionários e listas inicializados anteriormente não serão alterados, então
são tratados como variáveis globais.

Retorno: dicionário no formato {projeto: [lista de alunos cadastrados nele]}
A função não garante que todos os projetos terão todas as vagas preenchidas. Essa verificação
será feita mais tarde.
"""
def emparelhamento_estavel(alunos_in):
    # INICIALIZAÇÃO DE VARIÁVEIS

    # projeto: [lista de alunos cadastrados nele]
    matches = {projeto: [] for projeto in projetos}  #(começa com todos os projetos vazios)

    # lista de alunos livres
    alunos_livres = [aluno for aluno in alunos_in]  # (começa com todos os alunos)
    
    # aluno: índice do próximo projeto no qual ele ainda não tentou entrar
    proximo_pedido = {aluno: 0 for aluno in alunos_in}  # (começa em 0 para todos os alunos)

    # loop do algoritmo de Gale-Shapley com algumas modificações indicadas por comentários
    while len(alunos_livres) > 0:
        aluno_atual = alunos_livres.pop(0)

        if proximo_pedido[aluno_atual] < len(preferencia_alunos[aluno_atual]):
            projeto_atual = preferencia_alunos[aluno_atual][proximo_pedido[aluno_atual]]
            proximo_pedido[aluno_atual]+=1

            # conferir se a nota do aluno é suficiente para o projeto que ele quer
            if nota_alunos[aluno_atual] >= nota_projetos[projeto_atual]:
                # conferir se ainda há vagas para o projeto
                if len(matches[projeto_atual]) < vagas_projetos[projeto_atual]:
                    matches[projeto_atual].append(aluno_atual)
                else:
                    # assumindo que os projetos preferem os alunos com maiores notas
                    aluno = matches[projeto_atual][0]
                    if nota_alunos[aluno] < nota_alunos[aluno_atual]:
                        # se há aluno com nota menor que o atual, ele sai e o atual entra
                        matches[projeto_atual].remove(aluno)
                        alunos_livres.append(aluno)
                        matches[projeto_atual].append(aluno_atual)
                    else:
                        # se não há aluno com nota menor que o atual, o atual está livre
                        alunos_livres.append(aluno_atual)

        # ordena os alunos do projeto por nota para buscar o aluno com menor nota primeiro
        matches[projeto_atual].sort(key=lambda a: nota_alunos[a])

    return matches  # retorna um emparelhamento estável

# LEITURA DO ARQUIVO DE ENTRADA: chama a função "read_file"
read_file("./entradaProj2.24TAG.txt")

# GERAÇÃO DE EMPARELHAMENTOS ESTÁVEIS: chama a função "emparelhamento_estavel"
aumentos = 0    # quantos emparelhamentos gerados são maiores que todos os outros até então
tentativas = 0  # total de emparelhamentos gerados
arestas_max = 0 # arestas (alunos emparelhados) do maior emparelhamento até agora

"""
O loop a seguir gera vários emparelhamentos possíveis pela função "emparelhamento_estavel". Em
um cenário onde há poder computacional ilimitado, seria possível testar todas as permutações
da lista de alunos e comparar os emparelhamentos para encontrar o máximo. Porém, para permitir
a execução deste código, foi necessário limitar o número de tentativas para 1000.

A cada tentativa, a ordem da lista de alunos é aleatorizada pela função "shuffle", importada
acima. Desta forma, são gerados emparelhamentos para até 1000 permutações aleatórias da lista
de alunos. Este loop confere também o número de vagas para cada projeto, de forma a anular as
arestas de alunos que foram emparelhados a projetos que não foram completamente preenchidos. Em
seguida, é feita uma contagem do número de arestas válidas do emparelhamento gerado, e caso ele
seja um aumento em relação aos anteriores, ele é mostrado na tela.

O objetivo deste projeto é chegar a 10 aumentos, mas isso nem sempre será possível. O último
emparelhamento mostrado será o maior encontrado nas tentativas, mas não há garantia de que ele
é o emparelhamento estável máximo para o problema.
"""
while aumentos < 10 and tentativas < 1000:
    # gera o emparelhamento
    matches = emparelhamento_estavel(alunos)
    tentativas += 1

    # checa se as arestas são válidas
    arestas = 0
    for p, a in matches.items():
        if len(a) == vagas_projetos[p]:
            arestas+=len(a)

    # caso o emparelhamento seja um aumento em relação aos anteriores, mostra na tela
    if(arestas > arestas_max):
        arestas_max = arestas
        print("emparelhamento estável nº", tentativas)
        print("aumento nº", aumentos) if aumentos > 0 else ""
        print("quantidade de arestas (alunos emparelhados):", arestas)
        print("resultado do emparelhamento, no formato {projeto}: {lista de alunos}:")
        for p, a in matches.items():
            print(p+":", *a)
        aumentos+=1
        print("\n", end="")

    # aleatoriza a ordem da lista de alunos
    shuffle(alunos)

print("total de tentativas:", tentativas)
print("total de arestas no maior emparelhamento encontrado:", arestas_max)
