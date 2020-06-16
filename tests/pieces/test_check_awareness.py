from unittest.mock import MagicMock
import unittest
import contextlib

from board import Board
from chess_pieces.queen import Queen
from constants import FigureColor, FigureType, Rank, File
from position import Position
from test_utils import rotate_board, rotate_position


from tests import MoveGenerationTestCase

king_mock = MagicMock()
king_mock.figure_type = FigureType.KING

P = Position.from_str


class CheckAwarenessTests(MoveGenerationTestCase):
    def test_pieces_should_block(self):
        test_table = [
            {
                # white
                'name': 'should_not_be_able_to_move_from_diagonals',
                'board': Board.from_strings([
                    # bcdefgh
                    '.b.....q',  # 8
                    '........',  # 7
                    '...Q.Q..',  # 6
                    '....K...',  # 5
                    '...B.B..',  # 4
                    '........',  # 3
                    '.q.....b',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        P('f6'): {P('g7'), P('h8')},
                        P('f4'): {P('g3'), P('h2')},
                        P('d6'): {P('c7'), P('b8')},
                        P('d4'): {P('c3'), P('b2')},
                    }
                }
            },
            {
                # black
                'name': 'should_not_be_able_to_move_from_diagonals',
                'board': Board.from_strings([
                    # bcdefgh
                    '.B.....Q',  # 8
                    '........',  # 7
                    '...q.q..',  # 6
                    '....k...',  # 5
                    '...b.b..',  # 4
                    '........',  # 3
                    '.Q.....B',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'black': {
                        P('f6'): {P('g7'), P('h8')},
                        P('f4'): {P('g3'), P('h2')},
                        P('d6'): {P('c7'), P('b8')},
                        P('d4'): {P('c3'), P('b2')},
                    }
                }
            },
            {
                # white
                'name': 'should_not_be_able_to_move_from_straight',
                'board': Board.from_strings([
                    # bcdefgh
                    '....q...',  # 8
                    '........',  # 7
                    '....Q...',  # 6
                    '.q.QKQ.q',  # 5
                    '....Q...',  # 4
                    '........',  # 3
                    '....q...',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        P('f5'): {P('g5'), P('h5')},
                        P('d5'): {P('c5'), P('b5')},
                        P('e6'): {P('e7'), P('e8')},
                        P('e4'): {P('e3'), P('e2')},
                    }
                }
            },
            {
                # black
                'name': 'should_not_be_able_to_move_from_straight',
                'board': Board.from_strings([
                    # bcdefgh
                    '....Q...',  # 8
                    '........',  # 7
                    '....q...',  # 6
                    '.Q.qkq.Q',  # 5
                    '....q...',  # 4
                    '........',  # 3
                    '....Q...',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        P('f5'): {P('g5'), P('h5')},
                        P('d5'): {P('c5'), P('b5')},
                        P('e6'): {P('e7'), P('e8')},
                        P('e4'): {P('e3'), P('e2')},
                    }
                }
            },
            {
                'name': 'knight_should_block',
                'board': Board.from_strings([
                    # bcdefgh
                    'N.....n.',  # 8
                    '.q.....Q',  # 7
                    '........',  # 6
                    '.K.....k',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        P('a8'): {P('b6')}
                    },
                    'black': {
                        P('g8'): {P('h6')}
                    }
                }
            },
            {
                'name': 'pawn_should_block',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '......q.',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.....P..',  # 2
                    '..K.....'   # 1
                ]),
                'want': {
                    'white': {
                        P('f2'): {P('f4')}
                    },
                }
            }
        ]
        for test_case in test_table:
            self.runMoveGenerationTest(test_case)

    def test_pieces_should_not_move_if_in_check(self):
        test_table = [
            {
                'name': 'queen_should_not_move',
                'board': Board.from_strings([
                    # bcdefgh
                    '....q...',  # 8
                    '.q......',  # 7
                    '..Q.....',  # 6
                    '.K......',  # 5
                    '.......Q',  # 4
                    '....Q...',  # 3
                    '.....q..',  # 2
                    '....k...'   # 1
                ]),
                'want': {
                    'white': {P('c6'): {}},
                    'black': {P('f2'): {}}
                }
            }
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
