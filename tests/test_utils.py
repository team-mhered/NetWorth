#!/usr/bin/env python3

# tests/test_utils.py

""" Tests for Portfolio class"""

import unittest
import logging

from datetime import date
from src.utils import Portfolio, plot_piechart


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        """ Create a fixture of a basic portfolio with some items """

        # setup logging service
        # ::ENHANCEMENT:: should move this config info to an .env or a .cfg file
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
            {        # plot_piechart(piechart)
                'category': 'asset',
                'subcategory': 'stock',
                'currency': 'USD',
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
                'subcategory': 'account',
                'currency': 'ETH',
                'name': 'Ethereum',
                'description': 'Ethereum in Revolut'
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

        logging.info("Print 'my_portfolio' with %s items:\n %s",
                     len(my_portfolio.item_list), my_portfolio.display())

        for item in my_portfolio.item_list:
            if item.name == "Fondo NARANJA 50/40":
                item.update_history(when=date(2021, 8, 1),
                                    units_owned=1, cost_of_purchase=100000,
                                    value_of_asset=107963.89)
            if item.name == "Bitcoin":
                item.update_history(when=date(2021, 5, 12),
                                    units_owned=1, cost_of_purchase=50083.18,
                                    value_of_asset=1.1)

                item.update_history(when=date(2021, 8, 16),
                                    units_owned=1, cost_of_purchase=59407.83,
                                    value_of_asset=1.4)

                item.update_history(when=date(2021, 8, 21),
                                    units_owned=1, cost_of_purchase=59407.83,
                                    value_of_asset=1.4)

                item.update_history(when=date(2021, 6, 1),
                                    units_owned=1, cost_of_purchase=59407.83,
                                    value_of_asset=1.4)

        logging.info('Success')
        logging.info('\n--------FIXTURE CREATED---------\n')

        self.my_portfolio = my_portfolio

    def test_create(self):
        self.assertEqual(len(self.my_portfolio.item_list), 4)

    def test_balance(self):
        for i in [14]:  # , 17, 19, 21]:
            dat = date(2021, 8, i)
            balance = self.my_portfolio.get_portfolio_balance(given_date=dat)
            logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                         self.my_portfolio.currency, dat.isoformat(), str(balance))
            self.assertAlmostEqual(balance, 163860.222, places=4)

    def test_piechart(self):
        for i in [14]:  # , 17, 19, 21]:
            dat = date(2021, 8, i)
            piechart = self.my_portfolio.get_portfolio_piechart(given_date=dat)
            logging.info("Piechart of 'my_portfolio' in %s on %s:\n %s",
                         self.my_portfolio.currency, dat.isoformat(), str(piechart))
            self.assertAlmostEqual(piechart['fund'], 65.8878, places=4)
            # plot_piechart(piechart)


def test_purchase(self):
    """ Test that the purchase method works well"""

    dat1 = date(2021, 8, 14)
    balance1 = self.my_portfolio.get_portfolio_balance(given_date=dat1)
    logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                 self.my_portfolio.currency, dat1.isoformat(), str(balance1))

    # get item by name from item_list
    bitcoin_account = next(
        (item for item in self.my_portfolio.item_list
         if item.name == "Bitcoin"), None)

    dat2 = date(2021, 8, 15)
    num_titles = .1
    u_price = 50000
    other_charges = .05 * num_titles * u_price

    bitcoin_account.purchase(
        purchase_date=dat2,
        titles_purchased=num_titles,
        unit_price=u_price,
        fees=other_charges
    )

    balance2 = self.my_portfolio.get_portfolio_balance(given_date=dat2)
    logging.info("Balance of 'my_portfolio' in %s on %s:\n %s",
                 self.my_portfolio.currency, dat2.isoformat(), str(balance))

    self.assertAlmostEqual(balance2, 200000, places=4)

    def tearDown(self):
        pass


"""
def main():

if __name__ == "__main__":
    # test.py ran directly
    main()
else:
    # test.py was imported
    pass
"""
