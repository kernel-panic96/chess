from enum import Enum, IntEnum, IntFlag, auto
import functools


class FigureType(Enum):
    """Enum describing the piece types.

    Possible Values
    ---------------
    PAWN BISHOP ROOK KNIGHT QUEEN KING NONE
    """

    PAWN = 1
    BISHOP = 2
    ROOK = 3
    KNIGHT = 4
    QUEEN = 5
    KING = 6
    NONE = 7


class FigureColor(Enum):
    """Enum describing possible piece colors.

    Properties
    ----------
    forward_direction
        Returns the valid direction for pawn movement.
        For white that would be Direction.UP, black -> Direction.DOWN

    Possible Values
    ---------------
    WHITE BLACK
    """

    BLACK = 1
    WHITE = 2

    @property
    def forward_direction(self):
        return Direction.UP if self.value == self.WHITE.value else Direction.DOWN


class Rank(IntEnum):
    '''Enum used for indexing of board's first dimension.

    The rank coordinates are increasing from top to bottom

    >>> Rank.ONE.value > Rank.TWO.value
    True

    But comparison is as if the naming were natural numbers

    >>> Rank.TWO > Rank.ONE
    True


    It can be compared to other Rank instances

    Properties
    -------
        to_coordinate - Returns the would be index if the board was a 8x8 matrix

    Class methods
    -------------
        from_str(string: str) - Returns Rank instance from str
        eg.:
            from_str('1') -> Rank.ONE
            from_str('2') -> Rank.TWO
            ...
    '''

    ONE = 9
    TWO = 8
    THREE = 7
    FOUR = 6
    FIVE = 5
    SIX = 4
    SEVEN = 3
    EIGHT = 2

    @property
    def to_coordinate(self):
        """To coordinate would return the index of the row as if the board was a 2d array.
        Note that in chess the higher numbered rows are at the top.

        >>> Rank.ONE.to_coordinate
        7
        >>> Rank.EIGHT.to_coordinate
        0

        """
        return self.value - 2

    @classmethod
    def from_str(cls, string):
        """ A parsing method from string
        >>> Rank.from_str('1').name
        'ONE'
        >>> Rank.from_str('8').name
        'EIGHT'

        >>> Rank.from_str('11')
        Traceback (most recent call last):
            ...
        ValueError: "11" is not a valid Rank

        """

        if string not in list('12345678'):
            raise ValueError(f'"{string}" is not a valid {cls.__name__}')

        return cls(9 - (int(string) - 1))

    def __lt__(self, other):
        """
        >>> Rank.ONE < Rank.TWO
        True

        >>> Rank.TWO < Rank.ONE
        False

        """
        return self.value > other.value

    def __le__(self, other):
        """
        >>> Rank.THREE <= Rank.THREE
        True

        >>> Rank.THREE <= Rank.FOUR
        True

        """

        return self.value >= other.value

    def __gt__(self, other):
        """
        >>> Rank.FOUR > Rank.FOUR
        False

        >>> Rank.FOUR > Rank.THREE
        True

        """
        return self.value < other.value

    def __ge__(self, other):
        """
        >>> Rank.FIVE >= Rank.FIVE
        True

        >>> Rank.FIVE >= Rank.FOUR
        True

        >>> Rank.FIVE >= Rank.SIX
        False

        """
        return self.value <= other.value

    def __eq__(self, other):
        """
        >>> Rank.SIX == Rank.SIX
        True

        >>> Rank.SIX == Rank.SEVEN
        False

        """
        return self.value == other.value

    @property
    def display(self):
        return 9 - (self.value - 1)


class File(IntEnum):
    A = 2
    B = 3
    C = 4
    D = 5
    E = 6
    F = 7
    G = 8
    H = 9

    @property
    def to_coordinate(self):
        """Returns as the index as if files were an array.

        >>> File.A.to_coordinate
        0

        >>> File.H.to_coordinate
        7

        """
        return self.value - 2

    @classmethod
    def from_str(cls, string):
        """parse from string

        >>> File.from_str('h').name
        'H'

        Case insensitivity:
        >>> File.from_str('H').name
        'H'

        >>> File.from_str('a').name
        'A'

        >>> File.from_str('z')
        Traceback (most recent call last):
            ...
        ValueError: "z" is not a valid File

        """
        if string.lower() not in list('abcdefgh'):
            raise ValueError(f'"{string}" is not a valid {cls.__name__}')

        return cls(ord(string.lower()) - ord('a') + 2)


class Direction(Enum):
    """
    Direction is a helper class for moving positions (ranks & files)

    Example usage:
        >>> from chess.constants import Rank, File

        Moving one position up:
        >>> Rank(Rank.ONE + Direction.UP).name
        'TWO'

        NOTE: there is no boundary checking. This is left to the user

        Moving one position down:
        >>> Rank(Rank.TWO + Direction.DOWN).name
        'ONE'

        Moving right:
        >>> File(File.A + Direction.RIGHT).name
        'B'

        Moving left:
        >>> File(File.B + Direction.LEFT).name
        'A'

        You can unmake moves:
        >>> Rank(Rank.TWO - Direction.UP).name
        'ONE'

        Or move longer distances:
        >>> File(File.A + 3 * Direction.RIGHT).name
        'D'

    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @classmethod
    def from_name(cls, name):
        """ from_name takes the representation, 'UP', 'DOWN' etc. and returns the appropriate instance.

        >>> Direction.from_name('UP').name
        'UP'

        >>> Direction.from_name('DOWN').name
        'DOWN'

        >>> Direction.from_name('RIGHT').name
        'RIGHT'

        >>> Direction.from_name('LEFT').name
        'LEFT'

        """
        name = name.upper()

        if name == 'UP':
            return cls.UP
        elif name == 'DOWN':
            return cls.DOWN
        elif name == 'RIGHT':
            return cls.RIGHT
        else:
            assert name == 'LEFT'
            return cls.LEFT

    @property
    def _int_value(self):
        """_int_value returns the int value 1 or -1 as if want to move in that direction in an array.
        """
        return self.value[0] or self.value[1]

    def composites(self):
        """Composites returns a movement vector (y, x) for directions.

        >>> Direction.UP.composites()
        (-1, 0)

        >>> Direction.DOWN.composites()
        (1, 0)

        >>> Direction.LEFT.composites()
        (0, -1)

        >>> Direction.RIGHT.composites()
        (0, 1)

        """

        return self.value

    def __add__(self, other):
        """
        >>> Direction.UP + 1
        0

        >>> Direction.DOWN + 1
        2

        """

        return self._int_value + other

    def __radd__(self, other):
        """
        >>> 1 + Direction.UP
        0

        >>> 1 + Direction.DOWN
        2

        """

        return other + self._int_value

    def __rsub__(self, other):
        return other - self._int_value

    def __mul__(self, other):
        """
        >>> Direction.UP * 3
        -3

        """
        return self._int_value * other

    def __rmul__(self, other):
        """
        >>> Direction.DOWN * 3
        3

        """
        return other * self._int_value


class Diagonal(Enum):
    UP_RIGHT = (Direction.UP, Direction.RIGHT)
    DOWN_RIGHT = (Direction.DOWN, Direction.RIGHT)
    DOWN_LEFT = (Direction.DOWN, Direction.LEFT)
    UP_LEFT = (Direction.UP, Direction.LEFT)

    def __eq__(self, other):
        if isinstance(other, Diagonal):
            return self.value == other.value

        return False

    def composites(self):
        return self.value

    def __hash__(self):
        return hash(self.value)


class CastlingPerm(IntFlag):
    NONE = 0
    KING_SIDE = auto()
    QUEEN_SIDE = auto()
    ALL = 1 | 2
