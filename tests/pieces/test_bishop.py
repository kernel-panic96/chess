import unittest
from unittest.mock import MagicMock

from board               import Board
from chess_pieces.bishop import Bishop
from constants           import Diagonal
from constants           import FigureColor as Color, FigureType as Type
from constants           import Rank, File
from position            import Position

from tests import MoveGenerationTestCase

from functional import seq


class TestBishop(MoveGenerationTestCase):
    def test_board_constructor_works_for_bishops(self):
        board = Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.b......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.B......',  # 2
                    '........'   # 1
                ])
        self.assertEqual(board[Rank.TWO][File.B].type, Type.BISHOP)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.BISHOP)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_move_generation(self):
        test_table = [
            {
                'name': 'friendly_on_diagonals_should_not_be_capturable',
                'board': Board.from_strings([
                    # bcdefgh
                    'b.b.....',  # 8
                    '.b......',  # 7
                    'b.b.....',  # 6
                    '........',  # 5
                    '........',  # 4
                    'B.B.....',  # 3
                    '.B......',  # 2
                    'B.B.....'   # 1
                ]),
                'want': {
                    'white': {Position(Rank.TWO, File.B): {}},
                    'black': {Position(Rank.TWO, File.B): {}},
                }
            },
            {
                'name': 'enemies_on_diagonals_should_be_capturable',
                'board': Board.from_strings([
                    # bcdefgh
                    '..B...B.',  # 8
                    '........',  # 7
                    '....b...',  # 6
                    'b...b...',  # 5
                    '..B...B.',  # 4
                    '..B.....',  # 3
                    '........',  # 2
                    'b...b...'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.THREE, File.C): set.union(
                                # all diagonals within 2 squares
                                seq(-1, 1).cartesian(repeat=2).set(),
                                seq(-2, 2).cartesian(repeat=2).set()
                            )
                    },
                    'black': {
                        Position(Rank.SIX, File.E): set.union(
                                seq(-1, 1).cartesian(repeat=2).set(),
                                seq(-2, 2).cartesian(repeat=2).set()
                            )
                    }
                }
            },
            {
                'name': 'should_not_be_able_to_go_over_pieces',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '...bB...',  # 5
                    '........',  # 4
                    '..b..B..',  # 3
                    '........',  # 2
                    'B......b'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.A): {
                            Position(Rank.TWO,   File.B),
                            Position(Rank.THREE, File.C)
                        }
                    },
                    'black': {
                        Position(Rank.ONE, File.H): {
                            Position(Rank.TWO,   File.G),
                            Position(Rank.THREE, File.F),
                        }
                    }
                }
            },
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
