"""
Objetivo:

Script para extrair e normalizar dados da Fake Store API.
Produzir CSVs estruturados em formato dimensional
(dimensões e tabela fato) prontos para modelagem analítica.
(usuarios, produtos, carrinhos, fato_transacoes e dim_data).
"""

import os
import requests
import pandas as pd

BASE_URL = "https://fakestoreapi.com"


def get_data(endpoint: str):

    #Faz uma requisição GET para o endpoint fornecido da Fake Store API.

    response = requests.get(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()
    return response.json()


def process_users():

    # Extrai e normaliza os dados de usuários.

    users = get_data("users")
    df_users = pd.json_normalize(users)

    df_users.rename(columns={
        "address.city": "cidade",
        "address.street": "rua",
        "address.number": "numero",
        "address.zipcode": "cep",
        "address.geolocation.lat": "latitude",
        "address.geolocation.long": "longitude",
        "name.firstname": "primeiro_nome",
        "name.lastname": "sobrenome"
    }, inplace=True)

    df_users["nome_completo"] = df_users["primeiro_nome"] + " " + df_users["sobrenome"]

    df_users = df_users[
        [
            "id",
            "nome_completo",
            "username",
            "email",
            "phone",
            "cidade",
            "rua",
            "numero",
            "cep",
            "latitude",
            "longitude"
        ]
    ]

    df_users = df_users.astype({
        "id": "int64",
        "numero": "int64"
    })

    df_users.fillna("", inplace=True)

    return df_users


def process_products():

    # Extrai e normaliza os dados de produtos.

    products = get_data("products")
    df_products = pd.json_normalize(products)

    df_products.rename(columns={
        "rating.rate": "avaliacao_media",
        "rating.count": "quantidade_avaliacoes"
    }, inplace=True)

    df_products = df_products[
        [
            "id",
            "title",
            "category",
            "price",
            "avaliacao_media",
            "quantidade_avaliacoes"
        ]
    ]

    df_products = df_products.astype({
        "id": "int64",
        "price": "float64",
        "avaliacao_media": "float64",
        "quantidade_avaliacoes": "int64"
    })

    df_products.fillna(0, inplace=True)

    return df_products


def process_carts(products_df):

    # Extrai e normaliza os carrinhos e calcula valores.

    carts = get_data("carts")
    df_carts = pd.json_normalize(carts)

    df_carts["date"] = pd.to_datetime(df_carts["date"])

    df_carts = df_carts.explode("products")

    products_expanded = pd.json_normalize(df_carts["products"]).reset_index(drop=True)
    df_carts = df_carts.drop(columns=["products"]).reset_index(drop=True)
    df_carts = pd.concat([df_carts, products_expanded], axis=1)

    df_carts.rename(columns={
        "productId": "id_produto",
        "quantity": "quantidade"
    }, inplace=True)

    df_carts = df_carts.astype({
        "id": "int64",
        "userId": "int64",
        "id_produto": "int64",
        "quantidade": "int64"
    })

    df_carts = df_carts.merge(
        products_df[["id", "price"]],
        left_on="id_produto",
        right_on="id",
        how="left"
    )

    df_carts.rename(columns={
        "id_x": "id_carrinho",
        "userId": "id_usuario",
        "price": "preco_unitario"
    }, inplace=True)

    df_carts["valor_total"] = df_carts["quantidade"] * df_carts["preco_unitario"]

    df_carts = df_carts[
        [
            "id_carrinho",
            "id_usuario",
            "date",
            "id_produto",
            "quantidade",
            "preco_unitario",
            "valor_total"
        ]
    ]

    df_carts.fillna(0, inplace=True)

    return df_carts


def main():
    print("Processando usuários...")
    df_users = process_users()

    print("Processando produtos...")
    df_products = process_products()

    print("Processando carrinhos...")
    df_carts = process_carts(df_products)

    print("Salvando arquivos CSV...")
    base_dir = os.path.dirname(__file__)


    # RETORNO USUÁRIOS
    df_usuarios = df_users.rename(columns={
        "id": "id_usuario",
        "username": "usuario",
        "email": "email",
        "phone": "telefone"
    })

    df_usuarios.to_csv(os.path.join(base_dir, "users.csv"), index=False)


    # RETORNO PRODUTOS
    df_produtos = df_products.rename(columns={
        "id": "id_produto",
        "title": "titulo",
        "category": "categoria",
        "price": "preco_unitario"
    })

    df_produtos.to_csv(os.path.join(base_dir, "products.csv"), index=False)


    # FATO TRANSACOES
    df_fato = df_carts.rename(columns={
        "date": "data_hora"
    })

    # Converter data_hora para apenas data (remover horas)
    df_fato["data_hora"] = pd.to_datetime(df_fato["data_hora"]).dt.date

    df_fato.to_csv(os.path.join(base_dir, "fato_transacoes.csv"), index=False)


    # RETORNO DATA
    dim_data = (
        pd.to_datetime(df_fato["data_hora"])
        .drop_duplicates()
        .sort_values()
        .to_frame(name="data_hora")
    )

    dim_data["data"] = dim_data["data_hora"].dt.date
    dim_data["ano"] = dim_data["data_hora"].dt.year
    dim_data["mes"] = dim_data["data_hora"].dt.month
    dim_data["dia"] = dim_data["data_hora"].dt.day
    dim_data["dia_semana"] = dim_data["data_hora"].dt.day_name()
    dim_data["semana_iso"] = dim_data["data_hora"].dt.isocalendar().week

    dim_data.to_csv(os.path.join(base_dir, "dim_data.csv"), index=False)

    print("Processo finalizado com sucesso!")


if __name__ == "__main__":
    main()