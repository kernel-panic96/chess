import operator
import curses
import math

import controls as key_bindings


class SelectModal:
    def __init__(self, options):
        self.options = options
        self.max_option_len = max(map(len, map(operator.itemgetter(0), options)))
        self.max_option_len = int(math.ceil(self.max_option_len | 1))
        self.selected = 0

    def center(self, screen):
        win_max_y, win_max_x = screen.getmaxyx()
        win_center_x, win_center_y = win_max_x // 2, win_max_y // 2

        self.frame_x, self.frame_y = max(0, win_center_x - (self.max_option_len + 9) // 2), max(0, win_center_y - (len(self.options) - 1))

        self.top_x, self.top_y = self.frame_x + 2, self.frame_y + 1

    def __call__(self, screen):
        user_input = None
        curses.curs_set(0)
        self.center(screen)

        while True:

            if user_input in key_bindings.get('move_up'):
                self.selected = (self.selected - 1) % len(self.options)
            elif user_input in key_bindings.get('move_down'):
                self.selected = (self.selected + 1) % len(self.options)
            elif user_input in key_bindings.get('select'):
                break
            elif user_input == curses.KEY_RESIZE:
                self.center(screen)

            self._draw_frame(screen)
            self._draw(screen)

            user_input = screen.getch()

        curses.curs_set(1)
        return self.options[self.selected][1]

    def _draw_frame(self, screen):
        color_pair = curses.color_pair(3)
        header = 'Promotion'.center(self.max_option_len + 6, '-')
        screen.addstr(self.frame_y, self.frame_x, ' ' + header + '  ', color_pair)

        for i, _ in enumerate(self.options):
            screen.addstr(self.frame_y + i + 1, self.frame_x, '| ', color_pair)
            screen.addstr(self.frame_y + i + 1, self.frame_x + self.max_option_len + 6, ' |', color_pair)

        footer = '-' * (self.max_option_len + 6)
        screen.addstr(self.frame_y + len(self.options) + 1, self.frame_x, ' ' + footer + '  ', color_pair)

    def _draw(self, screen):
        marker_padding = '  '

        for i, opt in enumerate(self.options):
            color_pair = curses.color_pair(2) if i == self.selected else curses.color_pair(0)
            marker = '(x)' if i == self.selected else '( )'

            screen.addstr(self.top_y + i, self.top_x, marker + marker_padding, color_pair)
            screen.addstr(self.top_y + i, self.top_x + len(marker + marker_padding), opt[0].ljust(self.max_option_len), color_pair)
