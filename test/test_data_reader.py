import unittest
import os
import pickle
from unittest.mock import patch

from datetime import datetime

from app.model import Holding, Portfolio
from app.util import DataReader

class TestDataReader(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_portfolio_data.pkl'
        self.data_reader = DataReader(self.filename)
        self.portfolio = Portfolio()
        
        # Add sample holdings to the portfolio
        self.holding1 = Holding("AAPL", "Apple Inc.", 10, 150.0, "2023-01-01")
        self.holding2 = Holding("MSFT", "Microsoft Corp.", 5, 250.0, "2023-02-01")
        self.portfolio.add_holding(self.holding1)
        self.portfolio.add_holding(self.holding2)

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_portfolio(self):
        # Save the portfolio to file
        self.data_reader.save_portfolio(self.portfolio)
        
        # Check if the file exists
        self.assertTrue(os.path.exists(self.filename))
        
        # Check if the saved portfolio matches the original portfolio
        with open(self.filename, 'rb') as file:
            saved_portfolio = pickle.load(file)
        self.assertEqual(len(saved_portfolio.holdings), len(self.portfolio.holdings))
        self.assertEqual(saved_portfolio.holdings[0].ticker, self.portfolio.holdings[0].ticker)
        self.assertEqual(saved_portfolio.holdings[1].ticker, self.portfolio.holdings[1].ticker)

    def test_read_portfolio(self):
        # Save the portfolio first
        self.data_reader.save_portfolio(self.portfolio)
        
        # Read the portfolio from file
        read_portfolio = self.data_reader.read_portfolio()
        
        # Check if the read portfolio matches the original portfolio
        self.assertIsNotNone(read_portfolio)
        self.assertEqual(len(read_portfolio.holdings), len(self.portfolio.holdings))
        self.assertEqual(read_portfolio.holdings[0].ticker, self.portfolio.holdings[0].ticker)
        self.assertEqual(read_portfolio.holdings[1].ticker, self.portfolio.holdings[1].ticker)

    def test_read_portfolio_no_file(self):
        # Ensure the file does not exist
        if os.path.exists(self.filename):
            os.remove(self.filename)
        
        # Read the portfolio from a non-existing file
        read_portfolio = self.data_reader.read_portfolio()
        
        # Check if the read portfolio is None
        self.assertIsNone(read_portfolio)

if __name__ == '__main__':
    unittest.main()
