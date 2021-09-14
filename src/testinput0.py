#!/usr/bin/env python3

import readline


def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
        readline.set_startup_hook()


msg = "your name here"
while msg != "q":
    msg = rlinput("Edit line: ", msg)
    print("edited msg:", msg)
