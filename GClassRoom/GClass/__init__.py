from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c7b8cca095dcc5d18b3b9f55fb912967'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from GClass import routes