from constants import Rank, File, Direction, Diagonal
import math


class Position:
    """Represents a chess position.

    >>> Position(Rank.ONE, File.A)
    A1

    """

    def __init__(self, rank, file):
        self.rank = rank
        self.file = file

    @property
    def rank(self):
        """Returns the rank of position.

        >>> Position(rank=Rank.ONE, file=File.A).rank.name
        'ONE'

        """
        return self._rank

    @property
    def file(self):
        """Return the file of the position.

        >>> Position(rank=Rank.ONE, file=File.H).file.name
        'H'

        """
        return self._file

    @rank.setter
    def rank(self, value):
        try:
            self._rank = Rank(value)
        except ValueError:
            self._rank = value

    @file.setter
    def file(self, value):
        try:
            self._file = File(value)
        except ValueError:
            self._file = value

    def __eq__(self, other):
        """ If a file & rank are equal returns True

        >>> Position(Rank.ONE, File.A) == Position(Rank.ONE, File.A)
        True

        """
        if not isinstance(other, self.__class__):
            return False
        return self.rank == other.rank and self.file == other.file

    def __str__(self):
        return f'{self.file.name}{8-self.rank.to_coordinate}'

    def __repr__(self):
        try:
            return f'{self.file.name}{self.rank.display}'
        except Exception:
            return f'{self.file}:{self.rank}'

    def __hash__(self):
        """
        >>> hash(Position(Rank.ONE, File.A)) == hash(Position(Rank.ONE, File.A))
        True

        """
        return hash(f'{self.rank}{self.file}')

    @classmethod
    def from_str(cls, string: str):
        """Parses a position from string

        >>> Position.from_str('a1')
        A1

        >>> Position.from_str('A8')
        A8

        """

        if len(string) != 2:
            raise ValueError(f'"{string}" is not a valid {cls.__name__}')
        assert len(string) == 2
        assert string[0].lower() in 'abcdefgh'
        assert string[1].lower() in '12345678'

        file, rank = map(str.lower, list(string))
        return cls(Rank.from_str(rank), File.from_str(file))

    @property
    def coordinates(self):
        """Returns the would be indeces, if the board was a 2d matrix."""
        return self.rank.to_coordinate, self.file.to_coordinate

    @classmethod
    def from_board_coordinates(y, x):
        pass

    def dist(self, other):
        """Calculates the Chebyshev distance between two positions."""
        delta_rank = abs(self.rank - other.rank)
        delta_file = abs(self.file - other.file)

        return max(delta_rank, delta_file)

    def within(self, p1, p2):
        left_border = min(p2, p1, key=lambda p: p.file)
        right_border = max(p1, p2, key=lambda p: p.file)

        direction = left_border.relative_direction_towards_position(right_border)
        r_dir, f_dir = direction.composites()

        within_x = (right_border.file - self.file) * (left_border.file - self.file) <= 0
        within_y = (right_border.rank - self.rank) * (left_border.rank - self.rank) <= 0

        return within_x and within_y

    def relative_direction_towards_position(self, other):
        delta_rank = (other.rank - self.rank)
        delta_file = (other.file - self.file)

        # normalize them
        delta_rank //= abs(delta_rank) or 1
        delta_file //= abs(delta_file) or 1

        if delta_rank and delta_file:
            dir_vertical = Direction((delta_rank, 0))
            dir_horizontal = Direction((0, delta_file))

            return Diagonal((dir_vertical, dir_horizontal))
        elif delta_rank:
            return Direction((delta_rank, 0))
        elif delta_file:
            return Direction((0, delta_file))

    def __add__(self, other):
        """Add a position with a tuple."""
        return Position(self.rank - other[0], self.file + other[1])

    def __radd__(self, other):
        return self.__add__(other)

    def __getitem__(self, idx):
        if idx == 0:
            return 7 - self.rank.to_coordinate
        elif idx == 1:
            return self.file.to_coordinate

        raise IndexError('index out of range')
