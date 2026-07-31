import base64
import io

import numpy as np

from flask import Blueprint, render_template, request
from PIL import Image
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


fgsm_bp = Blueprint(
    "fgsm",
    __name__,
    url_prefix="/fgsm"
)


# =========================================================
# Modelo
# =========================================================

# O load_digits guarda cada pixel como um inteiro de 0 a 16.
VALOR_MAXIMO_DO_PIXEL = 16.0

modelo = None


def treinar_modelo():
    """
    Treina a regressão logística usando o dataset
    de dígitos do scikit-learn.

    Os pixels são divididos por 16 (o valor máximo do
    dataset) para ficarem em [0, 1] — exatamente a mesma
    escala produzida por preparar_imagem().

    Essa consistência entre treino e inferência é
    essencial: antes o treino usava MinMaxScaler (uma
    escala por pixel) e a inferência dividia por 255, o
    que colocava o desenho em um espaço diferente do que
    o modelo aprendeu.
    """

    digitos = load_digits()

    X = digitos.data / VALOR_MAXIMO_DO_PIXEL

    y = digitos.target

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    modelo = LogisticRegression(
        max_iter=5000
    )

    modelo.fit(
        X_treino,
        y_treino
    )

    acuracia = modelo.score(
        X_teste,
        y_teste
    )

    # Depois de medir a acurácia em dados que o modelo
    # nunca viu, reajusta usando o dataset completo.
    modelo.fit(
        X,
        y
    )

    print(
        f"[FGSM] Acurácia: {acuracia:.2%}"
    )

    return modelo


def inicializar_modelo():
    global modelo

    if modelo is None:
        modelo = treinar_modelo()


# =========================================================
# FGSM
# =========================================================

def calcular_gradiente_da_perda(
    modelo,
    x,
    classe_verdadeira
):
    """
    Calcula o gradiente da função de perda em relação
    à entrada x.

    Para regressão logística multiclasses:

        grad =
            (probabilidades - one_hot) @ pesos
    """

    probabilidades = modelo.predict_proba(
        x.reshape(1, -1)
    )[0]

    one_hot = np.zeros_like(
        probabilidades
    )

    one_hot[classe_verdadeira] = 1.0

    gradiente = (
        probabilidades - one_hot
    ) @ modelo.coef_

    return gradiente


def ataque_fgsm(
    modelo,
    x,
    classe_verdadeira,
    epsilon
):
    """
    Fast Gradient Sign Method.

    x_adv = x + epsilon * sign(gradiente)
    """

    gradiente = calcular_gradiente_da_perda(
        modelo,
        x,
        classe_verdadeira
    )

    perturbacao = (
        epsilon *
        np.sign(gradiente)
    )

    x_adversarial = (
        x + perturbacao
    )

    x_adversarial = np.clip(
        x_adversarial,
        0.0,
        1.0
    )

    return (
        x_adversarial,
        gradiente,
        perturbacao
    )


# =========================================================
# Imagem
# =========================================================

# Lado do bitmap intermediário. O optdigits (dataset do
# load_digits) foi construído a partir de bitmaps 32x32
# divididos em blocos 4x4: cada pixel 8x8 é a contagem de
# pixels acesos do seu bloco, de 0 a 16.
LADO_INTERMEDIARIO = 32

LADO_DO_BLOCO = LADO_INTERMEDIARIO // 8


def preparar_imagem(imagem):

    """
    Converte o desenho para o mesmo formato do load_digits.

    Reproduz o pré-processamento original do optdigits:

        1. escala de cinza (fundo preto, dígito claro)
        2. recorta o dígito pela bounding box
        3. redimensiona para ocupar TODA a caixa 32x32,
           preservando a proporção, e centraliza
        4. média de cada bloco 4x4 -> matriz 8x8 em [0, 1]

    Dois detalhes importam para a acurácia:

        * no dataset o dígito ocupa a altura inteira dos
          8 pixels (não sobra margem). A versão anterior
          acrescentava 20% de margem e deixava o dígito
          pequeno demais no centro.

        * a média do bloco reproduz a "densidade de tinta"
          do dataset. Redimensionar direto para 8x8 com
          LANCZOS produzia contraste e espessura de traço
          diferentes dos que o modelo aprendeu.
    """

    # -----------------------------------------------------
    # Escala de cinza
    #
    # Imagens com transparência (PNG do canvas, uploads)
    # são compostas sobre fundo preto antes da conversão.
    # -----------------------------------------------------

    if imagem.mode in ("RGBA", "LA", "P"):

        imagem = imagem.convert("RGBA")

        fundo = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 255)
        )

        imagem = Image.alpha_composite(
            fundo,
            imagem
        )

    imagem = imagem.convert("L")

    pixels = np.asarray(
        imagem,
        dtype=np.float32
    )

    # -----------------------------------------------------
    # Fundo preto / dígito branco
    #
    # Uploads costumam ter fundo claro; o load_digits usa
    # fundo escuro. Nesse caso invertemos.
    # -----------------------------------------------------

    if pixels.mean() > 127:

        pixels = 255.0 - pixels

    # Limiar usado apenas para localizar o dígito.
    limiar = max(
        40.0,
        0.25 * float(pixels.max())
    )

    mascara = pixels > limiar

    if not np.any(mascara):

        raise ValueError(
            "Nenhum dígito foi encontrado no desenho."
        )

    # -----------------------------------------------------
    # Bounding box (sem margem)
    # -----------------------------------------------------

    ys, xs = np.where(
        mascara
    )

    recorte = pixels[
        ys.min():ys.max() + 1,
        xs.min():xs.max() + 1
    ]

    # -----------------------------------------------------
    # Redimensiona para preencher a caixa 32x32
    # -----------------------------------------------------

    altura, largura = recorte.shape

    escala = min(
        LADO_INTERMEDIARIO / altura,
        LADO_INTERMEDIARIO / largura
    )

    nova_altura = max(
        1,
        int(round(altura * escala))
    )

    nova_largura = max(
        1,
        int(round(largura * escala))
    )

    imagem_pil = Image.fromarray(
        np.clip(recorte, 0, 255).astype(np.uint8)
    )

    imagem_pil = imagem_pil.resize(
        (nova_largura, nova_altura),
        Image.Resampling.LANCZOS
    )

    reduzido = np.asarray(
        imagem_pil,
        dtype=np.float32
    )

    # -----------------------------------------------------
    # Centraliza dentro do bitmap 32x32
    # -----------------------------------------------------

    bitmap = np.zeros(
        (LADO_INTERMEDIARIO, LADO_INTERMEDIARIO),
        dtype=np.float32
    )

    y_offset = (
        LADO_INTERMEDIARIO - nova_altura
    ) // 2

    x_offset = (
        LADO_INTERMEDIARIO - nova_largura
    ) // 2

    bitmap[
        y_offset:y_offset + nova_altura,
        x_offset:x_offset + nova_largura
    ] = reduzido

    # -----------------------------------------------------
    # Média dos blocos 4x4 -> 8x8 normalizado em [0, 1]
    # -----------------------------------------------------

    blocos = bitmap.reshape(
        8,
        LADO_DO_BLOCO,
        8,
        LADO_DO_BLOCO
    )

    resultado = blocos.mean(
        axis=(1, 3)
    ) / 255.0

    return resultado.reshape(-1)


def carregar_imagem_upload(arquivo):

    imagem = Image.open(
        arquivo
    )

    return preparar_imagem(
        imagem
    )

def carregar_desenho(drawing):

    try:

        header, encoded = drawing.split(
            ",",
            1
        )

        imagem_bytes = base64.b64decode(
            encoded
        )

        imagem = Image.open(
            io.BytesIO(
                imagem_bytes
            )
        )

        return preparar_imagem(
            imagem
        )

    except Exception as erro:

        raise ValueError(
            f"Não foi possível processar o desenho: {erro}"
        )




def imagem_para_base64(
    imagem,
    ampliar=30
    ):

    imagem = np.asarray(
        imagem
    )

    imagem = np.squeeze(
        imagem
    )

    imagem = np.clip(
        imagem * 255,
        0,
        255
    ).astype(np.uint8)

    pil_image = Image.fromarray(
        imagem,
        mode="L"
    )

    pil_image = pil_image.resize(
        (
            8 * ampliar,
            8 * ampliar
        ),
        Image.Resampling.NEAREST
    )

    buffer = io.BytesIO()

    pil_image.save(
        buffer,
        format="PNG"
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return (
        "data:image/png;base64,"
        + encoded
    )


def obter_imagem_da_requisicao():
    """
    Devolve (vetor de 64 posições, desenho em base64).

    O campo "drawing" é preenchido pelo JavaScript a cada
    envio, então ele pode conter um canvas em branco. Nesse
    caso caímos para a imagem enviada por upload.
    """

    desenho = request.form.get("drawing") or ""

    arquivo = request.files.get("image")

    if desenho:

        try:

            return carregar_desenho(desenho), desenho

        except ValueError:

            # Canvas em branco: tenta o upload.
            desenho = ""

    if arquivo and arquivo.filename:

        return carregar_imagem_upload(arquivo), ""

    raise ValueError(
        "Desenhe um dígito ou envie uma imagem."
    )


def obter_probabilidades(imagem):

    probabilidades = modelo.predict_proba(
        imagem.reshape(1, -1)
    )[0]

    return [
        {
            "digito": digito,
            "probabilidade": float(
                probabilidades[digito] * 100
            )
        }
        for digito in range(10)
    ]


# =========================================================
# Rota
# =========================================================

@fgsm_bp.route(
"/classificar",
methods=["POST"]
)
def classificar():

    inicializar_modelo()

    try:

        imagem, desenho = obter_imagem_da_requisicao()

        # -------------------------------------------------
        # Classificação
        # -------------------------------------------------

        probabilidades = modelo.predict_proba(
            imagem.reshape(1, -1)
        )[0]

        predicao = int(
            np.argmax(
                probabilidades
            )
        )

        confianca = float(
            probabilidades[predicao] * 100
        )

        resultado = {

            "tipo": "classificacao",

            "sucesso": True,

            # Mantém o desenho original para que ele
            # possa ser restaurado no canvas após o reload
            "drawing": desenho,

            "predicao": predicao,

            "confianca": confianca,

            "imagem": imagem_para_base64(
                imagem.reshape(8, 8)
            ),

            "probabilidades":
                obter_probabilidades(imagem)

        }

        return render_template(
            "fgsm.html",
            resultado=resultado
        )

    except Exception as erro:

        return render_template(
            "fgsm.html",
            resultado={
                "erro": str(erro)
            }
        )


@fgsm_bp.route(
"/atacar",
methods=["POST"]
)
def atacar():

    inicializar_modelo()

    try:

        epsilon = float(
            request.form.get(
                "epsilon",
                "0.10"
            )
        )

        epsilon = max(
            0.0,
            min(epsilon, 0.5)
        )

        # -------------------------------------------------
        # Recupera imagem
        # -------------------------------------------------

        imagem_original, desenho = obter_imagem_da_requisicao()

        # -------------------------------------------------
        # Classificação original
        # -------------------------------------------------

        probabilidades_original = modelo.predict_proba(
            imagem_original.reshape(1, -1)
        )[0]

        predicao_original = int(
            np.argmax(
                probabilidades_original
            )
        )

        confianca_original = float(
            probabilidades_original[
                predicao_original
            ] * 100
        )

        # -------------------------------------------------
        # FGSM
        #
        # Usa a classificação original como classe-alvo.
        # -------------------------------------------------

        (
            imagem_adversarial,
            gradiente,
            perturbacao
        ) = ataque_fgsm(
            modelo,
            imagem_original,
            predicao_original,
            epsilon
        )

        # -------------------------------------------------
        # Nova classificação
        # -------------------------------------------------

        probabilidades_adversarial = modelo.predict_proba(
            imagem_adversarial.reshape(1, -1)
        )[0]

        predicao_adversarial = int(
            np.argmax(
                probabilidades_adversarial
            )
        )

        confianca_adversarial = float(
            probabilidades_adversarial[
                predicao_adversarial
            ] * 100
        )

        # -------------------------------------------------
        # Perturbação visual
        #
        # Como o FGSM usa apenas o SINAL do gradiente, o
        # módulo da perturbação é igual (epsilon) em quase
        # todos os pixels — mostrá-lo geraria uma imagem
        # praticamente branca.
        #
        # Mostramos então a direção da alteração:
        #
        #     branco = pixel clareado  (+ epsilon)
        #     preto  = pixel escurecido(- epsilon)
        #     cinza  = pixel inalterado
        # -------------------------------------------------

        perturbacao_visual = (
            np.sign(perturbacao) + 1.0
        ) / 2.0

        maior_perturbacao = float(
            np.max(
                np.abs(perturbacao)
            )
        )

        # -------------------------------------------------
        # Probabilidades
        # -------------------------------------------------

        probabilidades = []

        for digito in range(10):

            probabilidades.append({

                "digito": digito,

                "original": float(
                    probabilidades_original[
                        digito
                    ] * 100
                ),

                "adversarial": float(
                    probabilidades_adversarial[
                        digito
                    ] * 100
                )

            })

        # -------------------------------------------------
        # Resultado
        # -------------------------------------------------

        resultado = {

            "tipo": "ataque",

            "sucesso": True,

            # Mantém o desenho para restaurar o canvas.
            "drawing": desenho,

            "epsilon": epsilon,

            "predicao_original":
                predicao_original,

            "confianca_original":
                confianca_original,

            "predicao_adversarial":
                predicao_adversarial,

            "confianca_adversarial":
                confianca_adversarial,

            "ataque_sucesso":
                (
                    predicao_original
                    !=
                    predicao_adversarial
                ),

            "maior_perturbacao":
                maior_perturbacao,

            "imagem_original":
                imagem_para_base64(
                    imagem_original.reshape(8, 8)
                ),

            "perturbacao":
                imagem_para_base64(
                    perturbacao_visual.reshape(8, 8)
                ),

            "imagem_adversarial":
                imagem_para_base64(
                    imagem_adversarial.reshape(8, 8)
                ),

            "probabilidades":
                probabilidades

        }

        return render_template(
            "fgsm.html",
            resultado=resultado
        )

    except Exception as erro:

        return render_template(
            "fgsm.html",
            resultado={
                "erro": str(erro)
            }
        )

@fgsm_bp.route(
"/",
methods=["GET"]
)
def index():

    inicializar_modelo()

    return render_template("fgsm.html")