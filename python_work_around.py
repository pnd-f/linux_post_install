import re
import subprocess


def get_python_version() -> float:
    command = 'python3 -V'
    try:
        string_result = subprocess.check_output(command, shell=True, text=True)
        values_list = re.split(r'[ .]', string_result)
        main_version = float(f'{values_list[1]}.{values_list[2]}')
    except Exception as e:
        print('smth went wrong...', e)
        exit(0)
    return main_version


def is_valid_version(version: float) -> bool:
    return version < 3.10


def suggest_install_python(version: float) -> None:
    if not is_valid_version(version):
        # suggesting
        print(f'You are using the wrong version of Python {version}. '
              f'For the installer to work, you have to use Python 3.10. '
              f'Do you want to install Python 3.10.')
        answer = input('(y/yes/д/да for confirmation): ')
        if answer in ('y', 'yes', 'д', 'да'):
            install_python()
            print('successfully installed! Please restart program, should work =)')
        exit(0)


def install_python() -> None:
    command1 = (
        'sudo apt install software-properties-common -y '
        '&& sudo add-apt-repository ppa:deadsnakes/ppa '
        '&& sudo apt install python3.10 -y'
    )
    command2 = 'sudo apt install python3.10'
    try:
        subprocess.run(command1, shell=True)
        # subprocess.run(command2, shell=True)
    except Exception as e:
        print(e)


def check_python_version() -> None:
    version = get_python_version()
    suggest_install_python(version)
