from models import connect_db, db, User, Portfolio, Stock, Portfolio_Stock, User_Stock, Transaction, Portfolio_Transaction
from app import app

# create tables
db.drop_all()
db.create_all()

# make a bunch of users
users = [User.register('ryboy', 'ryboy@test.com', 'ryboy'), User.register('sistaboy', 'sista@gmail.com',
                                                                          'rachelamy'), User.register('monstakilla', 'monstakilla@test.com', 'monstakilla')]
db.session.add_all(users)

# make a bunch of stocks
stocks = [Stock(stock_name='Google', ticker='GOOG', price=525.32), Stock(
    stock_name='Apple', ticker='AAPL', price=422.32), Stock(stock_name='Verizon', ticker='VZ', price=498.32)]

db.session.add_all(stocks)

# make a bunch of portfolios
portfolios = [Portfolio(portfolio_name='p1', user_id=1), Portfolio(
    portfolio_name='p2', user_id=2), Portfolio(portfolio_name='p3', user_id=3)]

db.session.add_all(portfolios)

db.session.commit()
