#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from datetime import datetime, date
from utils import Portfolio

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


class IntValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid number of titles',
                cursor_position=len(document.text))  # Move cursor to end


class FloatValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid amount',
                cursor_position=len(document.text))  # Move cursor to end


class DateValidator(Validator):
    def validate(self, document):
        date_string = document.text
        date_format = '%Y-%m-%d'
        try:
            datetime.strptime(date_string, date_format)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid YYYY-MM-DD date',
                cursor_position=len(document.text))  # Move cursor to end


def input_purchase(self):
    items = []
    for i, item in enumerate(self.item_list):
        items.append(str(i) + ". " + item.name + " (" + item.subcategory + ")")

    items.append(str(len(items))+". New Item")
    # print(items)

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
            'message': f'Unit price ({self.currency})?',
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
    answers['Item'] = self.item_list[answers['Item']]

    print(answers['Item'].name)
    return answers


portfolio_samples = [
    {
        'name': 'My First Portfolio',
        'description': 'Test Portfolio',
        'currency': 'EUR'
    }
]

# this allows creating more than one portfolio (maybe for future tests)
for i, portfolio_sample in enumerate(portfolio_samples):
    portfolio_name = 'portfolio'+str(i).zfill(2)
    portfolio_object = Portfolio(
        name=portfolio_sample['name'],
        currency=portfolio_sample['currency'],
        description=portfolio_sample['description'])

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
        'currency': 'EUR',
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
        'subcategory': 'real_state',
        'currency': 'EUR',
        'name': 'Kcity',
        'description': 'Apartamento en Kansas City'
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
    """
    logging.info("Adding Item '%s' to Portfolio '%s'...\n%s",
                 item_name, my_portfolio.name, sample)
                 """
    item_object = my_portfolio.add_item(
        category=sample['category'],
        subcategory=sample['subcategory'],
        currency=sample['currency'],
        name=sample['name'],
        description=sample['description'])

for item in my_portfolio.item_list:
    if item.name == "Fondo NARANJA 50/40":
        item.purchase(
            when=date(2021, 2, 1),
            units_purchased=1,
            unit_price=50000.0,
            fees=0.0
        )
        item.purchase(
            when=date(2021, 3, 1),
            units_purchased=1,
            unit_price=30000.0,
            fees=0.0
        )
        item.purchase(
            when=date(2021, 4, 1),
            units_purchased=1,
            unit_price=20000.0,
            fees=0.0
        )

    if item.name == "Amazon":
        item.purchase(
            when=date(2021, 5, 12),
            units_purchased=10,
            unit_price=5000.0,
            fees=0.0
        )

user_input = input_purchase(my_portfolio)
print('Summary of purchase:')
pprint(user_input)

user_input['Item'].purchase(
    when=user_input['date'],
    units_purchased=user_input['units_purchased'],
    unit_price=user_input['unit_price'],
    fees=user_input['fees'],
)

print(my_portfolio.display())
