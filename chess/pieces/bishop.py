import operator
from functools import reduce

from chess.pieces.base import ChessPiece
from chess.pieces.slider_mixin import PieceSliderMixin
from chess.constants import FigureType, Diagonal
from chess.position import Position
from chess.utils import prune_moves_if_king_in_check


class Bishop(PieceSliderMixin, ChessPiece):
    figure_type = FigureType.BISHOP

    @prune_moves_if_king_in_check
    def generate_moves(self, board, bishop_position: Position):
        return super().generate_diagonal_moves(board, bishop_position)
