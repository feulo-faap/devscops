from flask import Flask

import config

from routes.home import home_bp
from routes.auth import auth_bp
from routes.alunos import alunos_bp
from routes.admin import admin_bp
from routes.ferramentas import ferramentas_bp
from routes.fgsm import fgsm_bp

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(alunos_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(ferramentas_bp)
app.register_blueprint(fgsm_bp)

from flask import render_template

@app.errorhandler(404)
def pagina404(e):

    return (render_template("404.html"), 404)

if __name__ == "__main__":
    app.run(debug=True)