from __future__ import annotations

import functools
from abc import abstractmethod, ABC  # Abstract Base Class

import chess.constants as types  # used just for typing information
from chess.constants import FigureColor, FigureType, Rank, File


class ChessPiece(ABC):
    def __init__(
        self,
        color: types.FigureColor,
    ) -> ChessPiece:
        self.type = self.figure_type
        self.color = color

    def __repr__(self):
        color = self.color.name.capitalize()
        type = self.type.name.capitalize()
        return f'{color} {type}'

    @property
    @abstractmethod
    def figure_type(self) -> types.FigureType:
        pass

    @abstractmethod
    def generate_moves(self, board, piece_position):
        pass

    def is_enemy(self, other):
        return self.color != other.color
