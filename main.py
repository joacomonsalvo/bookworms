from flask import Flask
from config import Config
from controller import controller

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar Blueprints
    app.register_blueprint(auth_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
