#!/usr/bin/env python3

# tests/test_utils.py

""" Tests for Portfolio class"""

import logging
from unittest import TestCase
# from unittest.mock import patch

from datetime import date
from src.utils import Portfolio


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

        portfolio_samples = [
            {
                'name': 'My First Portfolio',
                'description': 'Test Portfolio',
                'currency': 'EUR'
            }
        ]

        # this allows creating more than one portfolio (maybe for future tests)
        for i, portfolio_sample in enumerate(portfolio_samples):
            portfolio_name = 'portfolio'+str(i).zfill(2)
            logging.info("Creating Portfolio '%s'...\n%s",
                         portfolio_name, portfolio_sample)
            portfolio_object = Portfolio(
                name=portfolio_sample['name'],
                currency=portfolio_sample['currency'],
                description=portfolio_sample['description'])
            if portfolio_object:
                logging.info('Success')

        # MH this is a ñapa
        my_portfolio = portfolio_object

        item_samples = [

            {
                'category': 'asset',
                'subcategory': 'fund',
                'currency': 'EUR',
                'name': 'Fondo NARANJA 50/40',
                'description': 'Investment fund in ING Direct'
            },
            {
                'category': 'asset',
                'subcategory': 'stock',
                'currency': 'EUR',
                'name': 'Amazon',
                'description': 'Amazon stock in Revolut'
            },
            {
                'category': 'asset',
                'subcategory': 'account',
                'currency': 'BTC',
                'name': 'Bitcoin',
                'description': 'Bitcoin in Revolut'
            },
            {
                'category': 'asset',
                'subcategory': 'real_state',
                'currency': 'EUR',
                'name': 'Kcity',
                'description': 'Apartamento en Kansas City'
            },
            {
                'category': 'other',
                'subcategory': 'other',
                'currency': 'ETH',
                'name': 'a',
                'description': 'Testing invalid input'
            }
        ]

        for i, sample in enumerate(item_samples):
            item_name = 'sample'+str(i).zfill(2)
            logging.info("Adding Item '%s' to Portfolio '%s'...\n%s",
                         item_name, my_portfolio.name, sample)
            item_object = my_portfolio.add_item(
                category=sample['category'],
                subcategory=sample['subcategory'],
                currency=sample['currency'],
                name=sample['name'],
                description=sample['description'])
            if item_object in my_portfolio.item_list:
                logging.info('Success')
                logging.debug("Printing '%s' :\n\n %s",
                              item_name, item_object.display())

        logging.debug("Print 'my_portfolio' with %s items:\n %s",
                      len(my_portfolio.item_list), my_portfolio.display())

        for item in my_portfolio.item_list:
            if item.name == "Fondo NARANJA 50/40":
                item.purchase(
                    when=date(2021, 2, 1),
                    units_purchased=1,
                    unit_price=50000.0,
                    fees=0.0
                )
                item.purchase(
                    when=date(2021, 3, 1),
                    units_purchased=1,
                    unit_price=30000.0,
                    fees=0.0
                )
                item.purchase(
                    when=date(2021, 4, 1),
                    units_purchased=1,
                    unit_price=20000.0,
                    fees=0.0
                )

            if item.name == "Amazon":
                item.purchase(
                    when=date(2021, 5, 12),
                    units_purchased=10,
                    unit_price=5000.0,
                    fees=0.0
                )
            """
            if item.name == "Bitcoin":
                item.purchase(
                    when=date(2021, 8, 1),
                    units_purchased=1,
                    unit_price=1.0,
                    fees=0.0
                )
            """
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
