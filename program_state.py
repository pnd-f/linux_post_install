import json
import os
import subprocess

from programs.apt.git import Git
from programs.apt.htop import Htop
from programs.apt.python3pip import Python3Pip
from programs.apt.virtualenv import Virtualenv
from programs.apt.xz_utils import XzUtils
from programs.dpkg.chrome import Chrome
from programs.apt.curl import Curl
from programs.dpkg.dbeaver import DBeaver
from programs.dpkg.insomnia import Insomnia
from programs.dpkg.microsoft_edge import MicrosoftEdge
from programs.dpkg.mongodb_compass import MongodbCompass
from programs.dpkg.slack_desktop import Slack
from programs.dpkg.sublime import Sublime
from color_menu import FStyle
from download_with_progres import AnimationDownloader
from programs.dpkg.viber import Viber
from programs.dpkg.virtualbox import Virtualbox
from programs.dpkg.vscode import Code
from programs.dpkg.zoom import Zoom
from programs.others.docker import Docker
from settings import APPS_PATH


class ProgramMap:
    class UrlMap:
        # put a logic to find the latest version
        @staticmethod
        def get_pycharm_professional() -> str:
            return 'https://download.jetbrains.com/product?code=PC&latest&distribution=linux'

        @staticmethod
        def get_pycharm_community() -> str:
            return 'https://download.jetbrains.com/product?code=PCC&latest&distribution=linux'


    @staticmethod
    def get_pycharm_version(pycharm_type: str) -> list[str]:
        versions = []
        home_dir = os.path.expanduser('~')
        # we don't check the cache
        # checking if the directory apps exists
        apps = os.path.join(home_dir, APPS_PATH)
        if not os.path.exists(apps):
            return versions
        start_folder_map = {'pro': 'pycharm-202', 'community': 'pycharm-community-202'}
        start_folder_name = start_folder_map[pycharm_type]
        pycharm_folders = [folder for folder in os.listdir(apps) if folder.startswith(start_folder_name)]
        for folder in pycharm_folders:
            # truing to get version from each folder
            goal_file = os.path.join(apps, folder, 'product-info.json')
            if os.path.exists(goal_file):
                with open(goal_file, 'r') as f:
                    json_data = f.read()
                    data = json.loads(json_data)
                    version = data['version']
                    versions.append(version)
        return versions

    # TODO remove after moving to class
    @staticmethod
    def check_version(command: str) -> list[str]:
        try:
            result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, Exception) as e:
            if e.returncode == 1 and e.stderr == '' and command.startswith('dpkg -l | grep'):
                pass  # the case when we can't find the program in dpkg manager, but it is not issue
            elif e.returncode == 127 and f'{command.split(maxsplit=1)[0]}: not found' in e.stderr:
                pass  # the case when the program not found, usual -> not installed
            else:
                print(f'{FStyle.RED}Warning!!! Version issue!\n'
                      f'"{command}" <-\n'
                      f'{e.stderr}{FStyle.RESET_ALL}')
            result = ''
        result_atr = result.split()
        return result_atr

    # Todo remove
    @staticmethod
    def install(command: str, name: str) -> None:
        command = command.format(name)
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print(f'\n{FStyle.GREEN}SUCCESSFUL!!!{FStyle.RESET_ALL}\n')
        else:
            print(f'\n{FStyle.RED}SOMeTHING WENT WRONG!!!{FStyle.RESET_ALL}\n')
            print(f'{FStyle.YELLOW}Trying to fix it...{FStyle.RESET_ALL}\n')
            ProgramMap.apt_fix_broken()
        ProgramMap.apt_autoremove()

    @staticmethod
    def install_pycharm(command: str, file_name: str) -> None:
        # getting the name of folder
        result = subprocess.check_output(f'tar -tf {APPS_PATH}/{file_name} | head -n 1', shell=True, text=True)
        folder_name = result.split('/')[0]
        # unpack an archive and create a symbol link
        command = command.format(path=APPS_PATH, file_name=file_name, folder_name=folder_name)
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print(f'\n{FStyle.GREEN}SUCCESSFUL!!!{FStyle.RESET_ALL}\n')
        else:
            print(f'\n{FStyle.RED}SOMeTHING WENT WRONG!!!{FStyle.RESET_ALL}\n')

    # TODO add remove/purge

    @staticmethod
    def apt_autoremove():
        subprocess.run('sudo apt autoremove -y', shell=True)

    @staticmethod
    def apt_fix_broken():
        subprocess.run('sudo apt --fix-broken install -y', shell=True)

    @staticmethod
    def finishing_touches():
        commands = '''sudo apt update -y
            sudo apt upgrade -y
            # восстановление зависимостей
            sudo apt install -y -f
            # удаление лишних пакетов, чистка кеша APT
            sudo apt autoremove -y
            sudo apt-get autoclean -y'''
        try:
            subprocess.run(args=commands, shell=True)
        except Exception as e:
            print(e)

    # TODO remove
    unpack_telegram_command = 'sudo apt install xz-utils -y && tar -xf apps/{} -C ~/apps'
    install_pycharm_p_command = ('tar -xf {path}/{file_name} -C ~/apps && '
                                 'sudo ln -s ~/apps/{folder_name}/bin/pycharm.sh /usr/local/bin/charm')
    install_pycharm_c_command = ('tar -xf {path}/{file_name} -C ~/apps && '
                                 'sudo ln -s ~/apps/{folder_name}/bin/pycharm.sh /usr/local/bin/pycharm')

    program_map = {
        'code': Code,
        'dbeaver': DBeaver,
        'chrome': Chrome,
        'Insomnia': Insomnia,
        'microsoft-edge': MicrosoftEdge,
        'mongodb-compass': MongodbCompass,
        'slack-desktop': Slack,
        'sublime-text': Sublime,
        'viber': Viber,
        'virtualbox': Virtualbox,
        'zoom': Zoom,
        'telegram': {
            'check_version': {  # TODO find a way
                'command': 'echo unknown',
                'func': check_version,
                'result_indices': [0],
            },
            'install': {
                'command': unpack_telegram_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': 'https://telegram.org/dl/desktop/linux'
            },
        },
        'pycharm-professional': {
            'check_version': {
                'command': 'pro',
                'func': get_pycharm_version,
                'result_indices': [0],
            },
            'install': {
                'command': install_pycharm_p_command,
                'func': install_pycharm,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_pycharm_professional(),
            },
        },
        'pycharm-community': {
            'check_version': {
                'command': 'community',
                'func': get_pycharm_version,
                'result_indices': [0],
            },
            'install': {
                'command': install_pycharm_c_command,
                'func': install_pycharm,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_pycharm_community(),
            },
        },
        'virtualenv': Virtualenv,
        'python3-pip': Python3Pip,
        'curl': Curl,
        'docker': Docker,
        'git': Git,
        'htop': Htop,
        'xz-utils': XzUtils,
    }


class ProgramState:
    __is_downloaded: bool | None = None
    __is_installed: bool | None = None
    __version: str = ''

    file_name: str

    def __init__(self, program_name: str):
        program_class = ProgramMap.program_map[program_name]
        self.program = program_class()

        self.is_need_recheck_install = True
        self.is_need_recheck_download = True

    def is_downloaded(self, files: list[str]) -> bool:
        if self.is_need_recheck_download:
            for file_name in files:
                if file_name.startswith(self.program.title):
                    self.__is_downloaded = True
                    self.file_name = file_name
                    break
            else:
                self.__is_downloaded = False
            self.is_need_recheck_download = False
        return self.__is_downloaded

    def is_installed(self):
        if self.is_need_recheck_install:
            self.__set_version_and_is_installed()
            self.is_need_recheck_install = False
        return self.__is_installed

    def download_and_install(self):
        if self.program.downloadable:
            if not self.__is_downloaded and not self.__is_installed:
                downloader = AnimationDownloader(self.program.url)
                file_name = downloader.download_with_animation()
                self.program.install(file_name)
            else:
                if not self.__is_installed:
                    self.program.install(self.file_name)
        else:
            # if it is not file -> apt
            if not self.__is_installed and hasattr(self.program, 'apt_title'):
                self.program.install(self.program.apt_title)
        # reset the condition for the rechecking
        self.is_need_recheck_download = True
        self.is_need_recheck_install = True

    # TODO add only download and only install -> separately

    @property
    def version(self):
        return self.__version

    def __set_version_and_is_installed(self) -> None:
        # todo   # version_list = self.check_func(self.check_command) if self.check_command else self.check_func()
        version_list = self.program.check_version()
        version = ' '.join([version_list[s] for s in self.program.result_indices]) if version_list else ''
        if version and not self.__is_installed:
            # TODO recheck
            if version != 'unknown':
                self.__is_installed = True
        else:
            self.__is_installed = False
        self.__version = version


    def __repr__(self):
        return f'{self.program} -> {self.__class__} - {id(self)}'
