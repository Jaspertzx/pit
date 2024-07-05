"""
Initialization Check

This module will provide a function to check for internet connection 
by fetching data from a popular stock ticker using yFinance.

Additionally, it will provide checks (in the future) for port openings 
and services to ensure both Node.js and Flask are operating as expected.

Author: Jasper Tan Zu Xiang
"""

import yfinance as yf

def is_connected():
    """
    Check if there is an internet connection by attempting to fetch 
    data using yfinance.

    Returns:
        bool: True if the internet connection is available, False otherwise.
    """
    try:
        ticker = yf.Ticker("AAPL")
        _ = ticker.history(period="1d")
        return True
    except Exception:
        return False