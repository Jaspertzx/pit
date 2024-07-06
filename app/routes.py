from flask import Flask, request, jsonify
from app import app
from .util import is_connected
from .util import DataReader
from app.model.portfolio import Portfolio
from app.model.holding import Holding

app = Flask(__name__)

# Initialize the data reader
data_reader = DataReader()

# Try to load the portfolio from file
portfolio = data_reader.read_portfolio()
if portfolio is None:
    portfolio = Portfolio()

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/initialize')
def initialize():
    if is_connected():
        return "Connected to the internet"
    else:
        return "No internet connection"

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    """
    Get the current portfolio.

    :return: JSON representation of the portfolio
    """
    return jsonify([holding.__dict__ for holding in portfolio.holdings])

@app.route('/portfolio/holding', methods=['POST'])
def add_holding():
    """
    Add a holding to the portfolio.

    :param ticker: str, the ticker symbol of the holding
    :param name: str, the name of the holding
    :param quantity: int, the number of shares/units held
    :param purchase_price: float, the purchase price per share/unit
    :param purchase_date: str, the date when the holding was purchased
    :return: JSON representation of the updated portfolio
    """
    data = request.json
    ticker = data['ticker']
    name = data['name']
    quantity = data['quantity']
    purchase_price = data['purchase_price']
    purchase_date = data['purchase_date']
    
    holding = Holding(ticker, name, quantity, purchase_price, purchase_date)
    portfolio.add_holding(holding)
    
    return jsonify([holding.__dict__ for holding in portfolio.holdings])

@app.route('/portfolio/holding/<ticker>', methods=['DELETE'])
def remove_holding(ticker):
    """
    Remove a holding from the portfolio by its ticker symbol.

    :param ticker: str, the ticker symbol of the holding to remove
    :return: JSON representation of the updated portfolio
    """
    portfolio.remove_holding(ticker)
    return jsonify([holding.__dict__ for holding in portfolio.holdings])

if __name__ == '__main__':
    app.run(debug=True)
