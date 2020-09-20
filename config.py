import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.


# Connect to the database
DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:moknine2020@localhost:5432/fyyurbase'


# TODO IMPLEMENT DATABASE URL OK

#user = postgres / password=moknine2020 "for me :)" / base name = fyyurbase
SQLALCHEMY_TRACK_MODIFICATIONS = False
