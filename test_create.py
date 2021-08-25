#!/usr/bin/env python3

""" Crude tests for add_item() a"""

from utils import Portfolio
import logging
from datetime import date


def main():
    """ Create a fixture of a basic portfolio with some assets """

    # setup logging service
    # ::ENHANCEMENT:: should move this config info to an .env file
    config_file = './networth.log'
    log_level = logging.INFO
    logging.basicConfig(filename=config_file, filemode='w',
                        format='%(asctime)s::%(levelname)s::%(message)s',
                        datefmt='%Y.%m.%d %I:%M:%S%p', level=log_level)

    logging.info('\n-------RUN STARTS-------')

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
        portfolio_object = Portfolio(name=portfolio_sample['name'],
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
        item_object = my_portfolio.add_item(category=sample['category'],
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

    logging.info('Success')
    logging.info('\n--------RUN ENDS--------\n')


if __name__ == "__main__":
    # test.py ran directly
    main()
else:
    # test.py was imported
    pass
