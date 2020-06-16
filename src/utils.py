from constants import Diagonal, Direction

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

        board[pos.rank][pos.file] = None
        attackers_positions = list(board.get_attackers(king_pos, self.color))
        board[pos.rank][pos.file] = self

        if attackers_positions:
            if len(attackers_positions) == 1:
                attack_direction = king_pos.relative_direction_towards_position(attackers_positions[0])

                if attack_direction in [Diagonal.UP_RIGHT, Diagonal.DOWN_LEFT]:
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

                elif attack_direction in [Direction.LEFT, Direction.RIGHT]:
                    target_rank = king_pos.rank
                    filtered = filter(lambda pos: pos.rank == target_rank, moves)
                    filtered = filter(lambda pos: pos.within(attackers_positions[0], king_pos), filtered)

                    return list(filtered)

            else:
                return []

        return moves

    return wrapper


def evaluate(f):
    return f()
