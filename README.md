Código desenvolvido para o projeto 2 da disciplina Teoria e Aplicação de Grafos, no semestre 2024.2 na Universidade de Brasília.

# Projeto 2

Por: Elis Rodrigues Borges - 231018875

O objetivo deste projeto é implementar um algoritmo de emparelhamento estável máximo para um grafo bipartido, no contexto do problema SPA (Student-Project Allocation). Ele foi desenvolvido em Python. O código-fonte da solução está no arquivo ```proj2-tag.py```, e os dados de entrada fornecidos pelo professor estão no arquivo ```entradaProj2.24TAG.txt```.

A solução para encontrar um emparelhamento estável entre alunos e projetos foi baseada no algoritmo de Gale-Shapley. No entanto, foram feitas algumas modificações em relação ao algoritmo original, de forma a considerar a nota dos alunos. A implementação do algoritmo de Gale-Shapley assume que os alunos poderiam se matricular em qualquer um dos projetos na sua lista de preferências, porém, neste problema, o aluno só pode fazer isso se sua nota for maior ou igual ao requisito mínimo para o projeto. Além disso, os projetos não oferecem uma lista de preferência de alunos, ao contrário do que ocorre tanto no problema HR (Hospitals/Residents), que o algoritmo de Gale-Shapley resolve, quanto nas soluções do problema SPA discutidas no artigo _Two algorithms for the student-project allocation problem_, fornecido pelo professor. Dessa forma, para gerar um emparelhamento estável, foi considerado que os projetos preferem os alunos com as maiores notas.

Tendo um algoritmo que gera um emparelhamento estável, resta encontrar o máximo. Para isso, seria necessário gerar um emparelhamento estável para cada permutação distinta da lista de alunos, tendo em vista que o algoritmo de Gale-Shapley gera emparelhamentos diferentes a depender da ordem da lista de proponentes (no caso, os alunos). Contudo, devido ao tamanho da lista de alunos, não foi possível testar todas as permutações. Para tentar chegar a um resultado próximo do máximo, foram testadas 1000 permutações aleatórias da lista de alunos, e o maior emparelhamento estável gerado por elas foi selecionado como solução do problema.

Uma documentação mais detalhada do passo a passo do algoritmo utilizado pode ser encontrada nos comentários do código fonte.

Referências:
Abraham, D.J. and Irving, R.W. and Manlove, D.F. (2007). Two algorithms for the student-project allocation problem.
Slides de aula fornecidos pelo prof. Díbio.