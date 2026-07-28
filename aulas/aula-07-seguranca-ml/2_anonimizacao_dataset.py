"""
Aula 7 - Seguranca em Machine Learning
Exemplo 2: anonimizacao e pseudonimizacao de um dataset

Cenario: temos um dataset de alunos (parecido com a tabela 'alunos' do
devsecops-lab) que sera usado para treinar um modelo de IA (ex.: prever
risco de evasao escolar). Antes de compartilhar esse dataset com uma
equipe de ciencia de dados (ou de publica-lo), precisamos reduzir o
risco de reidentificacao das pessoas.

Este script mostra 3 tecnicas, da mais fraca a mais forte:
  1. Pseudonimizacao: troca identificadores diretos (nome, e-mail) por
     um codigo (hash). Ainda e REVERSIVEL se alguem tiver a tabela
     original ou souber testar valores (ataque de dicionario) - por
     isso NAO e o mesmo que anonimizacao.
  2. Generalizacao: transforma valores especificos (idade exata, nota
     exata) em faixas (ex.: 18-24 anos), reduzindo a granularidade.
  3. Adicao de ruido (privacidade diferencial simplificada): adiciona
     uma pequena variacao aleatoria a valores numericos, dificultando
     ainda mais a reidentificacao a partir de uma unica consulta.

Para rodar:
    python 2_anonimizacao_dataset.py
"""

import hashlib
import random

DATASET_ORIGINAL = [
    {"nome": "Ana Souza", "email": "ana.souza@exemplo.com", "idade": 21, "nota": 8.7, "cidade": "São Paulo"},
    {"nome": "Bruno Lima", "email": "bruno.lima@exemplo.com", "idade": 23, "nota": 6.2, "cidade": "Campinas"},
    {"nome": "Carla Dias", "email": "carla.dias@exemplo.com", "idade": 19, "nota": 9.1, "cidade": "São Paulo"},
    {"nome": "Diego Alves", "email": "diego.alves@exemplo.com", "idade": 25, "nota": 5.4, "cidade": "Santos"},
]


def pseudonimizar(dataset: list[dict], sal: str) -> list[dict]:
    """Troca nome e e-mail por um hash (pseudonimo).

    O 'sal' (valor secreto adicional) impede que alguem de fora recrie
    o mesmo hash para tentar 'adivinhar' quem e cada pessoa a partir de
    uma lista de nomes conhecidos (ataque de dicionario).
    """

    dataset_pseudonimizado = []

    for registro in dataset:
        identificador_original = registro["email"] + sal
        pseudonimo = hashlib.sha256(identificador_original.encode()).hexdigest()[:10]

        novo_registro = dict(registro)
        del novo_registro["nome"]
        del novo_registro["email"]
        novo_registro["id_pseudonimo"] = pseudonimo

        dataset_pseudonimizado.append(novo_registro)

    return dataset_pseudonimizado


def generalizar_idade(idade: int) -> str:
    faixa_inicial = (idade // 5) * 5
    return f"{faixa_inicial}-{faixa_inicial + 4} anos"


def generalizar_nota(nota: float) -> str:
    if nota >= 7:
        return "aprovado (>= 7.0)"
    elif nota >= 5:
        return "recuperacao (5.0 - 6.9)"
    else:
        return "reprovado (< 5.0)"


def generalizar(dataset: list[dict]) -> list[dict]:
    """Reduz a granularidade de campos que poderiam, sozinhos ou
    combinados, ajudar a reidentificar uma pessoa (idade exata) ou
    revelar informacao sensivel de forma muito precisa (nota exata).
    """

    dataset_generalizado = []

    for registro in dataset:
        novo_registro = dict(registro)
        novo_registro["idade"] = generalizar_idade(registro["idade"])
        novo_registro["nota"] = generalizar_nota(registro["nota"])
        dataset_generalizado.append(novo_registro)

    return dataset_generalizado


def adicionar_ruido_numerico(valor: float, amplitude: float, semente: int) -> float:
    random.seed(semente)
    ruido = random.uniform(-amplitude, amplitude)
    return round(valor + ruido, 2)


def anonimizar_dataset_completo(dataset: list[dict], sal: str) -> list[dict]:
    """Aplica as 3 tecnicas em sequencia: pseudonimizacao -> generalizacao
    -> ruido (aplicado aqui sobre a nota original, antes de generalizar,
    apenas para fins didaticos de mostrar cada tecnica isoladamente)."""

    dataset_pseudonimizado = pseudonimizar(dataset, sal)
    dataset_final = generalizar(dataset_pseudonimizado)

    return dataset_final


if __name__ == "__main__":

    print("=== Dataset ORIGINAL (dados pessoais expostos) ===")
    for registro in DATASET_ORIGINAL:
        print(registro)

    print()
    print("=== Passo 1: apenas pseudonimizado (ainda reidentificavel) ===")
    sal_secreto = "sal-institucional-2026"
    pseudonimizado = pseudonimizar(DATASET_ORIGINAL, sal_secreto)
    for registro in pseudonimizado:
        print(registro)

    print()
    print("=== Passo 2: pseudonimizado + generalizado (mais protegido) ===")
    anonimizado = anonimizar_dataset_completo(DATASET_ORIGINAL, sal_secreto)
    for registro in anonimizado:
        print(registro)

    print()
    print("=== Demonstracao de ruido numerico (privacidade diferencial simplificada) ===")
    for i, registro in enumerate(DATASET_ORIGINAL):
        nota_com_ruido = adicionar_ruido_numerico(registro["nota"], amplitude=0.5, semente=i)
        print(f"  nota original: {registro['nota']:<4} -> nota com ruido: {nota_com_ruido}")

    print()
    print("Ponto de atencao: mesmo depois da pseudonimizacao, se a cidade")
    print("'Santos' aparecer para apenas 1 pessoa no dataset, ela pode ser")
    print("reidentificada por 'ataque de correlacao' (cruzando com outras")
    print("bases publicas). Isso e chamado de k-anonimidade insuficiente -")
    print("por isso tecnicas de generalizacao e ruido sao usadas em conjunto,")
    print("e nao uma tecnica isolada.")
