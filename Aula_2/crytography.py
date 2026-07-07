import bcrypt # instlar o módulo com o comando: pip install bcrypt

senha = input("Digite a senha: ")

print("Senha digitada:", senha)

hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

print(hash_senha)

# Divide a string pelos cifrões
partes = hash_senha.decode('utf-8').split("$")

versao = partes[1]  # 2b
custo = partes[2]   # 12

# O resto do texto contém o Salt (primeiros 22 caracteres) e o Hash (os 31 finais)
salt_e_hash = partes[3]
salt_puro = salt_e_hash[:22]
hash_puro = salt_e_hash[22:]

print(f"Versão: {versao}")
print(f"Fator de Custo (Força): 2^{custo} iterações")
print(f"Salt Isolado: {salt_puro}")
print(f"Hash Isolado: {hash_puro}")

nova_senha = input("Digite a senha novamente para verificação: ")

salt_configurado = f"${versao}${custo}${salt_puro}".encode("utf-8")

novo_hash_completo = bcrypt.hashpw(nova_senha.encode('utf-8'), salt_configurado)

print("Novo hash gerado:", novo_hash_completo)
#print(
#    bcrypt.checkpw(
#        senha.encode('utf-8'),
#        hash_senha
#    )
#)