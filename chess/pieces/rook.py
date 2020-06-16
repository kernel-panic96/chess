from chess.pieces.base import ChessPiece
from chess.constants import FigureType, Direction
from chess.position import Position
from chess.pieces.slider_mixin import PieceSliderMixin
from chess.utils import prune_moves_if_king_in_check


class Rook(PieceSliderMixin, ChessPiece):
    figure_type = FigureType.ROOK

    @prune_moves_if_king_in_check
    def generate_moves(self, board, rook_position: Position = None):
        return super().generate_straight_moves(board, rook_position)
