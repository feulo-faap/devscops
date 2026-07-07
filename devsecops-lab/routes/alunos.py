from flask import Blueprint
from flask import request

from database.database import conectar

alunos_bp = Blueprint(
    "alunos",
    __name__
)


@alunos_bp.route("/alunos")
def alunos():

    conn = conectar()

    alunos = conn.execute(
        """
        SELECT *
        FROM alunos
        """
    ).fetchall()

    conn.close()

    html = """
    <h2>Lista de alunos</h2>

    <table border=1>

    <tr>

        <th>ID</th>
        <th>Nome</th>
        <th>Curso</th>
        <th>Nota</th>

    </tr>
    """

    for aluno in alunos:

        html += f"""

        <tr>

        <td>{aluno["id"]}</td>

        <td>

        <a href="/perfil/{aluno["id"]}">

        {aluno["nome"]}

        </a>

        </td>

        <td>{aluno["curso"]}</td>

        <td>{aluno["nota"]}</td>

        </tr>

        """

    html += "</table>"

    return html


@alunos_bp.route("/perfil/<id>")
def perfil(id):

    conn = conectar()

    # VULNERABILIDADE
    query = f"""
    SELECT *
    FROM alunos
    WHERE id={id}
    """

    aluno = conn.execute(query).fetchone()

    conn.close()

    if aluno is None:

        return "Aluno não encontrado."

    return f"""

    <h2>Perfil</h2>

    Nome: {aluno["nome"]}

    <br>

    Curso: {aluno["curso"]}

    <br>

    Nota: {aluno["nota"]}

    """

@alunos_bp.route("/buscar")
def buscar():

    nome = request.args.get("nome","")

    conn = conectar()

    query = f"""
    SELECT *
    FROM alunos
    WHERE nome LIKE '%{nome}%'
    """

    alunos = conn.execute(query).fetchall()

    conn.close()

    html = "<h2>Resultado</h2>"

    for aluno in alunos:

        html += f"""

        {aluno["nome"]}

        <br>

        """

    return html


@alunos_bp.route("/mensagem")
def mensagem():

    nome = request.args.get("nome","")

    return f"""

    <h2>

    Olá {nome}

    </h2>

    """

@alunos_bp.route("/comentarios")
def comentarios():

    conn = conectar()

    comentarios = conn.execute(
        """
        SELECT *
        FROM comentarios
        """
    ).fetchall()

    conn.close()

    html = "<h2>Comentários</h2>"

    html += """

    <form
    action="/novo-comentario"
    method="post">

    Nome

    <input
    name="autor">

    <br><br>

    Comentário

    <input
    name="comentario">

    <br><br>

    <button>

    Enviar

    </button>

    </form>

    <hr>

    """

    for comentario in comentarios:

        html += f"""

        <b>

        {comentario["autor"]}

        </b>

        <br>

        {comentario["comentario"]}

        <hr>

        """

    return html

    from flask import redirect

@alunos_bp.route("/novo-comentario",methods=["POST"])
def novo_comentario():

    autor=request.form["autor"]

    comentario=request.form["comentario"]

    conn=conectar()

    conn.execute(
        """
        INSERT INTO comentarios
        VALUES(NULL,?,?)
        """,
        (
            autor,
            comentario
        )
    )

    conn.commit()

    conn.close()

    return redirect("/comentarios")