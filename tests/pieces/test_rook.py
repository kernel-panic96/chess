import unittest
from unittest.mock import MagicMock

from board             import Board
from chess_pieces.rook import Rook
from constants         import Direction
from constants         import FigureColor as Color, FigureType as Type
from constants         import Rank, File
from position          import Position

from tests import MoveGenerationTestCase

from functional import seq


class RookMoveTests(MoveGenerationTestCase):
    def test_board_constructor_works_for_rooks(self):
        board = Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.r......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.R......',  # 2
                    '........'   # 1
                ])
        self.assertEqual(board[Rank.TWO][File.B].type, Type.ROOK)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.ROOK)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_move_generation(self):
        test_table = [
            *self.all_board_rotations_of({
                'name': 'should_have_two_straights_available',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'R.......'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.A): set.union(
                            set(map(lambda dy: (dy, 0), range(8)[1:])),
                            set(map(lambda dx: (0, dx), range(8)[1:])),
                        )
                    },
                    'black': {
                        Position(Rank.EIGHT, File.H): set.union(
                            set(map(lambda dy: (-dy, 0), range(8)[1:])),
                            set(map(lambda dx: (0, -dx), range(8)[1:])),
                        )
                    },
                }
            }),
            *self.all_board_rotations_of({
                'name': 'should_not_go_over_pieces',
                'board': Board.from_strings([
                    # bcdefgh
                    '....r..r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '.......r',  # 5
                    'R.......',  # 4
                    '........',  # 3
                    '........',  # 2
                    'R..R....'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.A): set.union(
                            set(map(lambda dy: (dy, 0), range(1, 3))),
                            set(map(lambda dx: (0, dx), range(1, 3))),
                        )
                    },
                    'black': {
                        Position(Rank.EIGHT, File.H): set.union(
                            set(map(lambda dy: (-dy, 0), range(1, 3))),
                            set(map(lambda dx: (0, -dx), range(1, 3))),
                        )
                    }
                }
            }),
            {
                'name': 'should_recognize_enemies',
                'board': Board.from_strings([
                    # bcdefgh
                    '.....R.r',  # 8
                    '........',  # 7
                    '.......R',  # 6
                    '........',  # 5
                    '........',  # 4
                    'r.......',  # 3
                    '........',  # 2
                    'R.r.....'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.A): set.union(
                            set(map(lambda dy: (dy, 0), range(1, 3))),
                            set(map(lambda dx: (0, dx), range(1, 3))),
                        )
                    },
                    'black': {
                        Position(Rank.EIGHT, File.H): set.union(
                            set(map(lambda dy: (-dy, 0), range(1, 3))),
                            set(map(lambda dx: (0, -dx), range(1, 3))),
                        )
                    }
                }
            }
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)

    def setUp(self):
        self.board = MagicMock()
        self.mock_get_positions = MagicMock()

    def test_should_stop_at_first_enemy_and_add_it(self):
        positions = {
            Direction.UP: [
                Position(Rank.FOUR, File.C),
                Position(Rank.FOUR, File.B)
            ]
        }

        self.board.is_in_bounds = MagicMock(side_effect=[True, True, True])
        self.board.is_empty = MagicMock(side_effect=[True, False])
        self.board.are_enemies = MagicMock(return_value=True)

        self.board.get_positions_in_direction = MagicMock(return_value=positions)

        rook_pos = Position(Rank.FOUR, File.D)
        rook = Rook(Color.WHITE)

        positions = rook.generate_moves(self.board, rook_pos)

        self.assertSetEqual(set(positions), {
            Position(Rank.FOUR, File.C),
            Position(Rank.FOUR, File.B),
        })

    def test_should_stop_at_first_friendly_and_not_add_it(self):
        positions = {
            Direction.UP: [
                Position(Rank.FOUR, File.C),
                Position(Rank.FOUR, File.B)
            ]
        }

        self.board.is_in_bounds = MagicMock(side_effect=[True, True, True])
        self.board.is_empty = MagicMock(side_effect=[True, False])
        self.board.are_enemies = MagicMock(return_value=False)

        self.board.get_positions_in_direction = MagicMock(return_value=positions)

        rook_pos = Position(Rank.FOUR, File.D)
        rook = Rook(Color.WHITE)

        positions = rook.generate_moves(self.board, rook_pos)

        self.assertSetEqual(set(positions), {
            Position(Rank.FOUR, File.C),
        })
