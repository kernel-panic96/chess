from chess_pieces.base import ChessPiece
from constants import FigureType, Direction
from position import Position
from chess_pieces.slider_mixin import PieceSliderMixin
from utils import prune_moves_if_king_in_check


class Rook(PieceSliderMixin, ChessPiece):
    figure_type = FigureType.ROOK

    @prune_moves_if_king_in_check
    def generate_moves(self, board, rook_position: Position = None):
        return super().generate_straight_moves(board, rook_position)
