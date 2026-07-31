from flask import Blueprint, request, render_template, redirect


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

    return render_template("alunos.html", alunos=alunos)


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
    WHERE nome ='{nome}'
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

    return render_template("comentarios.html", comentarios=comentarios)


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