#!/usr/bin/env python3

# tests/test_utils.py

""" Tests for Portfolio class"""

import logging
from unittest import TestCase
from datetime import date


class TestPortfolio(TestCase):

    """ Class to test basic Portfolio methods """

    def setUp(self):
        """ Create a fixture of a basic portfolio with some items """

        # setup logging service
        # ::ENHANCEMENT:: move this config info to an .env or a .cfg file
        config_file = './tests/test_utils.log'
        log_level = logging.INFO
        logging.basicConfig(filename=config_file, filemode='w',
                            format='%(asctime)s::%(levelname)s::%(message)s',
                            datefmt='%Y.%m.%d %I:%M:%S%p', level=log_level)

        logging.info('\n--------CREATING FIXTURE--------\n')

        from src.readwrite import read_portfolio_from_file
        my_portfolio = read_portfolio_from_file('./tests/fixtures.json')

        logging.info('\n--------FIXTURE CREATED---------\n')

        self.my_portfolio = my_portfolio

    def test_create(self):
        """ Sample Portfolio contains 4 sample Items"""

        self.assertEqual(len(self.my_portfolio.item_list), 4)

    def test_balance1(self):
        """ Portfolio balance of 50k€ on 3/2/2021 is computed well"""

        for i in [3]:  # , 17, 19, 21]:
            dat = date(2021, 2, i)
            balance = self.my_portfolio.get_portfolio_balance(given_date=dat)
            logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                         self.my_portfolio.currency, dat.isoformat(),
                         str(balance))
            self.assertAlmostEqual(balance, 50000.00, places=4)

    def test_balance2(self):
        """ Portfolio balance of 150k€ on 13/5/2021 is computed well"""

        for i in [13]:  # , 17, 19, 21]:
            dat = date(2021, 5, i)
            balance = self.my_portfolio.get_portfolio_balance(given_date=dat)
            logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                         self.my_portfolio.currency, dat.isoformat(),
                         str(balance))
            self.assertAlmostEqual(balance, 150000.00, places=4)

    def test_piechart(self):
        """ Piechart of 33% stock on 13/5/2021 is computed well"""

        for i in [13]:  # , 17, 19, 21]:
            dat = date(2021, 5, i)
            piechart = self.my_portfolio.get_portfolio_piechart(given_date=dat)
            logging.info("Piechart of 'my_portfolio' in %s on %s:\n %s",
                         self.my_portfolio.currency,
                         dat.isoformat(), str(piechart))
            self.assertAlmostEqual(piechart['stock'], 50/150*100, places=4)

    def test_purchase(self):
        """
        Balance after purchase of 10.5k€ of Amazon stock is computed well
        """

        dat1 = date(2021, 8, 14)
        balance1 = self.my_portfolio.get_portfolio_balance(given_date=dat1)
        logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                     self.my_portfolio.currency,
                     dat1.isoformat(), str(balance1))

        # get item by name from item_list
        amazon_stock = next(
            (item for item in self.my_portfolio.item_list
             if item.name == "Amazon"), None)

        dat2 = date(2021, 8, 15)
        num_titles = 3
        u_price = 3500.0
        other_charges = .05 * num_titles * u_price

        amazon_stock.purchase(
            when=dat2,
            units_purchased=num_titles,
            unit_price=u_price,
            fees=other_charges
        )

        balance2 = self.my_portfolio.get_portfolio_balance(given_date=dat2)
        logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                     self.my_portfolio.currency, dat2.isoformat(),
                     str(balance2))

        self.assertAlmostEqual(balance2-balance1, u_price*num_titles, places=4)
