import unittest
import pandas as pd
from app.model.holding import Holding
from app.model.portfolio import Portfolio

import yfinance as yf
yf.Ticker = lambda ticker: MockTicker()

class MockTicker:
    def history(self, period):
        return {'Close': [150.0]}
    
    @property
    def dividends(self):
        dates = pd.date_range(start="2022-01-01", end="2023-01-01", freq='M')
        return pd.Series([0.5]*len(dates), index=dates)


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.holding1 = Holding("AAPL", "Apple Inc.", 10, 150.0, "2023-01-01")
        self.holding2 = Holding("MSFT", "Microsoft Corp.", 5, 250.0, "2023-02-01")
        self.portfolio = Portfolio()
        self.portfolio.add_holding(self.holding1)
        self.portfolio.add_holding(self.holding2)

    def test_add_holding(self):
        self.assertEqual(len(self.portfolio.holdings), 2)
        self.assertIn(self.holding1, self.portfolio.holdings)
        self.assertIn(self.holding2, self.portfolio.holdings)

    def test_remove_holding(self):
        self.portfolio.remove_holding("AAPL")
        self.assertEqual(len(self.portfolio.holdings), 1)
        self.assertNotIn(self.holding1, self.portfolio.holdings)

    def test_total_cost(self):
        expected_total_cost = self.holding1.total_cost() + self.holding2.total_cost()
        self.assertEqual(self.portfolio.total_cost(), expected_total_cost)

    def test_current_value(self):
        expected_current_value = self.holding1.current_value() + self.holding2.current_value()
        self.assertEqual(self.portfolio.current_value(), expected_current_value)

    def test_total_dividends(self):
        expected_total_dividends = self.holding1.dividends + self.holding2.dividends
        self.assertEqual(self.portfolio.total_dividends(), expected_total_dividends)

    def test_profit_loss(self):
        expected_profit_loss = self.portfolio.current_value() - self.portfolio.total_cost()
        self.assertEqual(self.portfolio.profit_loss(), expected_profit_loss)

    def test_profit_loss_percentage(self):
        if self.portfolio.total_cost() != 0:
            expected_profit_loss_percentage = (self.portfolio.profit_loss() / self.portfolio.total_cost()) * 100
        else:
            expected_profit_loss_percentage = 0.0
        self.assertAlmostEqual(self.portfolio.profit_loss_percentage(), expected_profit_loss_percentage)

if __name__ == '__main__':
    unittest.main()
