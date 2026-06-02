from dataset import carregar_dataset
from mediana_das_medianas import top_k_por_coluna


def mostrar_colunas_numericas(df):
    colunas = list(df.select_dtypes(include="number").columns)
    print("===========================================================")
    print("\nColunas numericas disponiveis:")
    for indice, coluna in enumerate(colunas, start=1):
        print(f"{indice}. {coluna}")

    return colunas


def ler_inteiro(mensagem, minimo=1, maximo=None):
    while True:
        entrada = input(mensagem).strip()

        try:
            valor = int(entrada)
        except ValueError:
            print("Digite um numero inteiro valido.")
            continue

        if valor < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue

        if maximo is not None and valor > maximo:
            print(f"Digite um valor menor ou igual a {maximo}.")
            continue

        return valor


def escolher_coluna(colunas):
    while True:
        indice = ler_inteiro("\nEscolha um numero relativo a qual coluna voce quer selecionar: ", minimo=1, maximo=len(colunas))
        return colunas[indice - 1]


def confirmar(mensagem):
    while True:
        entrada = input(mensagem).strip().lower()

        if entrada in ["s", "sim"]:
            return True

        if entrada in ["n", "nao", "não"]:
            return False

        else:
            print("Responda com s ou n.")


def main():
    print("===========================================================")
    print("Carregando dataset...")
    df = carregar_dataset()
    print(f"Dataset carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.")

    while True:
        colunas = mostrar_colunas_numericas(df)
        coluna = escolher_coluna(colunas)
        quantidade = ler_inteiro(
            "\nQuantos itens voce quer no seu top? ",
            minimo=1,
            maximo=len(df)
        )
        mostrar_passos = confirmar("\nMostrar os passos da mediana das medianas? (s/n): ")

        top = top_k_por_coluna(
            df,
            coluna,
            quantidade,
            mostrar_passos=mostrar_passos
        )

        colunas_resultado = ["title", coluna]

        print(f"\nTop {quantidade} por '{coluna}':")
        print(top[colunas_resultado].to_string(index=False))

        if not confirmar("\nDeseja fazer outra consulta? (s/n): "):
            print("\nFim do pograma. Obrigado por usar!")
            break


if __name__ == "__main__":
    main()
