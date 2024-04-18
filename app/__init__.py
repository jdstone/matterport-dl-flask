from flask import Flask
from config import config
from logging.handlers import RotatingFileHandler
import logging
import os


def create_app(config_class):
    app = Flask(__name__)

    app.config.from_object(config[config_class])

    ###################################################
    #### Register Blueprints
    ###################################################
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    ###################################################
    #### Error Logging to File - For Production
    ###################################################
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/matterport.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Matterport startup')

    return app
