import unittest
from unittest.mock import MagicMock

from chess_pieces.board_traverse_mixin import BoardTraverserMixin


class Test(unittest.TestCase):
    class FakePiece(BoardTraverserMixin):
        pass

    def setUp(self):
        self.board = MagicMock()
        self.board.get_positions_in_direction = MagicMock()

    def test_test(self):
        pass
