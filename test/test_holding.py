import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from app.model.holding import Holding
from app.model import DataReader

class TestHolding(unittest.TestCase):
    @patch('yfinance.Ticker')
    def setUp(self, mock_ticker):
        self.mock_stock = MagicMock()
        self.mock_stock.history.return_value = pd.DataFrame({'Close': [150.0]}, index=[pd.Timestamp('2024-07-05')])
        self.mock_stock.dividends = pd.Series([0.5, 0.5], index=[pd.Timestamp('2023-02-01'), pd.Timestamp('2024-01-01')])
        mock_ticker.return_value = self.mock_stock

        self.holding = Holding(
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=100.0,
            purchase_date="2023-01-01"
        )

    def test_initialization(self):
        self.assertEqual(self.holding.ticker, "AAPL")
        self.assertEqual(self.holding.name, "Apple Inc.")
        self.assertEqual(self.holding.quantity, 10)
        self.assertEqual(self.holding.purchase_price, 100.0)
        self.assertEqual(self.holding.purchase_date, "2023-01-01")
        self.assertEqual(self.holding.current_price, 150.0)
        self.assertEqual(self.holding.dividends, 1.0)

    def test_total_cost(self):
        self.assertEqual(self.holding.total_cost(), 1000.0)

    def test_current_value(self):
        self.assertEqual(self.holding.current_value(), 1500.0)

    def test_profit_loss(self):
        self.assertEqual(self.holding.profit_loss(), 500.0)

    def test_profit_loss_percentage(self):
        self.assertEqual(self.holding.profit_loss_percentage(), 50.0)

    @patch('yfinance.Ticker')
    def test_get_dividends(self, mock_ticker):
        mock_stock = MagicMock()
        mock_stock.dividends = pd.Series([0.5, 0.5], index=[pd.Timestamp('2023-02-01'), pd.Timestamp('2024-01-01')])
        mock_ticker.return_value = mock_stock
        holding = Holding(
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=100.0,
            purchase_date="2023-01-01"
        )
        self.assertEqual(holding.get_dividends(), 1.0)

if __name__ == '__main__':
    unittest.main()
