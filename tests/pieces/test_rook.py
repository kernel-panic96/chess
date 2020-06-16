from unittest.mock import MagicMock

from chess.board import Board
from chess.pieces.rook import Rook
from chess.constants import Direction
from chess.constants import FigureColor as Color, FigureType as Type
from chess.constants import Rank, File
from chess.position import Position

from tests import MoveGenerationTestCase, target_board

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
                    'white': target_board([
                        # bcdefgh
                        'x......r',  # 8
                        'x.......',  # 7
                        'x.......',  # 6
                        'x.......',  # 5
                        'x.......',  # 4
                        'x.......',  # 3
                        'x.......',  # 2
                        'Txxxxxxx'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        'xxxxxxxT',  # 8
                        '.......x',  # 7
                        '.......x',  # 6
                        '.......x',  # 5
                        '.......x',  # 4
                        '.......x',  # 3
                        '.......x',  # 2
                        'R......x'   # 1
                    ]),
                }
            }),
            *self.all_board_rotations_of({
                'name': 'should_stop_at_first_friendly',
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
                    'white': target_board([
                        # bcdefgh
                        '....r..r',  # 8
                        '........',  # 7
                        '........',  # 6
                        '.......r',  # 5
                        'R.......',  # 4
                        'x.......',  # 3
                        'x.......',  # 2
                        'TxxR....'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '....rxxT',  # 8
                        '.......x',  # 7
                        '.......x',  # 6
                        '.......r',  # 5
                        'R.......',  # 4
                        '........',  # 3
                        '........',  # 2
                        'R..R....'   # 1
                    ]),
                }
            }),
            {
                'name': 'should_stop_on_top_of_first_enemy',
                'board': Board.from_strings([
                    # bcdefgh
                    '....R..r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '.......R',  # 5
                    'r.......',  # 4
                    '........',  # 3
                    '........',  # 2
                    'R..r....'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '....xxxT',  # 8
                        '.......x',  # 7
                        '.......x',  # 6
                        '.......x',  # 5
                        'r.......',  # 4
                        '........',  # 3
                        '........',  # 2
                        'R..r....'   # 1
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '....R..r',  # 8
                        '........',  # 7
                        '........',  # 6
                        '.......R',  # 5
                        'x.......',  # 4
                        'x.......',  # 3
                        'x.......',  # 2
                        'Txxx....'   # 1
                    ]),
                }
            }
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
