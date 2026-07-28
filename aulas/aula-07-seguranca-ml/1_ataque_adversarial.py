"""
Aula 7 - Seguranca em Machine Learning
Exemplo 1: ataque adversarial simples (evasao) contra um classificador

Ideia central: um modelo de ML pode ser enganado por uma perturbacao
MUITO PEQUENA e imperceptivel nos dados de entrada, mesmo sem alterar
o modelo em si. Isso e diferente de um "erro" do modelo - e uma
manipulacao DELIBERADA feita por um atacante que conhece (ou consegue
estimar) o gradiente do modelo.

Este script:
  1. Treina um classificador simples (regressao logistica) no dataset
     de digitos escritos a mao (sklearn.datasets.load_digits).
  2. Escolhe uma imagem corretamente classificada.
  3. Gera uma perturbacao adversarial usando o metodo FGSM
     (Fast Gradient Sign Method), um dos ataques mais classicos.
  4. Mostra que a imagem "quase identica" ao olho humano passa a ser
     classificada como outro digito.

Requer: scikit-learn, numpy (ja disponiveis no ambiente do curso)

Para rodar:
    python 1_ataque_adversarial.py
"""

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def treinar_modelo():
    """Treina uma regressao logistica multi-classe no dataset de digitos."""

    digitos = load_digits()
    X, y = digitos.data, digitos.target

    # Normaliza os pixels para o intervalo [0, 1], que e o espaco onde
    # vamos aplicar a perturbacao adversarial (imagem valida = pixels em [0,1])
    escalador = MinMaxScaler()
    X_normalizado = escalador.fit_transform(X)

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X_normalizado, y, test_size=0.2, random_state=42
    )

    modelo = LogisticRegression(max_iter=2000)
    modelo.fit(X_treino, y_treino)

    acuracia = modelo.score(X_teste, y_teste)
    print(f"Acuracia do modelo no conjunto de teste: {acuracia:.2%}")

    return modelo, X_teste, y_teste


def calcular_gradiente_da_perda(modelo: LogisticRegression, x: np.ndarray, classe_verdadeira: int) -> np.ndarray:
    """Calcula o gradiente da funcao de perda (log-loss) em relacao a
    entrada x, para o modelo de regressao logistica.

    Para uma regressao logistica multi-classe (softmax), o gradiente da
    perda de entropia cruzada em relacao a entrada e:
        grad = (probabilidades - one_hot(classe_verdadeira)) @ pesos
    """

    probabilidades = modelo.predict_proba(x.reshape(1, -1))[0]

    one_hot = np.zeros_like(probabilidades)
    one_hot[classe_verdadeira] = 1.0

    # modelo.coef_ tem shape (n_classes, n_features)
    gradiente = (probabilidades - one_hot) @ modelo.coef_

    return gradiente


def ataque_fgsm(modelo: LogisticRegression, x: np.ndarray, classe_verdadeira: int, epsilon: float) -> np.ndarray:
    """Fast Gradient Sign Method (Goodfellow et al., 2014).

    A perturbacao e: epsilon * sinal(gradiente da perda em relacao a x)

    Ou seja: move cada pixel um pouquinho (epsilon) na direcao que MAIS
    aumenta o erro do modelo - sem se importar com o "significado visual"
    daquele pixel.
    """

    gradiente = calcular_gradiente_da_perda(modelo, x, classe_verdadeira)
    perturbacao = epsilon * np.sign(gradiente)

    x_adversarial = x + perturbacao

    # mantem os pixels em um intervalo valido de imagem [0, 1]
    x_adversarial = np.clip(x_adversarial, 0.0, 1.0)

    return x_adversarial


if __name__ == "__main__":

    modelo, X_teste, y_teste = treinar_modelo()

    # Escolhe um exemplo que o modelo ja classifica corretamente
    indice = 0
    imagem_original = X_teste[indice]
    classe_verdadeira = y_teste[indice]

    predicao_original = modelo.predict(imagem_original.reshape(1, -1))[0]

    print()
    print(f"Digito verdadeiro ............ {classe_verdadeira}")
    print(f"Predicao ANTES do ataque ..... {predicao_original}")

    for epsilon in [0.0, 0.05, 0.1, 0.2, 0.3]:

        if epsilon == 0.0:
            imagem_teste = imagem_original
        else:
            imagem_teste = ataque_fgsm(modelo, imagem_original, classe_verdadeira, epsilon)

        predicao = modelo.predict(imagem_teste.reshape(1, -1))[0]

        diferenca_maxima_pixel = np.max(np.abs(imagem_teste - imagem_original))

        print(
            f"epsilon={epsilon:<5} -> predicao = {predicao}  "
            f"(maior alteracao em 1 pixel: {diferenca_maxima_pixel:.3f})"
        )

    print()
    print("Conclusao: com uma perturbacao pequena (epsilon baixo), quase")
    print("imperceptivel visualmente, o modelo pode passar a errar a")
    print("classificacao. Isso mostra por que modelos de ML expostos em")
    print("producao precisam de defesas especificas (ex.: adversarial")
    print("training, deteccao de entradas anomalas, validacao de entrada).")
