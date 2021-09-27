#!/usr/bin/env python3

import logging
import json

import tkinter as tk
from tkinter import filedialog
from datetime import date, datetime

from src.utils import Portfolio


def portfolio_from_dict(portfolio_dict):
    """ Basic method to generate a Portfolio from a dict """

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
    """ Basic method to generate a dict from a Portfolio """

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


def serialize_date(obj):
    """ Aux function to serialize dates when saving JSON """

    if isinstance(obj, (datetime, date)):
        return {'_isoformat': obj.isoformat()}
    raise TypeError('...')


def deserialize_date(obj):
    """ Aux function to deserialize dates when reading JSON """

    _isoformat = obj.get('_isoformat')
    if _isoformat is not None:
        return date.fromisoformat(_isoformat)
    return obj


def read_portfolio_from_file(json_file_path=False):
    """ Read Portfolio from a JSON file """

    if not json_file_path:
        root = tk.Tk()
        root.withdraw()

        json_file_path = filedialog.askopenfilename(
            initialdir='./tests/',
            title="Select a file",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*"))
        )

    if not len(json_file_path):
        json_file_path = "./tests/fixtures.json"

    with open(json_file_path) as json_file:
        portfolio_dict = json.load(
            json_file, object_hook=deserialize_date)
    portfolio = portfolio_from_dict(portfolio_dict)
    return portfolio


def save_portfolio_to_file(portfolio, json_file_path=None):
    """ Save Portfolio to a JSON file """

    saved = False
    portfolio_dict = dict_from_portfolio(portfolio)
    if json_file_path is None:
        root = tk.Tk()
        root.withdraw()
        json_file_path = filedialog.asksaveasfilename(
            initialdir='./tests/',
            title='Choose filename',
            defaultextension='.json',
            filetypes=[("JSON files", "*.json")],
        )

    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(portfolio_dict, json_file, default=serialize_date,
                      ensure_ascii=False, indent=4, sort_keys=True)
        saved = True
    except Exception as error_msg:
        print("Saving failed because: ", error_msg)
    finally:
        return saved


if __name__ == '__main__':

    from tests.fixtures import sample_portfolio_dict

    portfolio_object = portfolio_from_dict(sample_portfolio_dict)

    print(f"Printing Portfolio with {len(portfolio_object.item_list)}"
          f" items:\n {portfolio_object.display()}")

