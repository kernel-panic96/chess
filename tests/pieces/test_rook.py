import unittest
from unittest.mock import MagicMock

from chess_pieces.rook import Rook
from constants import Rank, File, Direction, FigureColor
from position import Position


class MoveGenerationTests(unittest.TestCase):
    def setUp(self):
        self.board = MagicMock()
        self.mock_get_positions = MagicMock()

    def test_should_stop_at_first_enemy_and_add_it(self):
        positions = {
            Direction.UP: [
                Position(Rank.FOUR, File.C),
                Position(Rank.FOUR, File.B)
            ]
        }

        self.board.is_in_bounds = MagicMock(side_effect=[True, True, True])
        self.board.is_empty = MagicMock(side_effect=[True, False])
        self.board.are_enemies = MagicMock(return_value=True)

        self.board.get_positions_in_direction = MagicMock(return_value=positions)

        rook = Rook(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)

        positions = rook.generate_moves(self.board)

        self.assertSetEqual(set(positions), {
            Position(Rank.FOUR, File.C),
            Position(Rank.FOUR, File.B),
        })

    def test_should_stop_at_first_friendly_and_not_add_it(self):
        positions = {
            Direction.UP: [
                Position(Rank.FOUR, File.C),
                Position(Rank.FOUR, File.B)
            ]
        }

        self.board.is_in_bounds = MagicMock(side_effect=[True, True, True])
        self.board.is_empty = MagicMock(side_effect=[True, False])
        self.board.are_enemies = MagicMock(return_value=False)

        self.board.get_positions_in_direction = MagicMock(return_value=positions)

        rook = Rook(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)

        positions = rook.generate_moves(self.board)

        self.assertSetEqual(set(positions), {
            Position(Rank.FOUR, File.C),
        })
