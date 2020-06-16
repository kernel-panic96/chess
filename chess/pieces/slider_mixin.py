import functools

from chess.position import Position
from chess.constants import Diagonal, Direction


class PieceSliderMixin:
    '''Sliders are bishops, rooks and queens.
    Provides two methods, generate_diagonal_moves and generate_straight_moves.
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
