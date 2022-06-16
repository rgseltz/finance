from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, bcrypt
from sqlalchemy.exc import IntegrityError
# from forms import
from secret import finance_key

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///finance"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = finance_key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

print(finance_key)
connect_db(app)

toolbar = DebugToolbarExtension(app)
