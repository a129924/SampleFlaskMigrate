from flask import Flask
from flask_migrate import Migrate

from project_1.route import hello

from project_1.constants import DB_URL
from project_1.ext import db
import project_1.models 



def create_app():
    app = Flask(__name__)
    migrate = Migrate()
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.add_url_rule('/',"index",hello)
    
    return app