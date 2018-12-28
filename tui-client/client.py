from board import Board
from constants import FigureColor
from display_symbols import square_to_str
from position import Position

from collections import namedtuple
import curses
import operator


class TuiBoard:
    _Cursor = namedtuple('CursorPosition', 'y x')

    def __init__(self, screen, top_x=0, top_y=0):
        self.board = Board.standard_configuration()
        # ncurses screen object
        self.screen = screen

        # who's turn it is
        self.player, self.enemy = FigureColor.WHITE, FigureColor.BLACK

        # frame_x is the begginning of the files header and footer
        self.frame_x, self.frame_y = top_x, top_y
        self.step_y, self.step_x = 1, 2

        # top left corner of the board
        self.top_x, self.top_y = self.frame_x + 2, self.frame_y + 1
        self.cursor = self._Cursor(self.top_y, self.top_x)

        self.bot_x = self.top_x + 7 * self.step_x
        self.bot_y = self.top_y + 7 * self.step_y

        self.should_redraw = True
        self._selected = None
        self._selected_legal_moves = set()
        self.highlight_upon_selection = False

    def dispatch_move(self, from_pos, to_pos):
        assert self._selected is not None
        assert to_pos in self._selected_legal_moves

        from_pos = self._cursor_to_position(from_pos)
        to_pos = self._cursor_to_position(to_pos)

        self.board.move(from_pos=from_pos, to_pos=to_pos)

        self.should_redraw = True

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self.highlight_upon_selection:
            if self.selected:
                self.remove_highlighting()

            self.highlight_position(*value) and self.highlight_legal_moves()

        self._selected = value

    @property
    def is_current_select_in_legal_moves(self):
        return self.cursor in self._selected_legal_moves

    def draw(self):
        if self.should_redraw:
            self.screen.clear()
            self._draw_frame()
            self._draw_board()

            if self.selected:
                self.highlight_position(*self.selected) and self.highlight_legal_moves()

        self.screen.move(*self.cursor)
        self.screen.refresh()

    def highlight_position(self, y, x, color_pair=None):
        color_pair = color_pair or curses.color_pair(2)

        position = self._cursor_to_position((y, x))

        if self.board.is_empty(position):
            return False

        piece = self.board[position.rank][position.file]

        if piece.color != self.player:
            return False

        self.screen.chgat(y, x, 1, color_pair)

        self._selected = (y, x)
        return True

    def highlight_legal_moves(self, color_pair=None):
        if self._selected is None:
            raise ValueError('there is no selected position')

        color_pair = color_pair or curses.color_pair(2)

        self._selected_legal_moves.clear()

        position = self._cursor_to_position(self.selected)
        moves = self.board[position.rank][position.file].generate_moves(self.board, position)

        coordinates = list(map(self._position_to_coordinates, moves))

        y_coordinates = map(operator.itemgetter(0), coordinates)
        x_coordinates = map(operator.itemgetter(1), coordinates)

        for y, x, pos in zip(y_coordinates, x_coordinates, moves):
            if self.board.is_empty(pos):
                self.screen.addstr(y, x, 'x', color_pair)
            else:
                self.screen.chgat(y, x, 1, color_pair)

            self._selected_legal_moves.add((y, x))

    def remove_highlighting(self):
        coordinates = self._selected_legal_moves.union({self._selected})

        positions = map(self._cursor_to_position, coordinates)
        y_coordinates = map(operator.itemgetter(0), coordinates)
        x_coordinates = map(operator.itemgetter(1), coordinates)

        for y, x, pos in zip(y_coordinates, x_coordinates, positions):
            square = self.board[pos.rank][pos.file]
            self.screen.addstr(y, x, square_to_str(square), curses.color_pair(0))

        self._selected = None
        self._selected_legal_moves.clear()

    @property
    def is_piece_selected(self):
        return self._selected is not None

    def next_turn(self):
        self.player, self.enemy = self.enemy, self.player

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
            self.screen.addstr(self.frame_y + i + 1, self.frame_x + 4 + len(files), str(8 - i))

        self.screen.addstr(self.frame_y + 9, self.frame_x + 2, files)

    def _draw_board(self):
        for i, row in enumerate(self.board.projection):
            for j, elem in enumerate(row):
                self.screen.addstr(self.top_y + i, self.top_x + j * 2, square_to_str(elem))

    def _cursor_to_position(self, coordinates=None):
        # WARN: bool((0, 0)) == False,
        # therefore coordinates or self.cursor == self.cursor
        y, x = coordinates or self.cursor

        col, row = (x // self.step_x) - self.top_x, (y // self.step_y) - self.top_y
        rank = chr(row + ord('0'))
        file = chr(col + ord('a') + 1)

        return Position.from_str(file + rank)

    def _position_to_coordinates(self, position):
        y, x = position.to_coordinates

        return y * self.step_y + self.top_y, x * self.step_x + self.top_x
