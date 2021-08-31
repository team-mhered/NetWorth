#!/usr/bin/env python3

# tests/test_exchange.py

""" test get_exchange_rate"""

import unittest
import logging

from src.utils import get_exchange_rate
from datetime import date, timedelta

from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter


class Test_get_exchange_rate(unittest.TestCase):

    def setUp(self):

        c = CurrencyRates()
        b = BtcConverter()
        BTC_EUR = b.get_latest_price('EUR')
        USD_BTC = 1 / b.get_latest_price('USD')
        USD_EUR = c.get_rate('USD', 'EUR')

        self.my_test_points = [
            (date(2021, 8, 26), 'BTC', 'BTC', 'supported', 1),  # past BTC ab
            (date(2021, 8, 26), 'BTC', 'EUR', 'supported', 39848.2899),  # past BTC a
            (date(2021, 8, 26), 'USD', 'BTC', 'supported', 2.134799265262721e-05),  # past BTC b
            (date(2021, 8, 26), 'USD', 'EUR', 'supported', 0.8498342823149485),  # past forex ab
            (date(2021, 8, 26), 'EUR', 'USD', 'supported', 1.1767),  # past forex ab
            (date(2021, 8, 26), 'ETH', 'USD', 'unsupported', None),  # past unsup a
            (date(2021, 8, 26), 'EUR', 'AAA', 'unsupported', None),  # past unsup b
            (date(2021, 8, 26), 'BTC', 'AAA', 'unsupported', None),  # past BTC a unsup b
            (date(2021, 8, 26), 'BBB', 'CCC', 'unsupported', None),  # past unsup ab
            (date.today(), 'BTC', 'EUR', 'supported', BTC_EUR),  # today BTC a
            (date.today(), 'USD', 'BTC', 'supported', USD_BTC),  # today BTC b
            (date.today(), 'USD', 'EUR', 'supported', USD_EUR),  # today forex ab
            (date.today(), 'ETH', 'USD', 'unsupported', None),  # today unsup a
            (date.today(), 'EUR', 'AAA', 'unsupported', None),  # today unsup b
            (date.today(), 'BBB', 'CCC', 'unsupported', None),  # today unsup ab
            (date.today(), 'BTC', 'AAA', 'unsupported', None),  # today BTC a unsup b
            (date.today()+timedelta(days=2), 'BTC', 'BTC', 'supported', None),  # future BTC ab
            (date.today()+timedelta(days=2), 'BTC', 'EUR', 'supported', None),  # future BTC a
            (date.today()+timedelta(days=2), 'USD', 'BTC', 'supported', None),  # future BTC b
            (date.today()+timedelta(days=2), 'USD', 'EUR', 'supported', None),  # future forex ab
            (date.today()+timedelta(days=2), 'EUR', 'USD', 'supported', None),  # future forex ab
            (date.today()+timedelta(days=2), 'ETH', 'USD', 'unsupported', None),  # future unsup a
            (date.today()+timedelta(days=2), 'EUR', 'AAA', 'unsupported', None),  # future unsup b
            (date.today()+timedelta(days=2), 'BTC', 'AAA', 'unsupported', None),  # future BTC a unsup b
            (date.today()+timedelta(days=2), 'BBB', 'CCC', 'unsupported', None),  # future unsup ab
            (date(2021, 8, 28), 'USD', 'EUR', 'holiday', None),  # future BTC ab
            (date(2021, 8, 29), 'BTC', 'EUR', 'holiday', None),  # future BTC a
        ]

    def test_1_valid_cases(self):
        msg = ""
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'supported' and given_date < date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                check = point[4]
                msg += f"\nExchange rate {from_curr}/{to_curr} on {given_date.isoformat()}={str(result)} vs. {str(check)}"
                self.assertAlmostEqual(result, check, places=4)
        # print(msg)

    def test_2_today_rates(self):
        msg = ""
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'supported' and given_date == date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                check = point[4]
                msg += f"\nExchange rate {from_curr}/{to_curr} on {given_date.isoformat()}={str(result)}"
        # print(msg)

    def test_3_future_dates(self):
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if given_date > date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                self.assertIsNone(result, "Future rates should return None")

    def test_4_unsupported_cases(self):
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'unsupported' and given_date < date.today():
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                self.assertIsNone(result, "Unsupported rates should return None")

    def test_5_holiday(self):
        for point in self.my_test_points:
            given_date = point[0]
            case = point[3]
            if case == 'holiday':
                from_curr = point[1]
                to_curr = point[2]
                result = get_exchange_rate(given_date, from_curr, to_curr)
                self.assertIsNone(result, "Holidays should return None")
