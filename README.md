![](https://github.com/kernel-panic96/chess/workflows/Build/badge.svg)

This is a chess program written in Python 3.
The focus was to write it cleanly and experiment freely, not to be performant.

Currently it is *curses tui chess game* without a move engine.

## Installation

Set up a virtualenvironment of your choosing and:

```
git clone https://github.com/kernel-panic96/chess.git
cd chess
pip install -r requirements.txt
```

## Running it

```
make
```

The game uses unicode chess symbols by default
if your terminal or font does not support them and you don't want to bother.
Edit `tui-client/display_symbols.py :: square_to_str` to return `sym_table[square.type][square.color]['ascii']`

I haven't exposed them yet as a parameter to the runner.

## Developing

Same as the Installation, but in order to run the tests
you will need to pip install the `dev-requirements.txt`.

Tests are run using `make test`
