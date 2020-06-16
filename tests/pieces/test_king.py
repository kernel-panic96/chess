import unittest
import functools as fp
from unittest.mock import MagicMock

from test_utils import rotate_board, rotate_position
from tests import MoveGenerationTestCase

from chess_pieces.king import King
from board import Board
from position import Position
from constants import FigureType as Type, FigureColor as Color
from constants import Rank, File

from functional import seq


class MoveGenerationTests(MoveGenerationTestCase):
    def test_board_constructor_works_for_kings(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.k......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '.K......',  # 2
            '........'   # 1
        ])
        self.assertEqual(board[Rank.TWO][File.B].type, Type.KING)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.KING)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_move_generation(self):
        test_table = [
            {
                'name': 'clear_board_should_have_all_surrounding_positions',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.SEVEN, File.B): seq(-1, 0, 1).cartesian(repeat=2).filter_not(lambda a: a == (0, 0))
                    },
                    'black': {
                        Position(Rank.TWO, File.B): seq(-1, 0, 1).cartesian(repeat=2).filter_not(lambda a: a == (0, 0))
                    },
                }
            },
            *self.all_board_rotations_of({
                'name': 'should_be_bounds_aware',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......k',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'K.......'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.A):
                            seq(0, 1)\
                            .cartesian(repeat=2)\
                            .filter_not(lambda p: p == (0, 0))
                    },
                    'black': {
                        Position(Rank.EIGHT, File.H):
                            seq(0, -1)\
                            .cartesian(repeat=2)\
                            .filter_not(lambda p: p == (0, 0))
                    },
                }
            }),
            {
                'name': 'should_be_able_to_capture',
                'board': Board.from_strings([
                    # bcdefgh
                    'K.......',  # 8
                    'pp......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'PP......',  # 2
                    'k.......'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.EIGHT, File.A): {
                            Position(Rank.SEVEN, File.A),
                            Position(Rank.SEVEN, File.B),
                            Position(Rank.EIGHT, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.ONE, File.A): {
                            Position(Rank.ONE, File.B),
                            Position(Rank.TWO, File.B),
                            Position(Rank.TWO, File.A),
                        }
                    },
                }
            },
            {
                'name': 'should_not_include_friendlies',
                'board': Board.from_strings([
                    # bcdefgh
                    'kk......',  # 8
                    'kk......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'KK......',  # 2
                    'KK......'   # 1
                ]),
                'want': {
                    'white': {Position(Rank.ONE, File.A):   {}},
                    'black': {Position(Rank.EIGHT, File.A): {}},
                }
            },
            {
                'name': 'should_not_be_able_to_capture_if_piece_is_protected',
                'board': Board.from_strings([
                    # bcdefgh
                    'Kb......',  # 8
                    'pp......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'PP......',  # 2
                    'kB......'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.EIGHT, File.A): {
                            Position(Rank.SEVEN, File.B),
                            Position(Rank.EIGHT, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.ONE, File.A): {
                            Position(Rank.ONE, File.B),
                            Position(Rank.TWO, File.B),
                        }
                    },
                }
            },
            *self.all_board_rotations_of({
                'name': 'when_in_check_should_be_aware_of_its_own_position',
                'comment': '''
                    when a possible position is evaluated, the code should not consider
                    it's old position as a blocker of an attacker

                    In this situation:

                    a b c d e f g h
                    1 . Q . k . . . . 1

                    F1 should not be a valid move
                ''',
                'board': Board.from_strings([
                    # bcdefgh
                    'R..k....',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'r..K....'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.D): Position(Rank.ONE, File.E),
                        'assert': self.assertNotIn,
                    },
                    'black': {
                        Position(Rank.EIGHT, File.D): Position(Rank.EIGHT, File.E),
                        'assert': self.assertNotIn
                    },
                }
            }),
            {
                'name': 'should_not_be_able_to_step_on_attacked_squares',
                'board': Board.from_strings([
                    # bcdefgh
                    '...k....',  # 8
                    'R.......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'r.......',  # 2
                    '...K....'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.D): {
                            Position(Rank.TWO, File.C),
                            Position(Rank.TWO, File.D),
                            Position(Rank.TWO, File.E),
                        },
                        'assert': lambda want, actual: [self.assertNotIn(p, actual) for p in want]
                    },
                    'black': {
                        Position(Rank.EIGHT, File.D): {
                            Position(Rank.SEVEN, File.C),
                            Position(Rank.SEVEN, File.D),
                            Position(Rank.SEVEN, File.E),
                        },
                        'assert': lambda want, actual: [self.assertNotIn(p, actual) for p in want]
                    },
                }
            }
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
