from flask import Flask
from config import DokRegAppConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


app = Flask(__name__)
app.config.from_object(DokRegAppConfig)

login = LoginManager(app)

db = SQLAlchemy(app)

from app import routes