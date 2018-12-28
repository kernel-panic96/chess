from chess_pieces.base import ChessPieceBase
from constants import FigureType
from chess_pieces.board_traverse_mixin import BoardTraverserMixin


class Queen(BoardTraverserMixin, ChessPieceBase):
    figure_type = FigureType.QUEEN

    def generate_moves(self, board, position=None):
        return super().generate_diagonal_moves(board, position) + super().generate_straight_moves(board, position)
