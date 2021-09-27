#!/usr/bin/env python3

# tests/test_ui.py

""" Tests for UI functions """

from src.ui import ui_menu
import unittest
import logging


class TestUI(unittest.TestCase):
    """ Class to test user interface methods """

    def setUp(self):
        """ Create a fixture of a basic portfolio with some items """

        # setup logging service
        # ::ENHANCEMENT:: move this config info to an .env or a .cfg file
        config_file = './tests/test_ui.log'
        log_level = logging.INFO
        logging.basicConfig(filename=config_file, filemode='w',
                            format='%(asctime)s::%(levelname)s::%(message)s',
                            datefmt='%Y.%m.%d %I:%M:%S%p', level=log_level)

        logging.info('\n--------CREATING FIXTURE--------\n')

        from src.readwrite import read_portfolio_from_file
        my_portfolio = read_portfolio_from_file('./tests/fixtures.json')
        logging.info('\n--------FIXTURE CREATED---------\n')

        self.my_portfolio = my_portfolio

    def test_ui_menu(self):
        """ Interactive text user interface's main menu """

        ui_menu(self.my_portfolio)


if __name__ == '__main__':
    unittest.main()
