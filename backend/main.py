from app import app
from flask_cors import CORS
from models import db, User, Role, RolesUsers, Book, BookRequest
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
import logging
from logging.handlers import RotatingFileHandler



# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Access1234'
# app.config['JWT_SECRET_KEY'] = 'My-jwt-secret-key'
# app.config['JWT_TOKEN_LOCATION'] = ['headers']

# Initialize extensions
api = Api(app)
migrate = Migrate(app, db)
# jwt = JWTManager(app)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

# Import controllers
from controllers import *

with app.app_context():
    db.init_app(app)
    db.create_all()

    

# Check database file
db_path = 'instance/database.db'
if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
else:
    print(f"Database file found at {db_path}")
    print(f"File permissions: {oct(os.stat(db_path).st_mode)[-3:]}")

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

if __name__ == '__main__':
    app.run(debug=True)