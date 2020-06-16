import functools as fp

from chess_pieces.base import ChessPiece
from constants import (
    FigureType, Direction, FigureColor, Rank
)
from position import Position

from typing import List
from utils import prune_moves_if_king_in_check
from utils import evaluate

from functional import seq


class Pawn(ChessPiece):
    figure_type = FigureType.PAWN

    @property
    def is_white(self):
        return self.color == FigureColor.WHITE

    def is_at_starting_pos(self, position: Position):
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

    @prune_moves_if_king_in_check
    def generate_moves(self, board, pawn_pos: Position) -> List[Position]:
        if pawn_pos is None:
            pawn_pos = Position(self.rank, self.file)

        potential_positions = self.get_possible_positions(pawn_pos)

        left_attack  = potential_positions['attack_left']
        right_attack = potential_positions['attack_right']
        one_forward  = potential_positions['one_forward']
        two_forward  = potential_positions['two_forward']

        positions = []

        if board.is_in_bounds(one_forward) and board.is_empty(one_forward):
            positions.append(one_forward)

        if self.is_at_starting_pos(pawn_pos) and board.is_empty(two_forward):
            positions.append(two_forward)

        can_attack = fp.partial(self._can_attack, board, pawn_pos)

        if can_attack(left_attack):
            positions.append(left_attack)

        if can_attack(right_attack):
            positions.append(right_attack)

        return positions

    @staticmethod
    def _can_attack(board, from_pos, attack_pos):
        return board.is_in_bounds(attack_pos) and board.are_enemies(from_pos, attack_pos) or board.en_passant_pos == attack_pos
