from chess_pieces.base import ChessPieceBase
from chess_pieces.board_traverse_mixin import BoardTraverserMixin
from constants import FigureType, Diagonal
from position import Position

import operator
from functools import reduce


class Bishop(BoardTraverserMixin, ChessPieceBase):
    figure_type = FigureType.BISHOP

    def generate_moves(self, board, bishop_position: Position = None):
        return super().generate_diagonal_moves(board, bishop_position)
