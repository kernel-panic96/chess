import unittest

from board              import Board
from chess_pieces.queen import Queen
from constants          import FigureColor as Color, FigureType as Type
from constants          import Rank, File
from position           import Position


from tests import MoveGenerationTestCase


class TestMoveGeneration(MoveGenerationTestCase):
    def test_board_constructor_works_for_queen(self):
        board = Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.q......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.Q......',  # 2
                    '........'   # 1
                ])

        self.assertEqual(board[Rank.TWO][File.B].figure_type, Type.QUEEN)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].figure_type, Type.QUEEN)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_move_generation(self):
        test_table = [
            *self.all_board_rotations_of({
                'name': 'friendly_on_diagonals_should_not_be_capturable',
                'board': Board.from_strings([
                    # bcdefgh
                    '....q..q',  # 8
                    '........',  # 7
                    '........',  # 6
                    '....q..q',  # 5
                    'Q..Q....',  # 4
                    '........',  # 3
                    '........',  # 2
                    'Q..Q....'   # 1
                ]),
                'want': {
                    'white': {Position(Rank.ONE, File.A): {
                        (0, +1),
                        (0, +2),
                        (+1, +1),
                        (+2, +2),
                        (+1, 0),
                        (+2, 0),
                    }},
                    'black': {Position(Rank.EIGHT, File.H): {
                        (0, -1),
                        (0, -2),
                        (-1, -1),
                        (-2, -2),
                        (-1, 0),
                        (-2, 0),
                    }},
                }
            }),
        ]
