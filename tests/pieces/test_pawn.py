import unittest

from board             import Board
from chess_pieces.pawn import Pawn
from constants         import Rank, File
from constants         import FigureColor as Color, FigureType as Type
from position          import Position

from tests import MoveGenerationTestCase


class TestPawnMoveGeneration(MoveGenerationTestCase):
    def test_board_constructor_works_for_pawns(self):
        board = Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ])
        self.assertEqual(board[Rank.TWO][File.B].type,  Type.PAWN)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.PAWN)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_pawn_move_generation(self):
        test_table = [
            {
                'name': 'when_friendly_is_blocking',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    '........',  # 6
                    '.p......',  # 5
                    '.P......',  # 4
                    '........',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.TWO, File.B): {
                            Position(Rank.THREE, File.B)
                        }
                    },
                    'black': {
                        Position(Rank.SEVEN, File.B): {
                            Position(Rank.SIX, File.B)
                        }
                    },
                }
            },
            {
                'name': 'given_starting_position_enemy_is_blocking_two_squares_ahead',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    '........',  # 6
                    '.P......',  # 5
                    '.p......',  # 4
                    '........',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.TWO, File.B): {
                            Position(Rank.THREE, File.B)
                        }
                    },
                    'black': {
                        Position(Rank.SEVEN, File.B): {
                            Position(Rank.SIX, File.B)
                        }
                    },
                }
            },
            {
                'name': 'should_capture_left',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    'P.......',  # 5
                    'p.......',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.THREE, File.B): {
                            Position(Rank.FOUR, File.A),
                            Position(Rank.FOUR, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.SIX, File.B): {
                            Position(Rank.FIVE, File.A),
                            Position(Rank.FIVE, File.B),
                        }
                    },
                }
            },
            {
                'name': 'should_not_capture_left_friendly',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    'p.......',  # 5
                    'P.......',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.THREE, File.B): {
                            Position(Rank.FOUR, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.SIX, File.B): {
                            Position(Rank.FIVE, File.B),
                        }
                    },
                }
            },
            {
                'name': 'should_capture_right',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    '..P.....',  # 5
                    '..p.....',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.THREE, File.B): {
                            Position(Rank.FOUR, File.B),
                            Position(Rank.FOUR, File.C),
                        }
                    },
                    'black': {
                        Position(Rank.SIX, File.B): {
                            Position(Rank.FIVE, File.B),
                            Position(Rank.FIVE, File.C),
                        }
                    },
                }
            },
            {
                'name': 'should_not_capture_right_friendly',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    '..p.....',  # 5
                    '..P.....',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.THREE, File.B): {
                            Position(Rank.FOUR, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.SIX, File.B): {
                            Position(Rank.FIVE, File.B),
                        }
                    },
                }
            },
            {
                'name': 'should_be_have_two_ahead_from_start',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.TWO, File.B): {
                            Position(Rank.THREE, File.B),
                            Position(Rank.FOUR, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.SEVEN, File.B): {
                            Position(Rank.SIX, File.B),
                            Position(Rank.FIVE, File.B),
                        }
                    },
                }
            },
            {
                'name': 'should_have_all_positions',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    'P.P.....',  # 6
                    '........',  # 5
                    '........',  # 4
                    'p.p.....',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.TWO, File.B): {
                            Position(Rank.THREE, File.A),
                            Position(Rank.THREE, File.B),
                            Position(Rank.THREE, File.C),
                            Position(Rank.FOUR, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.SEVEN, File.B): {
                            Position(Rank.SIX, File.A),
                            Position(Rank.SIX, File.B),
                            Position(Rank.SIX, File.C),
                            Position(Rank.FIVE, File.B),
                        }
                    },
                }
            },
            {
                'name': 'clear_file_not_starting_square_should_have_only_one_ahead',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    '........',  # 5
                    '........',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.THREE, File.B): {
                            Position(Rank.FOUR, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.SIX, File.B): {
                            Position(Rank.FIVE, File.B),
                        }
                    },
                }
            },
            {
                'name': 'friendly_blocker_and_no_captures_should_have_no_moves',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    '.p......',  # 5
                    '.P......',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {Position(Rank.THREE, File.B): {}},
                    'black': {Position(Rank.SIX, File.B): {}},
                }
            },
            {
                'name': 'enemy_blocker_and_no_captures_should_have_no_moves',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.p......',  # 6
                    '.P......',  # 5
                    '.p......',  # 4
                    '.P......',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {Position(Rank.THREE, File.B): {}},
                    'black': {Position(Rank.SIX, File.B): {}},
                }
            },
        ]
        for test_case in test_table:
            self.runMoveGenerationTest(test_case)


class PawnHelpersTests(unittest.TestCase):
    def test_is_at_starting_rank_correctness(self):
        with self.subTest('white'):
            wp = Pawn(Color.WHITE)
            for file in File:
                self.assertTrue(wp.is_at_starting_pos(Position(Rank.TWO, file)))

            self.assertFalse(wp.is_at_starting_pos(Position(Rank.SEVEN, File.G)))

        with self.subTest('black'):
            bp = Pawn(Color.BLACK)
            for file in File:
                self.assertTrue(bp.is_at_starting_pos(Position(Rank.SEVEN, file)))

            self.assertFalse(bp.is_at_starting_pos(Position(Rank.TWO, File.G)))

    def test_is_white_correctness(self):
        with self.subTest('white'):
            self.assertTrue(Pawn(Color.WHITE).is_white)
        with self.subTest('black'):
            self.assertFalse(Pawn(Color.BLACK).is_white)

    def test_figure_type_class_attribute_is_pawn(self):
        self.assertEqual(Pawn.figure_type, Type.PAWN)
