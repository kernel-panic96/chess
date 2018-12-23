import unittest
from chess_pieces.king import King
from board import Board
from position import Position
from constants import FigureColor, Rank, File


class MoveGenerationTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_should_return_all_surrounding_squares_empty_board(self):
        king = King(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)
        self.board[king.rank][king.file] = king

        self.assertSetEqual(
            set(king.generate_moves(self.board)),
            {
                Position(Rank.THREE, File.C),
                Position(Rank.THREE, File.D),
                Position(Rank.THREE, File.E),
                Position(Rank.FOUR, File.E),
                Position(Rank.FIVE, File.E),
                Position(Rank.FIVE, File.D),
                Position(Rank.FIVE, File.C),
                Position(Rank.FOUR, File.C),
            }
        )

    def test_should_be_bounds_aware(self):
        with self.subTest('upper-right corner'):
            king = King(FigureColor.WHITE, rank=Rank.EIGHT, file=File.H)
            self.board[king.rank][king.file] = king

            self.assertSetEqual(
                set(king.generate_moves(self.board)),
                {
                    Position(Rank.EIGHT, File.G),
                    Position(Rank.SEVEN, File.G),
                    Position(Rank.SEVEN, File.H)
                }
            )
            self.board[king.rank][king.file] = None

        with self.subTest('upper-left corner'):
            king = King(FigureColor.WHITE, rank=Rank.EIGHT, file=File.A)
            self.board[king.rank][king.file] = king

            self.assertSetEqual(
                set(king.generate_moves(self.board)),
                {
                    Position(Rank.EIGHT, File.B),
                    Position(Rank.SEVEN, File.B),
                    Position(Rank.SEVEN, File.A)
                }
            )

            self.board[king.rank][king.file] = None

        with self.subTest('lower-left corner'):
            king = King(FigureColor.WHITE, rank=Rank.ONE, file=File.A)
            self.board[king.rank][king.file] = king

            self.assertSetEqual(
                set(king.generate_moves(self.board)),
                {
                    Position(Rank.ONE, File.B),
                    Position(Rank.TWO, File.B),
                    Position(Rank.TWO, File.A)
                }
            )
            self.board[king.rank][king.file] = None

        with self.subTest('lower-right corner'):
            king = King(FigureColor.WHITE, rank=Rank.ONE, file=File.H)
            self.board[king.rank][king.file] = king

            self.assertSetEqual(
                set(king.generate_moves(self.board)),
                {
                    Position(Rank.ONE, File.G),
                    Position(Rank.TWO, File.G),
                    Position(Rank.TWO, File.H)
                }
            )
            self.board[king.rank][king.file] = None

    def test_should_reject_friendly_piece_positions(self):
        king = King(FigureColor.WHITE, rank=Rank.FIVE, file=File.D)
        friendly = King(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)

        self.board[king.rank][king.file] = king
        self.board[Rank.FIVE][File.E] = \
            self.board[Rank.FIVE][File.C] = \
            self.board[Rank.FOUR][File.D] = \
            self.board[Rank.FOUR][File.E] = \
            self.board[Rank.FOUR][File.C] = \
            friendly

        self.assertSetEqual(set(king.generate_moves(self.board)), {
            Position(Rank.SIX, File.C),
            Position(Rank.SIX, File.D),
            Position(Rank.SIX, File.E),
        })

    def test_should_recognize_enemy_positions(self):
        king = King(FigureColor.WHITE, rank=Rank.FOUR, file=File.D)
        enemy = King(FigureColor.BLACK, rank=Rank.FIVE, file=File.D)

        self.board[king.rank][king.file] = king

        self.board[Rank.THREE][File.C] = \
            self.board[Rank.THREE][File.D] = \
            self.board[Rank.THREE][File.E] = \
            self.board[Rank.FOUR][File.C] = \
            self.board[Rank.FOUR][File.E] = \
            self.board[Rank.FIVE][File.C] = \
            self.board[Rank.FIVE][File.D] = \
            self.board[Rank.FIVE][File.E] = \
            enemy

        self.board[Rank.FIVE][File.D] = enemy

        positions = set(king.generate_moves(self.board))
        self.assertSetEqual(positions, {
            Position(Rank.THREE, File.C),
            Position(Rank.THREE, File.D),
            Position(Rank.THREE, File.E),
            Position(Rank.FOUR, File.C),
            Position(Rank.FOUR, File.E),
            Position(Rank.FIVE, File.C),
            Position(Rank.FIVE, File.D),
            Position(Rank.FIVE, File.E),
        })
