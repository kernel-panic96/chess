import unittest

from chess.board import Board
from chess.pieces.pawn import Pawn
from chess.constants import Rank, File
from chess.constants import FigureColor as Color, FigureType as Type
from chess.position import Position

from tests import MoveGenerationTestCase

P = Position.from_str


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
                'name': 'should_be_able_to_mode_two_ahead_from_start',
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

    def test_pawn_en_passant_legal_scenarios(self):
        test_table = [
            {
                # white captures
                'name': 'en_passant_square_is_legal_move',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    '........',  # 6
                    'P.P.....',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'move_before': {'from': P('b7'), 'to': P('b5')},
                'want': {
                    'white': {
                        # given: {want...}
                        P('c5'): {P('c6'), P('b6')},
                        P('a5'): {P('a6'), P('b6')}
                    }
                }
            },
            {
                # black captures
                'name': 'en_passant_position_is_in_legal_moves',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    'p.p.....',  # 4
                    '........',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ]),
                'move_before': {'from': P('b2'), 'to': P('b4')},
                'want': {
                    'black': {
                        P('c4'): {P('c3'), P('b3')},
                        P('a4'): {P('a3'), P('b3')}
                    }
                }
            }
        ]

        for test_case in test_table:
            board = test_case['board']
            f, t = test_case['move_before']['from'], test_case['move_before']['to']
            board.move(from_pos=f, to_pos=t)

            self.assertEqual(board[t.rank][t.file].figure_type, Type.PAWN)
            self.runMoveGenerationTest(test_case)

    def test_en_passant_should_capture_opposing_pawn(self):
        with self.subTest('black_captures_left'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '..p.....',  # 4
                '........',  # 3
                '.P......',  # 2
                '........'   # 1
                # bcdefgh
            ])
            board.move(from_pos=P('b2'), to_pos=P('b4'))
            self.assertIsInstance(board[Rank.FOUR][File.C], Pawn)
            black_pawn = board[Rank.FOUR][File.C]

            self.assertIn(P('b3'), black_pawn.generate_moves(board, P('c4')))

            self.assertIsInstance(board[Rank.FOUR][File.B], Pawn)
            board.move(from_pos=P('c4'), to_pos=P('b3'))
            self.assertIsNone(board[Rank.FOUR][File.B])

        with self.subTest('white_captures_left'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '..p.....',  # 7
                '........',  # 6
                '.P......',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
            ])
            board.move(from_pos=P('c7'), to_pos=P('c5'))
            self.assertIsInstance(board[Rank.FIVE][File.B], Pawn)
            white_pawn = board[Rank.FIVE][File.B]

            self.assertIn(P('c6'), white_pawn.generate_moves(board, P('b5')))
            board.move(from_pos=P('b5'), to_pos=P('c6'))
            self.assertIsNone(board[Rank.FIVE][File.C])

        with self.subTest('black_captures_right'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '..p.....',  # 4
                '........',  # 3
                '...P....',  # 2
                '........'   # 1
                # bcdefgh
            ])
            board.move(from_pos=P('d2'), to_pos=P('d4'))
            self.assertIsInstance(board[Rank.FOUR][File.C], Pawn)
            black_pawn = board[Rank.FOUR][File.C]

            self.assertIn(P('d3'), black_pawn.generate_moves(board, P('c4')))
            self.assertIsInstance(board[Rank.FOUR][File.D], Pawn)
            board.move(from_pos=P('c4'), to_pos=P('d3'))
            self.assertIsNone(board[Rank.FOUR][File.D])

        with self.subTest('white_captures_right'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '..p.....',  # 7
                '........',  # 6
                '...P....',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
            ])
            board.move(from_pos=P('c7'), to_pos=P('c5'))
            self.assertIsInstance(board[Rank.FIVE][File.D], Pawn)
            white_pawn = board[Rank.FIVE][File.D]

            self.assertIn(P('c6'), white_pawn.generate_moves(board, P('d5')))
            board.move(from_pos=P('d5'), to_pos=P('c6'))
            self.assertIsNone(board[Rank.FIVE][File.C])

    def test_en_passant_is_unavailable_after_making_another_move(self):
        with self.subTest('white'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '..p.....',  # 7
                '........',  # 6
                '...P....',  # 5
                '........',  # 4
                '........',  # 3
                '....P...',  # 2
                '........'   # 1
                # bcdefgh
            ])
            board.move(from_pos=P('c7'), to_pos=P('c5'))
            self.assertIsInstance(board[Rank.FIVE][File.D], Pawn)
            white_pawn = board[Rank.FIVE][File.D]

            self.assertIn(P('c6'), white_pawn.generate_moves(board, P('d5')))
            board.move(from_pos=P('e2'), to_pos=P('e3'))
            self.assertNotIn(P('c6'), white_pawn.generate_moves(board, P('d5')))

        with self.subTest('black'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '...p....',  # 7
                '........',  # 6
                '........',  # 5
                '..p.....',  # 4
                '........',  # 3
                '...P....',  # 2
                '........'   # 1
                # bcdefgh
            ])
            board.move(from_pos=P('d2'), to_pos=P('d4'))
            self.assertIsInstance(board[Rank.FOUR][File.C], Pawn)
            black_pawn = board[Rank.FOUR][File.C]

            self.assertIn(P('d3'), black_pawn.generate_moves(board, P('c4')))
            board.move(from_pos=P('d7'), to_pos=P('d6'))
            self.assertNotIn(P('d3'), black_pawn.generate_moves(board, P('c4')))

    def test_en_passant_square_is_set_on_the_board_object(self):
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

        with self.subTest('white'):
            en_passant_want = Position(Rank.THREE, File.B)
            f, t = Position(Rank.TWO, File.B), Position(Rank.FOUR, File.B)
            board.move(from_pos=f, to_pos=t)

            self.assertEqual(board.en_passant_pos, en_passant_want)

        with self.subTest('black'):
            en_passant_want = Position(Rank.SIX, File.B)
            f, t = Position(Rank.SEVEN, File.B), Position(Rank.FIVE, File.B)
            board.move(from_pos=f, to_pos=t)

            self.assertEqual(board.en_passant_pos, en_passant_want)


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
