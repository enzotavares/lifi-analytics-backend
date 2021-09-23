from flask import Flask
from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from os import path, walk, environ
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import sys

our_namespace = '/lifi'
load_dotenv()

app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate()

def create_app(debug=False):
    """Create an application."""
    extra_dirs = ['templates/', ]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app = Flask(__name__, template_folder="templates/")
    CORS(app)
    app.debug = debug
    app.config['SECRET_KEY'] = '69#js32%_d4-!xd$'
    app.config['JWT_TOKEN_LOCATION'] = ['query_string', 'headers']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 15420
    app.config['JWT_SECRET_KEY'] = '42@s3xn%o69^!xd$'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config.from_object(environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
