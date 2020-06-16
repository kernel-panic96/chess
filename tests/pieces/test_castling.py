import unittest

from board      import Board
from position   import Position
from constants  import Rank, File

from tests import MoveGenerationTestCase


class CastlingTests(MoveGenerationTestCase):
    def test_starting_configuration_should_not_be_able_to_castle(self):
        test_table = [
            {
                'name': 'standard_configuration_should_not_be_able_to_castle_because_of_blockers',
                'board': Board.from_strings([
                    # bcdefgh
                    'rnbqkbnr',  # 8
                    'pppppppp',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    'PPPPPPPP',  # 2
                    'RNBQKBNR'   # 1
                ]),
                'want': {
                    'white': {
                        Position(Rank.ONE, File.E): {}
                    },
                    'black': {
                        Position(Rank.EIGHT, File.E): {}
                    }
                }
            },
            {
                'name': 'should_not_castle_if_file_is_blocked_by_friendly',
                'board': Board.from_strings([
                    # bcdefgh
                    'rn..kn.r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'RN..KN.R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertNotIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertNotIn
                    }
                }
            },
            {
                'name': 'should_be_able_to_castle_both_sides',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k..r',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'R...K..R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertIn
                    }
                }
            },
            {
                'name': 'should_not_be_able_to_castle_if_king_is_in_check',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k..r',  # 8
                    '........',  # 7
                    '....R...',  # 6
                    '........',  # 5
                    '........',  # 4
                    '....r...',  # 3
                    '........',  # 2
                    'R...K..R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertNotIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertNotIn
                    }
                }
            },
            {
                'name': 'should_not_be_able_to_castle_if_king_will_be_in_check_if_he_castles',
                'board': Board.from_strings([
                    # bcdefgh
                    'r...k..r',  # 8
                    '........',  # 7
                    '..R...R.',  # 6
                    '........',  # 5
                    '........',  # 4
                    '..r...r.',  # 3
                    '........',  # 2
                    'R...K..R'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertNotIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertNotIn
                    }
                }
            },
            {
                'name': 'should_not_be_able_to_castle_if_last_files_are_not_rooks',
                'board': Board.from_strings([
                    # bcdefgh
                    'b...k..b',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'B...K..B'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertNotIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertNotIn
                    }
                }
            },
            {
                'name': 'should_not_be_able_to_castle_if_last_files_are_not_rooks',
                'board': Board.from_strings([
                    # bcdefgh
                    'b...k..b',  # 8
                    '........',  # 7
                    '........',  # 6
                    '........',  # 5
                    '........',  # 4
                    '........',  # 3
                    '........',  # 2
                    'B...K..B'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertNotIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertNotIn
                    }
                }
            },
            {
                'name': 'should_not_be_able_to_castle_if_the_king_passes_through_a_check',
                'board': Board.from_strings([
                    # bcdefgh
                    'b...k..b',  # 8
                    '........',  # 7
                    '...R.R..',  # 6
                    '........',  # 5
                    '........',  # 4
                    '...r.r..',  # 3
                    '........',  # 2
                    'B...K..B'   # 1
                ]),
                'want': {
                    'white_queen_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.C),
                        'assert': self.assertNotIn
                    },
                    'white_king_side': {
                        Position(Rank.ONE, File.E): Position(Rank.ONE, File.G),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.C),
                        'assert': self.assertNotIn
                    },
                    'black_king_side': {
                        Position(Rank.EIGHT, File.E): Position(Rank.EIGHT, File.G),
                        'assert': self.assertNotIn
                    }
                }
            },
        ]

        for test_case in test_table:
            self.runMoveGenerationTest(test_case)
