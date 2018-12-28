from constants import Rank, File, FigureColor, Diagonal, Direction
from position import Position
from chess_pieces import all as pieces
from utils import method_dispatch

import inspect


class OutOfBounds:
    def __repr__(self):
        return 'x'


OutOfBounds = OutOfBounds()


class Board:
    def __init__(self):
        self.board = self.empty()

    @classmethod
    def standard_configuration(self):
        board = Board()

        white_pawns = [
            pieces.Pawn(
                FigureColor.WHITE,
                file=file, rank=Rank.TWO
            )
            for file in range(File.A, File.H + 1)
        ]

        black_pawns = [
            pieces.Pawn(
                FigureColor.BLACK,
                file=file, rank=Rank.SEVEN
            )
            for file in range(File.A, File.H + 1)
        ]

        rank_one_default_white = [
            pieces.Rook(FigureColor.WHITE, file=File.A, rank=Rank.ONE),
            pieces.Knight(FigureColor.WHITE, file=File.B, rank=Rank.ONE),
            pieces.Bishop(FigureColor.WHITE, file=File.C, rank=Rank.ONE),
            pieces.Queen(FigureColor.WHITE, file=File.D, rank=Rank.ONE),
            pieces.King(FigureColor.WHITE, file=File.E, rank=Rank.ONE),
            pieces.Bishop(FigureColor.WHITE, file=File.F, rank=Rank.ONE),
            pieces.Knight(FigureColor.WHITE, file=File.G, rank=Rank.ONE),
            pieces.Rook(FigureColor.WHITE, file=File.H, rank=Rank.ONE)
        ]

        rank_eight_default_black = [
            pieces.Rook(FigureColor.BLACK, file=File.A, rank=Rank.EIGHT),
            pieces.Knight(FigureColor.BLACK, file=File.B, rank=Rank.EIGHT),
            pieces.Bishop(FigureColor.BLACK, file=File.C, rank=Rank.EIGHT),
            pieces.Queen(FigureColor.BLACK, file=File.D, rank=Rank.EIGHT),
            pieces.King(FigureColor.BLACK, file=File.E, rank=Rank.EIGHT),
            pieces.Bishop(FigureColor.BLACK, file=File.F, rank=Rank.EIGHT),
            pieces.Knight(FigureColor.BLACK, file=File.G, rank=Rank.EIGHT),
            pieces.Rook(FigureColor.BLACK, file=File.H, rank=Rank.EIGHT)
        ]

        board[Rank.ONE][2:-2] = rank_one_default_white
        board[Rank.EIGHT][2:-2] = rank_eight_default_black
        board[Rank.TWO][2:-2] = white_pawns
        board[Rank.SEVEN][2:-2] = black_pawns

        return board

    @classmethod
    def empty(cls):
        side_padding = [OutOfBounds, OutOfBounds]

        top_padding = [OutOfBounds] * 12
        empty_row = side_padding + [None] * 8 + side_padding
        return (
            [top_padding] + [top_padding]
            + [list(empty_row) for _ in range(8)]
            + [top_padding] + [top_padding]
        )

    @property
    def projection(self):
        return [row[2:-2] for row in self.board[2:-2]]

    def is_empty(self, position):
        square = self.board[position.rank][position.file]
        return square is None

    def is_out_of_bounds(self, position):
        square = self.board[position.rank][position.file]
        return square is OutOfBounds

    def is_in_bounds(self, position):
        return not self.is_out_of_bounds(position)

    @method_dispatch
    def are_enemies(self, pos1, pos2):
        pass

    @are_enemies.register
    def _(self, pos1: Position, pos2: Position):
        piece1 = self.board[pos1.rank][pos1.file]
        piece2 = self.board[pos2.rank][pos2.file]

        return piece1.color != piece2.color

    @are_enemies.register
    def _(self, color: FigureColor, pos2: Position):
        piece = self.board[pos2.rank][pos2.file]

        return color != piece.color

    def __getitem__(self, key):
        return self.board[key]

    def _get_position_in_single_direction(self, start_pos, direction):
        rank, file = start_pos.rank, start_pos.file

        delta_rank = delta_file = None

        if direction in [Direction.UP, Direction.DOWN]:
            delta_rank, delta_file = direction, 0

        elif direction in [Direction.RIGHT, Direction.LEFT]:
            delta_rank, delta_file = 0, direction

        elif isinstance(direction, Diagonal):
            delta_rank, delta_file = direction.composites()

        curr_pos = Position(rank + delta_rank, file + delta_file)

        while self.is_in_bounds(curr_pos):
            yield Position(curr_pos.rank, curr_pos.file)

            curr_pos.rank += delta_rank
            curr_pos.file += delta_file

    def get_positions_in_direction(self, start_pos, *directions):
        if len(directions) == 1:
            return self._get_position_in_single_direction(start_pos, directions[0])

        return {
            direction: self._get_position_in_single_direction(start_pos, direction)
            for direction in directions
        }

    def get_attackers(self, start_pos: Position, color: FigureColor):
        all_directions = list(Diagonal) + list(Direction)
        attack_positions = []

        directions = self.get_positions_in_direction(start_pos, *all_directions)
        directions['Knight'] = pieces.knight.possible_positions(start_pos)

        for direction, positions in self.get_positions_in_direction(start_pos, *all_directions):
            for position in positions:
                if not board.is_empty(position):
                    if board.are_enemies(color, position):
                        yield position
                    break
                yield position

    def move(self, *, from_pos, to_pos):
        square = self[from_pos.rank][from_pos.file]

        legal_moves = square.generate_moves(self, from_pos)
        if to_pos not in legal_moves:
            raise ValueError('Illegal move')

        self[from_pos.rank][from_pos.file], self[to_pos.rank][to_pos.file] = \
            None, self[from_pos.rank][from_pos.file]
