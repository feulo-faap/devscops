import hashlib
import base64

texto_original = "Aa"
texto_original_encondado = texto_original.encode('utf-8')
texto_encondado_64 = base64.b64encode(texto_original_encondado)
texto_encondado_decodado = texto_encondado_64.decode()
print("Texto original:", texto_original)
print("Texto encondado:", texto_original_encondado.hex(' '))
print("Texto encondado em Binário:", " ".join(map("{:08b}".format, texto_original_encondado)))
print("Texto encondado em bytes:", texto_encondado_64.hex(' '))
print("Texto encondado em bytes decodado:", texto_encondado_64.decode())