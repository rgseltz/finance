from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from wtforms_alchemy import ModelForm

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class to create new users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String, unique=True, nullable=False)

    password = db.Column(db.String, nullable=False)

    email = db.Column(db.String, nullable=False, unique=True)

    @classmethod
    def register(cls, username, email, pwd):
        """Register new user with hashed password"""
        hashed = bcrypt.generate_password_hash(pwd).decode('utf')
        return cls(username=username, email=email, password=hashed)

    @classmethod
    def authenticate(cls, username, pwd):
        """Authenticate user password. If password matches hashed password, return the user.
        If Invalid (unmatched) password to hash, return False"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
