"""
Aula 4 - Representacao Binaria, Encoding e Base da Criptografia
Script complementar ao Aula_2/enconding.py do repositorio devscops.

Objetivo: mostrar, de forma bem visual, como um mesmo dado pode ser
representado em varios "formatos" (binario, hexadecimal, Base64) sem que
isso, sozinho, ofereca qualquer protecao - encoding NAO e seguranca.

Para rodar:
    python representacao_e_encoding.py
"""

import base64


def mostrar_representacoes(texto: str) -> None:
    """Imprime o mesmo texto em varias representacoes diferentes."""

    dados_utf8 = texto.encode("utf-8")

    binario = " ".join(f"{byte:08b}" for byte in dados_utf8)
    hexadecimal = dados_utf8.hex(" ")
    base64_str = base64.b64encode(dados_utf8).decode("ascii")

    print(f"Texto original .......... {texto}")
    print(f"Quantidade de bytes UTF-8  {len(dados_utf8)}")
    print(f"Binario ................. {binario}")
    print(f"Hexadecimal ............. {hexadecimal}")
    print(f"Base64 .................. {base64_str}")
    print("-" * 70)


def revertendo_base64(texto_base64: str) -> str:
    """Mostra que Base64 e reversivel por QUALQUER pessoa, sem chave nenhuma.

    Isso e o ponto central da aula: encoding e publico e reversivel,
    diferente de criptografia (precisa de chave) e de hashing
    (nao e reversivel).
    """

    dados_originais = base64.b64decode(texto_base64)
    return dados_originais.decode("utf-8")


if __name__ == "__main__":

    # Texto simples (so caracteres ASCII, 1 byte cada)
    mostrar_representacoes("FAAP")

    # Texto com acentuacao (mostra que UTF-8 usa mais de 1 byte
    # para alguns caracteres, ex.: 'ç' e 'ã')
    mostrar_representacoes("Segurança")

    # Texto com emoji (curiosidade: emojis podem ocupar 4 bytes em UTF-8)
    mostrar_representacoes("Cadeado 🔒")

    # Demonstracao de que Base64 NAO protege nada:
    # qualquer pessoa com o texto codificado consegue decodificar,
    # sem precisar de nenhuma senha ou chave.
    segredo_mal_guardado = base64.b64encode(
        "senha_do_banco=123456".encode("utf-8")
    ).decode("ascii")

    print("Alguem 'escondeu' uma credencial em Base64:")
    print(segredo_mal_guardado)
    print()
    print("Mas qualquer pessoa consegue reverter, sem chave nenhuma:")
    print(revertendo_base64(segredo_mal_guardado))
