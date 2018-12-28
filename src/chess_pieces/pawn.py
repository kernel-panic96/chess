from chess_pieces.base import ChessPieceBase
from constants import (
    FigureType, Direction, FigureColor, Rank
)
from position import Position

from typing import List


class Pawn(ChessPieceBase):
    figure_type = FigureType.PAWN

    @property
    def is_white(self):
        return self.color == FigureColor.WHITE

    def is_at_starting_pos(self, position = None):
        if position is None:
            position = Position(self.rank, self.file)

        starting_rank = Rank.TWO if self.is_white else Rank.SEVEN
        return position.rank == starting_rank

    def get_possible_positions(self, position):
        rank, file = position.rank, position.file
        forward = Direction.UP if self.is_white else Direction.DOWN

        return {
            'one_forward': Position(rank + forward, file),
            'two_forward': Position(rank + 2 * forward, file),
            'attack_right': Position(rank + forward, file + Direction.RIGHT),
            'attack_left': Position(rank + forward, file + Direction.LEFT),
        }

    def generate_moves(self, board, pawn_pos: Position = None) -> List[Position]:
        if pawn_pos is None:
            pawn_pos = Position(self.rank, self.file)

        possible_positions = self.get_possible_positions(pawn_pos)
        cells = {
            k: board[pos.rank][pos.file]
            for k, pos in possible_positions.items()
        }

        positions = []

        if board.is_in_bounds(possible_positions['one_forward']) and board.is_empty(possible_positions['one_forward']):
            positions.append(possible_positions['one_forward'])

        if self.is_at_starting_pos(pawn_pos) and board.is_empty(possible_positions['two_forward']):
            positions.append(possible_positions['two_forward'])

        if (
            board.is_in_bounds(possible_positions['attack_left']) and
            not board.is_empty(possible_positions['attack_left']) and
            board.are_enemies(pawn_pos, possible_positions['attack_left'])
        ):
            positions.append(possible_positions['attack_left'])

        if (
            board.is_in_bounds(possible_positions['attack_right']) and
            not board.is_empty(possible_positions['attack_right']) and
            board.are_enemies(pawn_pos, possible_positions['attack_right'])
        ):
            positions.append(possible_positions['attack_right'])

        return positions
