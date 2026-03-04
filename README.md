# Case Técnico - Pipeline de Dados e Dashboard Analítico (Fake Store API)

Este projeto implementa um pipeline completo de extração, tratamento, modelagem e visualização de dados utilizando a Fake Store API como fonte.

A solução contempla:

- Consumo de múltiplos endpoints da API
- Normalização de estruturas JSON aninhadas
- Tratamento de tipos de dados e consistência
- Modelagem dimensional (Star Schema)
- Criação de dimensão calendário
- Construção de métricas analíticas no Power BI utilizando DAX

O objetivo final é disponibilizar uma base estruturada para análise de usuários, produtos e receita por meio de um dashboard interativo.

---

# Arquitetura da Solução
Fake Store API
        ↓
Script Python (teste.py)
        ↓
Geração de arquivos TXT
        ↓
Importação no Power BI Desktop
        ↓
Dashboard Analítico


# Informações de Estrutura

/src
teste.py

/data
users.csv
products.csv
fato_transacoes.csv
dim_data.csv

dashboard_fake_store.pbix
requirements.txt
README.md
.gitignore


# Descrição das Pastas

- **/src** → Contém o script Python responsável pelo pipeline
- **/data** → Armazena os arquivos CSV gerados pelo pipeline
- **.pbix** → Arquivo do relatório Power BI

---

# Modelagem de Dados

O projeto segue modelo dimensional em estrela (Star Schema).

# Dimensões

- `users.csv` → Dimensão de usuários (d_users)
- `products.csv` → Dimensão de produtos (d_products)
- `dim_data.csv` → Dimensão calendário (d_date)

# Tabela Fato

- `fato_transacoes.csv` → Tabela fato de transações (f_transactions)

# Granularidade da Tabela Fato

Cada linha representa:

> 1 item de produto dentro de um carrinho (transação)

Essa decisão garante:
- Correta agregação de receita
- Possibilidade de análises por produto, categoria e usuário
- Compatibilidade com modelo estrela

# Relacionamentos no Power BI

- d_users (1) → (*) f_transactions  
- d_products (1) → (*) f_transactions  
- d_date (1) → (*) f_transactions  

---

# Como Executar o Projeto
py -m pip install -r requirements.txt
py teste.py