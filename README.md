# Sistema de Recomendação
 
Sistema de recomendação de itens (livros, filmes, produtos) com três estratégias
intercambiáveis: filtragem colaborativa, filtragem baseada em conteúdo e um
recomendador híbrido. Projeto acadêmico de Engenharia de Software.

## Funcionamento do sistema

O sistema permitirá que usuários recebam recomendações de livros, filmes, jogos
e entre outros itens com base em seu histórico de preferências implícitas
(cliques, avaliações, etc).

## Tecnologias

- **Linguagem:** Python 3 + FastAPI + Scikit-learn
- **Dados:** Pandas para manipulação de dataset públicos (MoovieLens, Goodreads, etc)
- **Gerenciamento de dependências:** pip (`requirements.txt`)
- **Testes:** pytest
- **Banco de dados:** SQLite

## Arquitetura
 
```
src/recsys/
├── domain/          # Entidades do domínio (Usuario, Item, Interacao)
├── strategies/       # Strategy pattern: algoritmos de recomendação
├── repositories/     # Acesso a dados (interações, itens)
├── metrics/           # Avaliação de qualidade (precisão, recall)
└── api/               # Camada web (FastAPI)
```
