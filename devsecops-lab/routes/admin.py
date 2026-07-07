from flask import Blueprint
from database.database import conectar

admin_bp = Blueprint(
    "admin",
    __name__
)

# VULNERABILIDADE
# Não existe autenticação.
@admin_bp.route("/admin")
def admin():

    conn = conectar()

    usuarios = conn.execute(
        """
        SELECT *
        FROM usuarios
        """
    ).fetchall()

    conn.close()

    html = "<h2>Painel Administrativo</h2>"

    html += "<table border=1>"

    html += """
    <tr>

    <th>Usuário</th>

    <th>Senha</th>

    <th>Perfil</th>

    </tr>
    """

    for usuario in usuarios:

        html += f"""

        <tr>

        <td>{usuario["usuario"]}</td>

        <td>{usuario["senha"]}</td>

        <td>{usuario["perfil"]}</td>

        </tr>

        """

    html += "</table>"

    return html