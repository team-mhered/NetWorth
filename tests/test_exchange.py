#!/usr/bin/env python3

# tests/test_exchange.py

""" test get_exchange_rate"""

import unittest

from datetime import date, timedelta

from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

from src.utils import get_exchange_rate


class TestExchangeRates(unittest.TestCase):

    """ Class to test interface with exchange rate service """

    def setUp(self):

        btc_handler = BtcConverter()
        btc_eur = btc_handler.get_latest_price('EUR')
        usd_btc = 1 / btc_handler.get_latest_price('USD')

        currency_handler = CurrencyRates()
        usd_eur = currency_handler.get_rate('USD', 'EUR')

        date_26_8 = date(2021, 8, 26)
        date_today = date.today()
        date_future = date.today()+timedelta(days=2)
        date_holiday1 = date(2021, 8, 28)
        date_holiday2 = date(2021, 8, 29)

        self.my_test_points = [
            (date_26_8, 'BTC', 'BTC', 'supported', 1),  # past BTC ab
            (date_26_8, 'BTC', 'EUR', 'supported', 39848.2899),  # past BTC a
            (date_26_8, 'USD', 'BTC', 'supported', 2.1347992e-05),  # past BTC b
            (date_26_8, 'USD', 'EUR', 'supported', 0.84983428),  # past forex ab
            (date_26_8, 'EUR', 'USD', 'supported', 1.1767),  # past forex ab
            (date_26_8, 'ETH', 'USD', 'unsupported', None),  # past unsup a
            (date_26_8, 'EUR', 'AAA', 'unsupported', None),  # past unsup b
            (date_26_8, 'BTC', 'AAA', 'unsupported', None),  # past BTC + unsup
            (date_26_8, 'BBB', 'CCC', 'unsupported', None),  # past unsup ab
            (date_today, 'BTC', 'EUR', 'supported', btc_eur),  # today BTC a
            (date_today, 'USD', 'BTC', 'supported', usd_btc),  # today BTC b
            (date_today, 'USD', 'EUR', 'supported', usd_eur),  # today forex ab
            (date_today, 'ETH', 'USD', 'unsupported', None),  # today unsup a
            (date_today, 'EUR', 'AAA', 'unsupported', None),  # today unsup b
            (date_today, 'BBB', 'CCC', 'unsupported', None),  # today unsup ab
            (date_today, 'BTC', 'AAA', 'unsupported', None),  # today BTC + unsup
            (date_future, 'BTC', 'BTC', 'supported', None),  # future BTC ab
            (date_future, 'BTC', 'EUR', 'supported', None),  # future BTC a
            (date_future, 'USD', 'BTC', 'supported', None),  # future BTC b
            (date_future, 'USD', 'EUR', 'supported', None),  # future forex ab
            (date_future, 'EUR', 'USD', 'supported', None),  # future forex ab
            (date_future, 'ETH', 'USD', 'unsupported', None),  # future unsup a
            (date_future, 'EUR', 'AAA', 'unsupported', None),  # future unsup b
            (date_future, 'BTC', 'AAA', 'unsupported', None),  # fut BTC a unsup b
            (date_future, 'BBB', 'CCC', 'unsupported', None),  # fut unsup ab
            (date_holiday1, 'USD', 'EUR', 'holiday', None),  # future BTC ab
            (date_holiday2, 'BTC', 'EUR', 'holiday', None),  # future BTC a
        ]

    def test_1_valid_cases(self):
        """ Retrieving valid past exchange rates from service """

        msg = ""
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'supported' and given_date < date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                check = point[4]
                msg += f"\nExchange rate {from_curr}/{to_curr} on"\
                    "{given_date.isoformat()}={str(result)} vs. {str(check)}"
                self.assertAlmostEqual(result, check, places=4)
        # print(msg)

    def test_2_today_rates(self):
        """ Retrieving current exchange rates from service """

        msg = ""
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'supported' and given_date == date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                check = point[4]
                msg += f"\nExchange rate {from_curr}/{to_curr} "\
                    "on {given_date.isoformat()}={str(result)}"
                self.assertAlmostEqual(result, check, msg=f"Failed at sample: {point}", places=4)
        # print(msg) --> replace with logging

    def test_3_future_dates(self):
        """ Retrieving future exchange rates from service """

        for point in self.my_test_points:
            given_date = point[0]
            # not used: case = point[3]
            if given_date > date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                self.assertIsNone(result, "Future rates should return None")

    def test_4_unsupported_cases(self):
        """ Retrieving unsupported exchange rates from service """

        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'unsupported' and given_date < date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                self.assertIsNone(result, "Unsupported rates should return None")

    def test_5_holiday(self):
        """ Retrieving from service exchange rates on a holiday"""

        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'holiday':
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                self.assertIsNone(result, "Holidays should return None")
