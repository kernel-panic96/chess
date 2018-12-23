from enum import Enum, IntEnum


class FigureType(Enum):
    """Enum describing the piece types.

    Possible Values
    ---------------
    PAWN BISHOP ROOK KNIGHT QUEEN KING
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

    Possible Values
    ---------------
    WHITE BLACK
    """
    BLACK = 1
    WHITE = 2


class Rank(IntEnum):
    ONE = 9
    TWO = 8
    THREE = 7
    FOUR = 6
    FIVE = 5
    SIX = 4
    SEVEN = 3
    EIGHT = 2

    def display(self):
        return 7 - (self.value - 3)


class File(IntEnum):
    A = 2
    B = 3
    C = 4
    D = 5
    E = 6
    F = 7
    G = 8
    H = 9

    def display(self):
        return self.value - 2


class Direction(Enum):
    UP = (1, -1)
    DOWN = (2, 1)
    LEFT = (3, -1)
    RIGHT = (4, 1)

    @classmethod
    def from_name(cls, name):
        if name == 'UP':
            return cls.UP
        elif name == 'DOWN':
            return cls.DOWN
        elif name == 'RIGHT':
            return cls.RIGHT
        elif name == 'LEFT':
            return cls.LEFT

    @property
    def int_value(self):
        return self.value[1]

    @property
    def id(self):
        return self.value[0]

    def __add__(self, other):
        return self.int_value + other

    def __radd__(self, other):
        return other + self.int_value

    def __sub__(self, other):
        return self.int_value - other

    def __rsub__(self, other):
        return other - self.int_value

    def __mul__(self, other):
        return self.int_value * other

    def __rmul__(self, other):
        return other * self.int_value

    def __floordiv__(self, other):
        return self.int_value * other

    def __rfloordiv__(self, other):
        return other // self.int_value

    def __truediv__(self, other):
        return self.int_value / other

    def __rtruediv__(self, other):
        return other / self.int_value


class Diagonal(Enum):
    UP_RIGHT = (Direction.UP, Direction.RIGHT)
    DOWN_RIGHT = (Direction.DOWN, Direction.RIGHT)
    DOWN_LEFT = (Direction.DOWN, Direction.LEFT)
    UP_LEFT = (Direction.UP, Direction.LEFT)

    def __eq__(self, other):
        if isinstance(other, Diagonal):
            return self == other

        return False

    def composites(self):
        return self.value

    def __hash__(self):
        return hash(self.value)
