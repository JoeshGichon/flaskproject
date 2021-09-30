from posix import environ
from src.constants.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db
from flask_jwt_extended import JWTManager
from flask import jsonify
from  flask_migrate import Migrate, MigrateCommand
from flask_script import Manager,Server
from flasgger import Swagger
from src.config.swagger import template,swagger_config

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            SWAGGER={
                "title":"jaza keja",
                "uiversion":3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app) 

    manager = Manager(app)
    manager.add_command('server',Server)


    migrate = Migrate(app,db)
    manager.add_command('db',MigrateCommand)

    JWTManager(app)
    Swagger(app,config=swagger_config,template=template)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error":"Not found"}),HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error":"Internal server error"}),HTTP_500_INTERNAL_SERVER_ERROR

    return  app




