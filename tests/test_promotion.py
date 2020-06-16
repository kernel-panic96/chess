import unittest

from chess.board      import Board
from chess.position   import Position
from chess.constants  import Rank, File
from chess.constants  import FigureColor as Color


class PromotionTests(unittest.TestCase):
    def test_promotion_callback_should_be_called(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.P......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '.p......',  # 2
            '........'   # 1
        ])
        board.promotion_cb = unittest.mock.Mock()
        mock_piece = board.promotion_cb.return_value

        with self.subTest('white'):
            f, t = Position(Rank.SEVEN, File.B), Position(Rank.EIGHT, File.B)

            board.move(from_pos=f, to_pos=t)

            board.promotion_cb.assert_called_once()
            mock_piece.assert_called_once_with(Color.WHITE)

        board.promotion_cb.reset_mock()
        mock_piece = board.promotion_cb.return_value
        with self.subTest('black'):
            f, t = Position(Rank.TWO, File.B), Position(Rank.ONE, File.B)

            board.move(from_pos=f, to_pos=t)

            board.promotion_cb.assert_called_once()
            mock_piece.assert_called_once_with(Color.BLACK)

    def test_last_rank_should_be_with_changed_piece_type(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.P......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '........',  # 2
            '........'   # 1
        ])

        f, t = Position(Rank.SEVEN, File.B), Position(Rank.EIGHT, File.B)
        board.promotion_cb = unittest.mock.Mock()
        piece_cls_mock = board.promotion_cb.return_value

        board.move(from_pos=f, to_pos=t)
        self.assertEqual(board[t.rank][t.file], piece_cls_mock.return_value)
