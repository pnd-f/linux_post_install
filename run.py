#!/usr/bin/env python3
try:
    from install_menu import InstallMenu
except SyntaxError as e:
    print(e)
    from python_work_around import check_python_version
    check_python_version()


def main():
    menu = InstallMenu(
        title='Welcome to the PNDF installer =) \\m/',
        hints='Press Space for select and Enter for install'
    )

    while menu.exit_index not in (selected_option_indices := menu.show_menu()):
        menu.show_selected_programs(selected_option_indices)
        menu.work_with_selected_program(selected_option_indices)
    print('closing...')


if __name__ == '__main__':
    main()
