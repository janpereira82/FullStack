# Sistema "Esse eu já li!"

Sistema de gamificação para leitores onde os usuários podem marcar livros que já leram e ganhar pontos e troféus.

## Descrição

O sistema "Esse eu já li!" é um portal onde as pessoas podem marcar livros que já leram e ganhar pontos dentro de um sistema de gamificação. Ao fazerem o login no sistema, os usuários vêem uma lista de livros. Eles podem clicar para visualizar um livro e marcar que já leram aquele livro.

### Regras de Pontuação

- Cada livro lido vale 1 ponto base
- A cada 100 páginas que o livro tiver, ele vale um ponto adicional
  - Exemplos:
    - 72 páginas = 1 ponto
    - 124 páginas = 2 pontos
    - 350 páginas = 4 pontos

### Troféus

- A cada 5 livros que o usuário ler de um mesmo estilo, ele recebe um troféu "Leitor de #estilo#"
  - Exemplo: 5 livros do estilo "Ficção Científica" = troféu "Leitor de Ficção Científica"

### Funcionalidades

- Login de usuário
- Visualização de lista de livros
- Visualização de detalhes de um livro
- Marcação de livros como lidos
- Visualização de ranking dos 10 usuários com maior pontuação
- Visualização de pontos e troféus do usuário

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Inicialize o banco de dados:
   ```
   python app/init_db.py
   ```
4. Execute a aplicação:
   ```
   python app/app.py
   ```

## Documentação

A documentação do projeto está disponível na pasta `docs` e inclui:

- [User Stories](docs/user_stories.md)
- [Diagramas](docs/diagramas.md)
- [Planejamento das Iterações](docs/planejamento_iteracoes.md)

## Tecnologias Utilizadas

- Python
- Flask (Framework Web)
- SQLite (Banco de Dados)
- HTML/CSS/JavaScript (Frontend)
- Bootstrap (Framework CSS)

## Testes

Para executar os testes:
```
pytest
```
