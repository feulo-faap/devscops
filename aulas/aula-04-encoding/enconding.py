import base64


# 1. Processamento inicial padrão
texto_original = "Aa"
texto_original_encondado = texto_original.encode('utf-8')
texto_encondado_64 = base64.b64encode(texto_original_encondado)
texto_encondado_decodado = texto_encondado_64.decode()
print("Texto original:", texto_original)
print("Texto encondado em Decimal (ASCII):", " ".join(str(b) for b in texto_original_encondado))
print("Texto encondado em Hexadecimal:", texto_original_encondado.hex(' '))
print("Texto encondado em Binário:", " ".join("{:08b}".format(b) for b in texto_original_encondado))

# 2. Junta todos os bits originais em uma única string de '0's e '1's
todos_os_bits = "".join(f"{b:08b}" for b in texto_original_encondado)
print(f"Todos os bits unidos ({len(todos_os_bits)} bits): {todos_os_bits}")

# 3. Separa em grupos de 6 bits e trata o preenchimento com zeros
grupos_de_6 = []
for i in range(0, len(todos_os_bits), 6):
    bloco = todos_os_bits[i:i+6]
    
    # Se o bloco tem menos de 6 bits, preenche com zeros à direita
    if len(bloco) < 6:
        bits_faltando = 6 - len(bloco)
        bloco = bloco.ljust(6, '0')
        print(f"Bloco incompleto ajustado: adicionados {bits_faltando} zeros -> {bloco}")
        
    grupos_de_6.append(bloco)

print("Bits separados em grupos de 6:", " ".join(grupos_de_6))


# 4. Calcula e adiciona o padding '=' para fechar o bloco de 4 caracteres (24 bits)
# Cada 3 bytes geram 4 caracteres. Se temos menos grupos, precisamos de padding.
enquanto_falta_padding = len(grupos_de_6) % 4
if enquanto_falta_padding != 0:
    for _ in range(4 - enquanto_falta_padding):
        grupos_de_6.append("=") # Representação visual do padding

print("Grupos de 6 após aplicar o Padding (=):", " ".join(grupos_de_6))

# 5. NOVO: Converte cada grupo de 6 bits para o seu valor Decimal correspondente na tabela Base64
valores_decimais = []
for bloco in grupos_de_6:
    if bloco == "=":
        valores_decimais.append("-")  # Padding não tem valor numérico de dados
    else:
        # int(bloco, 2) converte a string binária (base 2) para um número inteiro (base 10)
        valores_decimais.append(str(int(bloco, 2)))

print("Valores Decimais para a tabela Base64 :", "  ".join(valores_decimais))
print("Texto encondado em bytes decodado:", texto_encondado_64.decode())
print("Texto encondado base64 em Binário (ASCII do resultado):", " ".join(f"{b:08b}" for b in texto_encondado_64))
print("Texto encondado base64 em Hexadecimal:", texto_encondado_64.hex(' '))
