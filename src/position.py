from constants import Rank, File


class Position:
    def __init__(self, rank, file):
        self.rank = rank
        self.file = file

    @property
    def rank(self):
        return self._rank

    @property
    def file(self):
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
        return self.rank == other.rank and self.file == other.file

    def dict(self):
        return {'rank': self.rank, 'file': self.file}
    
    def __str__(self):
        return f'{self.file.name}{8-self.rank.to_coordinate}'

    def __repr__(self):
        if hasattr(self.file, 'name') and hasattr(self.rank, 'display'):
            return f'{self.file.name}{self.rank.display()}'
        return f'{self.file}:{self.rank}'

    def __hash__(self):
        return hash(f'{self.rank}{self.file}')

    @staticmethod
    def from_str(string):
        file, rank = list(string)
        return Position(Rank.from_str(rank), File.from_str(file))

    @property
    def to_coordinates(self):
        return self.rank.to_coordinate, self.file.to_coordinate
