import subprocess
from abc import ABC, abstractmethod

from color_menu import FStyle


class CommonProgram(ABC):
    title: str
    check_version_cmd: str
    result_indices: list

    # commands
    dpkg_install_command = 'sudo dpkg -i apps/{}'
    apt_install_command = 'sudo apt install {} -y'
    apt_autoremove = 'sudo apt autoremove -y'
    apt_fix_broken = 'sudo apt --fix-broken install -y'

    @property
    @abstractmethod
    def install_cmd(self) -> str:
        """must be redefined"""

    def __init__(self):
        # fields that must be redefined
        fields_for_check = {
            'title',
            'check_version_cmd',
            'result_indices',
        }
        for field in fields_for_check:
            if not getattr(self, field):
                raise NotImplementedError(f"Children class must redefine {field}")

    def get_version(self) -> list[str]:
        try:
            result = subprocess.check_output(self.check_version_cmd, shell=True, text=True, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, Exception) as e:
            if e.returncode == 1 and e.stderr == '' and self.check_version_cmd.startswith('dpkg -l | grep'):
                pass  # the case when we can't find the program in dpkg manager, but it is not issue
            elif e.returncode == 127 and f'{self.check_version_cmd.split(maxsplit=1)[0]}: not found' in e.stderr:
                pass  # the case when the program not found, usual -> not installed
            else:
                print(f'{FStyle.RED}Warning!!! Version issue!\n'
                      f'"{self.check_version_cmd}" <-\n'
                      f'{e.stderr}{FStyle.RESET_ALL}')
            result = ''
        result_atr = result.split()
        return result_atr

    def install(self, arg: str) -> None:
        """
        Installs a package or a file.
        Args:
            arg (str): The name of the file or the apt package title.
        Returns:
            None
        """
        command = self.install_cmd.format(arg)
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print(f'\n{FStyle.GREEN}SUCCESSFUL!!!{FStyle.RESET_ALL}\n')
        else:
            print(f'\n{FStyle.RED}SOMeTHING WENT WRONG!!!{FStyle.RESET_ALL}\n')
            print(f'{FStyle.YELLOW}Trying to fix it...{FStyle.RESET_ALL}\n')
            self.execute(self.apt_fix_broken)
        self.execute(self.apt_autoremove)

    @staticmethod
    def execute(command: str):
        return subprocess.run(command, shell=True)

    @staticmethod
    def finishing_touches():
        commands = '''sudo apt update -y
        sudo apt upgrade -y
        # repair dependency
        sudo apt install -y -f
        # removing unnecessary packages, cleaning the APT cache
        sudo apt autoremove -y
        sudo apt-get autoclean -y'''
        try:
            subprocess.run(args=commands, shell=True)
        except Exception as e:
            print(e)
