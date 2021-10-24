from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from buzzcoin.blockchain import Blockchain
from textwrap import dedent
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


app.config['SECRET_KEY'] = "felkfsjeflkejldskjveslkfjw"
# creates sql database of users and stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db = SQLAlchemy(app)
# for encryption purposes
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Generates a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

from buzzcoin import routes
