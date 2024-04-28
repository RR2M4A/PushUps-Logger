from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)

    # Configurando o banco de dados
    app.config["SECRET_KEY"] = 'secret_key'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

app = create_app()

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True)