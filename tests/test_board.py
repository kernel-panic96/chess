import itertools
import unittest
from unittest.mock import (
    MagicMock, patch,
    DEFAULT, call,
    PropertyMock
)

from chess.board import Board, OutOfBounds
from chess.constants import (
    Rank, File,
    Direction, Diagonal,
    FigureColor, FigureType
)
from chess.position import Position
from chess.pieces import *


class PropertyTests(unittest.TestCase):
    def test_empty_configuration(self):
        board = Board.empty()

        expected = [
            [OutOfBounds] * 12,
            [OutOfBounds] * 12,
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds, OutOfBounds, None, None, None, None, None, None, None, None, OutOfBounds, OutOfBounds],
            [OutOfBounds] * 12,
            [OutOfBounds] * 12,
        ]

        self.assertEqual(board, expected)

    def test_empty_ctor_calls_board_empty(self):
        with patch('chess.board.Board.empty') as mock_empty:
            board = Board()
            mock_empty.assert_called_once()


class StandardConfigurationCorrectnessTests(unittest.TestCase):
    def init_mocks(self):
        class_dependencies = ['Pawn', 'Rook', 'Bishop', 'King', 'Queen', 'Knight']
        patchers = [patch(f'chess.board.{cls}') for cls in class_dependencies]

        for cls, patcher in zip(class_dependencies, patchers):
            setattr(self, f'{cls}Mock', patcher.start())

        self.addCleanup(patch.stopall)

    def setUp(self):
        self.init_mocks()
        self.board = Board.standard_configuration()

    def test_pawns_are_initialized_correctly(self):
        self.assertEqual(self.PawnMock.call_count, 16)

        with self.subTest('White pawns'):
            ctor_calls = [
                call(FigureColor.WHITE) for f in File
            ]

            self.PawnMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertTrue(all(square is self.PawnMock() for square in self.board[Rank.TWO][2:-2]))

        with self.subTest('Black pawns'):
            positions = [
                call(FigureColor.BLACK) for f in File
            ]

            self.PawnMock.assert_has_calls(positions, any_order=True)
            self.assertTrue(all(square is self.PawnMock() for square in self.board[Rank.SEVEN][2:-2]))

    def test_rooks_are_initialized_correctly(self):
        self.assertEqual(self.RookMock.call_count, 4)

        with self.subTest('White rooks'):
            ctor_calls = [
                call(FigureColor.WHITE),
                call(FigureColor.WHITE)
            ]

            self.RookMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.A], self.RookMock())
            self.assertIs(self.board[Rank.ONE][File.H], self.RookMock())

        with self.subTest('Black Rooks'):
            ctor_calls = [
                call(FigureColor.BLACK),
                call(FigureColor.BLACK)
            ]

            self.RookMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.A], self.RookMock())
            self.assertIs(self.board[Rank.ONE][File.H], self.RookMock())

    def test_knights_are_initialized_correctly(self):
        self.assertEqual(self.KnightMock.call_count, 4)

        with self.subTest('White knights'):
            ctor_calls = [
                call(FigureColor.WHITE),
                call(FigureColor.WHITE)
            ]

            self.KnightMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.G], self.KnightMock())
            self.assertIs(self.board[Rank.ONE][File.B], self.KnightMock())

        with self.subTest('Black knights'):
            ctor_calls = [
                call(FigureColor.BLACK),
                call(FigureColor.BLACK),
            ]

            self.KnightMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.G], self.KnightMock())
            self.assertIs(self.board[Rank.EIGHT][File.B], self.KnightMock())

    def test_bishops_are_initialized_correctly(self):
        self.assertEqual(self.BishopMock.call_count, 4)

        with self.subTest('White bishops'):
            ctor_calls = [
                call(FigureColor.WHITE),
                call(FigureColor.WHITE),
            ]
            self.BishopMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.C], self.BishopMock())
            self.assertIs(self.board[Rank.ONE][File.F], self.BishopMock())

        with self.subTest('Black bishops'):
            ctor_calls = [
                call(FigureColor.BLACK),
                call(FigureColor.BLACK),
            ]

            self.BishopMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.C], self.BishopMock())
            self.assertIs(self.board[Rank.EIGHT][File.F], self.BishopMock())

    def test_queens_are_initiailized_correctly(self):
        self.assertEqual(self.QueenMock.call_count, 2)

        with self.subTest('White queens'):
            ctor_calls = [call(FigureColor.WHITE)]

            self.QueenMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.D], self.QueenMock())

        with self.subTest('Black queens'):
            ctor_calls = [call(FigureColor.BLACK)]

            self.QueenMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.D], self.QueenMock())

    def test_kings_are_initialized_correctly(self):
        self.assertEqual(self.KingMock.call_count, 2)

        with self.subTest('White king'):
            ctor_calls = [call(FigureColor.WHITE)]

            self.KingMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.E], self.KingMock())

        with self.subTest('Black king'):
            ctor_calls = [call(FigureColor.BLACK)]

            self.KingMock.assert_has_calls(ctor_calls, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.E], self.KingMock())


class BoardIterationTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.default_start = Position(Rank.TWO, File.B)

    def test_iteratation_is_bounds_aware_to_the_left(self):
        self.assertSetEqual(
            set(self.board.get_positions_in_direction(self.default_start, Direction.LEFT)),
            {
                Position(Rank.TWO, File.A)
            }
        )

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

        with self.subTest('down-right diagonal'):
            start_pos = Position(Rank.FOUR, File.E)

            self.assertSetEqual(set(self.board.get_positions_in_direction(start_pos, Diagonal.DOWN_RIGHT)), {
                Position(Rank.THREE, File.F),
                Position(Rank.TWO, File.G),
                Position(Rank.ONE, File.H),
            })

        with self.subTest('down-left diagonal'):
            start_pos = Position(Rank.FOUR, File.D)

            self.assertSetEqual(set(self.board.get_positions_in_direction(start_pos, Diagonal.DOWN_LEFT)), {
                Position(Rank.THREE, File.C),
                Position(Rank.TWO, File.B),
                Position(Rank.ONE, File.A),
            })


class UtilMethods(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_are_enemies_should_be_affirmative(self):
        with self.subTest('Positional arguments are both Position instances'):
            piece1_pos = Position(Rank.ONE, File.A)
            piece2_pos = Position(Rank.ONE, File.B)

            self.board[piece1_pos.rank][piece1_pos.file] = MagicMock(color=FigureColor.BLACK)
            self.board[piece2_pos.rank][piece2_pos.file] = MagicMock(color=FigureColor.WHITE)

            self.assertTrue(self.board.are_enemies(piece1_pos, piece2_pos))
            self.assertTrue(self.board.are_enemies(piece2_pos, piece1_pos))

        with self.subTest('Type of first positional argument is FigureColor'):
            piece_pos = Position(Rank.ONE, File.A)

            self.board[piece_pos.rank][piece_pos.file] = MagicMock(color=FigureColor.BLACK)

            self.assertTrue(self.board.are_enemies(FigureColor.WHITE, piece_pos))

    def test_are_enemies_should_be_negative(self):
        piece1_pos = Position(Rank.ONE, File.A)
        piece2_pos = Position(Rank.ONE, File.B)
        piece1_mock = MagicMock()
        piece2_mock = MagicMock()
        self.board[piece1_pos.rank][piece1_pos.file] = piece1_mock
        self.board[piece2_pos.rank][piece2_pos.file] = piece2_mock

        with self.subTest('Positional arguments are both Position instances'):
            with self.subTest('Both are white'):
                piece1_mock.color = piece2_mock.color = FigureColor.WHITE
                self.assertFalse(self.board.are_enemies(piece1_pos, piece2_pos))
            with self.subTest('Both are black'):
                piece1_mock.color = piece2_mock.color = FigureColor.BLACK
                self.assertFalse(self.board.are_enemies(piece1_pos, piece2_pos))

        with self.subTest('Type of first positional argument is FigureColor'):
            with self.subTest('Both are white'):
                piece1_mock.color = FigureColor.WHITE
                self.assertFalse(self.board.are_enemies(FigureColor.WHITE, piece1_pos))
            with self.subTest('Both are black'):
                piece1_mock.color = FigureColor.BLACK
                self.assertFalse(self.board.are_enemies(FigureColor.BLACK, piece1_pos))


class EnemyDetectionTests(unittest.TestCase):
    SHOULD_DETECT_ALL = True
    SHOULD_DETECT_NONE = False

    def setUp(self):
        self.white_piece = MagicMock()
        self.black_piece = MagicMock()

        self.white_piece_board = Board()
        self.black_piece_board = Board()

        self.white_piece_board.get_positions_in_direction = MagicMock()
        self.black_piece_board.get_positions_in_direction = MagicMock()

        self.origin = Position(Rank.FOUR, File.D)

        self.diagonal_attack_positions = {
            Position(self.origin.rank + 2, self.origin.file + 2),
            Position(self.origin.rank + 2, self.origin.file - 2),
            Position(self.origin.rank - 2, self.origin.file + 2),
            Position(self.origin.rank - 2, self.origin.file - 2),
        }

        self.straights_attack_positions = {
            Position(self.origin.rank + Direction.UP * 2, self.origin.file),
            Position(self.origin.rank + Direction.DOWN * 2, self.origin.file),
            Position(self.origin.rank, self.origin.file + Direction.LEFT * 2),
            Position(self.origin.rank, self.origin.file + Direction.RIGHT * 2),
        }

        all_positions = itertools.chain(
            self.diagonal_attack_positions,
            self.straights_attack_positions,
        )

    def assertEnemyDetection(self, should_contain_all, directions, piece_types, attack_positions):
        type(self.black_piece).figure_type = PropertyMock(return_value=piece_types)
        type(self.white_piece).figure_type = PropertyMock(return_value=piece_types)

        for pos in attack_positions:
            self.white_piece_board[pos.rank][pos.file] = self.black_piece
            self.black_piece_board[pos.rank][pos.file] = self.white_piece

        positions = list(map(lambda pos: [pos], attack_positions))
        positions = dict(zip(directions, positions))

        self.black_piece_board.get_positions_in_direction.return_value = positions
        self.white_piece_board.get_positions_in_direction.return_value = positions

        self.assertSetEqual(
            set(self.white_piece_board.get_attackers(self.origin, FigureColor.WHITE)),
            attack_positions if should_contain_all else set()
        )

        self.assertSetEqual(
            set(self.black_piece_board.get_attackers(self.origin, FigureColor.BLACK)),
            attack_positions if should_contain_all else set()
        )

    def test_diagonals_with_bishops_and_queens(self):
        types = [FigureType.QUEEN, FigureType.BISHOP]

        for p_type in types:
            with self.subTest(p_type.name.capitalize()):
                self.assertEnemyDetection(
                    self.SHOULD_DETECT_ALL,
                    directions=Diagonal,
                    piece_types=p_type,
                    attack_positions=self.diagonal_attack_positions
                )

    def test_diagonals_with_pieces_which_cannot_slide_diagonally(self):
        types = [FigureType.ROOK, FigureType.KING, FigureType.PAWN, FigureType.KNIGHT]

        for p_type in types:
            with self.subTest(p_type.name.capitalize()):
                self.assertEnemyDetection(
                    self.SHOULD_DETECT_NONE,
                    directions=Diagonal,
                    piece_types=p_type,
                    attack_positions=self.diagonal_attack_positions
                )

    def test_straights_with_rooks_and_queens(self):
        types = [FigureType.ROOK, FigureType.QUEEN]

        for piece_type in types:
            with self.subTest(piece_type.name.capitalize()):
                self.assertEnemyDetection(
                    self.SHOULD_DETECT_ALL,
                    directions=list(Direction),
                    piece_types=piece_type,
                    attack_positions=self.straights_attack_positions,
                )

    def test_straights_with_pieces_which_cannot_slide_straight(self):
        for piece in [FigureType.BISHOP, FigureType.KNIGHT, FigureType.PAWN, FigureType.KING]:
            with self.subTest(piece.name.capitalize()):
                self.assertEnemyDetection(
                    self.SHOULD_DETECT_NONE,
                    directions=list(Direction),
                    piece_types=piece,
                    attack_positions=self.straights_attack_positions,
                )

    def test_detects_king_attacks(self):
        attack_positions = {
            Position(rank=self.origin.rank - 1, file=self.origin.file + 1),
            Position(rank=self.origin.rank,     file=self.origin.file + 1),
            Position(rank=self.origin.rank + 1, file=self.origin.file + 1),
            Position(rank=self.origin.rank + 1, file=self.origin.file),
            Position(rank=self.origin.rank - 1, file=self.origin.file - 1),
            Position(rank=self.origin.rank,     file=self.origin.file - 1),
            Position(rank=self.origin.rank - 1, file=self.origin.file - 1),
            Position(rank=self.origin.rank - 1, file=self.origin.file),
        }

        self.assertEnemyDetection(
            self.SHOULD_DETECT_ALL,
            directions=list(Direction) + list(Diagonal),
            piece_types=FigureType.KING,
            attack_positions=attack_positions
        )
