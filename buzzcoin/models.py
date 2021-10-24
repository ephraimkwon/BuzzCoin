from buzzcoin import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True, nullable=False)
    email_address = db.Column(db.String(100), unique = True, nullable=False)
    password_hash = db.Column(db.String(120), unique = False, nullable=False)
    ##key = db.Column(db.String(100000), unique = True, nullable=False)


def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}')"