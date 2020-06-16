import unittest

from board import Board
from position import Position
from test_utils import rotate_board, rotate_position

from functional import seq


class MoveGenerationTestCase(unittest.TestCase):
    recognized_iterables = (type(seq(0)), list, tuple, set, dict)

    def runMoveGenerationTest(self, test_case):
        try:
            board = test_case['board']
            test_data = test_case['want']

            for color in test_data.keys():
                with self.subTest('/'.join([test_case['name'], color])):
                    assert_fn = test_data[color].pop('assert', None)

                    for pos, want in test_data[color].items():
                        piece = board[pos.rank][pos.file]
                        actual = set(piece.generate_moves(board, pos))

                        if isinstance(want, self.recognized_iterables):
                            want = set(map(_transform_relative_offset_to_position(pos), want))
                        else:
                            want = _transform_relative_offset_to_position(pos)(want)

                        assert_fn = assert_fn or self.assertSetEqual

                        assert_fn(want, actual)
        except Exception as e:
            raise e.__class__(f'During test "{test_case["name"]}"') from e

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
        name  = test_case['name']
        want  = test_case['want']

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
