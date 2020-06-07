from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Talos.db'

# database instantiation
db = SQLAlchemy(app)

# encryption instantiation
bcrypt = Bcrypt(app)

# login manager instantiation
login_manager = LoginManager(app)
login_manager.login_view = 'login'

login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'badasslevelover9000@outlook.com'
app.config['MAIL_PASSWORD'] = 'MAWLR115'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

from Talos import route, model
from Talos.model import User
