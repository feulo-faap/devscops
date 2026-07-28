"""
Aula 5 - Criptografia Aplicada
Exemplo 4: Criptografia simetrica moderna com AES

Depois de ver cifras classicas (Cesar), cifras de substituicao com
alfabeto embaralhado, e uma cifra eletromecanica (Enigma), chegamos a
criptografia simetrica MODERNA: o AES (Advanced Encryption Standard).

Diferencas centrais em relacao aos exemplos anteriores:
  - A chave e um numero binario gigante (aqui, 256 bits = 2^256
    possibilidades), nao um deslocamento pequeno nem um mapa de 26 letras.
  - O algoritmo opera sobre BYTES (qualquer dado: texto, imagem, arquivo),
    nao apenas sobre letras do alfabeto.
  - Usamos o modo AES-GCM, que ja inclui autenticacao: alem de cifrar,
    ele detecta se a mensagem foi alterada no caminho (integridade).

Requer a biblioteca 'cryptography' (ja disponivel no ambiente do curso):
    pip install cryptography

Para rodar:
    python 4_aes_exemplo.py
"""

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def cifrar_aes_gcm(mensagem: bytes, chave: bytes) -> tuple[bytes, bytes]:
    """Cifra 'mensagem' com AES-256-GCM.

    Retorna (nonce, texto_cifrado). O nonce e um valor aleatorio que
    DEVE ser diferente a cada cifragem com a mesma chave - por isso ele
    e gerado aqui e precisa ser guardado/enviado junto com o texto
    cifrado (ele nao e secreto, so precisa ser unico).
    """

    aesgcm = AESGCM(chave)
    nonce = os.urandom(12)  # 96 bits, recomendado para GCM

    texto_cifrado = aesgcm.encrypt(nonce, mensagem, associated_data=None)

    return nonce, texto_cifrado


def decifrar_aes_gcm(nonce: bytes, texto_cifrado: bytes, chave: bytes) -> bytes:
    """Decifra e AUTOMATICAMENTE verifica a integridade dos dados.

    Se o texto cifrado tiver sido alterado (mesmo 1 bit), esta funcao
    lanca uma excecao em vez de devolver um resultado incorreto -
    isso e a diferenca central para cifras classicas, que nao detectam
    adulteracao.
    """

    aesgcm = AESGCM(chave)
    return aesgcm.decrypt(nonce, texto_cifrado, associated_data=None)


if __name__ == "__main__":

    mensagem_original = "Nota do aluno 12345: 9.5 - aprovado".encode("utf-8")

    # Chave de 256 bits (32 bytes). Em um sistema real, isso NUNCA fica
    # hardcoded no codigo - viria de um cofre de segredos (ex.: Vault,
    # AWS KMS, variavel de ambiente protegida etc).
    chave = AESGCM.generate_key(bit_length=256)

    nonce, texto_cifrado = cifrar_aes_gcm(mensagem_original, chave)
    mensagem_decifrada = decifrar_aes_gcm(nonce, texto_cifrado, chave)

    print(f"Mensagem original ... {mensagem_original.decode()}")
    print(f"Chave (256 bits) .... {chave.hex()}")
    print(f"Nonce (96 bits) ..... {nonce.hex()}")
    print(f"Texto cifrado (hex) . {texto_cifrado.hex()}")
    print(f"Mensagem decifrada .. {mensagem_decifrada.decode()}")
    print()

    # Demonstracao da autenticacao: alteramos 1 byte do texto cifrado
    # e tentamos decifrar - deve falhar, em vez de devolver lixo.
    print("Simulando adulteracao de 1 byte no texto cifrado...")

    texto_cifrado_adulterado = bytearray(texto_cifrado)
    texto_cifrado_adulterado[0] ^= 0xFF  # inverte os bits do 1o byte

    try:
        decifrar_aes_gcm(nonce, bytes(texto_cifrado_adulterado), chave)
        print("ERRO: deveria ter falhado, mas nao falhou!")
    except Exception:
        print("Falha detectada corretamente: a integridade foi violada,")
        print("o AES-GCM recusou-se a devolver um resultado adulterado.")

    print()
    print("Comparando com os exemplos anteriores:")
    print(f"  Cesar ............. 25 chaves possiveis")
    print(f"  Substituicao ....... ~4 x 10^26 chaves possiveis (26!)")
    print(f"  Enigma (simplif.) .. rotores x posicoes x plugboard")
    print(f"  AES-256 ............ 2^256 chaves possiveis")
    print("  (um numero maior que o de atomos no universo observavel)")
