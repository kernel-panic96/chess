from chess.board import Board
from chess.constants import FigureColor as Color, FigureType as Type
from chess.constants import Rank, File
from chess.position import Position


from tests import MoveGenerationTestCase
from tests import target_board


class TestMoveGeneration(MoveGenerationTestCase):
    def test_board_constructor_works_for_queen(self):
        board = Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '.q......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.Q......',  # 2
                    '........'   # 1
                ])

        self.assertEqual(board[Rank.TWO][File.B].figure_type, Type.QUEEN)
        self.assertEqual(board[Rank.TWO][File.B].color, Color.WHITE)

        self.assertEqual(board[Rank.SEVEN][File.B].figure_type, Type.QUEEN)
        self.assertEqual(board[Rank.SEVEN][File.B].color, Color.BLACK)

    def test_move_generation(self):
        test_table = [
            *self.all_board_rotations_of({
                'name': 'friendly_on_diagonals_should_not_be_capturable',
                'board': Board.from_strings([
                    # bcdefgh
                    '....q..q',  # 8
                    '........',  # 7
                    '........',  # 6
                    '....q..q',  # 5
                    'Q..Q....',  # 4
                    '........',  # 3
                    '........',  # 2
                    'Q..Q....'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        'Q..Q....',  # 4
                        'x.x.....',  # 3
                        'xx......',  # 2
                        'TxxQ....'   # 1
                        # bcdefgh
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '....qxxT',  # 8
                        '......xx',  # 7
                        '.....x.x',  # 6
                        '....q..q',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        '........'   # 1
                        # bcdefgh
                    ]),
                }
            }),
            *self.all_board_rotations_of({
                'name': 'should_go_no_further_than_the_enemy',
                'board': Board.from_strings([
                    # bcdefgh
                    '....Q..q',  # 8
                    '........',  # 7
                    '........',  # 6
                    '....Q..Q',  # 5
                    'q..q....',  # 4
                    '........',  # 3
                    '........',  # 2
                    'Q..q....'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        'x..x....',  # 4
                        'x.x.....',  # 3
                        'xx......',  # 2
                        'Txxx....'   # 1
                        # bcdefgh
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '....xxxT',  # 8
                        '......xx',  # 7
                        '.....x.x',  # 6
                        '....x..x',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        '........'   # 1
                        # bcdefgh
                    ]),
                }
            }),
            {
                'name': 'clear_board_all_positions',
                'board': Board.from_strings([
                    # bcdefgh
                    '.......K',  # 8
                    '........',  # 7
                    '........',  # 6
                    '...Q....',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        'x..x..x.',  # 8
                        '.x.x.x..',  # 7
                        '..xxx...',  # 6
                        'xxxTxxxx',  # 5
                        '..xxx...',  # 4
                        '.x.x.x..',  # 3
                        'x..x..x.',  # 2
                        '...x...x'   # 1
                    ]),
                }
            },
            {
                'name': 'clear_board_all_positions',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '...q....',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'black': target_board([
                        # bcdefgh
                        'x..x..x.',  # 8
                        '.x.x.x..',  # 7
                        '..xxx...',  # 6
                        'xxxTxxxx',  # 5
                        '..xxx...',  # 4
                        '.x.x.x..',  # 3
                        'x..x..x.',  # 2
                        '...x...x'   # 1
                    ]),
                }
            },
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
