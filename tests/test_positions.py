import unittest

from chess.constants import Rank, File
from chess.position import Position


class PositionTests(unittest.TestCase):
    def test_attributes_are_correct_after_construction(self):
        pos = Position(Rank.FOUR, File.D)

        self.assertEqual(pos.rank, Rank.FOUR)
        self.assertEqual(pos.file, File.D)

    def test_from_str_equal_as_with_normal_init(self):
        self.assertEqual(
            Position(Rank.ONE, File.A),
            Position.from_str('A1')
        )

        self.assertEqual(
            Position(Rank.TWO, File.H),
            Position.from_str('H2')
        )

        self.assertEqual(
            Position(Rank.EIGHT, File.H),
            Position.from_str('H8')
        )

    def test_coordinates_correctness(self):
        self.assertEqual(Position(Rank.EIGHT, File.H).coordinates, (0, 7))
        self.assertEqual(Position(Rank.ONE, File.A).coordinates, (7, 0))
        self.assertEqual(Position(Rank.EIGHT, File.A).coordinates, (0, 0))
        self.assertEqual(Position(Rank.FOUR, File.D).coordinates, (4, 3))
        self.assertEqual(Position(Rank.ONE, File.H).coordinates, (7, 7))

    def test_distance(self):
        h8 = Position(Rank.EIGHT, File.H)
        h7 = Position(Rank.SEVEN, File.H)
        h1 = Position(Rank.ONE, File.H)
        a8 = Position(Rank.EIGHT, File.A)
        a1 = Position(Rank.ONE, File.A)

        self.assertEqual(h8.dist(h7), 1)
        self.assertEqual(h8.dist(h1), 7)
        self.assertEqual(h8.dist(a8), 7)
        self.assertEqual(a8.dist(h8), 7)

        self.assertEqual(a1.dist(h8), 7)

    def test_hash_values(self):
        h8_1 = Position(Rank.EIGHT, File.H)
        h8_2 = Position(Rank.EIGHT, File.H)

        a1_1 = Position(Rank.ONE, File.A)
        a1_2 = Position(Rank.ONE, File.A)

        self.assertEqual(h8_1, h8_2)
        self.assertEqual(a1_1, a1_2)

        self.assertEqual(hash(h8_1), hash(h8_2))
        self.assertEqual(hash(a1_1), hash(a1_2))
