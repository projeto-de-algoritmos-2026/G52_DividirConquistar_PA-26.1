import pandas as pd
from pathlib import Path

# Passo 1: Carregar o dataset e definir as colunas que voce quer utilizar no seu top ranking
def carregar_dataset():

    caminho_dataset = Path(__file__).resolve().parent.parent / "datasets" / "games.csv"
    df = pd.read_csv(caminho_dataset)

    colunas = [
        "title",
        "metacritic_score",
        "global_sales_million",
        "genre",
        "publisher",
        "platform",
        "estimated_revenue_million_usd",
        "user_score",
        "na_sales_million",
        "eu_sales_million",
        "jp_sales_million",
    ]
    df = df[colunas]
    # Jogos com notas altas, porem vendas baixas
    df["gem_score"] = df["metacritic_score"] / (df["global_sales_million"] + 1)
    # Jogos com vendas altas, porem notas baixas
    df["hype_score"] = df["global_sales_million"] / df["metacritic_score"]
    # Remove dados faltantes
    df = df.dropna()

    return df

# Caso queira testar o carregamento do dataset, descomente as linhas abaixo
# if __name__ == "__main__":
#     df = carregar_dataset()
#     print(df.head())
#     print(df.shape)
