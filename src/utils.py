#!/usr/bin/env python3

""" Basic Classes Portfolio, Item, HistoryPoint and methods"""

import uuid
import logging
import bisect
from datetime import date
from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates

import matplotlib.pyplot as plt

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
            forex_handler = CurrencyRates()
            if given_date == today:
                rate = forex_handler.get_rate(from_currency, to_currency)
            else:
                rate = forex_handler.get_rate(from_currency, to_currency,
                                              given_date)
        else:
            # at least one of the rates is BTC
            # if both rates are BTC -> return 1
            if from_currency == 'BTC' and to_currency == 'BTC':
                rate = 1
            else:
                # one of the rates is BTC
                # if not bool(b): # initialize only if needed
                crypto_handler = BtcConverter()  # force_decimal=True for decimal rate
                if from_currency == 'BTC':
                    if given_date == today:
                        rate = crypto_handler.get_latest_price(to_currency)
                    else:
                        # given_date < today
                        rate = crypto_handler.get_previous_price(to_currency,
                                                                 given_date)
                elif to_currency == 'BTC':
                    if given_date == today:
                        rate = 1/crypto_handler.get_latest_price(from_currency)
                    else:
                        # given_date < today
                        rate = 1/crypto_handler.get_previous_price(from_currency,
                                                                   given_date)
                else:
                    logging.warning("get_exchange_rate failed unexpectedly")
    return rate


def plot_piechart(piechart_dict):
    """ Plot piechart with the slices ordered counter-clockwise. """

    labels = piechart_dict.keys()
    sizes = piechart_dict.values()
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
            closest_balance, _ = item.get_item_balance(
                self.currency, given_date)
            # would be good to return closest_date to give transparency
            portfolio_balance += closest_balance

        return portfolio_balance

    def get_portfolio_piechart(self, given_date: date):
        """ Get Portfolio piechart by subcategories on a given date in the Portfolio currency"""

        piechart = {'portfolio_balance': 0}
        for item in self.item_list:
            closest_balance, _ = item.get_item_balance(
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
        """ Display Portfolio as text"""

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

    def purchase(self, when: date, units_purchased: float,
                 unit_price: float, fees: float):
        """ Purchase units of an Item"""

        # 1) input validation
        # Given transaction inputs :
        # date, units_purchased, unit_price, fees paid

        valid_input = True

        # When date is valid date
        if not isinstance(when, date) or when <= date.today():
            success = False
            logging.warning("purchase fails due to invalid date %s",
                            when.isoformat())

        # And unit_price, fees are floats
        if isinstance(unit_price, float) and isinstance(fees, float):
            pass
        else:
            valid_input = False
            logging.warning("purchase fails because units_price or fees are"
                            " not of type float as expected")

        if self.subcategory in ['account', 'fund']:
            # And for assets of subcategory account, fund : units_purchased is always 1
            if units_purchased != 1:
                valid_input = False
                logging.warning(
                    "purchase fails due to units_purchased != 1"
                    " for %s item: %s ('%s')",
                    self.subcategory, str(self.unique_id), self.name)

        elif self.subcategory == 'stock':
            # And for assets of subcategory stock:
            # units_ purchased is an integer
            if not isinstance(units_purchased, int):
                valid_input = False
                logging.warning(
                    "purchase fails because units_purchased is not of "
                    "type int as expected for %s items : %s ('%s')",
                    self.subcategory, str(self.unique_id), self.name)

        elif self.subcategory == 'real state':
            # And for assets of subcategory real_state:
            # units_ purchased is a float in range [0-1]
            # (representing % of ownership)
            if isinstance(units_purchased, float):
                if units_purchased < 0 or units_purchased > 1:
                    valid_input = False
                    logging.warning(
                        "purchase fails because units_purchased out of "
                        "expected range [0, 1] for %s items : %s ('%s')",
                        self.subcategory, str(self.unique_id), self.name)
            else:
                valid_input = False
                logging.warning(
                    "purchase fails because units_purchased is not of "
                    "type float as expected for %s items : %s ('%s')",
                    self.subcategory, str(self.unique_id), self.name)
        else:
            valid_input = False
            logging.warning(
                "purchase fails for Item"
                " of unsupported subcategory %s: %s ('%s')",
                self.subcategory, str(self.unique_id), self.name)

        if valid_input:
            # 2) get asset status prior to purchase
            prior_hist_pt = self.get_hist_pt_by_date(self, when)
            if prior_hist_pt is None:
                cost = 0
                units = 0
                value = 0
            else:
                cost = prior_hist_pt.cost_of_purchase
                units = prior_hist_pt.units_owned
                value = prior_hist_pt.value_of_asset

            # 3) compute asset status post purchase

            # in what currency?
            cost += (units_purchased * unit_price + fees)
            units += units_purchased
            value = units * unit_price

            # date, amount_invested, fees paid, new_value
            # cost + = amount invested(unit_price) + fees
            # value = new value(after investment)

            # 4) call update_history method to save new hist_pt
            self.update_history(when=when, units_owned=units,
                                cost_of_purchase=cost, value_of_asset=value)
            sucess = True
        else:
            success = valid_input

        return success

    def update_history(self, when: date, units_owned: float,
                       cost_of_purchase: float, value_of_asset: float):
        """ Add to Item a HistoryPoint: historic valuation to an Item"""

        hist_pt = HistoryPoint(when=when, units_owned=units_owned,
                               cost_of_purchase=cost_of_purchase,
                               value_of_asset=value_of_asset)
        self.history.append(hist_pt)
        hist_pt.item = self  # to access properties of parent item

    def get_hist_pt_by_date(self, given_date: date,
                            force_exact_match: bool = False):
        """
           Get HistoryPoint in item_list by date
           By default it finds the HistoryPoint that is earlier and closest
           to the given date.
           force_exact_match flag = True forces an exact match
           returns None if not found.
           """

        if bool(self.history):
            tmp_list = [(hist_pt.when,
                         hist_pt.unique_id)
                        for hist_pt in self.history]
            logging.debug("tmp list %s", str(tmp_list))

            sorted_by_date = sorted(tmp_list, key=lambda tup: tup[0])
            logging.debug("sorted list %s", str(sorted_by_date))

            sorted_dates = [elem[0] for elem in sorted_by_date]
            logging.debug("sorted_dates %s", sorted_dates)

            index_closest_match = bisect.bisect(sorted_dates, given_date)-1

            if index_closest_match >= 0:
                closest_match = sorted_by_date[index_closest_match]
                logging.debug("i: %s tuple: %s",
                              str(index_closest_match), str(closest_match))
                closest_match_date, closest_match_uid = closest_match

                closest_hist_pt = next((hist_pt for hist_pt in self.history if
                                        hist_pt.unique_id == closest_match_uid
                                        ), None)
                if force_exact_match:
                    if closest_match_date != given_date:
                        closest_hist_pt = None

            else:
                logging.warning(
                    "get_hist_pt_by_date() returns None because"
                    " no history prior to %s in Item: %s ('%s')",
                    given_date.isoformat(),
                    str(self.unique_id), self.name)
                closest_hist_pt = None

        else:  # empty list
            logging.warning(
                "get_hist_pt_by_date() returns None for Item"
                " with empty History: %s ('%s')",
                str(self.unique_id), self.name)
            closest_hist_pt = None

        return closest_hist_pt

    def get_item_balance(self, currency: str, given_date: date):
        """ Get Item balance in a given currency and on a given date """

        hist_pt = self.get_hist_pt_by_date(given_date)

        if hist_pt is None:
            return 0, given_date
        else:
            exchange_rate = get_exchange_rate(given_date,
                                              from_currency=self.currency,
                                              to_currency=currency)
            closest_balance = (exchange_rate * hist_pt.units_owned
                               * hist_pt.value_of_asset)
            closest_date = hist_pt.when

        return closest_balance, closest_date

    def display(self):
        """ Display Item as text"""

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
        self.unique_id = generate_unique_id()
        self.when = when
        self.units_owned = units_owned
        self.cost_of_purchase = cost_of_purchase
        self.value_of_asset = value_of_asset
        self.item = None  # initializes HistoryPoint as orphan

    def display(self):
        """ Display HistoryPoint as text"""

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
    """ This runs if utils.py is run as script """
    pass


if __name__ == "__main__":
    # utils.py ran directly
    main()
else:
    # utils.py was imported
    pass
