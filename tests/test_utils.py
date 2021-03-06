from copy import deepcopy

from chess.position import Position


def rotate_board(board, times=1):
    board = deepcopy(board)
    for k, v in board.kings.items():
        if v is not None:
            board.kings[k] = rotate_position(v, times)

    for _ in range(times):  # ¯\_(ツ)_/¯
        board._board = (zip(*reversed(board._board)))  # rotate 90 deg == transpose + reverse columns
        board._board = [list(elem) for elem in board._board]

    return board


def rotate_position(position: Position, times=1):
    new_pos = deepcopy(position)

    for _ in range(times):
        rank, file = new_pos.coordinates

        new_rank, new_file = 7 - rank, file
        new_rank, new_file = new_file, new_rank
        # new_rank, new_file = 7 - file, rank
        # new_rank = 7 - new_rank
        new_rank, new_file = chr(7 - new_rank + ord('1')), chr(new_file + ord('a'))
        new_pos = Position.from_str(new_file + new_rank)

    return new_pos
