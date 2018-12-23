from board import Board
from constants import FigureType, FigureColor

sym_table = {
    FigureType.PAWN: {
        FigureColor.BLACK: {
            'unicode': '♟',
            'ascii': 'p'
        },
        FigureColor.WHITE: {
            'unicode': '♙',
            'ascii': 'P'
        }
    },
    FigureType.BISHOP: {
        FigureColor.BLACK: {
            'unicode': '♝',
            'ascii': 'b'
        },
        FigureColor.WHITE: {
            'unicode': '♗',
            'ascii': 'B'
        }
    },
    FigureType.KNIGHT: {
        FigureColor.BLACK: {
            'unicode': '♞',
            'ascii': 'n'
        },
        FigureColor.WHITE: {
            'unicode': '♘',
            'ascii': 'N'
        }
    },
    FigureType.QUEEN: {
        FigureColor.BLACK: {
            'unicode': '♛',
            'ascii': 'q'
        },
        FigureColor.WHITE: {
            'unicode': '♕',
            'ascii': 'Q'
        }
    },
    FigureType.KING: {
        FigureColor.BLACK: {
            'unicode': '♚',
            'ascii': 'k'
        },
        FigureColor.WHITE: {
            'unicode': '♔',
            'ascii': 'K'
        }
    },
    FigureType.ROOK: {
        FigureColor.BLACK: {
            'unicode': '♜',
            'ascii': 'r'
        },
        FigureColor.WHITE: {
            'unicode': '♖',
            'ascii': 'R'
        }
    },
}

def square_to_str(square):
    if square is None:
        return '.'
    elif square == 'X':
        return 'X'
    else:
        return sym_table[square.type][square.color]['unicode']

def print_board(board):
    proj = board.projection

    print(' ', 'a b c d e f g h')
    for num_row, row in enumerate(board.projection):
        _row = [square_to_str(elem) for elem in row]

        print(8 - num_row, ' '.join(_row), 8 - num_row)
    print(' ', 'a b c d e f g h')

def main():
    board = Board.standard_configuration()

    print_board(board)


if __name__ == '__main__':
    main()
