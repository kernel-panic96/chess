import os

from chess.board import Board
from chess.position import Position
from chess.constants import Rank, File


from tests import MoveGenerationTestCase, target_board

P = Position.from_str


class CheckAwarenessTests(MoveGenerationTestCase):
    def test_pieces_should_body_block_checks(self):
        """
        Even though there may be other possible moves if something body blocks a check,
        it should be able to make only such moves that keep blocking the check
        """

        test_table = [
            {'name': 'white_diagonal_pieces_should_not_be_able_to_move_from_diagonals',
                'board': Board.from_strings([
                    # bcdefgh
                    '.b.....q',  # 8
                    '........',  # 7
                    '...Q.Q..',  # 6
                    '....K...',  # 5
                    '...Q.Q..',  # 4
                    '........',  # 3
                    '.q.....b',  # 2
                    '........'   # 1
                    # bcdefgh
                ]),
                'want': {
                    'white': {
                        P('f6'): {P('g7'), P('h8')},
                        P('f4'): {P('g3'), P('h2')},
                        P('d6'): {P('c7'), P('b8')},
                        P('d4'): {P('c3'), P('b2')},
                    }
                },
                'expect_same_behaviour_for': ['bishop'],
            },
            {'name': 'black_diagonal_pieces_should_not_be_able_to_move_from_diagonals',
                'board': Board.from_strings([
                    # bcdefgh
                    '.B.....Q',  # 8
                    '........',  # 7
                    '...q.q..',  # 6
                    '....k...',  # 5
                    '...b.b..',  # 4
                    '........',  # 3
                    '.Q.....B',  # 2
                    '........'   # 1
                    # bcdefgh
                ]),
                'want': {
                    'black': {
                        P('f6'): {P('g7'), P('h8')},
                        P('f4'): {P('g3'), P('h2')},
                        P('d6'): {P('c7'), P('b8')},
                        P('d4'): {P('c3'), P('b2')},
                    }
                },
                'expect_same_behaviour_for': ['bishop'],
            },
            {'name': 'white_should_not_be_able_to_move_from_straight',
                'board': Board.from_strings([
                    # bcdefgh
                    '....q...',  # 8
                    '........',  # 7
                    '....Q...',  # 6
                    '.q.QKQ.q',  # 5
                    '....Q...',  # 4
                    '........',  # 3
                    '....q...',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        P('f5'): {P('g5'), P('h5')},
                        P('d5'): {P('c5'), P('b5')},
                        P('e6'): {P('e7'), P('e8')},
                        P('e4'): {P('e3'), P('e2')},
                    }
                },
                'expect_same_behaviour_for': ['rook'],
            },
            {'name': 'black_figure_should_not_be_able_to_move_from_straight',
                'board': Board.from_strings([
                    # bcdefgh
                    '....Q...',  # 8
                    '........',  # 7
                    '....q...',  # 6
                    '.Q.qkq.Q',  # 5
                    '....q...',  # 4
                    '........',  # 3
                    '....Q...',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'black': {
                        P('f5'): {P('g5'), P('h5')},
                        P('d5'): {P('c5'), P('b5')},
                        P('e6'): {P('e7'), P('e8')},
                        P('e4'): {P('e3'), P('e2')},
                    }
                },
                'expect_same_behaviour_from': ['rook'],
            },
            {'name': 'knight_should_be_allowed_only_to_block',
                'board': Board.from_strings([
                    # bcdefgh
                    'N.....n.',  # 8
                    '.q.....Q',  # 7
                    '........',  # 6
                    '.K.....k',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    '........'   # 1
                ]),
                'want': {
                    'white': {
                        P('a8'): {P('b6')}
                    },
                    'black': {
                        P('g8'): {P('h6')}
                    }
                }
            },
            {'name': 'pawn_should_be_allowed_only_to_block',
                'board': Board.from_strings([
                    # bcdefgh
                    '........',  # 8
                    '........',  # 7
                    '........',  # 6
                    '......q.',  # 5
                    '........',  # 4
                    '........',  # 3
                    '.....P..',  # 2
                    '..K.....'   # 1
                ]),
                'want': {
                    'white': {
                        P('f2'): {P('f4')}
                    },
                }
            },
            {'name': 'should_only_be_able_to_capture_when_knight_checks',
                'board': Board.from_strings([
                    # bcdefgh
                    '.....k..',  # 8
                    '....q..N',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'n..Q....',  # 2
                    '..K.....'   # 1
                    # bcdefgh
                ]),
                'want': {
                    'white': target_board([
                        # bcdefgh
                        '........',  # 8
                        '........',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        'x..T....',  # 2
                        '..K.....'   # 1
                        # bcdefgh
                    ]),
                    'black': target_board([
                        # bcdefgh
                        '.....k..',  # 8
                        '....T..x',  # 7
                        '........',  # 6
                        '........',  # 5
                        '........',  # 4
                        '........',  # 3
                        '........',  # 2
                        '........'   # 1
                    ]),
                }
            },
            {'name': 'pieces_that_cannot_protect_king_should_have_no_moves',
                'board': Board.from_strings([
                    # bcdefgh
                    '.....k..',  # 8
                    '.......N',  # 7
                    '...q....',  # 6
                    '........',  # 5
                    '........',  # 4
                    '...Q....',  # 3
                    'n.......',  # 2
                    '..K.....'   # 1
                    # bcdefgh
                ]),
                'want': {
                    'white': {P('d3'): {}},
                    'black': {P('d6'): {}},
                }
            },
        ]
        for test_case in test_table:
            self.runMoveGenerationTest(test_case)

    def test_double_check_no_other_pieces_other_than_king_should_move(self):
        for figure, figure_name in (
            ('q', 'queen'),
            ('n', 'knight'),
            ('b', 'bishop'),
            ('p', 'pawn'),
            ('r', 'rook'),
        ):
            test_case = {
                'name': f'{figure_name}_is_blocking_double_check_and_should_not_be_able_to_move',
                'board': Board.from_strings(os.linesep.join([
                    # bcdefgh
                    '....q...',  # 8
                    '.q......',  # 7
                    '..X.....',  # 6
                    '.K......',  # 5
                    '.......Q',  # 4
                    '....Q...',  # 3
                    '.....x..',  # 2
                    '....k...'   # 1
                ]).replace('x', figure).replace('X', figure.upper()).split(os.linesep)),
                'want': {
                    'white': {P('c6'): {}},
                    'black': {P('f2'): {}}
                }
            }
            self.runMoveGenerationTest(test_case)

    def test_king_should_not_be_able_to_step_on_attacked_square(self):
        test_table = [
            *self.all_board_rotations_of({'name': 'should_not_be_able_to_step_on_attacked_squares',
                'board': Board.from_strings([
                    # bcdefgh
                    '...k....',  # 8
                    'R.......',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'r.......',  # 2
                    '...K....'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.D): {
                            Position(Rank.TWO, File.C),
                            Position(Rank.TWO, File.D),
                            Position(Rank.TWO, File.E),
                        },
                        'assert': lambda want, actual, **_: [self.assertNotIn(p, actual) for p in want]
                    },
                    'black': {
                        Position(Rank.EIGHT, File.D): {
                            Position(Rank.SEVEN, File.C),
                            Position(Rank.SEVEN, File.D),
                            Position(Rank.SEVEN, File.E),
                        },
                        'assert': lambda want, actual, **_: [self.assertNotIn(p, actual) for p in want]
                    },
                }
            })
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)

    def test_when_king_is_in_check_he_should_be_aware_of_his_own_position(self):
        test_table = [
            *self.all_board_rotations_of({
                'comment': '''
                    when a possible position is evaluated, the code should not consider
                    it's old position as a blocker of an attacker

                    In this situation:

                              v
                    a b c d e f g h
                    1 . Q . k . . . . 1

                    F1(marked with `v`) should not be a valid move
                ''',
                'board': Board.from_strings([
                    # bcdefgh
                    'R..k....',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'r..K....'   # 1
                ]),
                'want': {
                    'white': {
                        'assert': self.assertNotIn,
                        Position(Rank.ONE, File.D): Position(Rank.ONE, File.E),
                    },
                    'black': {
                        'assert': self.assertNotIn,
                        Position(Rank.EIGHT, File.D): Position(Rank.EIGHT, File.E),
                    },
                },
                'name': '',
            }),
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
