#!/bin/env python3

from curses import wrapper
import logging
import os
import sys
import curses

from client import TuiBoard
from controls import controls

os.environ.setdefault('ESCDELAY', '10')


def setup_color():
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
        curses.init_pair(i+1, i, -1)


def main(screen, *argv):
    screen.clear()
    setup_color()

    board = TuiBoard(screen)
    board.highlight_upon_selection = False

    user_input = None
    while True:
        if user_input in controls['move_left']:
            board.move_left()

        elif user_input in controls['move_right']:
            board.move_right()

        elif user_input in controls['move_up']:
            board.move_up()

        elif user_input in controls['move_down']:
            board.move_down()

        elif user_input in controls['select']:
            if board.is_piece_selected and board.is_current_select_in_legal_moves:
                board.dispatch_move(board.selected, board.cursor)
                board.remove_highlighting()
                board.next_turn()
            else:
                board.selected = board.cursor

        elif user_input in controls['cancel']:
            if board.is_piece_selected:
                board.remove_highlighting()

        elif user_input in controls['quit']:
            return os.EX_OK

        board.draw()
        user_input = screen.getch()
        logging.debug(chr(user_input))



if __name__ == '__main__':
    logging.basicConfig()
    sys.exit(wrapper(main, *sys.argv))
