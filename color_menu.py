import re
from curses import wrapper
import curses


class FStyle:
    """stylize simple prints"""

    # font color
    BLACK: str = '\033[30m'
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    BLUE: str = '\033[34m'
    MAGENTA: str = '\033[35m'
    CYAN: str = '\033[36m'
    GREY: str = '\033[37m'

    # background color
    B_BLACK: str = '\033[40m'
    B_RED: str = '\033[41m'
    B_GREEN: str = '\033[42m'
    B_YELLOW: str = '\033[43m'
    B_BLUE: str = '\033[44m'
    B_MAGENTA: str = '\033[45m'
    B_CYAN: str = '\033[46m'
    B_GREY: str = '\033[47m'

    # style
    BOLD: str = '\033[1m'
    ITALIC: str = '\033[3m'
    UNDERLINE: str = '\033[4m'

    RESET_ALL: str = '\033[0m'

    hide_cursor: str = '\033[?25l'
    show_cursor: str = '\033[?25h'

    # Control structures
    go_to_up_screen = '\033[H'
    clear_row_after = '\033[K'

    full_symbol = '\u2588'
    empty_symbol = '\u2591'

    go_to_up_row = '\033[F'


class ColorMenu:
    """
    Allows you to use colors in menu.
    If you want to change the beginning and ending of special characters,
    create your own instance of the class.
    """
    GREEN: str = '//GREEN//'
    YELLOW: str = '//YELLOW//'
    RED: str = '//RED//'
    ZERO_COLOR: str = '//ZERO_COLOR//'

    def __init__(self,
                 color_marker: str = '//',
                 ):
        self.color_marker = color_marker
        self.GREEN = f'{self.color_marker}GREEN{self.color_marker}'
        self.YELLOW = f'{self.color_marker}YELLOW{self.color_marker}'
        self.RED = f'{self.color_marker}RED{self.color_marker}'
        self.ZERO_COLOR = f'{self.color_marker}ZERO{self.color_marker}'

        self.COLORS = [self.GREEN, self.YELLOW, self.RED, self.ZERO_COLOR]
        self.pattern = re.compile(f'{"|".join(self.COLORS)}')

    def get_color_int(self, color: str) -> int:
        colors_dict = {
            self.GREEN: 97,
            self.YELLOW: 98,
            self.RED: 99,
            self.ZERO_COLOR: 80,
        }
        return colors_dict[color]

    def init_color_pairs(self, scr):
        # should be called after receiving the screen
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(self.get_color_int(self.GREEN), curses.COLOR_GREEN, curses.ERR)
        curses.init_pair(self.get_color_int(self.YELLOW), curses.COLOR_YELLOW, curses.ERR)
        curses.init_pair(self.get_color_int(self.RED), curses.COLOR_RED, curses.ERR)
        curses.init_pair(self.get_color_int(self.ZERO_COLOR), curses.COLOR_WHITE, curses.ERR)


class Menu:
    # special codes
    SPACE = ord(' ')
    QUIT = ord('q')

    magic_number = 3  # rows: title, empty string, hints

    x: int = 0
    y: int = 0
    max_x: int
    max_y: int

    select_all_index: int = -1
    indices_for_select_all: list[int] = []

    def __init__(self,
                 menu_options: list[str],
                 *,
                 title: str = 'Your Title!',
                 hints: str = 'Your Hints!',
                 pointer: str = '>',
                 selector: str = '*',
                 colors: ColorMenu = ColorMenu(),
                 ):
        self.menu_options = [str(x) for x in menu_options]  # avoid int and etc
        self.menu_options_backup = self.menu_options[:]

        self.title = title
        self.hints = hints
        self.pointer = pointer
        self.position = 0
        self.menu_offset = 0

        self.selector = selector

        # for selected program
        self.indices = set()

        self.colors = colors

    def show_menu(self):
        wrapper(self.__show_menu)
        return self.indices

    def __show_menu(self, stdscr) -> None:
        def draw_menu():
            stdscr.clear()
            self.x = 0
            self.y = 0
            self.max_y, self.max_x = stdscr.getmaxyx()

            # show title
            stdscr.addstr(self.y, self.x + 1, self.title, curses.color_pair(1))
            self.y += 1
            # show hints
            try:
                stdscr.addstr(self.max_y, self.x + 1, self.hints, curses.color_pair(1))
            except:  # it is not always possible to draw something in the last line / for debug???
                self.max_y -= 1
                stdscr.addstr(self.max_y, self.x + 1, self.hints, curses.color_pair(1))

            # menu start not form first line -> 3
            if len(self.menu_options) > self.max_y - self.magic_number:
                # cut screen
                self.menu_options = self.menu_options[self.menu_offset:self.max_y - self.magic_number + self.menu_offset]

            # this is in case someone really wants to start their lists from empty positions...
            after_start = False
            start_offset = 0

            for index, option in enumerate(self.menu_options):
                self.y += 1
                if option == '' or option is None:

                    # the continuation of the case with empty positions at the beginning
                    if not after_start and self.position - start_offset == 0:
                        self.position += 1
                        start_offset += 1

                    continue
                # quantity of columns depends on type program, if it is file -3 , apt -2
                # column_quantity = self.__get_column_quantity(option)
                after_start = True
                self.__form_string(stdscr, index, option)

            stdscr.refresh()

        curses.use_default_colors()
        curses.curs_set(0)  # hide the cursor

        self.colors.init_color_pairs(stdscr)

        draw_menu()  # first time

        def one_step_above_horizont():
            # if it is top of menu
            if self.position + self.menu_offset == 0:
                self.position = len(self.menu_options) - 1
                self.menu_offset = len(self.menu_options_backup) - len(self.menu_options)
                self.menu_options = self.menu_options_backup[self.menu_offset:]
            elif len(self.menu_options) == len(self.menu_options_backup):
                self.position -= 1
            else:  # if it is not top menu
                self.menu_options = self.menu_options[:-1]
                self.menu_options.insert(0, self.menu_options_backup[self.menu_offset - 1])
                self.menu_offset -= 1

        def one_step_below_horizont():
            if self.position + self.menu_offset == len(self.menu_options_backup) - 1:
                self.position = 0
                self.menu_offset = 0
                self.menu_options = self.menu_options_backup[:self.max_y]
            elif len(self.menu_options) == len(self.menu_options_backup):
                self.position += 1
            else:  # len(self.menu_options) < len(self.menu_options_backup)
                # rewrite visible options
                self.menu_offset += 1
                self.menu_options = self.menu_options[1:]
                self.menu_options.append(self.menu_options_backup[len(self.menu_options) + self.menu_offset])

        while True:
            key = stdscr.getch()
            match key:
                # moving
                # up
                case curses.KEY_UP if self.position == 0:
                    one_step_above_horizont()
                case curses.KEY_UP if self.position > 0:
                    self.position -= 1
                    while self.__is_empty_position():
                        one_step_above_horizont()

                # down
                case curses.KEY_DOWN if self.position == len(self.menu_options) - 1:
                    one_step_below_horizont()
                case curses.KEY_DOWN if self.position < len(self.menu_options) - 1:
                    self.position += 1
                    while self.__is_empty_position():
                        one_step_below_horizont()

                # mark
                case self.SPACE:
                    # if selected select_all option
                    if self.is_select_all_selected():
                        self.work_with_select_all()
                    else:
                        # usual case
                        if self.position + self.menu_offset in self.indices:
                            self.indices.remove(self.position + self.menu_offset)
                        else:
                            self.indices.add(self.position + self.menu_offset)
                        # checking for select_all if we selected others elements
                        if self.indices == set(self.indices_for_select_all):
                            self.indices.add(self.select_all_index)
                        else:
                            # safety removing
                            self.indices.discard(self.select_all_index)

                # select
                case curses.KEY_ENTER | 10:
                    return
                case self.QUIT:
                    exit(0)  # break

            draw_menu()

    def __form_string(self, stdscr, index: int, option: str):
        # pointer
        self.x += 1
        stdscr.addstr(self.y, self.x, (" ", self.pointer)[index == self.position])

        # selector
        self.x += 2
        stdscr.addstr(self.y, self.x, f'[{(" ", self.selector)[index + self.menu_offset in self.indices]}]')

        # cut string, ibo nefig
        _, self.max_x = stdscr.getmaxyx()
        option = option[:self.max_x]

        # option
        self.x += 4
        if colors := self.colors.pattern.findall(option):
            for i in range(len(colors)):
                color_int = self.colors.get_color_int(colors[i])
                color_position = option.index(colors[i])
                if color_position > 0:  # there is simple text before colors
                    simple_print = option[:color_position]
                    stdscr.addstr(self.y, self.x, simple_print,
                                  (curses.color_pair(0), curses.A_REVERSE)[index == self.position])
                    self.x += len(simple_print)
                    option = option[len(simple_print):]

                current_color = colors[i]
                start_position = len(current_color)
                if i < len(colors) - 1:  # if there is next color
                    next_color = colors[i + 1]
                    end_position = option[start_position:].index(next_color) + start_position
                else:
                    next_color = ''
                    end_position = len(option)
                color_print = option[start_position:end_position]

                stdscr.addstr(self.y, self.x, color_print,
                              (curses.color_pair(color_int), curses.A_REVERSE)[index == self.position])
                self.x += len(color_print)

                option = option[start_position + len(color_print):]

        else:
            stdscr.addstr(self.y, self.x, option, (curses.color_pair(0), curses.A_REVERSE)[index == self.position])

        self.x = 0
        stdscr.refresh()

    def __is_empty_position(self) -> bool:
        return bool(self.menu_options_backup[self.position + self.menu_offset] == ''
                    or self.menu_options_backup[self.position + self.menu_offset] is None)

    def is_select_all_selected(self):
        return bool(self.select_all_index != -1
                    and self.indices_for_select_all
                    and self.position + self.menu_offset == self.select_all_index)

    def work_with_select_all(self):
        if self.position + self.menu_offset in self.indices:
            self.indices.clear()
        else:
            self.indices.add(self.position + self.menu_offset)
            self.indices.update(self.indices_for_select_all)

    def update_invisible_options(self, new_menu_options_backup: list) -> None:
        self.menu_options_backup = new_menu_options_backup[:]
