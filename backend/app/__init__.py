from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy()
jwt = JWTManager()


# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'Access1234'
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this!
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    db.init_app(app)
    jwt.init_app(app)

    from controllers import bp as main_bp
    app.register_blueprint(main_bp)

    return app