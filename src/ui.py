#!/usr/bin/env python3

""" Basic text-based UI methods """

from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from datetime import datetime, date
import logging

from src.utils import plot_piechart, Portfolio
from src.readwrite import read_portfolio_from_file, save_portfolio_to_file

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
    """ Returns a text list of items in Portfolio"""

    items = []
    for i, item in enumerate(portfolio.item_list):
        items.append(str(i) + ". " + item.name + " (" + item.subcategory + ")")
    return items


def save_open_portfolio(open_portfolio):
    saved = False
    if open_portfolio is not None:
        questions = [
            {
                'type': 'confirm',
                'name': 'confirmed',
                'message':
                    'The open Portfolio will be lost. Do you want to save it?',
                'default': True
            },
        ]

        user_selection = prompt(questions, style=style)
        if user_selection['confirmed']:
            print('Saving...')
            save_portfolio_to_file(open_portfolio)
            saved = True

    return saved


def ui_open_portfolio(target):
    """ Menu option - open Portfolio"""

    save_open_portfolio(target)

    print('Opening Portfolio...')
    portfolio = read_portfolio_from_file()

    return portfolio


def ui_quit(target):
    """ Menu option - quit"""

    save_open_portfolio(target)

    print('Bye!')

    return False


def ui_purchase(target):
    """ Menu option - make a purchase on an Item"""
    questions = [
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
            'message': f'Unit price ({target.currency})?',
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

    user_input = prompt(questions, style=style)
    target.purchase(
        when=user_input['date'],
        units_purchased=user_input['units_purchased'],
        unit_price=user_input['unit_price'],
        fees=user_input['fees']
    )

    return True


def ui_new_portfolio(target):
    """ Menu option - create new Portfolio"""

    save_open_portfolio(target)

    print('Creating New Portfolio...')

    questions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Give your Portfolio a short name (at least 3 letters)',
            'validate': lambda val: len(val) > 2
        },
        {
            'type': 'list',
            'name': 'currency',
            'message': 'Default Currency?',
            'choices': Portfolio.CURRENCIES+Portfolio.CRYPTO,
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Short description of the Portfolio',
            'default': lambda answers: (answers['name'] + ' (' +
                                        answers['currency'] + ')')
        },
    ]

    user_selection = prompt(questions, style=style)

    portfolio = Portfolio(
        name=user_selection['name'],
        description=user_selection['description'],
        currency=user_selection['currency'])

    return portfolio


def ui_show_portfolio(target):
    """ Menu option - display Portfolio"""

    print('Showing Portfolio...')
    print(target.display())
    return True


def ui_analyze_portfolio(target):
    """ Menu option - plot piechart of Portfolio"""

    print('Analyzing Portfolio...')
    piechart = target.get_portfolio_piechart(date.today())
    plot_piechart(piechart)
    return True


def ui_edit_portfolio(target):
    """ Menu option - edit Portfolio"""

    print('Editing Portfolio...')
    print(target.display())
    questions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Edit name (at least 3 letters)?',
            'default': target.name,
            'validate': lambda val: len(val) > 2
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Edit description?',
            'default': target.description
        },
        {
            'type': 'list',
            'name': 'currency',
            'message': 'Change default currency?',
            'choices': Portfolio.CURRENCIES+Portfolio.CRYPTO,
            'default': target.currency
        },

        {
            'type': 'confirm',
            'name': 'confirmed',
            'message': 'Accept changes?',
            'default': False
        },

    ]

    user_selection = prompt(questions, style=style)
    if user_selection['confirmed']:
        target.name = user_selection['name']
        target.description = user_selection['description']

    return True


def ui_new_item(target):
    """ Menu option - create new Item"""
    print('Creating New Item...')

    questions = [
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
            'validate': lambda val: len(val) > 2
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
                    category='asset',
                    subcategory=user_selection['subcategory'],
                    currency=user_selection['currency'],
                    )
    return True


def ui_edit_item(target):
    """ Menu option - edit Item"""

    print('Editing Item...')
    print(target.display())
    questions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Edit name? (at least 3 letters)',
            'default': target.name,
            'validate': lambda val: len(val) > 2
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Edit description?',
            'default': target.description
        },
        {
            'type': 'confirm',
            'name': 'confirmed',
            'message': 'Accept changes?',
            'default': False
        },

    ]

    user_selection = prompt(questions, style=style)
    if user_selection['confirmed']:
        target.name = user_selection['name']
        target.description = user_selection['description']

    return True


def ui_delete_item(target):
    """ Menu option - delete Item"""

    print('Deleting Item...')
    target.portfolio.remove_item(target)

    return True


def ui_show_item(target):
    """ Menu option - display Item"""

    print(target.display())
    return True


def ui_menu(current_portfolio):
    """ Interactive text user interface - Main menu"""

    menu = [
        (ui_new_portfolio, 'Create New Portfolio', None),
        (ui_open_portfolio, 'Open Portfolio', None),
        (ui_analyze_portfolio, 'Analyze Portfolio', 'portfolio'),
        (ui_show_portfolio, 'Show Portfolio', 'portfolio'),
        (ui_edit_portfolio, 'Edit Portfolio', 'portfolio'),
        (ui_new_item, 'New Item', 'portfolio'),
        (ui_edit_item, 'Edit Item', 'item'),
        (ui_purchase, 'Purchase', 'item'),
        (ui_delete_item, 'Delete Item', 'item'),
        (ui_show_item, 'Show Item', 'item'),
        (ui_quit, 'Quit', None),
    ]
    actions, user_options, required_targets = zip(*menu)

    user_options = list(user_options)

    # options that require an item as target
    item_as_target = []
    portfolio_as_target = []
    for i, required in enumerate(required_targets):
        if required == 'item':
            item_as_target.append(user_options[i])
        if required == 'portfolio':
            portfolio_as_target.append(user_options[i])
    keep_going = True

    while keep_going:

        if current_portfolio is None:
            show_user_options = []
            # disable options that require an open portfolio
            for user_option in user_options:
                if user_option in portfolio_as_target + item_as_target:
                    show_user_options.append(
                        {'name': user_option,
                         'disabled': 'no portfolio selected'})
                else:
                    show_user_options.append(user_option)
            items = ['0.None']
        else:
            # retrieve formatted list of items in current portfolio
            show_user_options = user_options
            items = get_item_list_in_text(current_portfolio)

        questions = [
            {
                'type': 'list',
                'name': 'Action',
                'message': 'What would you like to do?',
                'choices': show_user_options,
            },
            {
                'type': 'list',
                'name': 'Item',
                'message': 'Which Item?',
                'choices': items,
                'filter': lambda val: int(val[0:val.find('.')]),
                'when': lambda answers: answers['Action'] in item_as_target
            },
        ]

        user_selection = prompt(questions, style=style)

        # retrieve action_call
        action_call = [
            item[0] for item in menu if item[1] == user_selection['Action']]

        if user_selection['Action'] in portfolio_as_target:
            # operate on current portfolio
            target = current_portfolio
            keep_going = action_call[0](target)
            target_name = target.name
        elif user_selection['Action'] in item_as_target:
            # operate on item in current portfolio
            i = user_selection['Item']
            target = current_portfolio.item_list[i]
            keep_going = action_call[0](target)
            target_name = target.name
        else:
            # retrieve portfolio
            target = current_portfolio
            current_portfolio = action_call[0](target)
            if not bool(current_portfolio):
                break
            target_name = None
