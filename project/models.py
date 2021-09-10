from project import db

# Database ORMs
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique = True)
    mobile = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255), nullable=False)
