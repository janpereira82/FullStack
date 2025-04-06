# Diagramas do Sistema "Esse eu já li!"

## Justificativa dos Diagramas Escolhidos

Para este projeto, foram escolhidos dois diagramas principais para auxiliar na compreensão do sistema:

1. **Diagrama de Classes (Modelo de Domínio)**: Este diagrama foi escolhido para representar as entidades principais do sistema e seus relacionamentos. Ele ajuda a entender a estrutura de dados e as regras de negócio do sistema.

2. **Diagrama de Casos de Uso**: Este diagrama foi escolhido para representar as interações entre os usuários e o sistema. Ele ajuda a entender as funcionalidades disponíveis e como os usuários interagem com o sistema.

## Diagrama de Classes (Modelo de Domínio)

```
+----------------+       +----------------+       +----------------+
|     Usuário    |       |     Livro      |       |     Troféu     |
+----------------+       +----------------+       +----------------+
| id: int        |       | id: int        |       | id: int        |
| nome: str      |       | titulo: str    |       | nome: str      |
| email: str     |       | autor: str     |       | descricao: str |
| senha: str     |       | paginas: int   |       | estilo: str    |
| pontos: int    |       | estilo: str    |       +----------------+
+----------------+       | descricao: str |               ^
        |                +----------------+               |
        |                        ^                        |
        |                        |                        |
        v                        |                        |
+----------------+               |                        |
| LeituraLivro   |--------------+                        |
+----------------+                                       |
| id: int        |                                       |
| id_usuario: int|                                       |
| id_livro: int  |                                       |
| data: datetime |                                       |
+----------------+                                       |
        |                                                |
        |                                                |
        v                                                |
+----------------+                                       |
| TroféuUsuário  |---------------------------------------+
+----------------+
| id: int        |
| id_usuario: int|
| id_trofeu: int |
| data: datetime |
+----------------+
```

Este diagrama mostra as principais entidades do sistema:
- **Usuário**: Representa os usuários do sistema.
- **Livro**: Representa os livros disponíveis no sistema.
- **LeituraLivro**: Representa o registro de um livro lido por um usuário.
- **Troféu**: Representa os troféus que podem ser conquistados.
- **TroféuUsuário**: Representa os troféus conquistados por um usuário.

## Diagrama de Casos de Uso

```
                   +---------------------+
                   |                     |
                   |  Sistema "Esse eu   |
                   |     já li!"         |
                   |                     |
                   +---------------------+
                            ^
                            |
                            |
                  +---------+---------+
                  |                   |
                  |                   |
+------------+    |    +---------+    |    +------------+
|            |    |    |         |    |    |            |
|  Visitante |----+--->|  Login  |    |    |  Usuário   |
|            |    |    |         |    |    |  Logado    |
+------------+    |    +---------+    |    +------------+
                  |                   |           |
                  |                   |           |
                  |                   |           |
                  |                   |           v
                  |                   |    +------------+
                  |                   |    | Visualizar |
                  |                   |    | Lista de   |
                  |                   |    | Livros     |
                  |                   |    +------------+
                  |                   |           |
                  |                   |           |
                  |                   |           v
                  |                   |    +------------+
                  |                   |    | Visualizar |
                  |                   |    | Livro      |
                  |                   |    +------------+
                  |                   |           |
                  |                   |           |
                  |                   |           v
                  |                   |    +------------+
                  |                   |    | Marcar     |
                  |                   |    | Leitura de |
                  |                   |    | Livro      |
                  |                   |    +------------+
                  |                   |           |
                  |                   |           |
                  |                   |           v
                  |                   |    +------------+
                  |                   |    | Visualizar |
                  |                   |    | Ranking    |
                  |                   |    +------------+
                  |                   |           |
                  |                   |           |
                  |                   |           v
                  |                   |    +------------+
                  |                   |    | Visualizar |
                  |                   |    | Pontos e   |
                  |                   |    | Troféus    |
                  |                   |    +------------+
                  |                   |
                  +-------------------+
```

Este diagrama mostra as principais funcionalidades do sistema e como os usuários interagem com ele. O visitante pode apenas fazer login, enquanto o usuário logado pode acessar todas as funcionalidades do sistema.
