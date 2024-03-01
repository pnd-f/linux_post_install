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
            pass
        else:
            exit(0)


def install_python() -> None:
    command = (
        'sudo apt install software-properties-common -y '
        '&& sudo add-apt-repository ppa:deadsnakes/ppa '
        '&& sudo apt install python3.10 -y'
    )
    try:
        subprocess.run(command, shell=True)
        # subprocess.run(command2, shell=True)
    except Exception as e:
        print(e)


def check_necessary():
    command = 'python3.10 -V'
    is_exists = False
    try:
        subprocess.run(command, shell=True)
        is_exists = True
    except Exception as e:
        print(e)
    return is_exists

def re_run():
    command = 'python3.10 ./run.py'
    try:
        subprocess.run(command, shell=True, )
    except Exception as e:
        print(e)


def check_python_version() -> None:
    current_version = get_python_version()
    is_exists_necessary_version = check_necessary()
    if not is_exists_necessary_version:
        suggest_install_python(current_version)
        install_python()
    re_run()

