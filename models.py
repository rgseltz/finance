from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from wtforms_alchemy import ModelForm
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class to create new users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String, nullable=False)

    password = db.Column(db.String, nullable=False)

    email = db.Column(db.String, nullable=False, unique=True)

    # stocks = db.relationship('Stock', secondary=(
    #     'portfolios_stocks'), viewonly=True)

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

    def __repr__(self):
        return f'<User username={self.username}, email={self.email}>'


class Portfolio(db.Model):
    """Creates a new portfolio"""

    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    portfolio_name = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref=("portfolios"))

    stocks = db.relationship("Stock", secondary=(
        "portfolios_stocks"), backref=("portfolios"))

    # db relationship transactions.portfolio is backrefed at Transaction w/ passthru at portfolios_transactions


class Stock(db.Model):
    """Creates a new stock"""

    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    stock_name = db.Column(db.String, unique=True, nullable=False)

    ticker = db.Column(db.String, unique=True, nullable=False)

    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<stock_name={self.stock_name}, ticker={self.ticker}, price={self.price}>'


class Portfolio_Stock(db.Model):
    """Creates an object that joins a portfolio and a stock"""

    __tablename__ = 'portfolios_stocks'

    portfolio_id = db.Column(db.Integer, db.ForeignKey(
        'portfolios.id'), primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey(
        'stocks.id'), primary_key=True)

    # user_id = db.Column(db.Integer, db.ForeignKey(
    #     'users.id'), primary_key=True)


class Portfolio_Transaction(db.Model):
    """Join table for transaction and portfolio"""

    __tablename__ = 'portfolios_transactions'

    portfolio_id = db.Column(db.Integer, db.ForeignKey(
        'portfolios.id'), primary_key=True)

    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.id'), primary_key=True)


class Transaction(db.Model):
    """Object that records user trades"""

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    date = db.Column(db.DateTime, nullable=False, default=datetime.today())

    quantity = db.Column(db.Float, nullable=False)

    stock_id = db.Column(db.Integer, db.ForeignKey(
        'stocks.id'), nullable=False)

    price = db.Column(db.Float, nullable=False)

    portfolio = db.relationship('Portfolio', secondary=(
        'portfolios_transactions'), backref=('transactions'))


class LoginForm(ModelForm):
    class Meta:
        model = User

        only = ['username', 'password']


class RegisterForm(ModelForm):

    class Meta:
        model = User
