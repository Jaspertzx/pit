class Portfolio:
    def __init__(self):
        """
        Initializes a new portfolio object.
        """
        self.holdings = []

    def add_holding(self, holding):
        """
        Add a holding to the portfolio.

        :param holding: Holding, the holding object to add
        """
        self.holdings.append(holding)

    def remove_holding_by_index(self, index):
        """
        Remove a holding from the portfolio by its index.

        :param index: int, the index of the holding to remove
        """
        if 0 <= index < len(self.holdings):
            self.holdings.pop(index)

    def total_cost(self):
        """
        Calculate the total cost of the portfolio.

        :return: float, total cost of all holdings
        """
        return sum(h.total_cost() for h in self.holdings)

    def current_value(self):
        """
        Calculate the current value of the portfolio.

        :return: float, current value of all holdings
        """
        return sum(h.current_value() for h in self.holdings)

    def total_dividends(self):
        """
        Calculate the total dividends received from all holdings.

        :return: float, total dividends received
        """
        return sum(h.dividends for h in self.holdings)

    def profit_loss(self):
        """
        Calculate the total profit or loss of the portfolio.

        :return: float, total profit or loss of all holdings
        """
        return self.current_value() - self.total_cost()

    def profit_loss_percentage(self):
        """
        Calculate the total profit or loss percentage of the portfolio.

        :return: float, total profit or loss percentage
        """
        if self.total_cost() == 0:
            return 0.0
        return (self.profit_loss() / self.total_cost()) * 100

    def __repr__(self):
        """
        Return a string representation of the portfolio object.
        """
        return f"Portfolio(holdings={self.holdings})"
