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


class PropertyTests(unittest.TestCase):
    def test_empty_configuration(self):
        board = Board()

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

        for i, (rank, expected_rank) in enumerate(zip(board, expected)):
            for j, (file, expected_file) in enumerate(zip(rank, expected_rank)):
                self.assertEqual(file, expected_file, msg=f'at index [{i}][{j}]')

    def test_empty_ctor_calls_board_empty(self):
        with patch('chess.board.Board.empty') as mock_empty:
            Board()
            mock_empty.assert_called_once()

    def test_next_turn_swaps_players(self):
        board = Board()
        p1, p2 = board.player, board.enemy
        board.next_turn()

        self.assertEqual((p2, p1), (board.player, board.enemy))

class StandardConfigurationCorrectnessTests(unittest.TestCase):  # pylint: disable=no-member
    def init_mocks(self):
        class_dependencies = ['Pawn', 'Rook', 'Bishop', 'King', 'Queen', 'Knight']
        patchers = [patch(f'chess.board.{cls}') for cls in class_dependencies]

        for cls, patcher in zip(class_dependencies, patchers):
            setattr(self, f'{cls}', patcher.start())

        self.addCleanup(patch.stopall)

    def test_pieces_are_initialized_correctly(self):
        self.init_mocks()
        # HACK: workaround false-positive linting issues - pylint no-member
        PawnMock = getattr(self, 'Pawn')
        RookMock = getattr(self, 'Rook')
        KingMock = getattr(self, 'King')
        BishopMock = getattr(self, 'Bishop')
        KnightMock = getattr(self, 'Knight')
        QueenMock = getattr(self, 'Queen')

        board = Board.standard_configuration()

        with self.subTest('pawns'):
            self.assertEqual(PawnMock.call_count, 16)

            with self.subTest('white'):
                ctor_calls = [
                    call(FigureColor.WHITE) for f in File
                ]

                PawnMock.assert_has_calls(ctor_calls, any_order=True)  # pylint: disable=no-member
                self.assertTrue(all(square is PawnMock() for square in board[Rank.TWO][2:-2]))  # pylint: disable=no-member

            with self.subTest('black'):
                positions = [
                    call(FigureColor.BLACK) for f in File
                ]

                PawnMock.assert_has_calls(positions, any_order=True)
                self.assertTrue(all(square is PawnMock() for square in board[Rank.SEVEN][2:-2]))

        with self.subTest('rooks'):
            self.assertEqual(RookMock.call_count, 4)

            with self.subTest('white'):
                ctor_calls = [
                    call(FigureColor.WHITE),
                    call(FigureColor.WHITE)
                ]

                RookMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.ONE][File.A], RookMock())
                self.assertIs(board[Rank.ONE][File.H], RookMock())

            with self.subTest('black'):
                ctor_calls = [
                    call(FigureColor.BLACK),
                    call(FigureColor.BLACK)
                ]

                RookMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.ONE][File.A], RookMock())
                self.assertIs(board[Rank.ONE][File.H], RookMock())

        with self.subTest('knights'):
            self.assertEqual(KnightMock.call_count, 4)

            with self.subTest('white'):
                ctor_calls = [
                    call(FigureColor.WHITE),
                    call(FigureColor.WHITE)
                ]

                KnightMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.ONE][File.G], KnightMock())
                self.assertIs(board[Rank.ONE][File.B], KnightMock())

            with self.subTest('black'):
                ctor_calls = [
                    call(FigureColor.BLACK),
                    call(FigureColor.BLACK),
                ]

                KnightMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.EIGHT][File.G], KnightMock())
                self.assertIs(board[Rank.EIGHT][File.B], KnightMock())

        with self.subTest('bishoops'):
            self.assertEqual(BishopMock.call_count, 4)

            with self.subTest('white'):
                ctor_calls = [
                    call(FigureColor.WHITE),
                    call(FigureColor.WHITE),
                ]
                BishopMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.ONE][File.C], BishopMock())
                self.assertIs(board[Rank.ONE][File.F], BishopMock())

            with self.subTest('black'):
                ctor_calls = [
                    call(FigureColor.BLACK),
                    call(FigureColor.BLACK),
                ]

                BishopMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.EIGHT][File.C], BishopMock())
                self.assertIs(board[Rank.EIGHT][File.F], BishopMock())

        with self.subTest('queens'):
            self.assertEqual(QueenMock.call_count, 2)

            with self.subTest('white'):
                ctor_calls = [call(FigureColor.WHITE)]

                QueenMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.ONE][File.D], QueenMock())

            with self.subTest('black'):
                ctor_calls = [call(FigureColor.BLACK)]

                QueenMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.EIGHT][File.D], QueenMock())

        with self.subTest('kings'):
            self.assertEqual(KingMock.call_count, 2)

            with self.subTest('white'):
                ctor_calls = [call(FigureColor.WHITE)]

                KingMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.ONE][File.E], KingMock())

            with self.subTest('black'):
                ctor_calls = [call(FigureColor.BLACK)]

                KingMock.assert_has_calls(ctor_calls, any_order=True)
                self.assertIs(board[Rank.EIGHT][File.E], KingMock())


class TestGetPositionsInDirection(unittest.TestCase):
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