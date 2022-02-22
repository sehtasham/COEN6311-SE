from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import insert

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth
    from .search import search

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')

    from .models import User, Note, Flight
    create_database(app)

    return app

def create_database(app):
    from .models import Flight
    if not path.exists('website/'+ DB_NAME): 
        db.create_all(app=app) 
        print('Created Database!')
        with app.app_context():
            new_flight1 = Flight(sourceLocation='Montreal', \
                destinationLocation='Ontario', departureDate=date(2022,2,24), \
                    returnDate=date(2022,2,26), adults='2', children='1')
            new_flight2 = Flight(sourceLocation='Canada', \
                destinationLocation='USA', departureDate=date(2022,2,25), \
                    returnDate=date(2022,2,26), adults='2', children='1')
            db.session.add(new_flight1)
            db.session.add(new_flight2)
            db.session.commit()