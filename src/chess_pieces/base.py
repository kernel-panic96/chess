from abc import abstractmethod, ABC  # Abstract Base Class
from constants import FigureColor, Rank, File


class ChessPieceBase(ABC):
    def __init__(
        self,
        color: FigureColor,
        *,
        rank: Rank,
        file: File
    ):
        self.type = self.figure_type
        self.color = color
        self.rank = rank
        self.file = file

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
