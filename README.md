# Sistema de Recomendação
 
Sistema de recomendação de itens (livros, filmes, produtos) com três estratégias
intercambiáveis: filtragem colaborativa, filtragem baseada em conteúdo e um
recomendador híbrido. Projeto acadêmico de Engenharia de Software.

## Funcionamento do sistema

O sistema permitirá que usuários recebam recomendações de livros, filmes, jogos
e entre outros itens com base em seu histórico de preferências implícitas
(cliques, avaliações, etc).

## Tecnologias

- **Linguagem:** Backend { Python 3 + FastAPI + Scikit-learn } // Frontend { React + Vite }
- **Dados:** Pandas para manipulação de dataset públicos (MoovieLens, Goodreads, etc)
- **Gerenciamento de dependências:** backend { pip (`requirements.txt`) } // front-end { npm }
- **Testes:** backend { pytest } // front-end { vitest }
- **Banco de dados:** SQLite

## Arquitetura
 
```
bend/
└── src/recsys/
    ├── domain/          # Entidades do domínio (Usuario, Item, Interacao)
    ├── strategies/       # Strategy pattern: algoritmos de recomendação
    ├── repositories/     # Acesso a dados (interações, itens)
    └── metrics/           # Avaliação de qualidade (precisão, recall)
fend/
└── src/
    └── components/        # Interfaces de Usuário
    ├── hooks/           # Funções de estados
    └── pages/           # Páginas do sistema
```
