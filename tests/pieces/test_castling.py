import unittest

from chess.pieces import King, Rook
from chess.board import Board
from chess.position import Position
from chess.constants import Rank, File
from chess.constants import FigureColor as Color

from tests import MoveGenerationTestCase

P = Position.from_str


class Castling(MoveGenerationTestCase):
    def test_castling_scenarios(self):
        test_table = [
            {'name': 'should_be_able_to_castle_both_sides',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k..r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'R...K..R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        'assert': self.assertIn,
                        P('e1'): P('c1'),
                    },
                    'white_king_side': {
                        'assert': self.assertIn,
                        P('e1'): P('g1'),
                    },
                    'black_queen_side': {
                        'assert': self.assertIn,
                        P('e8'): P('c8'),
                    },
                    'black_king_side': {
                        'assert': self.assertIn,
                        P('e8'): P('g8'),
                    }
                }
            },
            {'name': 'should_be_able_to_castle_queen_side',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k...',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'R...K...'   # 1
                ]),
                'want': {
                    'white': {
                        'assert': self.assertIn,
                        P('e1'): P('c1'),
                    },
                    'black': {
                        'assert': self.assertIn,
                        P('e8'): P('c8'),
                    },
                }
            },
            {'name': 'should_be_able_to_castle_king_side',
                'board': Board.from_strings([
                    # bcdefgh
                    '....k..r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '....K..R'   # 1
                ]),
                'want': {
                    'white': {
                        'assert': self.assertIn,
                        P('e1'): P('g1'),
                    },
                    'black': {
                        'assert': self.assertIn,
                        P('e8'): P('g8'),
                    },
                }
            },
            {'name': 'standard_configuration_should_not_be_able_to_castle_because_of_blockers',
                'board': Board.from_strings([
                    # bcdefgh
                    'rnbqkbnr',  # 8
                    'pppppppp',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'PPPPPPPP',  # 2
                    'RNBQKBNR'   # 1
                ]),
                'want': {
                    'white': {P('e1'): {}},
                    'black': {P('e8'): {}},
                }
            },
            {'name': 'should_not_castle_if_file_is_blocked_by_friendly',
                'board': Board.from_strings([
                    # bcdefgh
                    'rn..k.nr',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'RN..K.NR'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('c1'),
                    },
                    'white_king_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('g1'),
                    },
                    'black_queen_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('c8'),
                    },
                    'black_king_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('g8'),
                    }
                }
            },
            {'name': 'should_not_be_able_to_castle_if_king_is_in_check',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k..r',  # 8
                    '........',  # 7
                    '....R...',  # 6
                    '........',  # 5
                    '........',  # 4
                    '....r...',  # 3
                    '........',  # 2
                    'R...K..R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('c1'),
                    },
                    'white_king_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('g1'),
                    },
                    'black_queen_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('c8'),
                    },
                    'black_king_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('g8'),
                    }
                }
            },
            {'name': 'should_not_be_able_to_castle_if_king_will_be_in_check_if_he_castles',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k..r',  # 8
                    '........',  # 7
                    '..R...R.',  # 6
                    '........',  # 5
                    '........',  # 4
                    '..r...r.',  # 3
                    '........',  # 2
                    'R...K..R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('c1'),
                    },
                    'white_king_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('g1'),
                    },
                    'black_queen_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('c8'),
                    },
                    'black_king_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('g8'),
                    }
                }
            },
            {'name': 'should_not_be_able_to_castle_if_last_files_are_not_rooks',
                'board': Board.from_strings([
                    # bcdefgh
                    'b...k..b',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'B...K..B'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('c1'),
                    },
                    'white_king_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('g1'),
                    },
                    'black_queen_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('c8'),
                    },
                    'black_king_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('g8'),
                    }
                }
            },
            {'name': 'should_not_be_able_to_castle_if_the_king_passes_through_a_check',
                'board': Board.from_strings([
                    # bcdefgh
                    'b...k..b',  # 8
                    '........',  # 7
                    '...R.R..',  # 6
                    '........',  # 5
                    '........',  # 4
                    '...r.r..',  # 3
                    '........',  # 2
                    'B...K..B'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('c1'),
                    },
                    'white_king_side': {
                        'assert': self.assertNotIn,
                        P('e1'): P('g1'),
                    },
                    'black_queen_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('c8'),
                    },
                    'black_king_side': {
                        'assert': self.assertNotIn,
                        P('e8'): P('g8'),
                    }
                }
            },
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)

    def test_moving_rooks_should_disallow_future_castling_only_on_that_side(self):
        with self.subTest('white queen side'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                'R...K..R'   # 1
                # bcdefgh
            ])
            white_king = board[Rank.ONE][File.E]

            moves = white_king.generate_moves(board, P('e1'))
            self.assertIn(P('c1'), moves)
            self.assertIn(P('g1'), moves)

            # move the rook and then return it in it's original position
            board.move(from_pos=P('h1'), to_pos=P('g1'))
            board.move(from_pos=P('g1'), to_pos=P('h1'))

            moves = white_king.generate_moves(board, P('e1'))
            self.assertNotIn(P('g1'), moves)
            self.assertIn(P('c1'), moves)

        with self.subTest('white king side'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                'R...K..R'   # 1
                # bcdefgh
            ])
            white_king = board[Rank.ONE][File.E]
            moves = white_king.generate_moves(board, P('e1'))
            self.assertIn(P('g1'), moves)
            self.assertIn(P('c1'), moves)

            # move the right rook and then return it in it's original position
            board.move(from_pos=P('a1'), to_pos=P('b1'))
            board.move(from_pos=P('b1'), to_pos=P('a1'))

            moves = white_king.generate_moves(board, P('e1'))
            self.assertNotIn(P('c1'), moves)
            self.assertIn(P('g1'), moves)

        with self.subTest('black queen side'):
            board = Board.from_strings([
                # bcdefgh
                'r...k..r',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
                # bcdefgh
            ])
            white_king = board[Rank.EIGHT][File.E]
            moves = white_king.generate_moves(board, P('e8'))
            self.assertIn(P('c8'), moves)

            # move the rook and then return it in it's original position
            board.move(from_pos=P('a8'), to_pos=P('b8'))
            board.move(from_pos=P('b8'), to_pos=P('a8'))

            moves =  white_king.generate_moves(board, P('e8'))
            self.assertNotIn(P('c8'), moves)
            self.assertIn(P('g8'), moves)

        with self.subTest('black king side'):
            board = Board.from_strings([
                # bcdefgh
                'r...k..r',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
                # bcdefgh
            ])
            white_king = board[Rank.EIGHT][File.E]
            moves = white_king.generate_moves(board, P('e8'))
            self.assertIn(P('g8'), moves)
            self.assertIn(P('c8'), moves)

            # move the rook and then return it in it's original position
            board.move(from_pos=P('h8'), to_pos=P('g8'))
            board.move(from_pos=P('g8'), to_pos=P('h8'))

            moves = white_king.generate_moves(board, P('e8'))
            self.assertNotIn(P('g8'), moves)
            self.assertIn(P('c8'), moves)

    def test_moving_the_king_should_disallow_any_further_castling(self):
        with self.subTest('white'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                'R...K..R'   # 1
                # bcdefgh
            ])
            white_king = board[Rank.ONE][File.E]
            moves = white_king.generate_moves(board, P('e1'))
            self.assertIn(P('c1'), moves)
            self.assertIn(P('g1'), moves)

            # move the king and then return it in it's original position
            board.move(from_pos=P('e1'), to_pos=P('f1'))
            board.move(from_pos=P('f1'), to_pos=P('e1'))

            moves = white_king.generate_moves(board, P('e1'))
            self.assertNotIn(P('c1'), moves)
            self.assertNotIn(P('g1'), moves)

        with self.subTest('black'):
            board = Board.from_strings([
                # bcdefgh
                'r...k..r',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
                # bcdefgh
            ])
            black_king = board[Rank.EIGHT][File.E]
            moves = black_king.generate_moves(board, P('e8'))
            self.assertIn(P('c8'), moves)
            self.assertIn(P('g8'), moves)

            board.move(from_pos=P('e8'), to_pos=P('f8'))
            board.move(from_pos=P('f8'), to_pos=P('e8'))

            moves = black_king.generate_moves(board, P('e8'))
            self.assertNotIn(P('c8'), moves)
            self.assertNotIn(P('g8'), moves)

    def test_should_move_rook_when_king_castles(self):
        with self.subTest('black king side'):
            board = Board.from_strings([
                # bcdefgh
                'r...k..r',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
                # bcdefgh
            ])
            black_king = board[Rank.EIGHT][File.E]
            self.assertIn(P('g8'), black_king.generate_moves(board, P('e8')))

            board.move(from_pos=P('e8'), to_pos=P('g8'))
            self.assertIsInstance(board[Rank.EIGHT][File.F], Rook)  # rook has moved

        with self.subTest('black queen side'):
            board = Board.from_strings([
                # bcdefgh
                'r...k..r',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                '........'   # 1
            ])
            black_king = board[Rank.EIGHT][File.E]
            self.assertIn(P('c8'), black_king.generate_moves(board, P('e8')))

            board.move(from_pos=P('e8'), to_pos=P('c8'))
            self.assertIsInstance(board[Rank.EIGHT][File.D], Rook)  # rook has moved

        with self.subTest('white king side'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                'R...K..R'   # 1
            ])
            white_king = board[Rank.ONE][File.E]
            self.assertIn(P('c1'), white_king.generate_moves(board, P('e1')))

            board.move(from_pos=P('e1'), to_pos=P('g1'))
            self.assertIsInstance(board[Rank.ONE][File.F], Rook)  # rook has moved

        with self.subTest('white queen side'):
            board = Board.from_strings([
                # bcdefgh
                '........',  # 8
                '........',  # 7
                '........',  # 6
                '........',  # 5
                '........',  # 4
                '........',  # 3
                '........',  # 2
                'R...K..R'   # 1
            ])
            white_king = board[Rank.ONE][File.E]
            self.assertIn(P('c1'), white_king.generate_moves(board, P('e1')))

            board.move(from_pos=P('e1'), to_pos=P('c1'))
            self.assertIsInstance(board[Rank.ONE][File.D], Rook)  # rook has moved