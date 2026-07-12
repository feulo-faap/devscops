from flask import Blueprint, render_template
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

    return render_template("admin.html", usuarios=usuarios)