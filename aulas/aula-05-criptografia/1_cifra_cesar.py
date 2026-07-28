"""
Aula 5 - Criptografia Aplicada
Exemplo 1: Cifra de Cesar

A cifra de Cesar e uma das formas mais antigas de criptografia: cada letra
do alfabeto e deslocada um numero fixo de posicoes (a "chave").

Ela serve para introduzir dois conceitos centrais da aula:
  1. O que e uma cifra de substituicao.
  2. Por que uma chave pequena (aqui, so 25 possibilidades) e fragil:
     um computador quebra por forca bruta em milissegundos.

Para rodar:
    python 1_cifra_cesar.py
"""

ALFABETO = "abcdefghijklmnopqrstuvwxyz"


def cifrar_cesar(texto: str, deslocamento: int) -> str:
    """Cifra um texto deslocando cada letra em 'deslocamento' posicoes."""

    resultado = []

    for caractere in texto.lower():
        if caractere in ALFABETO:
            posicao = ALFABETO.index(caractere)
            nova_posicao = (posicao + deslocamento) % 26
            resultado.append(ALFABETO[nova_posicao])
        else:
            # numeros, espacos e pontuacao passam direto
            resultado.append(caractere)

    return "".join(resultado)


def decifrar_cesar(texto_cifrado: str, deslocamento: int) -> str:
    """Decifrar e apenas cifrar com o deslocamento invertido."""

    return cifrar_cesar(texto_cifrado, -deslocamento)


def forca_bruta_cesar(texto_cifrado: str) -> None:
    """Testa as 25 chaves possiveis e imprime todas as tentativas.

    Como a chave e um numero entre 1 e 25, um atacante nem precisa
    de um computador potente: em menos de um segundo, todas as
    possibilidades sao testadas.
    """

    print("Forca bruta - testando todas as chaves possiveis:")

    for chave_tentativa in range(1, 26):
        tentativa = decifrar_cesar(texto_cifrado, chave_tentativa)
        print(f"  chave {chave_tentativa:>2}: {tentativa}")


if __name__ == "__main__":

    mensagem_original = "ataque ao amanhecer"
    chave = 3

    cifrado = cifrar_cesar(mensagem_original, chave)
    decifrado = decifrar_cesar(cifrado, chave)

    print(f"Mensagem original .... {mensagem_original}")
    print(f"Chave (deslocamento) . {chave}")
    print(f"Mensagem cifrada ..... {cifrado}")
    print(f"Mensagem decifrada ... {decifrado}")
    print()

    forca_bruta_cesar(cifrado)
    print()
    print("Conclusao: com apenas 25 chaves possiveis, a cifra de Cesar")
    print("e trivialmente quebrada. Isso motiva cifras mais robustas.")
