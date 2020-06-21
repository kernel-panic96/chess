import unittest
from copy import deepcopy

from chess.constants import Rank, File
from chess.constants import FigureColor as Color, FigureType as Type
from chess.position import Position
from tests.test_utils import rotate_board, rotate_position
from chess.pieces import (
    King, Queen, Rook, Bishop, Knight, Pawn
)

from functional import seq


figure_name_to_class = {
    'king': King,
    'queen': Queen,
    'rook': Rook,
    'bishop': Bishop,
    'knight': Knight,
    'pawn': Pawn,
}

color_to_class = {
    'white': Color.WHITE,
    'black': Color.BLACK,
}


class MoveGenerationTestCase(unittest.TestCase):
    recognized_iterables = (type(seq(0)), list, tuple, set, dict)

    def runMoveGenerationTest(self, test_case):
        # TODO: the code is a bit dense, maybe refactor, it supports a lot of
        # use cases, decide on one

        board = test_case['board']
        test_data = test_case['want']

        for color in test_data.keys():
            same_for = test_case.get('expect_same_behaviour_for')
            assert_fn = test_data[color].pop('assert', None)

            for pos, want in test_data[color].items():
                pieces_under_test = [board[pos.rank][pos.file]]
                if same_for:
                    pieces = map(str.lower, same_for)
                    pieces = map(figure_name_to_class.__getitem__, same_for)
                    figure_color = color_to_class[color.lower()]
                    pieces_under_test.extend(map(lambda piece: piece(figure_color), pieces))

                for test_piece in pieces_under_test:
                    test_name = [test_case['name'], color, test_piece.type.name.lower()]
                    with self.subTest('/'.join(test_name)):
                        try:
                            test_board = deepcopy(board)
                            test_board[pos.rank][pos.file] = test_piece

                            piece = test_board[pos.rank][pos.file]
                            if not hasattr(piece, 'generate_moves'):
                                raise ValueError('attribute missing "generate_moves"')

                            actual = set(piece.generate_moves(board, pos))
                            if isinstance(want, self.recognized_iterables):
                                want = set(map(_transform_relative_offset_to_position(pos), want))
                            else:
                                want = _transform_relative_offset_to_position(pos)(want)

                            assert_fn = assert_fn or self.assertSetEqual
                            assert_fn(want, actual)
                        except AssertionError as e:
                            raise AssertionError(f'testing {board[pos.rank][pos.file]} @ {pos}') from e
                        except Exception as e:
                            raise e.__class__(f'During test "{color} {test_case["name"]}"') from e

    def all_board_rotations_of(self, test_case):
        '''Returns all rotations of a test case.

        Example, given:
        {
            'name': 'test_case_name',
            'board': Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                'B.......'   # 1
            ]),
            'want': {
                'white': {
                    Position(Rank.ONE, File.A): {
                        (+1, +1),
                        (+2, +2),
                        ...
                        (+7, +7)
                    }
                },
            }
        }
        as a test case, the function will return a list with replicas of the test case with the bishop placed at
        a8, h8, h1 and a1 again. and it's target positions will be rotated accordingly.
        '''
        board = test_case['board']
        name = test_case['name']
        want = test_case['want']

        test_names = seq.range(90, 360, 90).map(lambda deg: f'rotated{deg}_clockwise')

        rotations = []
        for multiple_of_90, rot_name in enumerate(test_names, start=1):
            rotated_want = {}
            for color, positions in want.items():
                rotated_want[color] = {}

                if 'assert' in positions:
                    rotated_want[color]['assert'] = positions['assert']

                for target_pos, want_positions in positions.items():
                    if target_pos == 'assert':
                        continue

                    if isinstance(want_positions, self.recognized_iterables):
                        want_positions = seq(want_positions)\
                            .map(_transform_relative_offset_to_position(target_pos))

                        rotated_positions = seq(want_positions)\
                            .map(lambda p: rotate_position(p, multiple_of_90))\
                            .list()
                    else:
                        rotated_positions = rotate_position(want_positions, multiple_of_90)

                    rotated_target = rotate_position(target_pos, multiple_of_90)
                    rotated_want[color][rotated_target] = rotated_positions

            rotations.append({
                'name':  '_'.join([name, rot_name]),
                'board': rotate_board(board, multiple_of_90),
                'want':  rotated_want
            })

        return [test_case] + rotations


def _transform_relative_offset_to_position(base):
    def transform_according_to_base(pos):
        if isinstance(pos, Position):
            return pos
        return base + pos

    return transform_according_to_base


def target_board(positions):
    """
    >>> positions = target_board([
    ...     # bcdefgh
    ...     '........',  # 8
    ...     '........',  # 7
    ...     '........',  # 6
    ...     'X...X...',  # 5
    ...     '.x.x....',  # 4
    ...     '..T.....',  # 3
    ...     '.x.x....',  # 2
    ...     'X...X...'   # 1
    ... ]); ('C3' in str(positions.keys()), all(p in str(positions.values()) for p in {"A1", "D2", "B2", "A5", "E1", "B4", "D4", "E5"}))
    (True, True)

    The example above is so contrived because
    it needs to work around the way doctest verifies
    The output will be the following dict - {C3: {A1, A5, D2, E1, B4, B2, E5, D4}}

        T - target - maps to a key of the dict of type chess.position.Position
        x - expected move == X
    """
    wanted_moves = set()
    target = None

    for row, cur_rank in zip(positions, reversed(Rank)):
        for col, cur_file in zip(row, File):
            if col == 'T':
                target = Position(cur_rank, cur_file)
            elif col in ['x', 'X']:
                wanted_moves.add(Position(cur_rank, cur_file))

    return {target: wanted_moves}
