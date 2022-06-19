# from sys import ps1
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import LoginForm, RegisterForm, connect_db, db, User, bcrypt, Portfolio, Stock, Portfolio_Stock, User_Stock
from sqlalchemy.exc import IntegrityError
# from forms import
from secret import finance_key

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///finance"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'fe13a9b1386f3721801d04c07a6f707cf8e221f1f8a6c424f27600c5b5e00f9c'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

api_key = finance_key

connect_db(app)
db.create_all()

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
