from flask import Flask
from .extensions import db, login
from .home.views import home

def create_app():
    app = Flask(__name__)

    login.init_app(app)
    login.login_view='login'
    
    @login.user_loader
    def user_loader(id):
        return Users.query.get(int(id))
    
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(home)

    return app
