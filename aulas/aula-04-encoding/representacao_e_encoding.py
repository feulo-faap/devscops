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


def _decodificar_base64url(segmento: str) -> str:
    """Decodifica um segmento Base64URL (variante do Base64 usada em JWT).

    Base64URL troca os caracteres '+' e '/' por '-' e '_' (para o texto
    poder ir numa URL sem precisar de escaping) e costuma vir sem o
    padding '='. Por isso repomos o padding antes de decodificar com o
    Base64 "normal".
    """

    padding_necessario = (-len(segmento)) % 4
    segmento_com_padding = segmento + ("=" * padding_necessario)
    segmento_base64 = segmento_com_padding.replace("-", "+").replace("_", "/")
    return base64.b64decode(segmento_base64).decode("utf-8")


def demonstrar_jwt() -> None:
    """Decodifica um JWT (JSON Web Token) - o token usado por praticamente
    toda API com login que os alunos vao encontrar em projetos de IA.

    Um JWT tem 3 partes separadas por pontos, cada uma em Base64URL:
    cabecalho.corpo.assinatura. Cabecalho e corpo sao só encoding -
    qualquer pessoa decodifica sem chave nenhuma, exatamente como o
    Base64 que vimos no resto do script. A terceira parte (assinatura)
    e diferente: NAO decodifica para texto legivel, porque e o
    resultado de uma assinatura criptografica sobre as duas primeiras
    partes - isso e criptografia de verdade, e e assunto da Aula 5.
    """

    jwt_exemplo = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFuYSBTb3V6YSIsImFkbWluIjp0cnVlfQ."
        "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )

    cabecalho_b64, corpo_b64, assinatura_b64 = jwt_exemplo.split(".")

    print("JSON Web Token (JWT) - usado por quase toda API com login:")
    print(jwt_exemplo)
    print()
    print("Cabecalho decodificado (Base64URL -> JSON):")
    print(_decodificar_base64url(cabecalho_b64))
    print()
    print("Corpo / claims decodificado (Base64URL -> JSON):")
    print(_decodificar_base64url(corpo_b64))
    print()

    try:
        _decodificar_base64url(assinatura_b64)
    except UnicodeDecodeError:
        print("A assinatura NAO decodifica para texto legivel - ela nao e")
        print("Base64 de um JSON, e sim o resultado de uma assinatura")
        print("criptografica sobre o cabecalho e o corpo.")

    print()
    print("Ponto central: cabecalho e corpo de um JWT sao PUBLICOS e")
    print("reversiveis por qualquer pessoa, sem chave nenhuma - por isso")
    print("NUNCA se coloca informacao secreta (senha, numero de cartao)")
    print("dentro de um JWT. A seguranca dele esta inteira na assinatura.")


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

    print()
    print("=" * 70)
    print()
    demonstrar_jwt()
