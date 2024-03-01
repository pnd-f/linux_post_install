import os
import re
import subprocess

from color_menu import Menu, ColorMenu, FStyle
from program import ProgramState, ProgramMap
from settings import APPS_PATH, DEB_LIST, GENERAL_COMMANDS, APT_LIST, ARCHIVE_LIST


class InstallMenu(Menu):
    files: list[str]
    menu_options: list[str]
    general_commands: list[str] = GENERAL_COMMANDS
    max_option_len: int = 0

    program_map: dict[str, ProgramState]

    # print colors
    downloaded: str
    not_downloaded: str
    installed: str
    not_installed: str

    # gaps
    gap_len = 2

    def __init__(self,
                 *,  # wow wow wow polehche
                 path_with_programs: str = APPS_PATH,
                 apt_list: list['str'] = APT_LIST,
                 show_downloaded: bool = True,
                 show_installed: bool = True,
                 show_versions: bool = True,
                 **kwargs,
                 ):
        self.show_downloaded = show_downloaded
        self.show_installed = show_installed
        self.show_versions = show_versions

        if not os.path.exists(APPS_PATH):
            os.mkdir(APPS_PATH)

        self.files = os.listdir(path_with_programs)

        self.apt_list = apt_list
        self.program_lists = [DEB_LIST, ARCHIVE_LIST, self.apt_list]

        self.colors = ColorMenu()
        self.set_styling()

        self.__set_program_map(*self.program_lists)
        self.__merge_options(*self.program_lists)
        # create a copy for reassignment the menu options
        self.origin_menu_options = self.menu_options[:]

        self.__build_additional_columns()
        # adding general commands
        self.menu_options += self.general_commands

        self.select_all_index = self.menu_options.index('select all')
        self.exit_index = self.menu_options.index('exit')

        super().__init__(self.menu_options, colors=self.colors, **kwargs)

    def reassignment_menu_options(self):
        self.max_option_len = 0
        self.menu_options = self.origin_menu_options[:]
        self.__build_additional_columns()
        # adding general commands
        self.menu_options += self.general_commands
        self.update_invisible_options(self.menu_options)

    def set_styling(self):
        self.downloaded = f'{self.colors.GREEN}downloaded'
        self.not_downloaded = f'{self.colors.YELLOW}NOT downloaded'
        self.installed = f'{self.colors.GREEN}installed'
        self.not_installed = f'{self.colors.YELLOW}NOT installed'

    def __set_program_map(self, *args):
        self.program_map = {}
        for _list in args:
            for option in _list:
                self.program_map[option] = ProgramState(option)

    def set_max_option_len_from_args(self, *args: str):
        for elem in args:
            if self.colors.color_marker in elem:
                # rid off the len colors
                elem = re.sub('//[A-Z].*?//', '', elem)
            if len(elem) > self.max_option_len:
                self.max_option_len = len(elem)

    def __build_additional_columns(self):
        if self.show_downloaded:
            self.set_max_option_len_from_args(*self.menu_options)

            for i in range(len(self.menu_options)):
                if self.menu_options[i]:  # skip an empty options
                    self.__add_downloaded_column(i)

        if self.show_installed:
            self.set_max_option_len_from_args(*self.menu_options)

            for i in range(len(self.menu_options)):
                if self.menu_options[i]:  # skip an empty options
                    self.__add_installed_column(i)

        # TODO there according idea we should show menu async and when version ready show versions
        if self.show_versions:
            self.set_max_option_len_from_args(*self.menu_options)

            for i in range(len(self.menu_options)):
                if self.menu_options[i]:  # skip an empty options
                    self.__add_version_column(i)

    def __merge_options(self, *args: list) -> None:

        self.menu_options = []
        for program_list in args:
            if program_list:
                for program in program_list:
                    self.menu_options.append(program)
                self.menu_options.append('')

        # setting the indices for select all:
        for index, option in enumerate(self.menu_options):
            if option:
                self.indices_for_select_all.append(index)

    def __add_downloaded_column(self, i: int) -> None:
        if self.menu_options[i] in DEB_LIST + ARCHIVE_LIST:
            program = self.program_map[self.menu_options[i]]
            is_downloaded = program.is_downloaded(self.files)
            gap = ' ' * (self.max_option_len - len(self.menu_options[i]) + self.gap_len)
            self.menu_options[i] = (f'{self.menu_options[i]}{gap}'
                                    f'{self.downloaded if is_downloaded else self.not_downloaded}')

    def __add_installed_column(self, i: int) -> None:
        program_name = self.menu_options[i].split(maxsplit=1)[0]
        program = self.program_map[program_name]
        # TODO hard step should be async
        is_installed = program.is_installed()

        # rid off the len colors
        len_option = len(re.sub('//[A-Z].*?//', '', self.menu_options[i]))

        gap = ' ' * (self.max_option_len - len_option + self.gap_len)
        self.menu_options[i] = (
            f'{self.menu_options[i]}{gap}'
            f'{"unknown" if is_installed is None else self.installed if is_installed else self.not_installed}'
        )

    def __add_version_column(self, i: int) -> None:
        program_name = self.menu_options[i].split(maxsplit=1)[0]

        # TODO hard step, should be async, if version haven't calculated in installed column
        info = self.get_program_version(program_name)
        # rid off the len colors
        len_option = len(re.sub('//[A-Z].*?//', '', self.menu_options[i]))

        gap = ' ' * (self.max_option_len - len_option + self.gap_len)
        self.menu_options[i] = (
            f'{self.menu_options[i]}{gap}'
            f'{info if info else ""}'
        )

    def get_program_version(self, program: str) -> str | None:
        """
        check is program installed
        """
        program_state: ProgramState = self.program_map.get(program)
        if program_state is not None:
            try:
                return program_state.version
            except (subprocess.CalledProcessError, Exception) as e:
                if e.returncode == 1 and e.stderr == '' and program_state.check_command.startswith('dpkg -l | grep'):
                    pass  # the case when we can't find the program in dpkg manager, but it is not issue
                else:
                    print(f'{FStyle.RED}Warning!!! {program} version issue!\n'
                          f'"{program_state.check_command}" <-\n'
                          f'{e.stderr}{FStyle.RESET_ALL}')

        return None

    def show_selected_programs(self, selected_option_indices: set[int]):
        print(f'{FStyle.YELLOW}You have selected:{FStyle.GREEN}\n')
        if self.select_all_index in selected_option_indices:
            print(f'{self.menu_options_backup[self.select_all_index]}:\n')
            for index, menu_option in enumerate(self.menu_options_backup):
                if menu_option and menu_option not in self.general_commands:
                    print(f'{FStyle.GREEN} ● {menu_option.split(maxsplit=1)[0]}{FStyle.RESET_ALL}')
        else:
            [print(' ● ', self.menu_options_backup[i].split(maxsplit=1)[0]) for i in selected_option_indices]

        print(f'{FStyle.RESET_ALL}')

    def work_with_selected_program(self, selected_option_indices: set[int]) -> None:
        if self.select_all_index in selected_option_indices:
            selected_option_indices.remove(self.select_all_index)

        for i in selected_option_indices:
            program_name: str = self.menu_options_backup[i].split(maxsplit=1)[0]
            print(f'{FStyle.YELLOW}Working on {FStyle.GREEN}{program_name}{FStyle.RESET_ALL}\n')
            self.install_program(program_name)
            print(f'{FStyle.YELLOW}Finished with {program_name}{FStyle.RESET_ALL}\n')

        ProgramMap.finishing_touches()

    def install_program(self, name: str) -> None:
        program = self.program_map.get(name)
        if program is not None:
            program.download_and_install()
            self.reassignment_menu_options()
        else:
            print(f'{FStyle.RED}unknown program{FStyle.RESET_ALL}')
