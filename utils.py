#!/usr/bin/env python3

"""" Basic Classes Portfolio, Item, HistoryPoint"""

import logging
import uuid
from datetime import date


# cfr. Classes https://docs.python.org/3/tutorial/classes.html
# cfr. logging https://docs.python.org/3/howto/logging.html


def generate_unique_id():
    """ A wrapper function that calls an external service to generate unique IDs """
    return uuid.uuid4()


class Portfolio:
    """ Portfolio: List of Items (Assets and Liabilities) """

    def __init__(self, name: str, description: str, currency: str):
        self.unique_id = generate_unique_id()
        self.name = name
        self.description = description
        self.currency = currency
        self.item_list = []  # creates a new empty list of Items

    def add_item(self, category: str, subcategory: str, currency: str,
                 name: str, description: str):
        """ Add Item to Portfolio """
        new_item = Item(category=category, subcategory=subcategory, currency=currency,
                        name=name, description=description, portfolio=self)
        self.item_list.append(new_item)
        return new_item

    def display(self):
        """ Display Portfolio (text)"""
        msgs = []
        msgs.append('----------')
        msgs.append('\nPORTFOLIO')
        msgs.append('\n----------')
        msgs.append('\nUnique ID: ' + str(self.unique_id))
        msgs.append('\nName: ' + self.name)
        msgs.append('\nDescription: ' + self.description)
        msgs.append('\nCurrency: ' + self.currency)
        msgs.append('\nITEM LIST:')
        msgs.append('\n----------')
        if bool(self.item_list):
            for item in self.item_list:
                msgs.append(item.display())
        else:  # empty list
            msgs.append('\n  None\n')
        msg = ''.join(msgs)
        return msg


class Item:
    """Item: Asset or Liability"""

    def __init__(self, category: str, subcategory: str, currency: str,
                 name: str, description: str, portfolio: Portfolio):
        self.unique_id = generate_unique_id()
        self.name = name
        self.description = description
        self.currency = currency
        self.category = category
        self.subcategory = subcategory
        self.portfolio = portfolio  # initialize Item in portfolio
        self.history = []  # creates a new empty list of HistoryPt

    def update_history(self, when: date, units_owned: float,
                       cost_of_purchase: float, value_of_asset: float):
        """ Add to Item a HistoryPoint: historic valuation to an Item"""

        hist_pt = HistoryPoint(when=when, units_owned=units_owned,
                               cost_of_purchase=cost_of_purchase,
                               value_of_asset=value_of_asset)
        self.history.append(hist_pt)
        hist_pt.item = self  # to access properties of parent item

    def display(self):
        """ Display Item (text)"""
        msgs = []
        msgs.append('\n  ITEM')
        msgs.append('\n  ----')
        msgs.append('\n  Unique ID: ' + str(self.unique_id))
        msgs.append('\n  Category: ' + self.category)
        msgs.append('\n  Subcategory: ' + self.subcategory)
        msgs.append('\n  Currency: ' + self.currency)
        msgs.append('\n  Name: ' + self.name)
        msgs.append('\n  Description: ' + self.description)
        msgs.append('\n  HISTORY:')
        msgs.append('\n  --------')
        if bool(self.history):
            for hist_pt in self.history:
                msgs.append(hist_pt.display())
        else:  # empty list
            msgs.append('\n    None\n')
        msg = ''.join(msgs)
        return msg


class HistoryPoint:
    """ HistoryPoint: historic valuation of Item"""

    def __init__(self, when: date, units_owned: float,
                 cost_of_purchase: float, value_of_asset: float):
        self.when = when
        self.units_owned = units_owned
        self.cost_of_purchase = cost_of_purchase
        self.value_of_asset = value_of_asset
        self.item = None  # initializes HistoryPoint as orphan

    def get_currency_portfolio(self):
        """ Obtain currency of parent portfolio"""
        try:
            currency = self.item.portfolio.currency
        except Exception as ex:
            currency = None
            logging.warning(ex)
        return currency

    def display(self):
        """ Display HistoryPoint (text)"""
        msgs = []
        msgs.append('\n    HISTORY POINT')
        msgs.append('\n    -------------')
        msgs.append('\n    Date: ' + self.when.isoformat())  # date
        msgs.append('\n    Units Owned: ' + f'{self.units_owned:.2f}')  # units
        msgs.append('\n    Cost: ' + f'{self.cost_of_purchase:.2f}'
                    + ' ' + self.get_currency_portfolio())  # cost
        msgs.append('\n    Value: ' + f'{self.value_of_asset:.2f}'
                    + ' ' + self.get_currency_portfolio())  # value
        msg = ''.join(msgs)
        return msg


def main():
    """ Test creating a portfolio with a couple of assets """

    # setup logging service
    # ::ENHANCEMENT:: should move this config info to an .env file
    config_file = './networth.log'
    log_level = logging.DEBUG
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
                           value_of_asset=45131.46)

    crypto1.update_history(when=date(2021, 6, 1),
                           units_owned=1.4, cost_of_purchase=59407.83,
                           value_of_asset=42672.53)

    crypto1.update_history(when=date(2021, 8, 16),
                           units_owned=1.4, cost_of_purchase=59407.83,
                           value_of_asset=55091.67)

    logging.debug("Print 'crypto1' with 3 history points:\n\n %s",
                  crypto1.display())

    print("Print 'portfolio1' with 2 items with history:\n %s",
          portfolio1.display())

    logging.info('Success')
    logging.info('\n--------RUN ENDS--------\n')

    # this should fail
    crypto1 = Item(category='asset', subcategory='stock', currency='USD',
                   name='Amazon', description='Amazon stock in Revolut',
                   portfolio=None)


if __name__ == "__main__":
    # utils.py ran directly
    main()
else:
    # utils.py was imported
    pass
