# Case Técnico - Extração Fake Store API

Este repositório contém um script Python (`teste.py`) que extrai dados da Fake Store API e persiste em CSVs prontos para modelagem analítica.

Arquivos gerados:
- `users.csv` — dimensão `d_users`
- `products.csv` — dimensão `d_products`
- `d_date.csv` — dimensão de datas
- `fact_transactions.csv` — tabela fato (itens explodidos)

# Como rodar (Windows):
py -m pip install -r requirements.txt
py teste.py

