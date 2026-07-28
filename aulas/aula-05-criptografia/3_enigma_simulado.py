"""
Aula 5 - Criptografia Aplicada
Exemplo 3: Simulacao simplificada da maquina Enigma

A Enigma (usada pela Alemanha na 2a Guerra Mundial) e o exemplo classico
de criptografia ELETROMECANICA: ela usa rotores que giram a cada letra
digitada, um refletor e (na versao real) um painel de conexoes
(plugboard). Isso faz com que a mesma letra digitada duas vezes seguidas
seja cifrada de formas DIFERENTES - o grande avanco em relacao as
cifras de substituicao simples (Exemplo 2).

Esta e uma versao DIDATICA e simplificada (3 rotores + refletor +
plugboard), suficiente para demonstrar os conceitos de:
  - chave composta (posicao inicial dos rotores + fiacao + plugboard)
  - "estado" que muda a cada letra (os rotores giram)
  - simetria: a mesma configuracao que cifra tambem decifra
    (por isso a Enigma era pratica, mas tambem sua fraqueza matematica)

Para rodar:
    python 3_enigma_simulado.py
"""

from __future__ import annotations

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Rotor:
    """Um rotor com fiacao fixa e uma posicao (que gira a cada letra)."""

    def __init__(self, fiacao: str, entalhe: str, posicao_inicial: str = "A"):
        self.fiacao = fiacao  # substituicao de A..Z nessa ordem
        self.entalhe = entalhe  # letra em que, ao passar por ela, o
        # PROXIMO rotor tambem gira (como as "reentrancias" da Enigma real)
        self.posicao = ALFABETO.index(posicao_inicial)

    def girar(self) -> bool:
        """Gira o rotor uma posicao. Retorna True se passou pelo entalhe
        (o que faz o proximo rotor girar tambem)."""

        estava_no_entalhe = ALFABETO[self.posicao] == self.entalhe
        self.posicao = (self.posicao + 1) % 26
        return estava_no_entalhe

    def para_frente(self, letra: str) -> str:
        """Passagem do sinal 'entrando' no rotor (letra -> letra)."""

        deslocamento = self.posicao
        indice_entrada = (ALFABETO.index(letra) + deslocamento) % 26
        letra_fiacao = self.fiacao[indice_entrada]
        indice_saida = (ALFABETO.index(letra_fiacao) - deslocamento) % 26
        return ALFABETO[indice_saida]

    def para_tras(self, letra: str) -> str:
        """Passagem do sinal 'voltando' do refletor pelo rotor."""

        deslocamento = self.posicao
        indice_entrada = (ALFABETO.index(letra) + deslocamento) % 26
        letra_alfabeto = ALFABETO[indice_entrada]
        indice_na_fiacao = self.fiacao.index(letra_alfabeto)
        indice_saida = (indice_na_fiacao - deslocamento) % 26
        return ALFABETO[indice_saida]


class Enigma:
    """Maquina Enigma simplificada: 3 rotores + refletor + plugboard."""

    # Fiacoes inspiradas nos rotores historicos I, II e III
    ROTOR_I = ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    ROTOR_II = ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    ROTOR_III = ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")

    # Refletor B (simetrico: se A -> Y, entao Y -> A)
    REFLETOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

    def __init__(self, posicoes_iniciais: str = "AAA", plugboard: dict | None = None):
        self.rotor_esquerdo = Rotor(*self.ROTOR_I, posicoes_iniciais[0])
        self.rotor_meio = Rotor(*self.ROTOR_II, posicoes_iniciais[1])
        self.rotor_direito = Rotor(*self.ROTOR_III, posicoes_iniciais[2])
        self.plugboard = plugboard or {}

    def _plugboard_trocar(self, letra: str) -> str:
        return self.plugboard.get(letra, letra)

    def _girar_rotores(self) -> None:
        # O rotor da direita gira sempre; os outros giram por "arraste"
        # quando o rotor anterior passa pelo seu entalhe.
        passou_entalhe_direito = self.rotor_direito.girar()

        if passou_entalhe_direito:
            passou_entalhe_meio = self.rotor_meio.girar()

            if passou_entalhe_meio:
                self.rotor_esquerdo.girar()

    def cifrar_letra(self, letra: str) -> str:
        if letra not in ALFABETO:
            return letra  # espacos e pontuacao passam direto

        # 1) os rotores giram ANTES de cifrar (comportamento real da Enigma)
        self._girar_rotores()

        sinal = self._plugboard_trocar(letra)

        # 2) sinal passa pelos rotores da direita para a esquerda
        sinal = self.rotor_direito.para_frente(sinal)
        sinal = self.rotor_meio.para_frente(sinal)
        sinal = self.rotor_esquerdo.para_frente(sinal)

        # 3) reflete
        sinal = self.REFLETOR_B[ALFABETO.index(sinal)]

        # 4) sinal volta da esquerda para a direita
        sinal = self.rotor_esquerdo.para_tras(sinal)
        sinal = self.rotor_meio.para_tras(sinal)
        sinal = self.rotor_direito.para_tras(sinal)

        sinal = self._plugboard_trocar(sinal)

        return sinal

    def processar_texto(self, texto: str) -> str:
        return "".join(self.cifrar_letra(c) for c in texto.upper())


if __name__ == "__main__":

    mensagem_original = "ATAQUE AO AMANHECER"

    # A "chave do dia" seria: posicoes iniciais dos rotores + plugboard
    posicoes_iniciais = "AAA"
    plugboard = {"A": "F", "F": "A", "T": "G", "G": "T"}

    # Cifrando
    enigma_emissor = Enigma(posicoes_iniciais, plugboard)
    cifrado = enigma_emissor.processar_texto(mensagem_original)

    # Decifrando: para decifrar, basta montar OUTRA maquina com a MESMA
    # configuracao (mesmos rotores, mesma posicao inicial, mesmo plugboard)
    # e processar o texto cifrado - a Enigma e simetrica.
    enigma_receptor = Enigma(posicoes_iniciais, plugboard)
    decifrado = enigma_receptor.processar_texto(cifrado)

    print(f"Mensagem original ........ {mensagem_original}")
    print(f"Chave (posicao rotores) . {posicoes_iniciais}")
    print(f"Chave (plugboard) ....... {plugboard}")
    print(f"Mensagem cifrada ......... {cifrado}")
    print(f"Mensagem decifrada ....... {decifrado}")
    print()
    print("Repare: a letra 'A' se repete na mensagem original, mas e")
    print("cifrada de formas DIFERENTES cada vez - porque os rotores")
    print("giram a cada letra. Isso e o que tornava a Enigma tao mais")
    print("forte que uma simples cifra de substituicao (Exemplo 2).")
    print()
    print("Mesmo assim, a Enigma foi quebrada pelos Aliados (Turing e")
    print("equipe, em Bletchley Park) por ter uma fraqueza estrutural:")
    print("nenhuma letra podia ser cifrada nela mesma - uma pista que")
    print("ajudou a reduzir drasticamente o espaco de chaves testado.")
