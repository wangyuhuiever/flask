# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(env_name=None):
    app = Flask(__name__)
    app.config.from_pyfile('../settings.py')
    if env_name:
        if env_name in ['testing']:
            app.config.from_pyfile('../settings_test.py')


    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



