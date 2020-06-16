import unittest
from unittest.mock import MagicMock

from chess.board            import Board
from chess.constants        import FigureColor as Color, FigureType as Type
from chess.constants        import Rank, File
from chess.position         import Position

from tests import MoveGenerationTestCase, target_board

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
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '........',  # 7
                        '........',  # 6
                        'X...X...',  # 5
                        '.x.x....',  # 4
                        '..T.....',  # 3
                        '.x.x....',  # 2
                        'X...X...'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '..X...X.',  # 8
                        '...x.x..',  # 7
                        '....T...',  # 6
                        '...x.x..',  # 5
                        '..X...X.',  # 4
                        '........',  # 3
                        '........',  # 2
                        '........'   # 1
                    ])
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
                            (+1, +1), (+2, +2),  # up right
                        }
                    },
                    'black': {
                        Position(Rank.ONE, File.H): {
                            (+1, -1), (+2, -2),  # up left diagonal
                        }
                    }
                }
            },
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
