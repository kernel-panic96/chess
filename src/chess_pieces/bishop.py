from chess_pieces.base import ChessPiece
from chess_pieces.slider_mixin import PieceSliderMixin
from constants import FigureType, Diagonal
from position import Position
from utils import prune_moves_if_king_in_check

import operator
from functools import reduce


class Bishop(PieceSliderMixin, ChessPiece):
    figure_type = FigureType.BISHOP

    @prune_moves_if_king_in_check
    def generate_moves(self, board, bishop_position: Position):
        return super().generate_diagonal_moves(board, bishop_position)
