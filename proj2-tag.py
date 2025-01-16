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


read_file("./entradaProj2.24TAG.txt")

"""
# PARA TESTE DA LEITURA DO ARQUIVO
print(*alunos, *projetos)
print(*vagas_projetos.items())
print(*nota_projetos.items())
print(*preferencia_alunos.items())
print(*nota_alunos.items())
"""


