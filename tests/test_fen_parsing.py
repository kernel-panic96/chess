import unittest

from chess.board import Board
from chess.constants import Rank, File
from chess.constants import FigureColor as Color
from chess.constants import CastlingPerm
from chess.position import Position
from chess.pieces import *

P = Position.from_str


class TestFENParsing(unittest.TestCase):
    def test_starting_configuration_should_be_equivalent_to_standard_configuration(self):
        board = Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        std = Board.standard_configuration()

        with self.subTest('figure_types_should_match'):
            ref_projection = [
                [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],
                [Pawn] * 8,
                [type(None)] * 8,
                [type(None)] * 8,
                [type(None)] * 8,
                [type(None)] * 8,
                [Pawn] * 8,
                [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],
            ]

            for i in range(8):
                board_projection = board.projection
                std_projection = std.projection

                self.assertEqual(
                    [type(x) for x in board_projection[i]],
                    [type(x) for x in std_projection[i]],
                    f'row {i}'
                )
                self.assertEqual(
                    [x for x in ref_projection[i]],
                    [type(x) for x in std_projection[i]],
                    f'row {i}'
                )

        with self.subTest('colors_should_match'):
            ref_projection = [
                [Color.BLACK] * 8,
                [Color.BLACK] * 8,
                [None] * 8,
                [None] * 8,
                [None] * 8,
                [None] * 8,
                [Color.WHITE] * 8,
                [Color.WHITE] * 8,
            ]

            for i in range(8):
                self.assertEqual(
                    [getattr(x, 'color', None) for x in board_projection[i]],
                    [getattr(x, 'color', None) for x in std_projection[i]],
                    f'row {i}'
                )
                self.assertEqual(
                    [x for x in ref_projection[i]],
                    [getattr(x, 'color', None) for x in std_projection[i]],
                    f'row {i}'
                )

        with self.subTest('active side should be white'):
            self.assertEqual(board.player, Color.WHITE)
            self.assertEqual(board.enemy, Color.BLACK)

        with self.subTest('white castling perms should be correct'):
            self.assertTrue(
                board.castling_perms[Color.WHITE] & (CastlingPerm.KING_SIDE),
                'white should be able to castle king side'
            )
            self.assertTrue(
                board.castling_perms[Color.WHITE] & (CastlingPerm.QUEEN_SIDE),
                'white should be able to castle king side'
            )

        with self.subTest('black castling perms should be correct'):
            self.assertTrue(
                board.castling_perms[Color.BLACK] & (CastlingPerm.KING_SIDE),
                'white should be able to castle king side'
            )
            self.assertTrue(
                board.castling_perms[Color.BLACK] & (CastlingPerm.QUEEN_SIDE),
                'white should be able to castle king side'
            )

        with self.subTest('en passant square should be empty'):
            self.assertIsNone(board.en_passant_pos)

    def test_fen_empty_positions_are_parsed_correctly(self):
        board = Board.from_fen('3k4/2p5/8/8/8/8/6n1/1k6 w KQkq - 0 1').projection

        self.assertEqual(
            [type(None)] * 3 + [King] + [type(None)] * 4,
            [type(x) for x in board[0]],
        )
        self.assertEqual(
            [type(None)] * 2 + [Pawn] + [type(None)] * 5,
            [type(x) for x in board[1]],
        )
        self.assertEqual(
            [type(None)] * 6 + [Knight] + [type(None)] * 1,
            [type(x) for x in board[-2]],
        )
        self.assertEqual(
            [type(None)] * 1 + [King] + [type(None)] * 6,
            [type(x) for x in board[-1]],
        )

    def test_fen_castling_permissions(self):
        with self.subTest('white should have no permissions and black should have both'):
            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w --kq - 0 1').castling_perms[Color.WHITE],
                0,
            )
            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w --kq - 0 1').castling_perms[Color.BLACK],
                CastlingPerm.KING_SIDE | CastlingPerm.QUEEN_SIDE,
            )

        with self.subTest('black should have no permissions and white should have both'):
            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ-- - 0 1').castling_perms[Color.BLACK],
                0,
            )
            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ-- - 0 1').castling_perms[Color.WHITE],
                CastlingPerm.KING_SIDE | CastlingPerm.QUEEN_SIDE,
            )

        with self.subTest('both colors should have only queen side permission'):
            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w -Q-q - 0 1').castling_perms[Color.BLACK],
                CastlingPerm.QUEEN_SIDE,
            )

            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w -Q-q - 0 1').castling_perms[Color.WHITE],
                CastlingPerm.QUEEN_SIDE,
            )

        with self.subTest('both colors should have only king side permission'):
    
            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w K-k- - 0 1').castling_perms[Color.BLACK],
                CastlingPerm.KING_SIDE,
            )

            self.assertEqual(
                Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w K-k- - 0 1').castling_perms[Color.WHITE],
                CastlingPerm.KING_SIDE,
            )

    def test_en_passant(self):
        board = Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq A1 0 1')
        self.assertEqual(board.en_passant_pos, P('a1'))

        board = Board.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq h8 0 1')
        self.assertEqual(board.en_passant_pos, P('h8'))

    def test_active_side(self):
        with self.subTest('should be white'):
            board = Board.from_fen('8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1')
            self.assertEqual(board.player, Color.WHITE)
            self.assertEqual(board.enemy, Color.BLACK)

        with self.subTest('should be black'):
            board = Board.from_fen('8/8/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 0 1')
            self.assertEqual(board.player, Color.BLACK)
            self.assertEqual(board.enemy, Color.WHITE)
    
    @unittest.skipIf(not hasattr(Board(), 'half_move'), 'half move clock not yet supported')
    def test_half_move_clock(self):
        board = Board.from_fen('8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1')
        self.assertEqual(getattr(board, 'half_move'), 0)

        board = Board.from_fen('8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 12 1')
        self.assertEqual(getattr(board, 'half_move'), 12)

        self.assertTrue(False, 'Refactor this test')  # the getattr with direct attribute access

    @unittest.skipIf(not hasattr(Board(), 'full_move'), 'full move count not yet supported')
    def test_full_move_clock(self):
        board = Board.from_fen('8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1')
        self.assertEqual(getattr(board, 'full_move'), 1)

        board = Board.from_fen('8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 42')
        self.assertEqual(getattr(board, 'full_move'), 42)

        self.assertTrue(False, 'Refactor this test')  # the getattr with direct attribute access