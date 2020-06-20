from tests import MoveGenerationTestCase, target_board

from chess.pieces.king import King
from chess.board import Board
from chess.position import Position
from chess.constants import FigureType as Type, FigureColor as Color
from chess.constants import Rank, File

from functional import seq


class MoveGenerationTests(MoveGenerationTestCase):
    def test_board_constructor_works_for_kings(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.k......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '.K......',  # 2
            '........'   # 1
        ])
        self.assertEqual(board[Rank.TWO][File.B].type, Type.KING)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.KING)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_move_generation(self):
        test_table = [
            { 'name': 'clear_board_should_have_all_surrounding_positions',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '.k......',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        'xxx.....',  # 3
                        'xTx.....',  # 2
                        'xxx.....'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        'xxx.....',  # 8
                        'xTx.....',  # 7
                        'xxx.....',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '.K......',  # 2
                        '........'   # 1
                    ]),
                }
            },
            *self.all_board_rotations_of({ 'name': 'should_be_bounds_aware',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......k',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'K.......'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '......xT',  # 8
                        '......xx',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        'K.......'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '.......k',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        'xx......',  # 2
                        'Tx......'   # 1
                    ]),
                }
            }),
            { 'name': 'should_be_able_to_capture',
                'board': Board.from_strings([
                    # bcdefgh
                    'K.......',  # 8
                    'pp......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'PP......',  # 2
                    'k.......'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.EIGHT, File.A): {
                            Position(Rank.SEVEN, File.A),
                            Position(Rank.SEVEN, File.B),
                            Position(Rank.EIGHT, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.ONE, File.A): {
                            Position(Rank.ONE, File.B),
                            Position(Rank.TWO, File.B),
                            Position(Rank.TWO, File.A),
                        }
                    },
                }
            },
            { 'name': 'should_not_include_friendlies',
                'board': Board.from_strings([
                    # bcdefgh
                    'kk......',  # 8
                    'kk......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'KK......',  # 2
                    'KK......'   # 1
                ]),
                'want': {
                    'white': {Position(Rank.ONE, File.A):   {}},
                    'black': {Position(Rank.EIGHT, File.A): {}},
                }
            },
            { 'name': 'should_not_be_able_to_capture_if_piece_is_protected',
                'board': Board.from_strings([
                    # bcdefgh
                    'Kb......',  # 8
                    'pp......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'PP......',  # 2
                    'kB......'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.EIGHT, File.A): {
                            Position(Rank.SEVEN, File.B),
                            Position(Rank.EIGHT, File.B),
                        }
                    },
                    'black': {
                        Position(Rank.ONE, File.A): {
                            Position(Rank.ONE, File.B),
                            Position(Rank.TWO, File.B),
                        }
                    },
                }
            },
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)

    def test_is_in_check_from_all_figures(self):
        test_table = [
            { 'name': 'pawn checks from the left',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    'P.......',  # 6
                    '........',  # 5
                    '........',  # 4
                    'p.......',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'pawn checks from the right',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    '..P.....',  # 6
                    '........',  # 5
                    '........',  # 4
                    '..p.....',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'knight checks',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    '...N....',  # 6
                    '........',  # 5
                    '........',  # 4
                    '...n....',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'queen checks main diagonal',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    '..Q.....',  # 6
                    '........',  # 5
                    '........',  # 4
                    '..q.....',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'queen checks main diagonal 2',
                'board': Board.from_strings([
                    # bcdefgh
                    'Q.......',  # 8
                    '.k......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    'q.......',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'queen checks sec diagonal',
                'board': Board.from_strings([
                    # bcdefgh
                    '..Q.....',  # 8
                    '.k......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '...q....',  # 4
                    '........',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'queen checks sec diagonal 2',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.k......',  # 7
                    'Q.......',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.K......',  # 2
                    'q.......'   # 1
                ]),
            },
            { 'name': 'rook checks',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '.k.....R',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.K....r.',  # 2
                    '........'   # 1
                ]),
            },
            { 'name': 'bishop checks',
                'board': Board.from_strings([
                    # bcdefgh
                    '...B....',  # 8
                    '........',  # 7
                    '.k......',  # 6
                    '....b...',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.K......',  # 2
                    '........'   # 1
                ]),
            },
        ]

        for test_case in test_table:
            test_board = test_case['board']

            with self.subTest('/'.join([test_case['name'], 'white'])):
                white_king_pos = test_board.kings[Color.WHITE]
                white_king = test_board[white_king_pos.rank][white_king_pos.file]
                self.assertTrue(white_king.is_in_check(test_board, white_king_pos))

            with self.subTest('/'.join([test_case['name'], 'black'])):
                black_king_pos = test_board.kings[Color.BLACK]
                black_king = test_board[black_king_pos.rank][black_king_pos.file]
                self.assertTrue(black_king.is_in_check(test_board, black_king_pos))