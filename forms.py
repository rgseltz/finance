from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, DecimalField, IntegerField, IntegerRangeField
from wtforms.validators import InputRequired, Optional


class NewTransactionForm(FlaskForm):
    """Form for adding new transactions to a portfolio"""
    date = DateField("Date")

    quantity = IntegerField('Number of Shares')

    # stock_id = IntegerField()

    ticker = StringField('Ticker')

    price = FloatField('Price')

    # def remove_stock_id():
    #     form = NewTransactionForm(FlaskForm)
    #     if form:
    #         del form.stock_id
