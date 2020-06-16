from chess_pieces.base import ChessPiece

from position import Position
from constants import (
    FigureType,
    CastlingPerm,
    File
)

import itertools
import functools

from functional import seq


class King(ChessPiece):
    figure_type = FigureType.KING

    def __can_step(self, board, king_pos, pos):
        return board.is_empty(pos) or board.are_enemies(king_pos, pos)

    def __not_in_check(self, board, king_pos, pos):
        return not self.is_in_check(board, pos, ignore=[king_pos])

    def generate_moves(self, board, king_pos: Position = None):
        if king_pos is None:
            king_pos = board.kings[self.color]

        normal_moves = seq(self.possible_positions(king_pos))\
            .filter(board.is_in_bounds)\
            .filter(lambda p: self.__can_step(board, king_pos, p))\
            .filter(lambda p: not self.is_in_check(board, p, ignore=[king_pos]))\
            .list()

        castling_moves = []
        if board.is_able_to_castle(self.color, CastlingPerm.QUEEN_SIDE):
            castling_moves.append(Position(king_pos.rank, File.G))

        if board.is_able_to_castle(self.color, CastlingPerm.KING_SIDE):
            castling_moves.append(Position(king_pos.rank, File.C))

        return seq(normal_moves, castling_moves).flatten().to_list()

    def possible_positions(self, pos):
        rank, file = pos.rank, pos.file

        return seq([1, 0, -1])\
            .cartesian(repeat=2)\
            .filter(lambda p: p != (0, 0))\
            .map(lambda p: Position(rank, file) + p)\
            .to_list()

    def is_in_check(self, board, king_pos, *, ignore=None):
        ignore = ignore or []

        with board.temporarily_remove_position(*ignore):
            return any(board.get_attackers(king_pos, self.color))
