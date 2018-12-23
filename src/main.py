from chess_pieces.pawn import Pawn
from constants import FigureColor, Rank, File
from chess_pieces import all as pieces
from board import Board
from pprint import pprint

board = Board()
pawn = board[Rank.TWO][File.A]
moves = pawn.generate_moves(board)
import ipdb;ipdb.set_trace()
print(*map(str, pawn.generate_moves(board)))
print(pawn.generate_moves(board))
