from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect

import subprocess
import hashlib
import random
import tempfile
import requests
import os

ferramentas_bp = Blueprint(
    "ferramentas",
    __name__
)

@ferramentas_bp.route("/ping")
def ping():

    host = request.args.get("host","127.0.0.1")

    resultado = subprocess.check_output(

        f"ping -c 1 {host}",

        shell=True

    )

    return f"<pre>{resultado.decode()}</pre>"

@ferramentas_bp.route("/calculadora")
def calculadora():

    expressao = request.args.get("exp","1+1")

    resultado = eval(expressao)

    return str(resultado)

@ferramentas_bp.route("/hash")
def hash_md5():

    texto=request.args.get("texto","senha")

    h=hashlib.md5()

    h.update(texto.encode())

    return h.hexdigest()

@ferramentas_bp.route("/token")
def token():

    numero=random.randint(100000,999999)

    return str(numero)

@ferramentas_bp.route("/consulta")
def consulta():

    r=requests.get(

        "https://expired.badssl.com",

        verify=False

    )

    return r.text[:300]

@ferramentas_bp.route("/temp")
def temp():

    arquivo=tempfile.mktemp()

    return arquivo

@ferramentas_bp.route("/arquivo")
def arquivo():

    nome=request.args.get("nome")

    caminho=os.path.join(

        "static/uploads",

        nome

    )

    with open(caminho) as f:

        return f.read()
    
@ferramentas_bp.route("/upload")
def upload():

    return """

    <form

    method="POST"

    enctype="multipart/form-data"

    action="/enviar">

    <input

    type=file

    name=arquivo>

    <button>

    Enviar

    </button>

    </form>

    """

@ferramentas_bp.route(

"/enviar",

methods=["POST"]

)
def enviar():

    arquivo=request.files["arquivo"]

    arquivo.save(

        os.path.join(

            "static/uploads",

            arquivo.filename

        )

    )

    return redirect("/upload")