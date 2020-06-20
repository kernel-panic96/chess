import contextlib
import functools as fp
import math
from copy import deepcopy
from typing import Generator, Union, Dict, Iterator, Iterable, overload

from chess.pieces import *
from chess.constants import CastlingPerm
from chess.constants import Diagonal, Direction
from chess.constants import FigureColor as Color, FigureType as Type
from chess.constants import Rank, File
from chess.position import Position
from chess.utils import method_dispatch

from functional import seq


class OutOfBounds:
    def __repr__(self):
        return 'x'


OutOfBounds = OutOfBounds()


class _BoardAwareList(list):
    def __setitem__(self, key, value):
        if hasattr(value, 'figure_type') and value.figure_type is Type.KING:
            self.board.kings[value.color] = Position(self.rank, key)

        super().__setitem__(key, value)


def _maybe_castle(func):
    @fp.wraps(func)
    def wrapper(board, *, from_pos: Position, to_pos: Position):
        res = func(board, from_pos=from_pos, to_pos=to_pos)

        square = board[to_pos.rank][to_pos.file]

        if getattr(square, 'figure_type', None) is Type.KING:
            board.castling_perms[square.color] = CastlingPerm.NONE

            if from_pos.dist(to_pos) == 2:  # Castling -> Move rook
                direction = from_pos.relative_direction_towards_position(to_pos)

                if direction is Direction.LEFT:
                    board._castle_move_rook(square.color, CastlingPerm.QUEEN_SIDE)
                else:
                    board._castle_move_rook(square.color, CastlingPerm.KING_SIDE)

        return res

    return wrapper


def _set_or_clear_en_passant(func):
    @fp.wraps(func)
    def wrapper(board, *, from_pos: Position, to_pos: Position):
        res = func(board, from_pos=from_pos, to_pos=to_pos)

        square = board[to_pos.rank][to_pos.file]

        if to_pos == board.en_passant_pos:  # capture(delete) the pawn
            if hasattr(square, 'figure_type') and square.figure_type is Type.PAWN:
                board[from_pos.rank][to_pos.file] = None

        if hasattr(square, 'figure_type') and square.figure_type is Type.PAWN and from_pos.dist(to_pos) == 2:
            direction = square.color.forward_direction
            board.en_passant_pos = Position(to_pos.rank - direction, to_pos.file)
        else:
            board.en_passant_pos = None

        return res

    return wrapper


def _promote_if_necessary(func):
    @fp.wraps(func)
    def wrapper(board, *, from_pos: Position, to_pos: Position):
        res = func(board, from_pos=from_pos, to_pos=to_pos)
        square = board[to_pos.rank][to_pos.file]

        if hasattr(square, 'figure_type') and square.figure_type is Type.PAWN:
            last_rank = Rank.EIGHT if square.color == Color.WHITE else Rank.ONE

            if to_pos.rank == last_rank:
                piece_cls = board.promotion_cb()

                board[to_pos.rank][to_pos.file] = piece_cls(
                    square.color,
                )

        return res

    return wrapper


class Board:
    def __init__(self, promotion_cb=None):
        self.board = self.empty()
        self.player, self.enemy = Color.WHITE, Color.BLACK
        self.en_passant_pos = None
        self.promotion_cb = promotion_cb

        self.castling_perms = {
            Color.WHITE: CastlingPerm.ALL,
            Color.BLACK: CastlingPerm.ALL
        }

        for rank in reversed(Rank):
            self.board[rank].board = self
            self.board[rank].rank = rank

        self.kings = {
            Color.WHITE: None,
            Color.BLACK: None,
        }

    @classmethod
    def standard_configuration(cls):
        board = cls()

        BlackPawn = fp.partial(Pawn, Color.BLACK)
        WhitePawn = fp.partial(Pawn, Color.WHITE)

        main_rank = seq(Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

        padding = 2
        board[Rank.ONE][padding:-padding]   = main_rank.map(lambda kls: kls(Color.WHITE)).list()
        board[Rank.EIGHT][padding:-padding] = main_rank.map(lambda kls: kls(Color.BLACK)).list()
        board[Rank.TWO][padding:-padding]   = main_rank.map(lambda _: WhitePawn()).list()
        board[Rank.SEVEN][padding:-padding] = main_rank.map(lambda _: BlackPawn()).list()

        board.kings = {
            Color.BLACK: Position(Rank.EIGHT, File.E),
            Color.WHITE: Position(Rank.ONE, File.E),
        }

        board.player, board.enemy = Color.WHITE, Color.BLACK

        board.castling_perms[Color.WHITE] = CastlingPerm.ALL
        board.castling_perms[Color.BLACK] = CastlingPerm.ALL

        board.en_passant_pos = None

        return board

    def set_square(self, obj, rank: Rank, file: File) -> None:
        if hasattr(obj, 'figure_type') and obj.figure_type is Type.KING:
            self.kings[obj.color] = Position(Rank, File)

        self.board[rank][file] = obj

    @classmethod
    def empty(cls):
        side_padding = [OutOfBounds, OutOfBounds]

        top_padding = [OutOfBounds] * 12
        empty_row = side_padding + [None] * 8 + side_padding
        return (
            [top_padding] + [top_padding]
            + [_BoardAwareList(empty_row, rank=rank) for rank in reversed(Rank)]
            + [top_padding] + [top_padding]
        )

    @classmethod
    def from_fen_file(cls, fname: str):
        with open(fname) as file_handle:
            return cls.from_fen(file_handle.readline())

    fen_lookup_table = {
        'N': Knight,
        'K': King,
        'B': Bishop,
        'R': Rook,
        'P': Pawn,
        'Q': Queen
    }

    # XXX: For now half_move_clock and full_move_clock
    #  are ignored
    @classmethod
    def from_fen(cls, fen: str):
        fen_board, active_side, castling, en_passant, _, _ = fen.split()

        board = cls()
        board.player = Color.WHITE if active_side.lower() == 'w' else Color.BLACK
        board.enemy = Color.BLACK if active_side.lower() == 'w' else Color.WHITE

        for rank, row in zip(reversed(Rank), fen_board.split('/')):
            col_i = 0

            for char in row:
                if char.upper() in cls.fen_lookup_table:
                    piece_class = cls.fen_lookup_table[char.upper()]

                    color = Color.WHITE if char.isupper() else Color.BLACK

                    p_file = File.from_str(chr(col_i + ord('a')))
                    piece = piece_class(color)
                    board[rank][p_file] = piece

                    if char.upper() == 'K':
                        board.kings[color] = Position(rank, p_file)

                    col_i += 1

                else:
                    count_empty = int(char)
                    col_i += count_empty

        board.castling_perms[Color.WHITE] = CastlingPerm.NONE
        board.castling_perms[Color.BLACK] = CastlingPerm.NONE

        board.castling_perms[Color.WHITE] |= int('K' in castling) << int(math.log2(CastlingPerm.KING_SIDE))
        board.castling_perms[Color.WHITE] |= int('Q' in castling) << int(math.log2(CastlingPerm.QUEEN_SIDE))
        board.castling_perms[Color.BLACK] |= int('k' in castling) << int(math.log2(CastlingPerm.KING_SIDE))
        board.castling_perms[Color.BLACK] |= int('q' in castling) << int(math.log2(CastlingPerm.QUEEN_SIDE))

        if en_passant != '-':
            board.en_passant_pos = Position.from_str(en_passant)

        return board

    @classmethod
    def from_strings(cls, inp: Iterable[str]):
        '''Creates a board from list of string.
        Used in testing

        >>> board = Board.from_strings([
        ...     "........",
        ...     ".p......",
        ...     "........",
        ...     "........",
        ...     "........",
        ...     "........",
        ...     ".P......",
        ...     "........"
        ... ])
        >>> board[Rank.TWO][File.B]
        White Pawn

        '''

        lookup = {
            'N': fp.partial(Knight, Color.WHITE),
            'K': fp.partial(King,   Color.WHITE),
            'B': fp.partial(Bishop, Color.WHITE),
            'R': fp.partial(Rook,   Color.WHITE),
            'P': fp.partial(Pawn,   Color.WHITE),
            'Q': fp.partial(Queen,  Color.WHITE),

            'n': fp.partial(Knight, Color.BLACK),
            'k': fp.partial(King,   Color.BLACK),
            'b': fp.partial(Bishop, Color.BLACK),
            'r': fp.partial(Rook,   Color.BLACK),
            'p': fp.partial(Pawn,   Color.BLACK),
            'q': fp.partial(Queen,  Color.BLACK),

            '.': lambda: None
        }
        projection = seq(inp).flatten().map(lambda c: lookup[c]()).grouped(8).to_list()
        board = cls()
        for r, res in zip(list(Rank), reversed(projection)):
            for f, obj in zip(File, res):
                board.set_square(obj, rank=r, file=f)
        return board

    def next_turn(self):
        self.player, self.enemy = self.enemy, self.player

    @property
    def projection(self):
        """
        Returns 8x8 representation, the internal representation
        need not be 8x8. So use this or index the board with constants.Rank & File

        """
        return [row[2:-2] for row in self.board[2:-2]]

    def is_empty(self, position: Position):
        square = self.board[position.rank][position.file]
        return square is None

    def is_out_of_bounds(self, pos: Position):
        square = self.board[pos.rank][pos.file]
        return type(square) is type(OutOfBounds)

    def is_in_bounds(self, pos: Position):
        return not self.is_out_of_bounds(pos)

    @method_dispatch
    def are_enemies(self, pos1, pos2):  # pragma: no cover
        pass

    @are_enemies.register
    def _(self, pos1: Position, pos2: Position) -> bool:
        piece1 = self.board[pos1.rank][pos1.file]
        piece2 = self.board[pos2.rank][pos2.file]

        return piece1 and piece2 and piece1.color != piece2.color

    @are_enemies.register
    def _(self, color: Color, pos2: Position) -> bool:
        piece = self.board[pos2.rank][pos2.file]

        return piece and color != piece.color

    def __getitem__(self, key: Union[int, Rank]):
        return self.board[key]

    def _get_position_in_single_direction(
        self,
        start_pos: Position,
        direction: Union[Direction, Diagonal]
    ) -> Generator[Position, None, None]:
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

    def get_positions_in_direction(
        self,
        start_pos: Position,
        *directions: Union[Direction, Diagonal]
    ) -> Dict[Union[Direction, Diagonal], Iterator[Position]]:
        if len(directions) == 1:
            return self._get_position_in_single_direction(start_pos, directions[0])

        return {
            direction: self._get_position_in_single_direction(start_pos, direction)
            for direction in directions
        }

    def get_attackers(
        self,
        start_pos: Position,
        color: Color
    ) -> Generator[Position, None, None]:
        all_directions = list(Diagonal) + list(Direction)

        positions_by_dir = self.get_positions_in_direction(start_pos, *all_directions)
        positions_by_dir['Knight'] = filter(self.is_in_bounds, Knight.possible_positions(start_pos))

        for direction, positions in positions_by_dir.items():
            for position in positions:
                if not self.is_empty(position):
                    if self.are_enemies(color, position):
                        piece = self.board[position.rank][position.file]
                        piece_type = piece.figure_type

                        if direction in Diagonal and piece_type in [Type.BISHOP, Type.QUEEN]:
                            yield position

                        elif direction in Direction and piece_type in [Type.ROOK, Type.QUEEN]:
                            yield position

                        elif direction == 'Knight' and piece_type is Type.KNIGHT:
                            yield position

                        elif piece_type is Type.KING and start_pos.dist(position) == 1:
                            yield position

                        elif piece_type is Type.PAWN:
                            direction = Direction.DOWN if piece.color == Color.WHITE else Direction.UP
                            pawn_positions = {
                                Position(rank=start_pos.rank + direction, file=start_pos.file + Direction.RIGHT),
                                Position(rank=start_pos.rank + direction, file=start_pos.file + Direction.LEFT)
                            }
                            if position in pawn_positions:
                                yield position

                    if direction != 'Knight':
                        break

    def _castle_move_rook(self, color: Color, side: CastlingPerm) -> None:
        rank = Rank.ONE if color is Color.WHITE else Rank.EIGHT

        if side is CastlingPerm.QUEEN_SIDE:
            from_pos = Position(rank, File.A)
            to_pos = Position(rank, File.D)
        else:
            from_pos = Position(rank, File.H)
            to_pos = Position(rank, File.F)

        self.move(from_pos=from_pos, to_pos=to_pos)

    @_promote_if_necessary
    @_maybe_castle
    @_set_or_clear_en_passant
    def move(self, *, from_pos: Position, to_pos: Position) -> None:
        """
        Move whatever is in `from_pos` to `to_pos`.
        move() is permissive it won't deny a move or check for it's validity.
        It also doesn't care about who's turn is it.
        """
        square = self[from_pos.rank][from_pos.file]

        assert square is not None and square is not OutOfBounds
        # assert to_pos in square.generate_moves(self, from_pos)  # potentially
        # expensive, hence the commenting out

        if square.figure_type is Type.ROOK:
            if self.castling_perms[square.color]:
                if from_pos.file == File.A:
                    remove_mask = ~CastlingPerm.KING_SIDE
                elif from_pos.file == File.H:
                    remove_mask = ~CastlingPerm.QUEEN_SIDE
                else:
                    remove_mask = ~CastlingPerm.NONE

                self.castling_perms[square.color] &= remove_mask

        self.set_square(self[from_pos.rank][from_pos.file], to_pos.rank, to_pos.file)
        self.set_square(None, from_pos.rank, from_pos.file)

    def shallow_copy(self, board) -> None:
        self.__dict__.update(board.__dict__)
        # self.board = board.board
        # self.kings = board.kings
        # self.player, self.enemy = board.player, board.enemy
        # self.castling_perms = board.castling_perms
        # self.en_passant_pos = board.en_passant_pos

    @contextlib.contextmanager
    def temporarily_remove_position(self, *positions):
        cache = [self[p.rank][p.file] for p in positions]

        for p in positions:
            self[p.rank][p.file] = None
        try:
            yield
        finally:
            for piece, pos in zip(cache, positions):
                self[pos.rank][pos.file] = piece

    def is_able_to_castle(self, color: Color, castling_side: CastlingPerm):
        '''
        The necessary conditions are:

        1) A king may not castle if the file is blocked.
        2) A king may not castle if he or the chosen rook has previously moved. (not checked here)
        3) A king may not move if he is, will be or passes through a check.

        '''

        if not self.castling_perms[color] & castling_side:
            return False

        king_pos = self.kings[color]
        king = self.board[king_pos.rank][king_pos.file]

        if king.is_in_check(self, king_pos):
            return False

        queen_side = castling_side == CastlingPerm.QUEEN_SIDE
        direction = Direction.LEFT if queen_side else Direction.RIGHT

        castling_target_file = File.C if queen_side else File.G
        target_file = File.A if queen_side else File.H

        ps = seq(self.get_positions_in_direction(king_pos, direction))\
            .take_while(self.is_empty)
        ps += seq(self.get_positions_in_direction(king_pos, direction))\
            .drop_while(self.is_empty).take(1)

        last_pos = ps[-1] if ps else None

        # the predicates are wrapped in lambdas because laziness is desired
        predicates = seq(
            lambda: bool(ps),
            lambda: last_pos.file == target_file,
            lambda: not self.is_empty(last_pos),
            lambda: self[last_pos.rank][last_pos.file].figure_type == Type.ROOK,
            lambda: not self.are_enemies(king_pos, last_pos),
            lambda: ps.take(2).map(lambda p: not king.is_in_check(self, p)).all()
        )

        return predicates.map(lambda f: f()).all()
