from position import Position
from constants import Diagonal, Direction
import functools


class BoardTraverserMixin:
    def _generate_moves_in_direction(self, board, piece_position: Position = None, *, directions):
        if piece_position is None:
            piece_position = Position(self.rank, self.file)

        directions = board.get_positions_in_direction(piece_position, *directions)
        moves = []

        for direction, positions in directions.items():
            for position in positions:
                if not board.is_empty(position):
                    if board.are_enemies(piece_position, position):
                        moves.append(position)
                    break

                moves.append(position)

        return moves

    generate_diagonal_moves = functools.partialmethod(_generate_moves_in_direction, directions=list(Diagonal))
    generate_straight_moves = functools.partialmethod(_generate_moves_in_direction, directions=list(Direction))
