#!/usr/bin/env python3
import logging
import uuid
from datetime import date


# cfr. Classes https://docs.python.org/3/tutorial/classes.html
# cfr. logging https://docs.python.org/3/howto/logging.html


def UniqueID():
    """ A function that generates unique IDs """

    unique_id = uuid.uuid4()
    return unique_id


class Portfolio:
    """ Portfolio of Assets and Liabilities """

    def __init__(self, name: str, description: str, currency: str):
        self.id = UniqueID()
        self.name = name
        self.description = description
        self.currency = currency
        self.item_list = []  # creates a new empty list of Items

    def add_item(self, type: str, subtype: str, currency: str,
                 name: str, description: str):
        new_item = Item(type=type, subtype=subtype, currency=currency,
                        name=name, description=description, portfolio=self)
        self.item_list.append(new_item)
        return new_item

    def display(self):
        l = []
        l.append('----------')
        l.append('\nPORTFOLIO')
        l.append('\n----------')
        l.append('\nUniqueID: ' + str(self.id))
        l.append('\nName: ' + self.name)
        l.append('\nDescription: ' + self.description)
        l.append('\nCurrency: ' + self.currency)
        l.append('\nITEM LIST:')
        l.append('\n----------')
        if len(self.item_list):
            for item in self.item_list:
                l.append(item.display())
        else:  # empty list
            l.append('\n  None\n')
        s = ''.join(l)
        return s


class Item:
    """Item: Asset or Liability"""

    def __init__(self, type: str, subtype: str, currency: str,
                 name: str, description: str, portfolio: Portfolio):
        self.id = UniqueID()
        self.name = name
        self.description = description
        self.currency = currency
        self.type = type
        self.subtype = subtype
        self.portfolio = portfolio  # initialize Item in portfolio
        self.history = []  # creates a new empty list of HistoryPt

    def update_history(self, when: date, units_owned: float,
                       cost_of_purchase: float, value_of_asset: float):

        hist_pt = HistoryPoint(when=when, units_owned=units_owned,
                               cost_of_purchase=cost_of_purchase,
                               value_of_asset=value_of_asset)
        self.history.append(hist_pt)
        hist_pt.item = self  # to access properties of parent item

    def display(self):
        l = []
        l.append('\n  ITEM')
        l.append('\n  ----')
        l.append('\n  UniqueID: ' + str(self.id))
        l.append('\n  Type: ' + self.type)
        l.append('\n  Subtype: ' + self.subtype)
        l.append('\n  Currency: ' + self.currency)
        l.append('\n  Name: ' + self.name)
        l.append('\n  Description: ' + self.description)
        l.append('\n  HISTORY:')
        l.append('\n  --------')
        if len(self.history):
            for hist_pt in self.history:
                l.append(hist_pt.display())
        else:  # empty list
            l.append('\n    None\n')
        s = ''.join(l)
        return s


class HistoryPoint:
    def __init__(self, when: date, units_owned: float,
                 cost_of_purchase: float, value_of_asset: float):
        self.when = when
        self.units_owned = units_owned
        self.cost_of_purchase = cost_of_purchase
        self.value_of_asset = value_of_asset
        self.item = None  # initializes HistoryPoint as orphan

    def display(self):
        """ Display data of history point"""

        l = []
        l.append('\n    HISTORY POINT')
        l.append('\n    -------------')
        l.append('\n    Date: ' + self.when.isoformat())  # date
        l.append('\n    Units Owned: ' + f'{self.units_owned:.2f}')  # units
        l.append('\n    Cost: ' + f'{self.cost_of_purchase:.2f}'
                 + ' ' + self.item.portfolio.currency)  # cost
        l.append('\n    Value: ' + f'{self.value_of_asset:.2f}'
                 + ' ' + self.item.portfolio.currency)  # value
        s = ''.join(l)
        return s


def main():
    """ Test creating a portfolio with a couple of assets """

    # setup logging service
    # ::ENHANCEMENT:: need to move this config info to an .env file
    CONFIGFILE = './networth.log'
    LOGLEVEL = logging.DEBUG
    logging.basicConfig(filename=CONFIGFILE, filemode='w',
                        format='%(asctime)s::%(levelname)s::%(message)s',
                        datefmt='%Y.%m.%d %I:%M:%S%p', level=LOGLEVEL)

    logging.info('\n-------RUN STARTS-------')
    logging.info('Create a Portfolio')
    portfolio1 = Portfolio(name="My First Portfolio", currency="USD",
                           description="Test portfolio")
    logging.debug("Print 'portfolio1' with empty list of items:\n" + portfolio1.display())

    logging.info("Add 'fund1' Item")

    fund1 = portfolio1.add_item(type='asset', subtype='fund', currency='EUR',
                                name='Fondo NARANJA 50/40',
                                description='Investment fund in ING Direct')

    logging.debug("Print 'fund1' without history:\n\n" + fund1.display())

    logging.info("Update History of 'fund1' Item")

    fund1.update_history(when=date(2021, 8, 16),
                         units_owned=1, cost_of_purchase=100000,
                         value_of_asset=107963.89)
    logging.debug("Print 'fund1' with 1 history point:\n\n" + fund1.display())

    logging.debug("Print 'portfolio1' with item 'fund1':\n" + portfolio1.display())

    logging.info("Add 'crypto1' Item")

    crypto1 = portfolio1.add_item(type='asset', subtype='currency', currency='BTC',
                                  name='Bitcoin', description='Bitcoin in Revolut')

    logging.debug("Print 'crypto1' without history:\n\n" + crypto1.display())

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

    logging.debug("Print 'crypto1' with 3 history points:\n\n" + crypto1.display())

    print("Print 'portfolio1' with 2 items with history:\n", portfolio1.display())

    logging.info('Success')
    logging.info('\n--------RUN ENDS--------\n')


if __name__ == "__main__":
    # utils.py ran directly
    main()
else:
    # utils.py was imported
    pass
