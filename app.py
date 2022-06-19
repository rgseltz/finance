from flask import Flask, render_template, redirect, session, flash, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, bcrypt, Portfolio, Stock, Portfolio_Stock, User_Stock
from sqlalchemy.exc import IntegrityError
# from forms import
from secret import finance_key

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///finance"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = finance_key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

############Handle Session Data - User Login - Flask Global################


@app.before_first_request
def add_global_user():
    """If user is currently logged in, add user to flask global"""
    if session['CURR_USER_KEY']:
        g.user = User.query.get_or_404(session['CURR_USER_KEY'])


################Flask Routes#################################

@app.route('/', methods=["GET"])
def show_homepage():
    return render_template('index.html')


@app.route('/portfolios', methods=["GET"])
def show_portfolios():
    return render_template('portfolios.html')
