from buzz_coin import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(35), unique = False, nullable=False)
    username = db.Column(db.String(15), unique = True, nullable=False)
    email = db.Column(db.String(100), unique = True, nullable=False)
    password = db.Column(db.String(120), unique = False, nullable=False)
    key = db.Column(db.String(100000), unique = True, nullable=False)

def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}')"