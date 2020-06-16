import unittest

from chess.pieces import (
    King, Bishop, Rook, Pawn, Queen, Knight
)
from chess.constants import FigureColor as Color


class TestIsEnemy(unittest.TestCase):
    def test_all_figures_should_be_enemies_of_the_opposite_color(self):
        figures = [King, Bishop, Rook, Pawn, Queen, Knight]
        white_figures = [figure(color=Color.WHITE) for figure in figures]
        black_figures = [figure(color=Color.BLACK) for figure in figures]

        for white in white_figures:
            for black in black_figures:
                self.assertTrue(
                    white.is_enemy(black),
                    msg=f'white {white.type} was not enemy to black {black.type}'
                )
                self.assertTrue(
                    black.is_enemy(white),
                    msg=f'black {black.type} was not enemy to white {white.type}'
                )
