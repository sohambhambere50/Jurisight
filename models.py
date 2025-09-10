from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True, nullable = False)
    email = db.Column(db.String(25), unique = True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # New fields for email verificaiton

    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    verification_code_hash = db.Column(db.String(256), nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    verification_attempts = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
