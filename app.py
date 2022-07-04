# from sys import ps1
from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import NewTransactionForm, AddToWatchListForm
from models import LoginForm, RegisterForm, AddPortfolioForm, connect_db, db, User, bcrypt, Portfolio, Stock, Portfolio_Stock, Transaction, Portfolio_Transaction
from sqlalchemy.exc import IntegrityError
# from forms import
from secret import finance_key, yfapi_key
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
yfapi_key = yfapi_key

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
            return redirect('/')
        else:
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
    market_summary_url = "https://yfapi.net/v6/finance/quote/marketSummary"
    quote_url = "https://yfapi.net/v6/finance/quote"
    query_string = {"symbols": "^SP500TR,^DJI,NDAQ,BTC-USD,EURUSD=X"}
    response = requests.request(
        "GET", quote_url, headers={'x-api-key': yfapi_key}, params=query_string)
    print(f'###########################{session}#############')
    data = response.json()
    print(data["quoteResponse"])
    return render_template('index.html', data=data["quoteResponse"])

###########Quote Resources#####################
# quote route profile resource


@ app.route('/quote/<ticker>/profile', methods=["GET"])
def get_stock_profile(ticker):
    # symbol = response.params
    # stock = 'goog'
    user = User.query.get(session['user_id'])
    url = f'https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    stock = (data[0])
    json.dumps(response.text)
    print(stock)
    return render_template('quote/stock_info.html', stock=stock, user=user)

# quote route price resource


@ app.route('/quote/<ticker>/price', methods=["GET"])
def get_stock_price(ticker):
    if session:
        user = User.query.get(session['user_id'])
    url = f'https://financialmodelingprep.com/api/v3/quote/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'applications/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return render_template('quote/stock_info.html', stock=data, user=user)

# quote route income statment resource


@ app.route('/quote/<ticker>/financials/inc', methods=["GET"])
def get_stock_income_statement(ticker):
    url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'applications/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return render_template('quote/stock_info.html', stock=data)

# quote route balance statement resource


@ app.route('/quote/<ticker>/financials/bal', methods=["GET"])
def get_stock_balance_sheet(ticker):
    url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'applications/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return render_template('quote/stock_info.html', stock=data)

# quote route historical data resource


def today_clean():
    today = datetime.today()
    today_iso = today.isoformat()
    return today_iso[0:10]


@ app.route('/quote/<ticker>/history', methods=["GET"])
def get_stock_history(ticker):

    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from=2018-03-12&to={today_clean()}&apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'applications/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return render_template('quote/stock_info.html', stock=data)

###########Portfolio Resources#####################

# show user portfolios


@ app.route('/portfolios', methods=["GET"])
def show_portfolios():
    if "user_id" not in session:
        flash('Please sign in to access your portfolio', "danger")
        return redirect('/')
    else:
        user = User.query.get(session["user_id"])
        form = AddPortfolioForm()
        return render_template('portfolios.html', form=form, user=user)

# make new portfolio


@ app.route('/portfolios/add', methods=["GET", "POST"])
def add_portfolio():
    form = AddPortfolioForm()
    user = User.query.get(session["user_id"])
    portfolio_name = form.portfolio_name.data
    portfolio = Portfolio(portfolio_name=portfolio_name)
    user.portfolios.append(portfolio)
    db.session.add(portfolio)
    db.session.add(user)
    db.session.commit()
    return redirect('/portfolios')

# edit portfolio


@ app.route('/portfolios/<int:portfolio_id>/edit', methods=["GET", "POST"])
def edit_portfolio(portfolio_id):
    if session:
        user = User.query.get(session['user_id'])
        portfolio = Portfolio.query.get(portfolio_id)
        form = AddPortfolioForm(obj=portfolio)
        if form.validate_on_submit():
            name = form.portfolio_name.data
            portfolio.portfolio_name = name
            db.session.add(portfolio)
            db.session.commit()
            return redirect('/portfolios')
    return render_template('portfolio/portfolio_edit.html', form=form, user=user)

# delete portfolio


@ app.route('/portfolios/<int:id>/delete', methods=["POST"])
def delete_portfolio(id):
    portfolio = Portfolio.query.get(id)
    print('###########################TEST')
    print(portfolio)
    db.session.delete(portfolio)
    db.session.commit()
    return redirect('/portfolios')
# view portfolio


@ app.route('/portfolios/<int:id>')
def get_portfolio(id):
    if "user_id" not in session:
        flash('Please sign in to access your portfolio', "danger")
        return redirect('/')
    else:
        user = User.query.get(session["user_id"])
        portfolio = Portfolio.query.get(id)
        transactions = portfolio.transactions
        if portfolio not in user.portfolios:
            flash('That is not your portfolio! Stay out')
            return redirect('/portfolios')
        else:
            return render_template('/portfolio/portfolio_info.html', user=user, portfolio=portfolio)


# add stock to portfolio from inside portfolio

@ app.route('/portfolios/<int:id>/addstock', methods=["GET", "POST"])
def add_stock_to_portfolio(id):
    portfolio = Portfolio.query.get(id)
    ticker = request.form['add-stock']
    if ticker == "":
        flash('Please enter symbol into textbox', 'warning')
        return redirect(f'/portfolios/{portfolio.id}')
    url = f'https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    Stock.query.filter_by(ticker=data[0]["symbol"])
    stock = Stock(stock_name=data[0]["companyName"],
                  ticker=data[0]["symbol"], price=data[0]["price"])
    portfolio.stocks.append(stock)
    db.session.add(stock)
    db.session.add(portfolio)
    db.session.commit()
    return redirect(f'/portfolios/{portfolio.id}')


# remove stock from portfolio
@ app.route('/portfolios/<int:port_id>/stock/<id>/delete', methods=["POST"])
def delete_stock(port_id, id):
    stock = Stock.query.get(id)
    portfolio = Portfolio.query.get(port_id)
    db.session.delete(stock)
    db.session.commit()
    return redirect(f'/portfolios/{port_id}')


# add transaction to portfolio


@ app.route('/portfolios/<int:portfolio_id>/transactions/<int:stock_id>/new', methods=["GET", "POST"])
def new_transaction(portfolio_id, stock_id):
    portfolio = Portfolio.query.get(portfolio_id)
    stock = Stock.query.get(stock_id)
    form = NewTransactionForm(obj=stock)
    if form.validate_on_submit():
        date = form.date.data
        quantity = form.quantity.data
        ticker = form.ticker.data
        price = form.price.data
        # stock_id = form.stock_id.data
        # del form.stock_id

        transaction = Transaction(
            date=date, quantity=quantity, ticker=ticker, price=price)
        portfolio.transactions.append(transaction)
        db.session.add(transaction)
        db.session.add(portfolio)
        db.session.commit()
        return redirect(f'/portfolios/{portfolio.id}')
    return render_template('transaction/transaction.html', form=form, stock=stock, portfolio=portfolio)

# View Transactions


@app.route('/portfolios/<int:port_id>/transactions/<int:tran_id>', methods=["GET"])
def view_transaction(port_id, tran_id):
    if session:
        user = User.query.get(session["user_id"])

        transaction = Transaction.query.get(tran_id)
        portfolio = Portfolio.query.get(port_id)
        value = transaction.price * transaction.quantity
        return render_template('transaction/transaction_info.html', portfolio=portfolio, transaction=transaction, value=value, user=user)
    else:
        flash('You do not have access!', 'danger')


# delete transaction from portfolio
@ app.route('/portfolios/<int:port_id>/transactions/<int:tran_id>/delete', methods=["POST"])
def delete_transaction(port_id, tran_id):
    portfolio = Portfolio.query.get(port_id)
    transaction = Transaction.query.get(tran_id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(f'/portfolios/{portfolio.id}')

# edit transaction


@app.route('/portfolios/<int:port_id>/transactions/<int:trans_id>/edit', methods=["POST"])
def edit_transaction(port_id, trans_id):
    if session:
        user = User.query.get(session['user_id'])
        portfolio = Portfolio.query.get(port_id)
        transaction = Transaction.query.get(trans_id)
        form = NewTransactionForm(obj=transaction)
        if form.validate_on_submit():
            date = form.date.data
            ticker = form.ticker.data
            quantity = form.quantity.data
            price = form.price.data

            transaction.date = date
            transaction.ticker = ticker
            transaction.quantity = quantity
            transaction.price = price

            db.session.add(transaction)
            db.session.commit()

            return redirect(f'/portfolios/{portfolio.id}')
    return render_template('transaction/transaction_edit.html', form=form, portfolio=portfolio, transaction=transaction, user=user)


# search for stock

@app.route('/search', methods=["GET"])
def search_ticker():
    if session:
        user = User.query.get(session['user_id'])
    q = request.args["q"]
    url = f'https://financialmodelingprep.com/api/v3/search?query={q}&limit=50&apikey=9e5ca9243a059ff6320c70bfe3e964d7'

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    print('SEARCH RESULTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    data = response.json()
    return render_template('search.html', response=data, user=user)


@app.route('/watchlist/add/<ticker>', methods=["GET", "POST"])
def add_stock_to_watchlist(ticker):
    url = f'https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey=9e5ca9243a059ff6320c70bfe3e964d7'
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    Stock.query.filter_by(ticker=data[0]["symbol"])
    stock = Stock(stock_name=data[0]["companyName"],
                  ticker=data[0]["symbol"], price=data[0]["price"])
    if session:
        user = User.query.get_or_404(session['user_id'])
        portfolios = user.portfolios
        form = AddToWatchListForm()
        form.portfolio_name.choices = [
            portfolio.portfolio_name or portfolio.id for portfolio in portfolios]
        if form.validate_on_submit():
            portfolio = form.portfolio_name.choices
            print(portfolio)
            portfolio.stock.append(stock)
            db.session.add(stock)
            db.session.add(portfolio)
            db.session.commit()

        return render_template('add_watchlist.html', form=form, ticker=ticker)
