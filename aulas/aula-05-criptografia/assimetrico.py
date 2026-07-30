# Gerar a chave privada com openssl genrsa -out chave_aula 2048
# Gerar a chave publica com openssl rsa -in chave_aula -pubout -out chave_aula.pub


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

# 1. Carregar as chaves (substitua pelas suas strings ou arquivos)

with open('chave_aula', 'rb') as arquivo_privado:
    dados_privados = arquivo_privado.read()
    chave_privada = load_pem_private_key(dados_privados, password=None)

with open('chave_aula.pub', 'rb') as arquivo_publico:
    dados_publicos = arquivo_publico.read()
    chave_publica = load_pem_public_key(dados_publicos)

texto_original = "Mensagem ultra secreta".encode()

# 2. Cifrar com a chave pública
texto_cifrado = chave_publica.encrypt(
    texto_original,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print('Texto cifrado: ', texto_cifrado.hex())

# 3. Decifrar com a chave privada
texto_decifrado = chave_privada.decrypt(
    texto_cifrado,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print('Texto decifrado: ', texto_decifrado.decode())