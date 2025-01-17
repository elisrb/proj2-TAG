alunos = []
projetos = []

vagas_projetos = {}
nota_projetos = {}
preferencia_alunos = {}
nota_alunos = {}

def read_file(path):
    with open(path, "r") as file:
        texto = file.read()  # extrai texto do arquivo

    for linha in texto.split("\n"):
        if(linha and linha[0] == '('):  # as linhas significativas do arquivo de entrada são apenas as linhas que começam em '('
            if(':' not in linha):  # descreve os projetos
                linha = linha[1:-1]  # tira parênteses
                projeto, vagas, notas = linha.split(", ")

                projetos.append(projeto)
                vagas_projetos[projeto] = int(vagas)
                nota_projetos[projeto] = int(notas)

            else:  # descreve os alunos
                aluno, atributos = linha.split(":")
                preferencia, nota = atributos.split(") (")
                # as linhas seguintes tiram os parênteses que restaram
                aluno = aluno[1:-1]
                preferencia = preferencia[1:]
                nota = nota[:-1]

                alunos.append(aluno)
                preferencia_alunos[aluno] = []
                for p in preferencia.split(", "):
                    preferencia_alunos[aluno].append(p)
                nota_alunos[aluno] = int(nota)

def emparelhamento_estavel(alunos):
    matches = {projeto: [] for projeto in projetos}
    alunos_livres = alunos
    proximo_pedido = {aluno: 0 for aluno in alunos}

    while len(alunos_livres) > 0:
        aluno_atual = alunos_livres[0]
        if proximo_pedido[aluno_atual] < len(preferencia_alunos[aluno_atual]):
            projeto_atual = preferencia_alunos[aluno_atual][proximo_pedido[aluno_atual]]
            proximo_pedido[aluno_atual]+=1

            if nota_alunos[aluno_atual] >= nota_projetos[projeto_atual]:
                if len(matches[projeto_atual]) < vagas_projetos[projeto_atual]:
                    matches[projeto_atual].append(aluno_atual)

                else:
                    for aluno in matches[projeto_atual]:  # fazer recursivo com uma opção para substituir cada item dos alunos no match atual, e maximizar
                        if nota_alunos[aluno] > nota_alunos[aluno_atual]:
                            matches[projeto_atual].remove(aluno)
                            alunos_livres.append(aluno)
                            matches[projeto_atual].append(aluno_atual)
                            break

        alunos_livres.pop(0)

        matches[projeto_atual].sort(key=lambda a: nota_alunos[a])
        #print(*[nota_alunos[a] for a in matches[projeto_atual]])

    return matches


read_file("./entradaProj2.24TAG.txt")

"""
# PARA TESTE DA LEITURA DO ARQUIVO
print(*alunos, *projetos)
print(*vagas_projetos.items())
print(*nota_projetos.items())
print(*preferencia_alunos.items())
print(*nota_alunos.items())
"""

results = []
matches = emparelhamento_estavel(alunos)
total = 0
for p, a in matches.items():
    #print(p + ":", *a)
    total+=len(a)
    if len(a) < vagas_projetos[p]:
        print("UEPA")
print(total)
results.append(total)

print(*results)
