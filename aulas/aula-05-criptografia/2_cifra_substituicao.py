"""
Aula 5 - Criptografia Aplicada
Exemplo 2: Cifra de substituicao com alfabeto embaralhado

Em vez de deslocar o alfabeto (como na cifra de Cesar), aqui cada letra
e trocada por outra letra de um alfabeto embaralhado. A "chave" passa a
ser o proprio mapeamento entre as letras.

Isso aumenta MUITO o espaco de chaves (26! = mais de 4 x 10^26
possibilidades), tornando a forca bruta inviavel na pratica. Mas o
script tambem mostra por que essa cifra ainda e fraca contra
analise de frequencia de letras.

Para rodar:
    python 2_cifra_substituicao.py
"""

import random
import string
from collections import Counter

ALFABETO = string.ascii_lowercase


def gerar_chave_embaralhada(semente: int | None = None) -> dict:
    """Gera um mapeamento letra -> letra embaralhado (a chave secreta)."""

    letras_embaralhadas = list(ALFABETO)

    if semente is not None:
        random.seed(semente)

    random.shuffle(letras_embaralhadas)

    return dict(zip(ALFABETO, letras_embaralhadas))


def cifrar_substituicao(texto: str, chave: dict) -> str:
    return "".join(chave.get(c, c) for c in texto.lower())


def decifrar_substituicao(texto_cifrado: str, chave: dict) -> str:
    chave_inversa = {v: k for k, v in chave.items()}
    return "".join(chave_inversa.get(c, c) for c in texto_cifrado)


def analise_de_frequencia(texto_cifrado: str) -> None:
    """Mostra a frequencia de cada letra no texto cifrado.

    Em portugues e ingles, a letra 'e'/'a' tende a ser a mais frequente.
    Um atacante pode comparar a frequencia das letras cifradas com a
    frequencia esperada do idioma para comecar a 'adivinhar' a chave -
    isso e chamado de criptoanalise por frequencia.
    """

    contagem = Counter(c for c in texto_cifrado if c in ALFABETO)
    total = sum(contagem.values())

    print("Analise de frequencia das letras no texto cifrado:")

    for letra, quantidade in contagem.most_common(5):
        percentual = 100 * quantidade / total
        print(f"  '{letra}': {quantidade} ocorrencias ({percentual:.1f}%)")


if __name__ == "__main__":

    mensagem_original = (
        "a segurança da informação depende de confidencialidade "
        "integridade e disponibilidade"
    )

    chave = gerar_chave_embaralhada(semente=42)

    cifrado = cifrar_substituicao(mensagem_original, chave)
    decifrado = decifrar_substituicao(cifrado, chave)

    print(f"Mensagem original .... {mensagem_original}")
    print(f"Chave (mapa a-z) ..... {chave}")
    print(f"Mensagem cifrada ..... {cifrado}")
    print(f"Mensagem decifrada ... {decifrado}")
    print()

    analise_de_frequencia(cifrado)
    print()
    print("Conclusao: o espaco de chaves e enorme (26! possibilidades),")
    print("mas a estrutura estatistica do idioma ainda vaza informacao.")
    print("Isso motiva cifras modernas, sem essa fragilidade estatistica.")
