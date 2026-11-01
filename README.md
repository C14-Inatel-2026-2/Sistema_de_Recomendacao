# Sistema de Recomendação
 
Sistema de recomendação de itens (livros, filmes, produtos, etc) com três estratégias intercambiáveis: filtragem colaborativa, filtragem baseada em conteúdo e um recomendador híbrido. Projeto acadêmico de Engenharia de Software.

## Funcionamento do sistema

O sistema permitirá que usuários recebam recomendações de diferentes itens com base em seu histórico de avaliações. O histórico de outros usuários cadastrado no sistema também é utilizado para compor as recomendações.

## Tecnologias

- **Linguagem:** Backend { Python 3 + FastAPI } // Frontend { React + Vite }
- **Gerenciamento de dependências:** backend { pip (`requirements.txt`) } // front-end { npm (`package.json`) }
- **Testes:** backend { pytest } // front-end { vitest }
- **Banco de dados:** SQLite

## Arquitetura
 
```
bend/
└── src/recsys/
    ├── api/             # Aplicação, rotas e esquemas dos dados
    ├── domain/          # Entidades do domínio (Usuario, Item, Interacao)
    ├── strategies/      # Strategy pattern: algoritmos de recomendação
    ├── repositories/    # Acesso a dados (interações, itens)
    └── metrics/         # Avaliação de qualidade (precisão, recall)
fend/
└── src/
    ├── components/      # Interfaces de Usuário
    ├── hooks/           # Funções de estados
    └── pages/           # Páginas do sistema

jenkins/                 # Configurações em código de Jenkins
```

## Instalaçao

- Faça uso do Makefile
- `make install` para instalar dependências
- `make dev` para compilar e executar
- Abrir `http://localhost:5173`

## Requisitos Funcionais

|                                Requisito                                | Prioridade |          Situação        |
|:-----------------------------------------------------------------------:|:----------:|:------------------------:|
|                       Cadastrar e listar usuários                       |    Baixa   | API entregue, UI parcial |
|                         Cadastrar e listar itens                        |    Baixa   | API entregue, UI parcial |
|                       Registrar avaliação de 0 a 5                      |    Alta    |         Entregue         |
|               Reavaliar um item: vale a nota mais recente               |    Média   |         Entregue         |
|            Consultar somente últimas avaliações de um usuário           |    Média   |         Entregue         |
| Gerar recomendações por 3 estratégias (colaborativa, conteúdo, híbrida) |    Média   |         Entregue         |
|                   Nunca recomendar itens já avaliados                   |    Média   |         Entregue         |
|                        Autenticar usuário (login)                       |    Alta    |         Planejado        |

## Requisitos Não Funcionais

|     Categoria     |                                              Requisito                                              |
|:-----------------:|:---------------------------------------------------------------------------------------------------:|
|  Manutenibilidade | Estratégias intercambiáveis (Strategy + Factory); acesso a dados através de interfaces (Repository) |
|   Testabilidade   |       Memória e SQLite devem se comportar de forma idêntica; testes unitários e de integração       |
| Configurabilidade |               CORS e URL da API por variáveis de ambiente (CORS_ORIGINS, VITE_API_URL)              |
|  Entrega contínua |            Pipeline Jenkins com build, testes, relatórios e deploy automático só na main            |
| Reprodutibilidade |                               Dependências com versões fixas e npm ci                               |

