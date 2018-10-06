from flask import Flask
from config import config_by_name
from flask_bcrypt import Bcrypt
from flask_restful import Api

flask_bcrypt = Bcrypt()


def create_app(environment):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[environment])
    flask_bcrypt.init_app(app)

    from app.api.model import db
    db.init_app(app)

    from app.api.views import SendMessageView
    api = Api(app)
    api.add_resource(SendMessageView, '/api/v1.0/sendMessage')

    return app, db
