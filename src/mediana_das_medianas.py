def _valor(item, coluna):
    return item[coluna]


def _nome_item(item):
    return item.get("title", str(item))


def _mostrar_item(item, coluna):
    return f"{_nome_item(item)} ({coluna}={_valor(item, coluna)})"


def _mediana_simples(itens, coluna):
    ordenados = sorted(itens, key=lambda item: _valor(item, coluna))
    return ordenados[len(ordenados) // 2]


def selecionar_k_esimo(
    itens,
    k,
    coluna,
    mostrar_passos=False,
    profundidade=0,
    max_grupos_print=3,
    max_profundidade_print=2,
    max_chamadas_print=5,
    contexto_print=None
):
    """
    Retorna o item que estaria na posicao k se a lista fosse ordenada pela coluna.
    k usa indice baseado em zero: k=0 retorna o menor item.
    """
    if not 0 <= k < len(itens):
        raise IndexError("k esta fora do intervalo da lista")

    if contexto_print is None:
        contexto_print = {"chamadas": 0}

    indentacao = "  " * profundidade
    pode_mostrar = (
        mostrar_passos
        and profundidade <= max_profundidade_print
        and contexto_print["chamadas"] < max_chamadas_print
    )

    if pode_mostrar:
        contexto_print["chamadas"] += 1
        print(f"\n{indentacao}Selecionando k={k} em uma lista com {len(itens)} itens")

    if len(itens) <= 5:
        ordenados = sorted(itens, key=lambda item: _valor(item, coluna))

        if pode_mostrar:
            valores = [_mostrar_item(item, coluna) for item in ordenados]
            print(f"{indentacao}Caso base ordenado: {valores}")
            print(f"{indentacao}Escolhido: {_mostrar_item(ordenados[k], coluna)}")

        return ordenados[k]

    grupos = [itens[i:i + 5] for i in range(0, len(itens), 5)]
    medianas = []

    if pode_mostrar:
        print(f"{indentacao}Dividindo em {len(grupos)} grupos de ate 5 itens")

    for indice, grupo in enumerate(grupos, start=1):
        ordenado = sorted(grupo, key=lambda item: _valor(item, coluna))
        mediana = ordenado[len(ordenado) // 2]
        medianas.append(mediana)

        if pode_mostrar and indice <= max_grupos_print:
            valores = [_valor(item, coluna) for item in ordenado]
            print(f"{indentacao}Grupo {indice} ordenado: {valores}")
            print(f"{indentacao}Mediana do grupo {indice}: {_mostrar_item(mediana, coluna)}")

    if pode_mostrar and len(grupos) > max_grupos_print:
        grupos_ocultos = len(grupos) - max_grupos_print
        print(f"{indentacao}... {grupos_ocultos} grupos ocultos para manter a saida legivel")

    if pode_mostrar:
        print(f"{indentacao}Buscando a mediana das {len(medianas)} medianas")

    pivo = selecionar_k_esimo(
        medianas,
        len(medianas) // 2,
        coluna,
        mostrar_passos,
        profundidade + 1,
        max_grupos_print,
        max_profundidade_print,
        max_chamadas_print,
        contexto_print
    )
    valor_pivo = _valor(pivo, coluna)

    if pode_mostrar:
        print(f"{indentacao}Pivo escolhido: {_mostrar_item(pivo, coluna)}")

    menores = [item for item in itens if _valor(item, coluna) < valor_pivo]
    iguais = [item for item in itens if _valor(item, coluna) == valor_pivo]
    maiores = [item for item in itens if _valor(item, coluna) > valor_pivo]

    if pode_mostrar:
        print(
            f"{indentacao}Particao: "
            f"{len(menores)} menores, {len(iguais)} iguais, {len(maiores)} maiores"
        )

    if k < len(menores):
        if pode_mostrar:
            print(f"{indentacao}O k esta nos menores")

        return selecionar_k_esimo(
            menores,
            k,
            coluna,
            mostrar_passos,
            profundidade + 1,
            max_grupos_print,
            max_profundidade_print,
            max_chamadas_print,
            contexto_print
        )

    if k < len(menores) + len(iguais):
        if pode_mostrar:
            print(f"{indentacao}O k caiu nos itens iguais ao pivo")

        return iguais[0]

    novo_k = k - len(menores) - len(iguais)

    if pode_mostrar:
        print(f"{indentacao}O k esta nos maiores. Novo k={novo_k}")

    return selecionar_k_esimo(
        maiores,
        novo_k,
        coluna,
        mostrar_passos,
        profundidade + 1,
        max_grupos_print,
        max_profundidade_print,
        max_chamadas_print,
        contexto_print
    )


def top_k_por_coluna(df, coluna, k=10, mostrar_passos=False):
    """
    Encontra os k maiores registros de um DataFrame usando mediana das medianas.
    """
    if coluna not in df.columns:
        raise ValueError(f"Coluna '{coluna}' nao existe no dataset")

    if k <= 0:
        return df.head(0)

    registros = df.to_dict("records")
    k = min(k, len(registros))

    # Para obter os k maiores, achamos o limite na posicao n-k da ordem crescente.
    if mostrar_passos:
        print(f"\nProcurando o top {k} pela coluna '{coluna}'")
        print(f"O limite do top {k} fica na posicao {len(registros) - k} da ordem crescente")

    limite = selecionar_k_esimo(
        registros,
        len(registros) - k,
        coluna,
        mostrar_passos=mostrar_passos
    )
    valor_limite = _valor(limite, coluna)

    if mostrar_passos:
        print(f"\nValor limite encontrado: {valor_limite}")
        print("Todos os itens acima desse limite entram no top.")

    maiores = [item for item in registros if _valor(item, coluna) > valor_limite]
    empatados = [item for item in registros if _valor(item, coluna) == valor_limite]
    top_registros = maiores + empatados[:k - len(maiores)]

    return df.__class__(top_registros).sort_values(by=coluna, ascending=False)


if __name__ == "__main__":
    from dataset import carregar_dataset

    df = carregar_dataset()
    top_10 = top_k_por_coluna(df, "global_sales_million", 10)

    print(top_10[["title", "global_sales_million", "genre", "publisher", "platform"]])
