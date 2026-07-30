from flask import Blueprint, render_template,session, abort
from database.database import conectar

admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route('/admin2')
def admin2():
    if not session.get("usuario") or not session.get("perfil") == 'admin':
        abort(403) 


    conn = conectar()


    
    usuarios = conn.execute(
        """
        SELECT *
        FROM usuarios
        """
    ).fetchall()
    
    conn.close()
    
    return render_template("admin2.html", usuarios=usuarios) 

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