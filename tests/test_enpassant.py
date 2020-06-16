import unittest
from copy import deepcopy

from board      import Board
from constants  import Rank, File
from constants  import FigureType as Type
from position   import Position

from tests import MoveGenerationTestCase

P = Position.from_str


class EnPassantTests(MoveGenerationTestCase):
    def test_en_passant_square_is_set_on_the_board_object(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.p......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '.P......',  # 2
            '........'   # 1
        ])

        with self.subTest('white'):
            en_passant_want = Position(Rank.THREE, File.B)
            f, t = Position(Rank.TWO, File.B), Position(Rank.FOUR, File.B)
            board.move(from_pos=f, to_pos=t)

            self.assertEqual(board.en_passant_pos, en_passant_want)

        with self.subTest('black'):
            en_passant_want = Position(Rank.SIX, File.B)
            f, t = Position(Rank.SEVEN, File.B), Position(Rank.FIVE, File.B)
            board.move(from_pos=f, to_pos=t)

            self.assertEqual(board.en_passant_pos, en_passant_want)

    def test_pawn_can_capture_en_passant(self):
        test_table = [
            {
                # white captures
                'name': 'en_passant_square_is_legal_move',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.p......',  # 7
                    '........',  # 6
                    'P.P.....',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'move_before': {'from': P('b7'), 'to': P('b5')},
                'want': {
                    'white': {
                        # given: {want...}
                        P('c5'): {P('c6'), P('b6')},
                        P('a5'): {P('a6'), P('b6')}
                    }
                }
            },
            {
                # black captures
                'name': 'en_passant_position_is_in_legal_moves',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    'p.p.....',  # 4
                    '........',  # 3
                    '.P......',  # 2
                    '........'   # 1
                ]),
                'move_before': {'from': P('b2'), 'to': P('b4')},
                'want': {
                    'black': {
                        P('c4'): {P('c3'), P('b3')},
                        P('a4'): {P('a3'), P('b3')}
                    }
                }
            }
        ]

        for test_case in test_table:
            board = test_case['board']
            f, t = test_case['move_before']['from'], test_case['move_before']['to']
            board.move(from_pos=f, to_pos=t)

            self.assertEqual(board[t.rank][t.file].figure_type, Type.PAWN)
            self.runMoveGenerationTest(test_case)

    def test_en_passant_square_should_be_cleared_after_one_move(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.p......',  # 7
            '........',  # 6
            'P.P.....',  # 5
            '........',  # 4
            '........',  # 3
            '........',  # 2
            '........'   # 1
        ])
        f, t = P('b7'), P('b5')
        board.move(from_pos=f, to_pos=t)
        self.assertEqual(board.en_passant_pos, P('b6'))

        board.move(from_pos=P('c5'), to_pos=P('c6'))
        self.assertNotEqual(board.en_passant_pos, P('b6'))

    def test_en_passant_move_should_capture_pawn(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.p......',  # 7
            '........',  # 6
            'P.P.....',  # 5
            '........',  # 4
            '........',  # 3
            '........',  # 2
            '........'   # 1
        ])
        f, t = P('b7'), P('b5')
        board.move(from_pos=f, to_pos=t)
        self.assertEqual(board.en_passant_pos, P('b6'))

        self.assertNotEqual(board[Rank.FIVE][File.B], None)
        board.move(from_pos=P('c5'), to_pos=board.en_passant_pos)
        self.assertEqual(board[Rank.FIVE][File.B], None)
