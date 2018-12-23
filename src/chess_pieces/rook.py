from chess_pieces.base import ChessPieceBase
from constants import FigureType, Direction
from position import Position
from chess_pieces.board_traverse_mixin import BoardTraverserMixin


class Rook(BoardTraverserMixin, ChessPieceBase):
    figure_type = FigureType.ROOK

    def generate_moves(self, board, rook_position: Position = None):
        return super().generate_straight_moves(board, rook_position)
