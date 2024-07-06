"""
Holding object

This object will encapsulate one of the user's holdings. 
Will be part of the user's portfolio
"""
import pytz
import yfinance as yf
import pandas as pd
from datetime import datetime

class Holding:
    def __init__(self, ticker, name, quantity, purchase_price, purchase_date):
        """
        Initializes a new holding object.

        :param ticker: str, the ticker symbol of the holding
        :param name: str, the name of the holding
        :param quantity: int, the number of shares/units held
        :param purchase_price: float, the purchase price per share/unit
        :param purchase_date: str, the date when the holding was purchased
        """
        self.ticker = ticker
        self.name = name
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date
        self.current_price = self.get_current_price()
        self.dividends = self.get_dividends()

    def get_current_price(self):
        """
        Fetch the current price of the holding using yfinance.

        :return: float, the current price per share/unit
        """
        stock = yf.Ticker(self.ticker)
        return stock.history(period="1d")['Close'][0]

    def get_dividends(self):
        stock = yf.Ticker(self.ticker)
        dividends = stock.dividends

        # Convert purchase_date to timezone-aware datetime
        purchase_date_obj = datetime.strptime(self.purchase_date, "%Y-%m-%d")
        purchase_date_obj = pytz.timezone('America/New_York').localize(purchase_date_obj)
        
        # Ensure dividends index is timezone-aware
        if dividends.index.tz is None:
            dividends.index = dividends.index.tz_localize('America/New_York')
        
        dividends_since_purchase = dividends[dividends.index >= purchase_date_obj]
        total_dividends = dividends_since_purchase.sum()
        return total_dividends

    def total_cost(self):
        """
        Calculate the total cost of the holding.

        :return: float, total cost (quantity * purchase price)
        """
        return self.quantity * self.purchase_price

    def current_value(self):
        """
        Calculate the current value of the holding.

        :return: float, current value (quantity * current price)
        """
        return self.quantity * self.current_price

    def profit_loss(self):
        """
        Calculate the profit or loss of the holding.

        :return: float, profit or loss (current value - total cost)
        """
        return self.current_value() - self.total_cost()

    def profit_loss_percentage(self):
        """
        Calculate the profit or loss percentage of the holding.

        :return: float, profit or loss percentage
        """
        if self.total_cost() == 0:
            return 0.0
        return (self.profit_loss() / self.total_cost()) * 100

    def __repr__(self):
        """
        Return a string representation of the holding object.
        """
        return (f"Holding(ticker={self.ticker}, name={self.name}, quantity={self.quantity}, "
                f"purchase_price={self.purchase_price}, current_price={self.current_price}, "
                f"purchase_date={self.purchase_date}, dividends={self.dividends})")
