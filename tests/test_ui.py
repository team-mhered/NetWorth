#!/usr/bin/env python3

# tests/test_ui.py

""" Tests for UI functions """

from src.ui import UI_purchase, UI_menu
from src.utils import Portfolio
from datetime import date
import unittest
import logging


class TestUI(unittest.TestCase):
    """ Class to test user interface methods """

    def setUp(self):
        """ Create a fixture of a basic portfolio with some items """

        # setup logging service
        # ::ENHANCEMENT:: move this config info to an .env or a .cfg file
        config_file = './tests/test_ui.log'
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

    def test_purchase_UI(self):
        """
        Balance after purchase created through text UI is computed well
        """

        dat1 = date(2021, 8, 14)
        balance1 = self.my_portfolio.get_portfolio_balance(given_date=dat1)
        logging.info("Balance of 'my_portfolio' in %s on %s: %s",
                     self.my_portfolio.currency,
                     dat1.isoformat(), str(balance1))

        user_input = UI_purchase(self.my_portfolio)

        user_input['Item'].purchase(
            when=user_input['date'],
            units_purchased=user_input['units_purchased'],
            unit_price=user_input['unit_price'],
            fees=user_input['fees'],
        )
        delta_balance = user_input['units_purchased']*user_input['unit_price']

        logging.info(self.my_portfolio.display())

        date_post_purchase = user_input['date']

        balance2 = self.my_portfolio.get_portfolio_balance(
            given_date=date_post_purchase)
        logging.info("Balance of 'my_portfolio' in %s on %s: %s",
                     self.my_portfolio.currency, date_post_purchase.isoformat(),
                     str(balance2))

        self.assertAlmostEqual(balance2-balance1, delta_balance, places=4)

    def test_purchase_UI(self):
        """
        Interactive text user interface's main menu
        """

        user_action = UI_menu(self.my_portfolio)

        # self.assertEqual(balance2-balance1, delta_balance)


if __name__ == '__main__':
    unittest.main()
