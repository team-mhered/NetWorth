#!/usr/bin/env python3

""" Crude tests for get_portfolio_balance()"""

from utils import Portfolio, Item  # HistoryPoint, generate_unique_id
import logging
from datetime import date


def main():
    """ Test creating a portfolio with a couple of assets """

    # setup logging service
    # ::ENHANCEMENT:: should move this config info to an .env file
    config_file = './networth.log'
    log_level = logging.INFO
    logging.basicConfig(filename=config_file, filemode='w',
                        format='%(asctime)s::%(levelname)s::%(message)s',
                        datefmt='%Y.%m.%d %I:%M:%S%p', level=log_level)

    logging.info('\n-------RUN STARTS-------')
    logging.info('Create a Portfolio')
    portfolio1 = Portfolio(name="My First Portfolio", currency="USD",
                           description="Test portfolio")
    logging.debug("Print 'portfolio1' with empty list of items:\n %s",
                  portfolio1.display())

    logging.info("Add 'fund1' Item")

    fund1 = portfolio1.add_item(category='asset', subcategory='fund', currency='EUR',
                                name='Fondo NARANJA 50/40',
                                description='Investment fund in ING Direct')

    logging.debug("Print 'fund1' without history:\n\n %s", fund1.display())

    logging.info("Update History of 'fund1' Item")

    fund1.update_history(when=date(2021, 8, 16),
                         units_owned=1, cost_of_purchase=100000,
                         value_of_asset=107963.89)
    logging.debug("Print 'fund1' with 1 history point:\n\n %s",
                  fund1.display())

    logging.debug("Print 'portfolio1' with item 'fund1':\n %s",
                  portfolio1.display())

    logging.info("Add 'crypto1' Item")

    crypto1 = portfolio1.add_item(category='asset', subcategory='currency', currency='BTC',
                                  name='Bitcoin', description='Bitcoin in Revolut')

    logging.debug("Print 'crypto1' without history:\n\n %s",
                  crypto1.display())

    logging.info("Update History of 'crypto1' Item")

    crypto1.update_history(when=date(2021, 5, 12),
                           units_owned=1.1, cost_of_purchase=50083.18,
                           value_of_asset=30000)

    crypto1.update_history(when=date(2021, 8, 16),
                           units_owned=1.4, cost_of_purchase=59407.83,
                           value_of_asset=45000)

    crypto1.update_history(when=date(2021, 8, 21),
                           units_owned=1.4, cost_of_purchase=59407.83,
                           value_of_asset=60000)

    crypto1.update_history(when=date(2021, 6, 1),
                           units_owned=1.4, cost_of_purchase=59407.83,
                           value_of_asset=35000)

    logging.debug("Print 'crypto1' with 4 history points:\n\n %s",
                  crypto1.display())

    logging.info("Print 'portfolio1' with 2 items with history:\n %s",
                 portfolio1.display())

    logging.info('Testing get_item_balance...\n')
    for i in [14, 15, 16, 17, 19, 20, 21]:
        dat = date(2021, 8, i)
        balance = crypto1.get_item_balance(currency='EUR', given_date=dat)
        logging.debug("Balance of 'crypto1' in EUR on %s:\n %s",
                      dat.isoformat(), str(balance))

    logging.info('Testing get_portfolio_balance...\n')
    for i in [14, 15, 16, 17, 19, 20, 21]:
        dat = date(2021, 8, i)
        balance = portfolio1.get_portfolio_balance(given_date=dat)
        logging.debug("Balance of 'portfolio1' in EUR on %s:\n %s",
                      dat.isoformat(), str(balance))

    logging.info('Success')
    logging.info('\n--------RUN ENDS--------\n')

    """
    # this should fail
    crypto1 = Item(category='asset', subcategory='stock', currency='USD',
                   name='Amazon', description='Amazon stock in Revolut',
                   portfolio=None)
    """


if __name__ == "__main__":
    # test.py ran directly
    main()
else:
    # test.py was imported
    pass
