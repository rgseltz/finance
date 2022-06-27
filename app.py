# from sys import ps1
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import LoginForm, RegisterForm, connect_db, db, User, bcrypt, Portfolio, Stock, Portfolio_Stock, Transaction, Portfolio_Transaction
from sqlalchemy.exc import IntegrityError
# from forms import
from secret import finance_key
import json
import requests
import certifi
from urllib.request import urlopen
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///finance"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'fe13a9b1386f3721801d04c07a6f707cf8e221f1f8a6c424f27600c5b5e00f9c'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

api_key = finance_key

connect_db(app)

toolbar = DebugToolbarExtension(app)

############Handle Session Data - User Login - Flask Global################


# @app.before_first_request
# def add_global_user():
#     """If user is currently logged in, add user to flask global"""
#     if session:
#         g.user = User.query.get_or_404(session['CURR_USER_KEY'])
#     else:
#         g.user = None


@app.route('/register', methods=["GET", "POST"])
def register_new_user():
    """"""
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(username=username, email=email, pwd=password)
        db.session.add(new_user)
        try:
            db.session.commit()
            session["user_id"] = new_user.id
            return redirect('/')

        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def log_in_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, pwd=password)
        if user:
            session['user_id'] = user.id
            flash("Welcome back!", "success")
            redirect('/')

        flash("Incorrect username/password", "danger")
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id')
    flash('Successfully logged out', 'success')
    return redirect('/')


################Flask Routes#################################
STOCK = 'goog'
url = 'https://financialmodelingprep.com/api/v3/'
profile_url = f'{url}/profile/{STOCK}?api_key={finance_key}'


@app.route('/', methods=["GET"])
def show_homepage():
    print(f'###########################{session}#############')
    return render_template('index.html')


@app.route('/portfolios', methods=["GET"])
def show_portfolios():
    if "user_id" not in session:
        flash('Please sign in to access your portfolio', "danger")
        redirect('/')
    return render_template('portfolios.html')


@app.route('/quote/<ticker>/profile', methods=["GET"])
def get_stock_profile(ticker):
    # symbol = response.params
    # stock = 'goog'
    url = f'https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    stock = (data[0])
    json.dumps(response.text)
    return render_template('stock_info.html', stock=stock)


@app.route('/quote/<ticker>/price', methods=["GET"])
def get_stock_price(ticker):
    import requests
    url = f'https://financialmodelingprep.com/api/v3/quote/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'applications/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return render_template('quote/stock_info.html', stock=data)


@app.route('/quote/<ticker>/chart', methods=["GET"])
def get_stock_chart(ticker):
    import requests
    url = f'https://financialmodelingprep.com/api/v3/quote/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'applications/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return render_template('quote/stock_info.html', stock=data)


@app.route('/search', methods=["GET"])
def search_ticker():
    url = "https://financialmodelingprep.com/api/v3/search?query=goog&limit=50&apikey=9e5ca9243a059ff6320c70bfe3e964d7"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return redirect('/')
