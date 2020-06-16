import unittest
from unittest.mock import MagicMock

from tests import MoveGenerationTestCase

from chess_pieces.knight import Knight
from board import Board
from position import Position
from constants import FigureType as Type, FigureColor as Color
from constants import Rank, File


class KnightMoveTests(MoveGenerationTestCase):
    def test_board_constructor_works_for_knights(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.n......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '.N......',  # 2
            '........'   # 1
        ])
        self.assertEqual(board[Rank.TWO][File.B].type, Type.KNIGHT)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.KNIGHT)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_knight_move_gen(self):
        test_table = [
            {

            }
        ]
