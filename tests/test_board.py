import unittest

from board import Board
from constants import Rank, File, Direction, Diagonal
from position import Position


class BoardIteartionTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.default_start = Position(Rank.TWO, File.B)

    def test_iteratation_is_bounds_aware_to_the_left(self):
        self.assertSetEqual(
            set(self.board.get_positions_in_direction(self.default_start, Direction.LEFT)), {
            Position(Rank.TWO, File.A)
        })

    def test_iteration_is_bounds_aware_to_the_right(self):
        self.assertSetEqual(
            set(self.board.get_positions_in_direction(self.default_start, Direction.RIGHT)),
            {
                Position(Rank.TWO, File.C),
                Position(Rank.TWO, File.D),
                Position(Rank.TWO, File.E),
                Position(Rank.TWO, File.F),
                Position(Rank.TWO, File.G),
                Position(Rank.TWO, File.H),
            }
        )

    def test_iteration_is_bounds_aware_direction_up(self):
        self.assertSetEqual(
            set(self.board.get_positions_in_direction(self.default_start, Direction.UP)),
            {
                Position(Rank.THREE, File.B),
                Position(Rank.FOUR, File.B),
                Position(Rank.FIVE, File.B),
                Position(Rank.SIX, File.B),
                Position(Rank.SEVEN, File.B),
                Position(Rank.EIGHT, File.B),
            }
        )

    def test_iterations_is_bounds_aware_direction_down(self):
        self.assertSetEqual(
            set(self.board.get_positions_in_direction(self.default_start, Direction.DOWN)),
            {Position(Rank.ONE, File.B)}
        )

    def test_iteration_works_with_more_than_one_direction(self):
        dirs = self.board.get_positions_in_direction(self.default_start, Direction.DOWN, Direction.UP)

        positions_up = {
            Position(Rank.THREE, File.B),
            Position(Rank.FOUR, File.B),
            Position(Rank.FIVE, File.B),
            Position(Rank.SIX, File.B),
            Position(Rank.SEVEN, File.B),
            Position(Rank.EIGHT, File.B),
        }
        positions_down = {Position(Rank.ONE, File.B)}

        self.assertIn(Direction.UP, dirs)
        self.assertIn(Direction.DOWN, dirs)
        self.assertEqual(len(dirs), 2)

        self.assertSetEqual(
            set(dirs[Direction.UP]),
            positions_up
        )

        self.assertSetEqual(
            set(dirs[Direction.DOWN]),
            positions_down
        )

    def test_diagonals(self):

        with self.subTest('upper-right diagonal'):
            start_pos = Position(Rank.FOUR, File.D)

            positions = set(self.board.get_positions_in_direction(start_pos, Diagonal.UP_RIGHT))
            self.assertSetEqual(positions, {
                Position(Rank.FIVE, File.E),
                Position(Rank.SIX, File.F),
                Position(Rank.SEVEN, File.G),
                Position(Rank.EIGHT, File.H),
            })

        with self.subTest('upper-left diagonal'):
            start_pos = Position(Rank.FIVE, File.D)

            self.assertSetEqual(set(self.board.get_positions_in_direction(start_pos, Diagonal.UP_LEFT)), {
                Position(Rank.SIX, File.C),
                Position(Rank.SEVEN, File.B),
                Position(Rank.EIGHT, File.A),
            })

        # with self.subTest('down-right diagonal'):
        #     start_pos = Position(Rank.FOUR, File.E)

        #     self.assertSetEqual(set(self.board.get_positions_in_direction(start_pos, Diagonal.DOWN_RIGHT)), {
        #         Position(Rank.THREE, File.C),
        #         Position(Rank.TWO, File.B),
        #         Position(Rank.ONE, File.A),
        #     })


