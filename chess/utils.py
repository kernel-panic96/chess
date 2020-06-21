from chess.constants import Diagonal, Direction
from chess.pieces import King
from chess.constants import FigureType

import functools


def method_dispatch(method):
    dispatcher = functools.singledispatch(method)

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    wrapper.register = dispatcher.register
    return wrapper


def prune_moves_if_king_in_check(method):
    @functools.wraps(method)
    def wrapper(self, board, pos):
        moves = method(self, board, pos)
        king_pos = board.kings[self.color]

        if king_pos is None:
            return moves

        assert isinstance(board[king_pos.rank][king_pos.file], King), f'board[{king_pos.rank}][{king_pos.file}] is not a King'

        board[pos.rank][pos.file] = None
        attackers_positions = list(board.get_attackers(king_pos, self.color))
        board[pos.rank][pos.file] = self

        if not attackers_positions:
            return moves
        if attackers_positions and len(attackers_positions) > 1:
            return []

        attack_direction = king_pos.relative_direction_towards_position(attackers_positions[0])
        attack_pos = attackers_positions[0]

        if board[attack_pos.rank][attack_pos.file].figure_type == FigureType.KNIGHT:
            return list(filter(lambda pos: pos == attack_pos, moves))

        elif attack_direction in [Diagonal.UP_RIGHT, Diagonal.DOWN_LEFT]:
            diagonal = king_pos.rank + king_pos.file
            filtered = filter(lambda x: x.rank + x.file == diagonal, moves)
            filtered = filter(lambda x: x.within(attackers_positions[0], king_pos), filtered)

            return list(filtered)

        elif attack_direction in [Diagonal.UP_LEFT, Diagonal.DOWN_RIGHT]:
            diagonal = king_pos.rank - king_pos.file
            filtered = filter(lambda pos: pos.rank - pos.file == diagonal, moves)
            filtered = filter(lambda pos: pos.within(attackers_positions[0], king_pos), filtered)

            return list(filtered)

        elif attack_direction in [Direction.UP, Direction.DOWN]:
            target_file = king_pos.file
            filtered = filter(lambda pos: pos.file == target_file, moves)
            filtered = filter(lambda pos: pos.within(attackers_positions[0], king_pos), filtered)

            return list(filtered)

        else:
            assert attack_direction in [Direction.LEFT, Direction.RIGHT]
            target_rank = king_pos.rank
            filtered = filter(lambda pos: pos.rank == target_rank, moves)
            filtered = filter(lambda pos: pos.within(attackers_positions[0], king_pos), filtered)

            return list(filtered)

    return wrapper
