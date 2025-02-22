from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_mail import Mail
from appfile.config import Config



db = SQLAlchemy()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()
    mail.init_app(app)

    from appfile.routes import routes_main
    app.register_blueprint(routes_main)


    return app






