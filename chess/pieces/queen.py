from chess.pieces.base         import ChessPiece
from chess.pieces.slider_mixin import PieceSliderMixin
from chess.constants           import FigureType
from chess.position            import Position
from chess.utils               import prune_moves_if_king_in_check


class Queen(PieceSliderMixin, ChessPiece):
    figure_type = FigureType.QUEEN

    @prune_moves_if_king_in_check
    def generate_moves(self, board, position: Position):
        return super().generate_diagonal_moves(board, position) + super().generate_straight_moves(board, position)
