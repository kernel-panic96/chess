from position import Position
from constants import Diagonal, Direction
import functools


class PieceSliderMixin:
    '''Sliders are bishops, rooks and queens.
    Provides two methods, _generate_diagonal_moves and _generate_straight_moves.
    Both methods are bounds aware and will stop at the first non-empty square,
    and will return it, based on whether or not it is an enemy piece or not, respectively
    '''

    def _generate_moves_in_direction(self, board, piece_position: Position, *, directions):
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

    def is_legal_move_straight(self, to_pos, from_pos: Position = None):
        from_pos = from_pos or Position(self.rank, self.file)

        return from_pos.rank == to_pos.rank or from_pos.file == to_pos.file

    def is_legal_move_diagonal(self, to_pos, from_pos: Position = None):
        from_pos = from_pos or Position(self.rank, self.file)

        return (
            from_pos.rank + from_pos.file == to_pos.rank + to_pos.file or
            from_pos.rank - from_pos.file == to_pos.rank - to_pos.file
        )
