import pickle
import os
from app.model import Holding, Portfolio

class DataReader:
    def __init__(self, filename='portfolio_data.pkl'):
        """
        Initializes the DataReader with a filename for storing the data.

        :param filename: str, the name of the file to store the portfolio data
        """
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, '..', 'data')  # Correct path to the data directory
        os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists
        self.filename = os.path.join(data_dir, filename)

    def save_portfolio(self, portfolio):
        """
        Save the portfolio object to a file.

        :param portfolio: Portfolio, the portfolio object to save
        """
        with open(self.filename, 'wb') as file:
            pickle.dump(portfolio, file)

    def read_portfolio(self):
        """
        Read the portfolio object from a file.

        :return: Portfolio, the portfolio object read from the file
        """
        if not os.path.exists(self.filename):
            return None
        
        with open(self.filename, 'rb') as file:
            portfolio = pickle.load(file)
        return portfolio

    def compare_holdings(self, holdings_list):
        """
        Compare the holdings in the file with the provided holdings list.

        :param holdings_list: list of Holding, the list of holdings to compare
        :return: bool, True if the holdings match, False otherwise
        """
        portfolio = self.read_portfolio()
        if not portfolio:
            return False
        
        file_holdings = portfolio.holdings
        if len(file_holdings) != len(holdings_list):
            return False
        
        for holding in holdings_list:
            if holding not in file_holdings:
                return False
        
        return True

def main():
    portfolio = Portfolio()
    holding1 = Holding("AAPL", "Apple Inc.", 10, 150.0, "2023-01-01")
    holding2 = Holding("MSFT", "Microsoft Corp.", 5, 250.0, "2023-02-01")
    portfolio.add_holding(holding1)
    portfolio.add_holding(holding2)

    data_reader = DataReader()
    data_reader.save_portfolio(portfolio)

if __name__ == '__main__':
    # just testing
    main()
