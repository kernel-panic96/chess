from chess_pieces.base import ChessPiece
from constants import FigureType, Direction
from position import Position

from utils import prune_moves_if_king_in_check


class Knight(ChessPiece):
    figure_type = FigureType.KNIGHT

    _one_up, _two_up = Direction.UP, Direction.UP * 2
    _one_right, _two_right = Direction.RIGHT, Direction.RIGHT * 2
    _one_left, _two_left = Direction.LEFT, Direction.LEFT * 2
    _one_down, _two_down = Direction.DOWN, Direction.DOWN * 2

    @classmethod
    def possible_positions(cls, position):
        rank, file = position.rank, position.file

        return [
            Position(rank + cls._two_up, file + cls._one_right),
            Position(rank + cls._one_up, file + cls._two_right),
            Position(rank + cls._one_down, file + cls._two_right),
            Position(rank + cls._two_down, file + cls._one_right),
            Position(rank + cls._two_down, file + cls._one_left),
            Position(rank + cls._one_down, file + cls._two_left),
            Position(rank + cls._one_up, file + cls._two_left),
            Position(rank + cls._two_up, file + cls._one_left),
        ]

    @prune_moves_if_king_in_check
    def generate_moves(self, board, knight_position: Position = None):
        knight_position = knight_position or Position(self.rank, self.file)

        possible_positions = self.possible_positions(knight_position)

        moves = []
        for position in possible_positions:
            if (
                board.is_in_bounds(position) and
                (board.is_empty(position) or board.are_enemies(knight_position, position))
            ):
                moves.append(position)

        return moves
