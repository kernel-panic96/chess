import unittest

from constants import Rank, File, FigureColor, FigureType, Direction
from chess_pieces.pawn import Pawn
from position import Position
from board import Board


class TestPawnMoveGeneration(unittest.TestCase):
    def setUp(self):
        self.board = Board()

        self.file = File.B
        black_starting_rank, white_starting_rank = Rank.SEVEN, Rank.TWO

        self.white_pawn = Pawn(FigureColor.WHITE, rank=white_starting_rank, file=self.file)
        self.black_pawn = Pawn(FigureColor.BLACK, rank=black_starting_rank, file=self.file)

        self.board[self.white_pawn.rank][self.white_pawn.file] = self.white_pawn
        self.board[self.black_pawn.rank][self.black_pawn.file] = self.black_pawn

    def test_generate_moves_from_starting_square(self):
        self.assertSetEqual(set(self.white_pawn.generate_moves(self.board)), {
            Position(Rank.FOUR, self.white_pawn.file),
            Position(Rank.THREE, self.white_pawn.file),
        })

        self.assertSetEqual(set(self.black_pawn.generate_moves(self.board)), {
            Position(Rank.SIX, self.black_pawn.file),
            Position(Rank.FIVE, self.black_pawn.file),
        })

    def test_generate_moves_from_starting_square_when_two_ahead_is_blocked_by_friendly(self):
        self.arrangeBlockers(self.white_pawn, self.black_pawn)

        self.assertSetEqual(set(self.white_pawn.generate_moves(self.board)), {
            Position(self.white_pawn.rank + Direction.UP, self.white_pawn.file)
        })

        self.assertSetEqual(set(self.black_pawn.generate_moves(self.board)), {
            Position(self.black_pawn.rank + Direction.DOWN, self.black_pawn.file)
        })

    def test_generate_moves_from_starting_square_when_two_ahead_is_blocked_by_enemy(self):
        white_blocker, black_blocker = self.arrangeBlockers(self.white_pawn, self.black_pawn)
        white_blocker.color = FigureColor.BLACK
        black_blocker = FigureColor.WHITE

        self.assertSetEqual(set(self.white_pawn.generate_moves(self.board)), {
            Position(self.white_pawn.rank + Direction.UP, self.white_pawn.file)
        })

        self.assertSetEqual(set(self.black_pawn.generate_moves(self.board)), {
            Position(self.black_pawn.rank + Direction.DOWN, self.black_pawn.file)
        })

    def test_when_enemy_is_present_at_left_attack_square(self):
        whites_enemy, blacks_enemy = self.arrangeAttackers(self.white_pawn, self.black_pawn, Direction.LEFT)
        whites_enemy.color, blacks_enemy.color = (
            FigureColor.BLACK, FigureColor.WHITE
        )

        self.assertIn(Position(whites_enemy.rank, whites_enemy.file), self.white_pawn.generate_moves(self.board))

        self.assertIn(Position(blacks_enemy.rank, blacks_enemy.file), self.black_pawn.generate_moves(self.board))

    def test_when_friend_is_present_at_left_attack_square(self):
        whites_friend, blacks_friend = self.arrangeAttackers(self.white_pawn, self.black_pawn, Direction.LEFT)
        whites_friend.color, blacks_friend.color = (
            FigureColor.WHITE, FigureColor.BLACK
        )

        self.assertNotIn(Position(whites_friend.rank, whites_friend.file), self.white_pawn.generate_moves(self.board))

        self.assertNotIn(Position(blacks_friend.rank, blacks_friend.file), self.black_pawn.generate_moves(self.board))

    def test_when_enemy_is_present_at_right_attack_square(self):
        whites_enemy, blacks_enemy = self.arrangeAttackers(self.white_pawn, self.black_pawn, Direction.RIGHT)
        whites_enemy.color, blacks_enemy.color = (
            FigureColor.BLACK, FigureColor.WHITE
        )

        self.assertIn(Position(whites_enemy.rank, whites_enemy.file), self.white_pawn.generate_moves(self.board))

        self.assertIn(Position(blacks_enemy.rank, blacks_enemy.file), self.black_pawn.generate_moves(self.board))

    def test_when_friend_is_present_at_left_attack_square(self):
        whites_friend, blacks_friend = self.arrangeAttackers(self.white_pawn, self.black_pawn, Direction.RIGHT)
        whites_friend.color, blacks_friend.color = (
            FigureColor.WHITE, FigureColor.BLACK
        )

        self.assertNotIn(Position(whites_friend.rank, whites_friend.file), self.white_pawn.generate_moves(self.board))

        self.assertNotIn(Position(blacks_friend.rank, blacks_friend.file), self.black_pawn.generate_moves(self.board))

    def test_all_positions_should_be_present(self):
        l_whites_enemy, l_blacks_enemy = self.arrangeAttackers(self.white_pawn, self.black_pawn, Direction.LEFT)
        r_whites_enemy, r_blacks_enemy = self.arrangeAttackers(self.white_pawn, self.black_pawn, Direction.RIGHT)

        l_whites_enemy.color = r_whites_enemy.color = FigureColor.BLACK
        l_blacks_enemy.color = r_blacks_enemy.color = FigureColor.WHITE

        up, down, left, right = (
            Direction.UP, Direction.DOWN,
            Direction.LEFT, Direction.RIGHT
        )

        self.assertSetEqual(set(self.white_pawn.generate_moves(self.board)), {
            Position(self.white_pawn.rank + up, self.white_pawn.file),
            Position(self.white_pawn.rank + up + up, self.white_pawn.file),
            Position(self.white_pawn.rank + up, self.white_pawn.file + left),
            Position(self.white_pawn.rank + up, self.white_pawn.file + right),
        })

        self.assertSetEqual(set(self.black_pawn.generate_moves(self.board)), {
            Position(self.black_pawn.rank + down, self.black_pawn.file),
            Position(self.black_pawn.rank + down + down, self.black_pawn.file),
            Position(self.black_pawn.rank + down, self.black_pawn.file + left),
            Position(self.black_pawn.rank + down, self.black_pawn.file + right),
        })

    def arrangeBlockers(self, white_pawn, black_pawn):
        white_block_rank = self.white_pawn.rank + 2 * Direction.UP
        black_block_rank = self.black_pawn.rank + 2 * Direction.DOWN

        white_blocker = Pawn(FigureColor.WHITE, rank=white_block_rank, file=self.white_pawn.file)
        black_blocker = Pawn(FigureColor.BLACK, rank=white_block_rank, file=self.black_pawn.file)

        self.board[white_block_rank][self.white_pawn.file] = white_blocker
        self.board[black_block_rank][self.black_pawn.file] = black_blocker

        return white_blocker, black_blocker

    def arrangeAttackers(self, white_pawn, black_pawn, direction):
        w_enemy_rank = self.white_pawn.rank + Direction.UP
        b_enemy_rank = self.black_pawn.rank + Direction.DOWN

        whites_enemy = Pawn(FigureColor.BLACK, rank=w_enemy_rank, file=self.white_pawn.file + direction)
        blacks_enemy = Pawn(FigureColor.WHITE, rank=b_enemy_rank, file=self.black_pawn.file + direction)

        self.board[whites_enemy.rank][whites_enemy.file] = whites_enemy
        self.board[blacks_enemy.rank][blacks_enemy.file] = blacks_enemy

        return whites_enemy, blacks_enemy


class PawnHelpersTests(unittest.TestCase):
    def test_is_at_starting_rank_correctness(self):
        self.assertTrue(Pawn(FigureColor.WHITE, rank=Rank.TWO, file=File.G).is_at_starting_pos)
        self.assertTrue(Pawn(FigureColor.BLACK, rank=Rank.SEVEN, file=File.G).is_at_starting_pos)

        self.assertFalse(Pawn(FigureColor.BLACK, rank=Rank.TWO, file=File.G).is_at_starting_pos)
        self.assertFalse(Pawn(FigureColor.WHITE, rank=Rank.SEVEN, file=File.G).is_at_starting_pos)

    def test_is_white_correctness(self):
        self.assertTrue(Pawn(FigureColor.WHITE, rank=Rank.TWO, file=File.G).is_white)
        self.assertFalse(Pawn(FigureColor.BLACK, rank=Rank.TWO, file=File.G).is_white)

    def test_figure_type_class_attribute_is_pawn(self):
        self.assertEqual(Pawn.figure_type, FigureType.PAWN)
