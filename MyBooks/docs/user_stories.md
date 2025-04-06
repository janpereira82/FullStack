# User Stories - Sistema "Esse eu já li!"

## User Story 1: Logar usuário
**Como um** usuário do sistema,  
**Eu quero** fazer login na plataforma,  
**De modo que** eu possa acessar minha conta e todas as funcionalidades do sistema.

**Tamanho:** 3 pontos de história  
**Valor de Negócio (BV):** 8  
**Testes de Aceitação:**
- Verificar se o usuário consegue fazer login com credenciais válidas
- Verificar se o sistema exibe mensagem de erro para credenciais inválidas
- Verificar se o usuário é redirecionado para a página principal após o login

## User Story 2: Visualizar lista de livros
**Como um** usuário logado,  
**Eu quero** visualizar a lista de livros disponíveis,  
**De modo que** eu possa encontrar livros para marcar como lidos.

**Tamanho:** 2 pontos de história  
**Valor de Negócio (BV):** 7  
**Testes de Aceitação:**
- Verificar se a lista de livros é exibida corretamente
- Verificar se a paginação funciona corretamente (se houver muitos livros)
- Verificar se é possível filtrar livros por estilo/categoria

## User Story 3: Visualizar livro
**Como um** usuário logado,  
**Eu quero** visualizar os detalhes de um livro específico,  
**De modo que** eu possa conhecer mais informações sobre ele antes de marcá-lo como lido.

**Tamanho:** 2 pontos de história  
**Valor de Negócio (BV):** 5  
**Testes de Aceitação:**
- Verificar se todos os detalhes do livro são exibidos corretamente (título, autor, número de páginas, estilo, etc.)
- Verificar se o status de leitura do livro (lido/não lido) é exibido corretamente
- Verificar se há um botão para marcar o livro como lido

## User Story 4: Marcar leitura de livro
**Como um** usuário logado,  
**Eu quero** marcar um livro como lido,  
**De modo que** eu possa ganhar pontos e acompanhar meu progresso de leitura.

**Tamanho:** 5 pontos de história  
**Valor de Negócio (BV):** 10  
**Testes de Aceitação:**
- Verificar se o sistema registra corretamente o livro como lido
- Verificar se os pontos são calculados corretamente com base no número de páginas
- Verificar se o troféu é concedido ao atingir 5 livros do mesmo estilo
- Verificar se não é possível marcar o mesmo livro como lido mais de uma vez

## User Story 5: Visualizar ranking de usuários
**Como um** usuário logado,  
**Eu quero** visualizar o ranking dos 10 usuários com maior pontuação,  
**De modo que** eu possa ver minha posição em relação aos outros usuários.

**Tamanho:** 3 pontos de história  
**Valor de Negócio (BV):** 6  
**Testes de Aceitação:**
- Verificar se o ranking exibe os 10 usuários com maior pontuação em ordem decrescente
- Verificar se as informações de cada usuário (nome e pontuação) são exibidas corretamente
- Verificar se o ranking é atualizado quando há mudanças na pontuação dos usuários

## User Story 6: Visualizar pontos e troféus de usuário
**Como um** usuário logado,  
**Eu quero** visualizar meus pontos e troféus conquistados,  
**De modo que** eu possa acompanhar meu progresso e conquistas no sistema.

**Tamanho:** 3 pontos de história  
**Valor de Negócio (BV):** 8  
**Testes de Aceitação:**
- Verificar se os pontos do usuário são exibidos corretamente
- Verificar se todos os troféus conquistados são exibidos corretamente
- Verificar se há informações sobre como conquistar novos troféus
