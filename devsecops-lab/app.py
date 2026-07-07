from flask import Flask

import config

from routes.home import home_bp
from routes.auth import auth_bp
from routes.alunos import alunos_bp
from routes.admin import admin_bp

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(alunos_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)