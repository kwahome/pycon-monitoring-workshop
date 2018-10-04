from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

db = SQLAlchemy()


def create_app(environment):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[environment])
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
