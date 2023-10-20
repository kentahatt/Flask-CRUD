import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .config import config
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()


# The create_app function is responsible for creating and
# configuring a Flask application based on the provided configuration name.
def create_app(config_name):

    # Set the template folder path using os.path module
    template_folder = os.path.join(os.path.dirname(__file__), '..', 'templates')
    
    # Set the static folder path using os.path module
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
    
    # Create the Flask app instance with the template and static folder paths
    app = Flask(__name__, template_folder=template_folder)
    app._static_folder = static_folder

    # App Secret Key
    app.secret_key = os.environ.get('SECRET_KEY')

    # Load the config from the config dictionary and initialize the app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize the SQLAlchemy instance db with the app instance
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Handle for logging in
    from .models import LoginUser
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return LoginUser.query.get(int(user_id))

    # blueprint for auth routes in the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for other routes in the app
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
