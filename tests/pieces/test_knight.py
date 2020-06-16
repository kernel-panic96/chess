from tests import MoveGenerationTestCase, target_board

from chess.pieces.knight import Knight
from chess.board import Board
from chess.position import Position
from chess.constants import FigureType as Type, FigureColor as Color
from chess.constants import Rank, File


class KnightMoveTests(MoveGenerationTestCase):
    def test_board_constructor_works_for_knights(self):
        board = Board.from_strings([
            # bcdefgh
            '........',  # 8
            '.n......',  # 7
            '........',  # 6
            '........',  # 5
            '........',  # 4
            '........',  # 3
            '.N......',  # 2
            '........'   # 1
        ])
        self.assertEqual(board[Rank.TWO][File.B].type, Type.KNIGHT)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].type, Type.KNIGHT)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_knight_move_geneneration(self):
        test_table = [
            {
                'name': 'clear_board_should_have_all_surrounding_positions_white',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '....N...',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '........',  # 7
                        '...x.x..',  # 6
                        '..x...x.',  # 5
                        '....T...',  # 4
                        '..x...x.',  # 3
                        '...x.x..',  # 2
                        '........'   # 1
                    ]),
                },
            },
            {
                'name': 'clear_board_should_have_all_surrounding_positions_black',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '....n...',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '........',  # 7
                        '...x.x..',  # 6
                        '..x...x.',  # 5
                        '....T...',  # 4
                        '..x...x.',  # 3
                        '...x.x..',  # 2
                        '........'   # 1
                    ]),
                },
            },
            *self.all_board_rotations_of({
                'name': 'should_be_bounds_aware',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......N',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'n.......'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '.......T',  # 8
                        '.....x..',  # 7
                        '......x.',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        'n.......'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '.......N',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '.x......',  # 3
                        '..x.....',  # 2
                        'T.......'   # 1
                    ]),
                },
            }),
            *self.all_board_rotations_of({
                'name': 'should_not_be_able_to_capture_friendlies',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......N',  # 8
                    '.....N..',  # 7
                    '......N.',  # 6
                    '........',  # 5
                    '........',  # 4
                    '.n......',  # 3
                    '..n.....',  # 2
                    'n.......'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '.......T',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        'n.......'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '.......N',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        'T.......'   # 1
                    ]),
                },
            }),
            *self.all_board_rotations_of({
                'name': 'should_be_able_to_capture_enemies',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......N',  # 8
                    '.....n..',  # 7
                    '......n.',  # 6
                    '........',  # 5
                    '........',  # 4
                    '.N......',  # 3
                    '..N.....',  # 2
                    'n.......'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '.......T',  # 8
                        '.....x..',  # 7
                        '......x.',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        'n.......'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '.......N',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '.x......',  # 3
                        '..x.....',  # 2
                        'T.......'   # 1
                    ]),
                },
            }),
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
