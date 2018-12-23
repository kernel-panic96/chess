import unittest
from unittest.mock import MagicMock

from board import Board
from chess_pieces.bishop import Bishop
from constants import Rank, File, FigureColor, Diagonal
from position import Position


class MoveGenerationTests(unittest.TestCase):
    def setUp(self):
        self.board = MagicMock()
        self.mock_get_positions = MagicMock()

    def test_should_call_get_positions_in_directions_with_all_diagonals(self):
        piece_position = Position(Rank.FOUR, File.D)

        mock_return_value = {Diagonal.UP_LEFT: [Position(Rank.THREE, File.B)]}
        self.mock_get_positions.return_value = mock_return_value
        self.board.get_positions_in_direction = self.mock_get_positions

        bishop = Bishop(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)

        bishop.generate_moves(self.board)

        self.mock_get_positions.assert_called_once()
        call_position = self.mock_get_positions.call_args[0][0]
        call_directions = self.mock_get_positions.call_args[0][1:]

        self.assertEqual(call_position, piece_position)
        self.assertSetEqual(set(call_directions), set(Diagonal))

    def test_should_return_empty_list_if_there_are_no_positions(self):
        self.mock_get_positions.return_value = {}
        self.board.get_positions_in_direction = self.mock_get_positions

        bishop = Bishop(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)

        self.assertEqual(bishop.generate_moves(self.board), [])

    def test_should_stop_at_first_enemy_and_add_it(self):
        positions = {
            Diagonal.UP_RIGHT: [
                Position(Rank.TWO, File.B),
                Position(Rank.THREE, File.C),
                Position(Rank.FOUR, File.D),
            ]
        }

        self.board.is_in_bounds = MagicMock(side_effect=[True, True, True])
        self.board.is_empty = MagicMock(side_effect=[True, False])
        self.board.are_enemies = MagicMock(return_value=True)

        self.board.get_positions_in_direction = MagicMock(return_value=positions)

        bishop = Bishop(FigureColor.WHITE, rank=Rank.ONE, file=File.A)

        positions = bishop.generate_moves(self.board)

        self.assertSetEqual(set(positions), {
            Position(Rank.TWO, File.B),
            Position(Rank.THREE, File.C),
        })

    def test_should_stop_at_first_friendly_and_not_add_it(self):
        positions = {
            Diagonal.UP_RIGHT: [
                Position(Rank.TWO, File.B),
                Position(Rank.THREE, File.C),
                Position(Rank.FOUR, File.D),
            ]
        }

        self.board.is_in_bounds = MagicMock(side_effect=[True, True, True])
        self.board.is_empty = MagicMock(side_effect=[True, False])
        self.board.are_enemies = MagicMock(return_value=False)

        self.board.get_positions_in_direction = MagicMock(return_value=positions)

        bishop = Bishop(FigureColor.WHITE, rank=Rank.ONE, file=File.A)

        positions = bishop.generate_moves(self.board)

        self.assertSetEqual(set(positions), {
            Position(Rank.TWO, File.B),
        })
