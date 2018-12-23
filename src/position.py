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
        return f'{self.file.name}{self.rank.display()}'

    def __repr__(self):
        if hasattr(self.file, 'name') and hasattr(self.rank, 'display'):
            return f'{self.file.name}{self.rank.display()}'
        return f'{self.file}:{self.rank}'

    def __hash__(self):
        return hash(f'{self.rank}{self.file}')
