#!/usr/bin/env python3

""" test get_exchange_rate"""

from utils import get_exchange_rate
from datetime import date, timedelta

"""
# used to ::COMPARE::
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import logging
"""


def main():
    points = [
        (date.today()-timedelta(days=2), 'BTC', 'BTC'),  # today BTC ab
        (date.today()-timedelta(days=2), 'BTC', 'EUR'),  # today BTC a
        (date.today()-timedelta(days=2), 'USD', 'BTC'),  # today BTC b
        (date.today()-timedelta(days=2), 'USD', 'EUR'),  # today forex ab
        (date.today()-timedelta(days=2), 'EUR', 'USD'),  # today forex ab
        (date.today()-timedelta(days=2), 'ETH', 'USD'),  # today unsup a
        (date.today()-timedelta(days=2), 'EUR', 'AAA'),  # today unsup b
        (date.today()-timedelta(days=2), 'BBB', 'CCC'),  # today unsup ab
        (date.today()-timedelta(days=2), 'BTC', 'AAA'),  # today BTC a unsup b
        (date.today(), 'BTC', 'BTC'),  # today BTC ab
        (date.today(), 'BTC', 'EUR'),  # today BTC a
        (date.today(), 'USD', 'BTC'),  # today BTC b
        (date.today(), 'USD', 'EUR'),  # today forex ab
        (date.today(), 'EUR', 'USD'),  # today forex ab
        (date.today(), 'ETH', 'USD'),  # today unsup a
        (date.today(), 'EUR', 'AAA'),  # today unsup b
        (date.today(), 'BBB', 'CCC'),  # today unsup ab
        (date.today(), 'BTC', 'AAA'),  # today BTC a unsup b
        (date.today()+timedelta(days=2), 'BTC', 'BTC'),  # today BTC ab
        (date.today()+timedelta(days=2), 'BTC', 'EUR'),  # today BTC a
        (date.today()+timedelta(days=2), 'USD', 'BTC'),  # today BTC b
        (date.today()+timedelta(days=2), 'USD', 'EUR'),  # today forex ab
        (date.today()+timedelta(days=2), 'EUR', 'USD'),  # today forex ab
        (date.today()+timedelta(days=2), 'ETH', 'USD'),  # today unsup a
        (date.today()+timedelta(days=2), 'EUR', 'AAA'),  # today unsup b
        (date.today()+timedelta(days=2), 'BBB', 'CCC'),  # today unsup ab
        (date.today()+timedelta(days=2), 'BTC', 'AAA'),  # today BTC a unsup b
    ]

    """
    # used to ::COMPARE::
    supported_currencies = ['USD', 'EUR', 'PLN', 'GBP']
    c = CurrencyRates()
    """
    for point in points:
        print(
            f"Exchange rate {point[1]}/{point[2]} on {point[0].isoformat()}={str(get_exchange_rate(point[0], point[1], point[2]))}")

        """
        # used to ::COMPARE::
        matches = {curr for curr in [point[1], point[2]]
                   if curr in supported_currencies}
        test = all(curr in supported_currencies
                   for curr in [point[1], point[2]])
        print(matches, test)
        if test:
            print("get_rate Rate: ", c.get_rate(point[1], point[2], point[0]))
        else:
            print('get_rate Rate: not supported')
        """


if __name__ == "__main__":
    # file was run directly
    main()
else:
    # file was imported
    pass
