from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importer et enregistrer les routes
    from .routes import routes_app  as routes_app
    app.register_blueprint(routes_app)

    return app
