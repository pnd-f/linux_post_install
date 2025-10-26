from programs.apt.git import Git
from programs.apt.htop import Htop
from programs.apt.python3 import Python3
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
from download_with_progres import AnimationDownloader
from programs.dpkg.viber import Viber
from programs.dpkg.virtualbox import Virtualbox
from programs.dpkg.vscode import Code
from programs.dpkg.zoom import Zoom
from programs.others.docker import Docker
from programs.others.pycharm import PycharmProfessional, PycharmCommunity
from programs.others.telegram import Telegram


class ProgramMap:
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
        'telegram': Telegram,
        'pycharm-professional': PycharmProfessional,
        'pycharm-community': PycharmCommunity,
        'virtualenv': Virtualenv,
        'python3': Python3,
        'python3-pip': Python3Pip,
        'curl': Curl,
        'docker': Docker,
        'git': Git,
        'htop': Htop,
        'xz-utils': XzUtils,
    }


class ProgramWrapper:
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
    def download(self):
        pass

    def install(self):
        pass

    @property
    def version(self):
        return self.__version

    def __set_version_and_is_installed(self) -> None:
        # todo   # version_list = self.check_func(self.check_command) if self.check_command else self.check_func()
        version_list = self.program.get_version()
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
