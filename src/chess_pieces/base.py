from abc import abstractmethod, ABC  # Abstract Base Class
from constants import FigureColor, Rank, File
import functools


class ChessPiece(ABC):
    def __init__(
        self,
        color: FigureColor,
    ):
        self.type = self.figure_type
        self.color = color

    def __repr__(self):
        color = self.color.name.capitalize()
        type = self.type.name.capitalize()
        return f'{color} {type} at (x:{self.file}, y:{self.rank})'

    @property
    @abstractmethod
    def figure_type(self):
        pass

    def __repr__(self):
        return self.type.name + ' ' + self.color.name

    @abstractmethod
    def generate_moves(self, board, piece_position):
        pass

    def is_enemy(self, other):
        return self.color != other.color


def prune_if_piece_protects_the_king(move_gen_fn):
    '''This decorator checks if the piece is protecting the king
    with it's current position and if so prunes the legal moves
    '''
    @functools.wraps(move_gen_fn)
    def wrapper(self, board, position, *args, **kwargs):
        positions = move_gen_fn(self, board, piece_position,
                                *args, **kwargs)
        new_board = board.copy()

        king_pos = self.kings[self.color]
        new_board[position.rank][position.file] = None

        if board.get_attackers(king_pos, self.color):
            pass

        # check if the absence of the piece will put the king in check
        #   if not return the positions
        # if yes
        # check if there's only one attacker
        #   if so, check if he is in the attack vector of said piece
        #       if so, prune such that only the positions in the attack vector remain
        #   if there is more than one attacker
        #       prune all
        return positions

    return wrapper
