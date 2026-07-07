from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from database.database import conectar

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login")
def login():

    return render_template("login.html")


@auth_bp.route("/autenticar", methods=["POST"])
def autenticar():

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conn = conectar()

    cursor = conn.cursor()

    # VULNERABILIDADE
    query = f"""
    SELECT *
    FROM usuarios
    WHERE usuario='{usuario}'
    """

    usuario_db = cursor.execute(query).fetchone()

    conn.close()

    if usuario_db is None:

        # ENUMERAÇÃO DE USUÁRIOS
        return "Usuário inexistente"

    if usuario_db["senha"] != senha:

        # ENUMERAÇÃO DE USUÁRIOS
        return "Senha incorreta"

    session["usuario"] = usuario

    session["perfil"] = usuario_db["perfil"]

    return f"""
    Login realizado.

    <br><br>

    <a href='/alunos'>
    Consultar alunos
    </a>
    """


@auth_bp.route("/logout")
def logout():

    session.clear()

    return "Logout realizado."