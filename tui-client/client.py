from board import Board
from constants import FigureColor, FigureType
from display_symbols import square_to_str
from position import Position

import chess_pieces as pieces

from collections import namedtuple
import curses
import operator
import functools

from select_modal import SelectModal

promotion_options = [
    ('Queen', pieces.Queen),
    ('Knight', pieces.Knight),
    ('Rook', pieces.Rook),
    ('Bishop', pieces.Bishop),
]

class TuiBoard(Board):
    _Cursor = namedtuple('CursorPosition', 'y x')

    #TODO: handle self.promotion_cb properly
    def __init__(self, screen, top_x=0, top_y=0, centered=False, *, fen: str=None):
        if fen is not None:
            self.shallow_copy(Board.from_fen(fen))
        else:
            self.shallow_copy(Board.standard_configuration())

        # ncurses screen object
        self.screen = screen
        self.centered = centered
        self.promotion_cb = functools.partial(SelectModal(promotion_options), self.screen)

        # frame_x is the begginning of the files header and footer
        self.frame_x, self.frame_y = top_x, top_y
        self.step_y, self.step_x = 1, 2

        # top left corner of the board
        self.top_x, self.top_y = self.frame_x + 2, self.frame_y + 1
        self.cursor = self._Cursor(self.top_y, self.top_x)

        self.bot_x = self.top_x + 7 * self.step_x
        self.bot_y = self.top_y + 7 * self.step_y

        if centered:
            self.center()

        self.should_redraw = True
        self._selected = None
        self._selected_legal_moves = set()
        self.highlight_upon_selection = False

    def dispatch_move(self, from_pos, to_pos):
        assert self._selected is not None

        to_pos = self._cursor_to_position(to_pos)

        assert to_pos in self._selected_legal_moves


        self.move(from_pos=from_pos, to_pos=to_pos)

        self.should_redraw = True

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self.highlight_upon_selection:
            if self.selected:
                self.remove_highlighting()

            self.highlight_position(value) and self.highlight_legal_moves()

        self._selected = self._cursor_to_position(value)

    def center(self):
        cursor_position = self._cursor_to_position()

        win_max_y, win_max_x = self.screen.getmaxyx()
        win_center_x, win_center_y = win_max_x // 2, win_max_y // 2

        self.frame_x, self.frame_y = max(0, win_center_x - 10), max(0, win_center_y - 5)

        self.step_y, self.step_x = 1, 2

        # top left corner of the board
        self.top_x, self.top_y = self.frame_x + 2, self.frame_y + 1

        self.bot_x = self.top_x + 7 * self.step_x
        self.bot_y = self.top_y + 7 * self.step_y

        new_cursor_position = self._position_to_coordinates(cursor_position)
        self.cursor = self._Cursor(*new_cursor_position)


    @property
    def is_current_select_in_legal_moves(self):
        return self._cursor_to_position(self.cursor) in self._selected_legal_moves

    def draw(self, top_x=0, top_y=0):
        if self.should_redraw:
            self.screen.clear()

            self._draw_frame()
            self._draw_board()

            if self.selected:
                self.highlight_position(self.selected) and self.highlight_legal_moves()

        self.screen.move(*self.cursor)
        self.screen.refresh()

    def highlight_position(self, position, color_pair=None):
        color_pair = color_pair or curses.color_pair(2)

        if self.is_empty(position):
            return False

        piece = self[position.rank][position.file]

        if piece.color != self.player:
            return False

        y, x = self._position_to_coordinates(position)
        self.screen.chgat(y, x, 1, color_pair)

        self._selected = position
        return True

    def highlight_legal_moves(self, color_pair=None):
        if self._selected is None:
            raise ValueError('there is no selected position')

        color_pair = color_pair or curses.color_pair(2)

        self._selected_legal_moves.clear()

        position = self.selected
        moves = self[position.rank][position.file].generate_moves(self, position)

        coordinates = list(map(self._position_to_coordinates, moves))

        y_coordinates = map(operator.itemgetter(0), coordinates)
        x_coordinates = map(operator.itemgetter(1), coordinates)

        for y, x, pos in zip(y_coordinates, x_coordinates, moves):
            if self.is_empty(pos):
                self.screen.addstr(y, x, 'x', color_pair)
            else:
                self.screen.chgat(y, x, 1, color_pair)

            self._selected_legal_moves.add(pos)

    def remove_highlighting(self):
        positions = self._selected_legal_moves.union({self._selected})

        coordinates = list(map(self._position_to_coordinates, positions))
        y_coordinates = map(operator.itemgetter(0), coordinates)
        x_coordinates = map(operator.itemgetter(1), coordinates)

        for y, x, pos in zip(y_coordinates, x_coordinates, positions):
            square = self[pos.rank][pos.file]
            self.screen.addstr(y, x, square_to_str(square), curses.color_pair(0))

        self._selected = None
        self._selected_legal_moves.clear()

    @property
    def is_piece_selected(self):
        return self._selected is not None

    def move_down(self):
        y, x = self.cursor
        self.cursor = self._Cursor(min(self.bot_y, y + self.step_y), x)

    def move_up(self):
        y, x = self.cursor
        self.cursor = self._Cursor(max(self.top_y, y - self.step_y), x)

    def move_right(self):
        y, x = self.cursor
        self.cursor = self._Cursor(y, min(self.bot_x, x + self.step_x))

    def move_left(self):
        y, x = self.cursor
        self.cursor = self._Cursor(y, max(self.top_x, x - self.step_x))

    def _draw_frame(self):
        files = 'a b c d e f g h'
        self.screen.addstr(self.frame_y, self.frame_x + 2, files)

        for i in range(8):
            self.screen.addstr(self.frame_y + i + 1, self.frame_x, str(8 - i))
            self.screen.addstr(self.frame_y + i + 1, self.frame_x + 3 + len(files), str(8 - i))

        self.screen.addstr(self.frame_y + 9, self.frame_x + 2, files)

    def _draw_board(self):
        for i, row in enumerate(self.projection):
            for j, elem in enumerate(row):
                self.screen.addstr(self.top_y + i, self.top_x + j * 2, square_to_str(elem))

    def _cursor_to_position(self, coordinates=None):
        # WARN: bool((0, 0)) == False,
        # therefore coordinates or self.cursor == self.cursor
        y, x = coordinates or self.cursor

        col, row = (x - self.top_x) // self.step_x, (y - self.top_y) // self.step_y
        rank = chr(7 - row + ord('0') + 1)
        file = chr(col + ord('a'))

        return Position.from_str(file + rank)

    def _position_to_coordinates(self, position):
        y, x = position.coordinates

        return y * self.step_y + self.top_y, x * self.step_x + self.top_x
