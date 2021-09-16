#!/usr/bin/env python3

from src.utils import Portfolio
from datetime import date

import logging

from pprint import pprint

""" Basic method to read Portfolio from a dict """


def portfolio_from_dict(portfolio_dict):

    portfolio_object = Portfolio(
        name=portfolio_dict['name'],
        currency=portfolio_dict['currency'],
        description=portfolio_dict['description'])

    item_list = portfolio_dict['item_list']

    for i, sample in enumerate(item_list):
        item_name = 'sample'+str(i).zfill(2)
        logging.info("Adding Item '%s' to Portfolio '%s'...\n%s",
                     item_name, portfolio_object.name, sample)
        item_object = portfolio_object.add_item(
            category=sample['category'],
            subcategory=sample['subcategory'],
            currency=sample['currency'],
            name=sample['name'],
            description=sample['description'])
        if item_object in portfolio_object.item_list:
            logging.info('Success')
            logging.debug("Printing '%s' :\n\n %s",
                          item_name, item_object.display())

        if 'ledger' in sample:
            ledger = sample['ledger']
            for j, transaction in enumerate(ledger):
                transaction_name = 'transaction'+str(j).zfill(3)
                logging.info("Applying transaction '%s' to Item '%s'...\n%s",
                             transaction_name, item_object.name, transaction)
                transaction_type, transaction_data = transaction
                if transaction_type == 'purchase':
                    item_object.purchase(
                        when=transaction_data['when'],
                        units_purchased=transaction_data['units_purchased'],
                        unit_price=transaction_data['unit_price'],
                        fees=transaction_data['fees'],
                    )
                else:
                    debug.warning("Unsupported transaction of type %s",
                                  transaction_type)

    return portfolio_object


def dict_from_portfolio(portfolio):
    portfolio_dict = {}
    portfolio_keys = ['name', 'description', 'currency']
    item_keys = ['category', 'subcategory', 'currency', 'name', 'description']
    # ::bug:: these are not hist_pt properties they are parameters for purchase
    transaction_keys = ['when', 'units_purchased', 'unit_price', 'fees']

    for portfolio_key in portfolio_keys:
        if hasattr(portfolio, portfolio_key):
            portfolio_dict[portfolio_key] = getattr(portfolio, portfolio_key)
        else:
            portfolio_dict[portfolio_key] = None

    # scan and retrieve item_list
    item_list_dict = []

    if hasattr(portfolio, 'item_list'):
        for item in portfolio.item_list:
            item_dict = {}
            # retrieve keys
            for item_key in item_keys:
                if hasattr(item, item_key):
                    item_dict[item_key] = getattr(item, item_key)
                else:
                    item_dict[item_key] = None

            # scan and retrieve history
            ledger_dict = []
            if hasattr(item, 'ledger'):
                for transaction in item.ledger:
                    ledger_dict.append(transaction)

            item_dict['ledger'] = ledger_dict[:]
            item_list_dict.append(item_dict)

    portfolio_dict['item_list'] = item_list_dict[:]

    return portfolio_dict


portfolio_dict = {
    'name': 'My First Portfolio',
    'description': 'Test Portfolio',
    'currency': 'EUR',
    'item_list': [
            {
                'category': 'asset',
                'subcategory': 'fund',
                'currency': 'EUR',
                'name': 'Fondo NARANJA 50/40',
                'description': 'Investment fund in ING Direct',
                'ledger': [
                    ('purchase',
                        {
                            'when': date(2021, 2, 1),
                            'units_purchased': 1,
                            'unit_price': 50000.0,
                            'fees': 0.0
                        }
                     ),
                    ('purchase',
                        {
                            'when': date(2021, 3, 1),
                            'units_purchased': 1,
                            'unit_price': 30000.0,
                            'fees': 0.0
                        }
                     ),
                    ('purchase',
                     {
                         'when': date(2021, 4, 1),
                         'units_purchased': 1,
                         'unit_price': 20000.0,
                         'fees': 0.0
                     }
                     ),
                ],
            },
        {
                'category': 'asset',
                'subcategory': 'stock',
                'currency': 'EUR',
                'name': 'Amazon',
                'description': 'Amazon stock in Revolut',
                'ledger': [
                            ('purchase',
                             {
                                 'when': date(2021, 5, 12),
                                 'units_purchased': 10,
                                 'unit_price': 5000.0,
                                 'fees': 0.0,
                             }
                             ),
                ],
            },
        {
                'category': 'asset',
                'subcategory': 'account',
                'currency': 'BTC',
                'name': 'Bitcoin',
                'description': 'Bitcoin in Revolut',
            },
        {
                'category': 'asset',
                'subcategory': 'real_state',
                'currency': 'EUR',
                'name': 'Kcity',
                'description': 'Apartamento en Kansas City',
            },
        {
                'category': 'other',
                'subcategory': 'other',
                'currency': 'ETH',
                'name': 'a',
                'description': 'Testing invalid input',
            },
    ],
}

portfolio_object = portfolio_from_dict(portfolio_dict)

print(f"Printing 'my_portfolio' with {len(portfolio_object.item_list)}"
      f" items:\n {portfolio_object.display()}")

dict = dict_from_portfolio(portfolio_object)
pprint(dict)
portfolio_object2 = portfolio_from_dict(dict)


print("Check :", portfolio_object == portfolio_object2)
