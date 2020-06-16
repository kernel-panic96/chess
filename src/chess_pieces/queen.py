from chess_pieces.base         import ChessPiece
from chess_pieces.slider_mixin import PieceSliderMixin
from constants                 import FigureType
from position                  import Position
from utils                     import prune_moves_if_king_in_check


class Queen(PieceSliderMixin, ChessPiece):
    figure_type = FigureType.QUEEN

    @prune_moves_if_king_in_check
    def generate_moves(self, board, position: Position):
        return super().generate_diagonal_moves(board, position) + super().generate_straight_moves(board, position)
