from chess_pieces.base import ChessPieceBase
from constants import FigureType
from position import Position


class Knight(ChessPieceBase):
    figure_type = FigureType.KNIGHT

    def possible_positions(self, position):
        one_up, two_up = Direction.UP, Direction.UP * 2
        one_right, two_right = Direction.RIGHT, Direction.RIGHT * 2
        one_left, two_left = Direction.LEFT, Direction.LEFT * 2
        one_down, two_down = Direction.DOWN, Direction.DOWN * 2

        rank, file = position.rank, position.file

        return [
            Position(rank + two_up, file + one_right),
            Position(rank + one_up, file + two_right),
            Position(rank + one_down, file + two_right),
            Position(rank + two_down, file + one_right),
            Position(rank + two_down, file + one_left),
            Position(rank + two_down, file + two_left),
            Position(rank + one_up, file + two_left),
            Position(rank + two_up, file + one_left),
        ]

    def generate_moves(self, board, knight_position: Position = None):
        if knight_position is None:
            knight_position = Position(self.rank, self.file)

        possible_positions = self.get_possible_positions(knight_position)

        moves = []
        for position in possible_positions:
            if (
                board.is_in_bounds(position) and
                (board.is_empty(position) or board.are_enemies(knight_position, position))
            ):
                moves.append(position)

        return moves
