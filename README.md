# Case Técnico - Extração Fake Store API

Este repositório contém um script Python (`teste.py`) que extrai dados da Fake Store API e persiste em CSVs prontos para modelagem analítica.

Arquivos gerados:
- `users.csv` — dimensão `d_users`
- `products.csv` — dimensão `d_products`
- `d_date.csv` — dimensão de datas
- `fact_transactions.csv` — tabela fato (itens explodidos)

Como rodar (Windows):

```powershell
py -m pip install -r requirements.txt
py teste.py
```

Observações:
- Para carregar no Power BI, importe as dimensões e a tabela fato e monte o modelo em estrela.
- Para exportar ao BigQuery, posso adicionar script adicional se você fornecer o `project_id` e credenciais.
