import unittest
from unittest.mock import MagicMock, patch, DEFAULT, call

from board import Board, OutOfBounds
from constants import Rank, File, Direction, Diagonal, FigureColor
from position import Position
from chess_pieces.all import *


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
        with patch('board.Board.empty') as mock_empty:
            board = Board()
            mock_empty.assert_called_once()


class StandardConfigurationCorrectnessTests(unittest.TestCase):
    def init_mocks(self):
        class_dependencies = ['Pawn', 'Rook', 'Bishop', 'King', 'Queen', 'Knight']
        patchers = [patch(f'board.pieces.{cls}') for cls in class_dependencies]

        for cls, patcher in zip(class_dependencies, patchers):
            setattr(self, f'{cls}Mock', patcher.start())

        self.addCleanup(patch.stopall)

    def setUp(self):
        self.init_mocks()
        self.board = Board.standard_configuration()

    def test_pawns_are_initialized_correctly(self):
        self.assertEqual(self.PawnMock.call_count, 16)

        with self.subTest('White pawns'):
            positions = [
                call(FigureColor.WHITE, rank=Rank.TWO, file=f) for f in File
            ]

            self.PawnMock.assert_has_calls(positions, any_order=True)
            self.assertTrue(all(square is self.PawnMock() for square in self.board[Rank.TWO][2:-2]))

        with self.subTest('Black pawns'):
            positions = [
                call(FigureColor.BLACK, rank=Rank.SEVEN, file=f) for f in File
            ]

            self.PawnMock.assert_has_calls(positions, any_order=True)
            self.assertTrue(all(square is self.PawnMock() for square in self.board[Rank.SEVEN][2:-2]))

    def test_rooks_are_initialized_correctly(self):
        self.assertEqual(self.RookMock.call_count, 4)

        with self.subTest('White rooks'):
            positions = [
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.A),
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.H)
            ]

            self.RookMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.A], self.RookMock())
            self.assertIs(self.board[Rank.ONE][File.H], self.RookMock())

        with self.subTest('Black Rooks'):
            positions = [
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.A),
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.H)
            ]

            self.RookMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.A], self.RookMock())
            self.assertIs(self.board[Rank.ONE][File.H], self.RookMock())

    def test_knights_are_initialized_correctly(self):
        self.assertEqual(self.KnightMock.call_count, 4)

        with self.subTest('White knights'):
            positions = [
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.G),
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.B)
            ]

            self.KnightMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.G], self.KnightMock())
            self.assertIs(self.board[Rank.ONE][File.B], self.KnightMock())

        with self.subTest('Black knights'):
            positions = [
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.G),
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.B),
            ]

            self.KnightMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.G], self.KnightMock())
            self.assertIs(self.board[Rank.EIGHT][File.B], self.KnightMock())

    def test_bishops_are_initialized_correctly(self):
        self.assertEqual(self.BishopMock.call_count, 4)

        with self.subTest('White bishops'):
            positions = [
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.C),
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.F),
            ]
            self.BishopMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.C], self.BishopMock())
            self.assertIs(self.board[Rank.ONE][File.F], self.BishopMock())

        with self.subTest('Black bishops'):
            positions = [
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.C),
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.F),
            ]

            self.BishopMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.C], self.BishopMock())
            self.assertIs(self.board[Rank.EIGHT][File.F], self.BishopMock())

    def test_queens_are_initiailized_correctly(self):
        self.assertEqual(self.QueenMock.call_count, 2)

        with self.subTest('White queens'):
            positions = [call(FigureColor.WHITE, rank=Rank.ONE, file=File.D)]

            self.QueenMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.D], self.QueenMock())

        with self.subTest('Black queens'):
            positions = [call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.D)]

            self.QueenMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.D], self.QueenMock())

    def test_kings_are_initialized_correctly(self):
        self.assertEqual(self.KingMock.call_count, 2)

        with self.subTest('White king'):
            positions = [
                call(FigureColor.WHITE, rank=Rank.ONE, file=File.E)
            ]

            self.KingMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.ONE][File.E], self.KingMock())

        with self.subTest('Black king'):
            positions = [
                call(FigureColor.BLACK, rank=Rank.EIGHT, file=File.E)
            ]

            self.KingMock.assert_has_calls(positions, any_order=True)
            self.assertIs(self.board[Rank.EIGHT][File.E], self.KingMock())


class BoardIterationTests(unittest.TestCase):
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
