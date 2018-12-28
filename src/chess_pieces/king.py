from chess_pieces.base import ChessPieceBase
from position import Position
from constants import FigureType
import itertools


class King(ChessPieceBase):
    figure_type = FigureType.KING

    def generate_moves(self, board, king_pos: Position = None):
        if king_pos is None:
            king_pos = Position(self.rank, self.file)

        return [
            pos for pos in self.possible_positions
            if (
                board.is_in_bounds(pos) and
                (board.is_empty(pos) or
                board.are_enemies(king_pos, pos))
            )
        ]

    @property
    def possible_positions(self):
        rank, file = self.rank, self.file

        surrounding_positions = [
            Position(rank + delta_rank, file + delta_file)
            for delta_rank, delta_file in itertools.product([1, 0, -1], repeat=2)
            if (delta_rank, delta_file) != (0, 0)
        ]

        return surrounding_positions

    def is_in_check(self):
        pass
