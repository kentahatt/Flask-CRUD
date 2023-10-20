import os
# Remember to set the database URL to the environment variable DEV_DATABASE_URL, which is the
# URL for the MySQL database. Run the command in the terminal to define the env var

# Linux:
# export DEV_DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:<port>/<database_name>

# Windows:
# SET DEV_DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:<port>/<database_name>

# Set to False in order to disable the modification tracking system
# Good practice to avoid tracking changes from Flask-SQLAlchemy to the SQLAlchemy library


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static method that is used to initialize app configurations
    @staticmethod
    def init_app(app):
        pass


# 3 Child classes for each environment following the Config parent class
# Dev Config class has Debug set as true to see the debug messages if there are errors
# SQLALCHEMY_DATABASE_URI sets to the database URL to connect to the database
class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    ENVIRONMENT = 'development'

    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
