from chess.pieces.base import ChessPiece
from chess.position import Position
from chess.constants import (
    FigureType,
    CastlingPerm,
    File
)

from functional import seq


class King(ChessPiece):
    figure_type = FigureType.KING

    def __can_step(self, board, king_pos, pos):
        return board.is_empty(pos) or board.are_enemies(king_pos, pos)

    def generate_moves(self, board, king_pos: Position = None):
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

        return (
            seq([1, 0, -1]).
            cartesian(repeat=2).
            filter(lambda p: p != (0, 0)).  # except + (0, 0) which is the `pos` itself
            map(lambda p: Position(rank, file) + p).
            to_list()
        )

    def is_in_check(self, board, king_pos, *, ignore=None):
        ignore = ignore or []

        with board.temporarily_remove_position(*ignore):
            return any(board.get_attackers(king_pos, self.color))
