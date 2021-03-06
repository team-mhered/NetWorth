#!/usr/bin/env python3

# run_tests.py

import unittest

# import your test modules
import tests.test_utils as test_utils
import tests.test_exchange as test_exchange
import tests.test_ui as test_ui
# import tests.test_others as test_others


# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# run test methods in the order they are defined (it does not work, why?)
loader.sortTestMethodsUsing = None

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_utils))
suite.addTests(loader.loadTestsFromModule(test_exchange))

# UI testing fails when called from the suite (conflict with prompt?).
# Call manually instead using python3 -m tests.test_ui
# suite.addTests(loader.loadTestsFromModule(test_ui))

# suite.addTests(loader.loadTestsFromModule(test_others))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
