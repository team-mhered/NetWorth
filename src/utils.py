#!/usr/bin/env python3

""" Basic Classes Portfolio, Item, HistoryPoint and methods"""

import uuid
import matplotlib.pyplot as plt
from datetime import date
from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates
import logging
import bisect

# cfr. Classes https://docs.python.org/3/tutorial/classes.html
# cfr. logging https://docs.python.org/3/howto/logging.html


supported_categories = ['asset', 'liability']
supported_subcategories = ['account', 'fund', 'stock', 'real state']
supported_currencies = ['USD', 'EUR', 'PLN', 'GBP']
supported_crypto = ['BTC']


def generate_unique_id():
    """ Wrapper function that generates unique IDs via an external service """
    return uuid.uuid4()


def get_exchange_rate(given_date: date, from_currency: str, to_currency: str):
    """
    Get exchange rates on a given date for USD EUR PLN GBP BTC
    """

    rate = None
    today = date.today()
    # check date is valid
    if given_date > today:
        logging.warning("%s is a date in the future", given_date.isoformat())
    else:
        # check input currencies are valid
        supported_currencies = ['USD', 'EUR', 'PLN', 'GBP']
        supported_crypto = ['BTC']
        supported_all = supported_currencies + supported_crypto
        curr_not_supported = {curr for curr in
                              [from_currency, to_currency]
                              if curr not in supported_all}
        if bool(curr_not_supported):
            logging.warning('%s currency not supported',
                            str(curr_not_supported))
        elif all(curr in supported_currencies
                 for curr in [from_currency, to_currency]):
            # all currencies are forex
            # if not bool(c): # initialize only if needed
            init_forex = CurrencyRates()
            if given_date == today:
                rate = init_forex.get_rate(from_currency, to_currency)
            else:
                rate = init_forex.get_rate(from_currency, to_currency,
                                           given_date)
        else:
            # at least one of the rates is BTC
            # if both rates are BTC -> return 1
            if from_currency == 'BTC' and to_currency == 'BTC':
                rate = 1
            else:
                # one of the rates is BTC
                # if not bool(b): # initialize only if needed
                init_crypto = BtcConverter()  # force_decimal=True for decimal rate
                if from_currency == 'BTC':
                    if given_date == today:
                        rate = init_crypto.get_latest_price(to_currency)
                    else:
                        # given_date < today
                        rate = init_crypto.get_previous_price(to_currency,
                                                              given_date)
                elif to_currency == 'BTC':
                    if given_date == today:
                        rate = 1/init_crypto.get_latest_price(from_currency)
                    else:
                        # given_date < today
                        rate = 1/init_crypto.get_previous_price(from_currency,
                                                                given_date)
                else:
                    logging.warning("get_exchange_rate failed unexpectedly")
    return rate


def plot_piechart(dict):
    """ Plot piechart with the slices ordered counter-clockwise. """

    labels = dict.keys()
    sizes = dict.values()
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio so pie is drawn as a circle.

    plt.show()


class Portfolio:
    """ Portfolio: List of Items (Assets and Liabilities) """

    def __init__(self, name: str, description: str, currency: str):
        """ Portfolio constructor"""

        self.unique_id = generate_unique_id()
        self.name = name
        self.description = description
        self.currency = currency
        self.item_list = []  # creates a new empty list of Items

    def add_item(self, category: str, subcategory: str, currency: str,
                 name: str, description: str):
        """ Add Item to Portfolio """

        logging.info("Adding Item '%s' to Portfolio '%s'...",
                     name, self.name)
        reason = ""
        if len(name) < 3:
            reason += f"\nName '{name}' is too short. "
        if category.lower() not in supported_categories:
            reason += f"\nCategory '{category}' not supported. "
        if subcategory.lower() not in supported_subcategories:
            reason += f"\nSubcategory '{subcategory}' not supported. "
        if len(reason) > 0:
            logging.warning("Item '%s' not added to Portfolio '%s' due to: %s",
                            name, self.name, reason)
            return None
        if currency.upper() not in supported_currencies + supported_crypto:
            logging.warning("Auto-update of '%s' currency is not supported.",
                            currency)

        new_item = Item(category=category, subcategory=subcategory,
                        currency=currency, name=name,
                        description=description, portfolio=self)
        self.item_list.append(new_item)
        if new_item in self.item_list:
            logging.info("Success")
        return new_item

    def get_portfolio_balance(self, given_date: date):
        """ Get Portfolio balance on a given date in the Portfolio currency"""

        portfolio_balance = 0
        for item in self.item_list:
            (closest_date, closest_balance) = item.get_item_balance(
                self.currency, given_date)
            # would be good to return closest_date to give transparency
            portfolio_balance += closest_balance

        return portfolio_balance

    def get_portfolio_piechart(self, given_date: date):
        """ Get Portfolio piechart by subcategories on a given date in the Portfolio currency"""

        piechart = {'portfolio_balance': 0}
        for item in self.item_list:
            (closest_date, closest_balance) = item.get_item_balance(
                self.currency, given_date)
            # would be good to return closest_date to give transparency
            piechart['portfolio_balance'] += closest_balance
            if item.subcategory in piechart:
                piechart[item.subcategory] += closest_balance
            else:
                piechart[item.subcategory] = closest_balance
        balance = piechart.pop('portfolio_balance')
        for key, value in piechart.items():
            piechart[key] = 100 * value/balance
        return piechart

    def get_portfolio_currency(self):
        """ Get currency of a Portfolio"""

        return self.currency

    def display(self):
        """ Display Portfolio(text)"""

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
        """Item constructor"""

        self.name = name
        self.description = description
        self.category = category
        self.subcategory = subcategory
        self.currency = currency

        self.unique_id = generate_unique_id()
        self.deleted = False
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

    def get_item_balance(self, currency: str, given_date: date):
        """ Get Item balance in a given currency and on a given date """

        if bool(self.history):
            tmp_list = [(hist_pt.when,
                         hist_pt.units_owned * hist_pt.value_of_asset)
                        for hist_pt in self.history]

            logging.debug("tmp list %s", str(tmp_list))
            sorted_by_date = sorted(tmp_list, key=lambda tup: tup[0])

            logging.debug("sorted list %s", str(sorted_by_date))
            sorted_dates = [elem[0] for elem in sorted_by_date]

            logging.debug("sorted_dates %s", sorted_dates)
            index_closest_match = bisect.bisect(sorted_dates, given_date)

            closest_match = sorted_by_date[index_closest_match-1]
            logging.debug("i: %s tuple: %s",
                          str(index_closest_match), str(closest_match))

            exchange_rate = get_exchange_rate(given_date,
                                              from_currency=self.currency,
                                              to_currency=currency)
            closest_date = closest_match[0]
            closest_balance = closest_match[1] * exchange_rate
        else:  # empty list
            logging.warning(
                "get_item_balance() returns 0 for Item with empty History: %s ('%s')",
                str(self.unique_id), self.name)
            closest_date = given_date
            closest_balance = 0

        return (closest_date, closest_balance)

    def display(self):
        """ Display Item(text)"""

        msgs = []
        msgs.append('\n  ITEM')
        msgs.append('\n  ----')
        msgs.append('\n  Unique ID: ' + str(self.unique_id))
        msgs.append('\n  Category: ' + self.category)
        msgs.append('\n  Subcategory: ' + self.subcategory)
        msgs.append('\n  Currency: ' + self.currency)
        msgs.append('\n  Name: ' + self.name)
        msgs.append('\n  Description: ' + self.description)
        msgs.append('\n  HISTORY')
        curr_port = self.portfolio.get_portfolio_currency()
        curr_item = self.currency

        msgs.append(f"""
        _________________________________________________________________
        |     Date      |  Units Owned  |   Cost ({curr_port})  |  Value ({curr_item})  |
        -----------------------------------------------------------------""")

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

    def display(self):
        """ Display HistoryPoint(text)"""

        msgs = []
        msgs.append("\n        |")
        msgs.append("{0:^15}".format(
            self.when.isoformat())+'|')  # date
        msgs.append("{0:^15}".format(
            f'{self.units_owned:.2f}')+'|')  # units
        msgs.append("{0:^15}".format(
            f'{self.cost_of_purchase:.2f}')+'|')  # cost
        msgs.append("{0:^15}".format(
            f'{self.value_of_asset:.2f}')+'|')  # value
        msgs.append("""
        -----------------------------------------------------------------""")

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

    fund1 = portfolio1.add_item(category='asset', subcategory='fund',
                                currency='EUR', name='Fondo NARANJA 50/40',
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

    crypto1 = portfolio1.add_item(category='asset', subcategory='account',
                                  currency='BTC', name='Bitcoin',
                                  description='Bitcoin in Revolut')

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

    crypto1.update_history(when=date(2021, 8, 21),
                           units_owned=1.4, cost_of_purchase=59407.83,
                           value_of_asset=58584.21)

    logging.debug("Print 'crypto1' with 3 history points:\n\n %s",
                  crypto1.display())

    print("Print 'portfolio1' with 2 items with history:\n %s",
          portfolio1.display())

    logging.info('Success')
    logging.info('\n--------RUN ENDS--------\n')

    """
    # this should fail
    crypto1 = Item(category='asset', subcategory='stock', currency='USD',
                   name='Amazon', description='Amazon stock in Revolut',
                   portfolio=None)
    """


if __name__ == "__main__":
    # utils.py ran directly
    main()
else:
    # utils.py was imported
    pass
