import unittest
import os
import pickle

from app.model.holding import Holding
from app.model.portfolio import Portfolio
from app.model.data_reader import DataReader

class TestDataReader(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_portfolio_data.pkl'
        self.data_reader = DataReader(self.filename)
        self.portfolio = Portfolio()
        
        self.holding1 = Holding("AAPL", "Apple Inc.", 10, 150.0, "2023-01-01")
        self.holding2 = Holding("MSFT", "Microsoft Corp.", 5, 250.0, "2023-02-01")
        self.portfolio.add_holding(self.holding1)
        self.portfolio.add_holding(self.holding2)

    def tearDown(self):
        if os.path.exists(self.data_reader.filename):
            os.remove(self.data_reader.filename)

    def test_save_portfolio(self):
        self.data_reader.save_portfolio(self.portfolio)
        self.assertTrue(os.path.exists(self.data_reader.filename))
        with open(self.data_reader.filename, 'rb') as file:
            saved_portfolio = pickle.load(file)
        self.assertEqual(len(saved_portfolio.holdings), len(self.portfolio.holdings))
        self.assertEqual(saved_portfolio.holdings[0].ticker, self.portfolio.holdings[0].ticker)
        self.assertEqual(saved_portfolio.holdings[1].ticker, self.portfolio.holdings[1].ticker)

    def test_read_portfolio(self):
        self.data_reader.save_portfolio(self.portfolio)
        read_portfolio = self.data_reader.read_portfolio()
        self.assertIsNotNone(read_portfolio)
        self.assertEqual(len(read_portfolio.holdings), len(self.portfolio.holdings))
        self.assertEqual(read_portfolio.holdings[0].ticker, self.portfolio.holdings[0].ticker)
        self.assertEqual(read_portfolio.holdings[1].ticker, self.portfolio.holdings[1].ticker)

    def test_read_portfolio_no_file(self):
        if os.path.exists(self.data_reader.filename):
            os.remove(self.data_reader.filename)
        read_portfolio = self.data_reader.read_portfolio()
        self.assertIsNone(read_portfolio)

if __name__ == '__main__':
    unittest.main()
