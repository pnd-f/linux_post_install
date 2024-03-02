import sys
import subprocess


def get_python_version() -> tuple:
    version = sys.version_info.major, sys.version_info.minor
    return version


def is_valid_version(version: tuple) -> bool:
    return version[0] == 3 and version[1] >= 10


def suggest_install_python() -> None:
    # suggesting
    print(f'You are using the wrong version of Python - {sys.version}. '
          'For the installer to work, you have to use Python 3.10 or higher. '
          'Do you want to install Python 3.10?')
    answer = input('(y/yes/д/да for confirmation): ')
    if answer in ('y', 'yes', 'д', 'да'):
        pass
    else:
        print('exit!')
        exit(0)


def install_python() -> None:
    command = (
        'sudo apt install software-properties-common -y '
        '&& echo | sudo add-apt-repository ppa:deadsnakes/ppa '
        '&& sudo apt install python3.10 -y'
    )
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(e)


def is_exists_necessary_version():
    command = 'python3.10 -V'
    is_exists = False
    try:
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            is_exists = True
    except Exception as e:
        print(e)
    return is_exists


def re_run():
    command = 'python3.10 ./run.py'
    try:
        result = subprocess.run(command, shell=True, )
        if result.returncode != 0:
            raise Exception(result.returncode)
    except Exception as e:
        print(e)


def check_python_version() -> None:
    current_version = get_python_version()
    if not is_valid_version(current_version):
        if not is_exists_necessary_version():
            suggest_install_python()
            install_python()
        re_run()
    else:
        print('something went wrong... it should work! but...')
    exit(0)
