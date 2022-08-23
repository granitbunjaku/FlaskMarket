from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '1825478ccde4a6f7dbd1aae9'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_managerr = LoginManager(app)
login_managerr.login_view = "login_page"

from market import routes