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
    None: {
        'unicode': '',
        'ascii': '.'
    }
}


def square_to_str(square):
    if square is None:
        return '·'
    elif square == 'X':
        return 'X'
    else:
        return sym_table[square.type][square.color]['unicode']
