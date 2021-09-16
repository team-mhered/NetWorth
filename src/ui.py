#!/usr/bin/env python3

""" Basic text-based UI methods """

from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from datetime import datetime, date
import logging
from pprint import pprint

from src.utils import plot_piechart, Portfolio
from src.readwrite import dict_from_portfolio

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


class IntValidator(Validator):
    """ Validator for int """

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid number of titles',
                cursor_position=len(document.text))  # Move cursor to end


class FloatValidator(Validator):
    """ Validator for float """

    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid amount',
                cursor_position=len(document.text))  # Move cursor to end


class DateValidator(Validator):
    """ Validator for date """

    def validate(self, document):
        date_string = document.text
        date_format = '%Y-%m-%d'
        try:
            datetime.strptime(date_string, date_format)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid YYYY-MM-DD date',
                cursor_position=len(document.text))  # Move cursor to end


def get_item_list_in_text(portfolio):
    items = []
    for i, item in enumerate(portfolio.item_list):
        items.append(str(i) + ". " + item.name + " (" + item.subcategory + ")")
    return items


def UI_purchase(portfolio):
    """ Interactive text user interface to make a purchase on an Item"""
    items = get_item_list_in_text(portfolio)
    questions = [
        {
            'type': 'list',
            'name': 'Item',
            'message': 'Which item?',
            'choices': items,
            'filter': lambda val: int(val[0:val.find('.')]),
        },
        {
            'type': 'input',
            'name': 'date',
            'message': 'Date of the transaction',
            'default': date.today().isoformat(),
            'validate': DateValidator,
            'filter': lambda val: datetime.strptime(val, '%Y-%m-%d').date(),
        },
        {
            'type': 'input',
            'name': 'units_purchased',
            'message': 'How many titles?',
            'validate': IntValidator,
            'filter': lambda val: int(val),
        },
        {
            'type': 'input',
            'name': 'unit_price',
            'message': f'Unit price ({portfolio.currency})?',
            'validate': FloatValidator,
            'filter': lambda val: float(val),
        },
        {
            'type': 'input',
            'name': 'fees',
            'message': 'Fees paid?',
            'validate': FloatValidator,
            'filter': lambda val: float(val),
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Description of the transaction',
            'default': lambda answers: ("Purchase of " +
                                        str(answers['units_purchased']) +
                                        " units on " +
                                        answers['date'].isoformat()),
        },
    ]

    answers = prompt(questions, style=style)
    # replace answers['Item']
    index_of_Item_selected = answers['Item']
    answers['Item'] = portfolio.item_list[index_of_Item_selected]

    return answers


def new_portfolio(target):
    print('Creating New Portfolio')
    return True


def open_portfolio(target):
    print('Opening Portfolio')
    return True


def show_portfolio(target):
    print('Showing Portfolio')
    print(target.display())
    pprint(dict_from_portfolio(target))
    return True


def analyze_portfolio(target):
    """ Plots piechart of portfolio """
    print('Analyzing Portfolio')
    piechart = target.get_portfolio_piechart(date.today())
    plot_piechart(piechart)
    return True


def edit_portfolio(analyzetarget):
    print('Editing Portfolio')
    return True


def delete_portfolio(target):
    print('Deleting Portfolio')
    return True


def new_item(target):
    print('Creating New Item')

    questions = [
        {
            'type': 'list',
            'name': 'category',
            'message': 'Which item?',
            'choices': Portfolio.CATEGORIES,
        },
        {
            'type': 'list',
            'name': 'subcategory',
            'message': 'Which item?',
            'choices': Portfolio.SUBCATEGORIES,
        },
        {
            'type': 'list',
            'name': 'currency',
            'message': 'Default Currency?',
            'choices': Portfolio.CURRENCIES+Portfolio.CRYPTO,
        },
        {
            'type': 'input',
            'name': 'name',
            'message': 'Give your Item a short name (at least 3 letters)',
            'validate': lambda val: len(val) > 3
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Short description of the Item',
            'default': lambda answers: (answers['name']+' '
                                        + answers['subcategory'] + ' ('
                                        + answers['currency'] + ')')
        },
    ]

    user_selection = prompt(questions, style=style)

    target.add_item(name=user_selection['name'],
                    description=user_selection['description'],
                    category=user_selection['category'],
                    subcategory=user_selection['subcategory'],
                    currency=user_selection['currency'],
                    )
    return True


def edit_item(target):
    print('Editing Item')
    return True


def delete_item(target):
    print('Deleting Item')
    return True


def show_item(target):
    print(target.display())
    return True


def analyze_item(target):
    print('Analyzing Item')
    return True


def quit_app(target):
    print('Quitting')
    return False


def UI_menu(portfolio):
    """ Interactive text user interface - Main menu"""

    menu = [
        (new_portfolio, '_Create New Portfolio'),
        (open_portfolio, '_Open Portfolio'),
        (show_portfolio, 'Show Portfolio'),
        (analyze_portfolio, 'Analyze Portfolio'),
        (edit_portfolio, 'Edit Portfolio'),
        (delete_portfolio, '_Delete Portfolio'),
        (new_item, 'New Item'),
        (edit_item, '_Edit Item'),
        (delete_item, '_Delete Item'),
        (show_item, 'Show Item'),
        (analyze_item, '_Analyze Item'),
        (quit_app, 'Quit'),
    ]

    actions, user_options = zip(*menu)

    user_options = list(user_options)

    for i, option in enumerate(user_options):
        if option[0] == '_':
            user_options[i] = {'name': option[1:], 'disabled': 'WIP'}

    keep_going = True

    while keep_going:

        items = get_item_list_in_text(portfolio)

        questions = [
            {
                'type': 'list',
                'name': 'Action',
                'message': 'What would you like to do?',
                'choices': user_options,
            },
            {
                'type': 'list',
                'name': 'Item',
                'message': 'Which Item?',
                'choices': items,
                'filter': lambda val: int(val[0:val.find('.')]),
                'when': lambda answers: answers['Action'] in ['Edit Item',
                                                              'Delete Item',
                                                              'Show Item',
                                                              'Analyze Item',
                                                              ]
            },
        ]

        user_selection = prompt(questions, style=style)

        if 'Item' in user_selection:
            i = user_selection['Item']
            target = portfolio.item_list[i]
        else:
            target = portfolio

        execute_action = [item[0] for item in menu if item[1] == user_selection['Action']]

        logging.debug(f"{user_selection['Action']}:  target is "
                      f"{type(target)} {target.name}")
        logging.debug(f"Calling {execute_action}.")

        keep_going = execute_action[0](target)
