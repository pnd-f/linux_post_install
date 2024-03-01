import json
import os
import subprocess

from color_menu import FStyle
from download_with_progres import AnimationDownloader
from settings import APPS_PATH


class ProgramMap:
    class UrlMap:
        # put a logic to find the latest version
        @staticmethod
        def get_vscode_url() -> str:
            return 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'

        @staticmethod
        def get_dbeaver_url() -> str:
            return 'https://dbeaver.io/files/dbeaver-ce_latest_amd64.deb'

        @staticmethod
        def get_google_url() -> str:
            return 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'

        @staticmethod
        def get_insomnia_url() -> str:
            return 'https://updates.insomnia.rest/downloads/ubuntu/latest?&app=com.insomnia.app&source=website'

        @staticmethod
        def get_edge_url() -> str:
            return 'https://go.microsoft.com/fwlink?linkid=2149051&brand=M102'

        @staticmethod
        def get_compas_url() -> str:
            return 'https://downloads.mongodb.com/compass/mongodb-compass_1.41.0_amd64.deb'

        @staticmethod
        def get_slack_url() -> str:
            return 'https://downloads.slack-edge.com/releases/linux/4.35.131/prod/x64/slack-desktop-4.35.131-amd64.deb'

        @staticmethod
        def get_sublime_url() -> str:
            return 'https://download.sublimetext.com/sublime-text_build-3211_amd64.deb'

        @staticmethod
        def get_viber_url() -> str:
            return 'https://download.cdn.viber.com/cdn/desktop/Linux/viber.deb'

        @staticmethod
        def get_virtualbox_url() -> str:
            return ('https://download.virtualbox.org/virtualbox/7.0.12/'
                    'virtualbox-7.0_7.0.12-159484~Ubuntu~jammy_amd64.deb')

        @staticmethod
        def get_zoom_url() -> str:
            return 'https://zoom.us/client/5.17.1.1840/zoom_amd64.deb'

        @staticmethod
        def get_telegram_url() -> str:
            return 'https://telegram.org/dl/desktop/linux'

        @staticmethod
        def get_pycharm_professional() -> str:
            return 'https://download.jetbrains.com/product?code=PC&latest&distribution=linux'

        @staticmethod
        def get_pycharm_community() -> str:
            return 'https://download.jetbrains.com/product?code=PCC&latest&distribution=linux'

        @staticmethod
        def get_mock() -> str:
            return 'mock'

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

    # TODO add remuve/purge

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

    dpkg_install_command = 'sudo dpkg -i apps/{}'
    unpack_telegram_command = 'sudo apt install xz-utils -y && tar -xf apps/{} -C ~/apps'
    install_pycharm_p_command = ('tar -xf {path}/{file_name} -C ~/apps && '
                                 'sudo ln -s ~/apps/{folder_name}/bin/pycharm.sh /usr/local/bin/charm')
    install_pycharm_c_command = ('tar -xf {path}/{file_name} -C ~/apps && '
                                 'sudo ln -s ~/apps/{folder_name}/bin/pycharm.sh /usr/local/bin/pycharm')
    apt_install_command = 'sudo apt install {} -y'
    install_docker_command = '''# Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
    echo -e -e '\033[33m                            введите ctrl + D'
    newgrp docker
    '''  #

    program_map = {  # TODO redo it to dict[str, CLASS]
        'code': {
            'check_version': {
                'command': 'code -v',
                'func': check_version,
                'result_indices': [0, 2]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_vscode_url()
            }
        },
        'dbeaver': {
            'check_version': {
                'command': 'dbeaver -version -nosplash',
                'func': check_version,
                'result_indices': [1],
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_dbeaver_url()
            },
        },
        'google': {
            'check_version': {
                'command': 'google-chrome --version',
                'func': check_version,
                'result_indices': [2],
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_google_url(),
            },
        },
        'Insomnia': {
            'check_version': {
                'command': 'dpkg -l | grep insomnia',
                'func': check_version,
                'result_indices': [2, 3]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_insomnia_url(),
            },
        },
        'microsoft-edge': {
            'check_version': {
                'command': 'microsoft-edge --version',
                'func': check_version,
                'result_indices': [2]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_edge_url(),
            },
        },
        'mongodb-compass': {
            'check_version': {
                'command': 'dpkg -l | grep mongodb-compass',
                'func': check_version,
                'result_indices': [2, 3]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_compas_url(),
            },
        },
        'slack-desktop': {
            'check_version': {
                'command': 'slack -v',
                'func': check_version,
                'result_indices': [0]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_slack_url(),
            },
        },
        'sublime-text': {
            'check_version': {
                'command': 'subl -v',
                'func': check_version,
                'result_indices': [3]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_sublime_url(),
            },
        },
        'teams': {  # TODO ??? the development of the package has been abandoned
            'check_version': {
                'command': 'dpkg -l | grep teams',
                'func': check_version,
                'result_indices': [2, 3]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
                # 'url': UrlMap.get_mock()
            },
        },
        'viber': {
            'check_version': {
                'command': 'dpkg -l | grep viber',
                'func': check_version,
                'result_indices': [2, 3]},
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_viber_url()
            },
        },
        'virtualbox': {
            'check_version': {
                'command': 'dpkg -l | grep virtualbox',
                'func': check_version,
                'result_indices': [2, 3]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_virtualbox_url()
            },
        },
        'zoom': {
            'check_version': {
                'command': 'dpkg -l | grep zoom',
                'func': check_version,
                'result_indices': [2, 3]
            },
            'install': {
                'command': dpkg_install_command,
                'func': install,
            },
            'download': {
                'downloadable': True,
                'url': UrlMap.get_zoom_url(),
            },
        },
        'tsetup': {
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
                'url': UrlMap.get_telegram_url(),
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
        'virtualenv': {
            'check_version': {
                'command': 'virtualenv --version',
                'func': check_version,
                'result_indices': [1],
            },
            'install': {
                'command': apt_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
        'python3-pip': {
            'check_version': {
                'command': 'pip3 --version',
                'func': check_version,
                'result_indices': [1],
            },
            'install': {
                'command': apt_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
        'curl': {
            'check_version': {
                'command': 'curl -V',
                'func': check_version,
                'result_indices': [1, 2],
            },
            'install': {
                'command': apt_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
        'docker': {
            'check_version': {
                'command': 'docker --version',
                'func': check_version,
                'result_indices': [2],
            },
            'install': {
                'command': install_docker_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
        'git': {
            'check_version': {
                'command': 'git --version',
                'func': check_version,
                'result_indices': [2],
            },
            'install': {
                'command': apt_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
        'htop': {
            'check_version': {
                'command': 'htop -V',
                'func': check_version,
                'result_indices': [1],
            },
            'install': {
                'command': apt_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
        'xz-utils': {
            'check_version': {
                'command': 'xz -V',
                'func': check_version,
                'result_indices': [3],
            },
            'install': {
                'command': apt_install_command,
                'func': install,
            },
            'download': {
                'downloadable': False,
            },
        },
    }


class ProgramState:
    __is_downloaded: bool | None = None
    __is_installed: bool | None = None
    __version: str = ''

    file_name: str

    def __init__(self, program_name: str):
        self.program_name = program_name
        self.program_map = ProgramMap.program_map[self.program_name]

        check_version = self.program_map['check_version']
        self.result_indices = check_version['result_indices']
        self.check_func = check_version['func']
        self.check_command = check_version['command']
        download = self.program_map['download']

        self.downloadable = download['downloadable']
        if self.downloadable:
            self.url = download['url']

        install = self.program_map['install']
        self.installer = install['func']
        self.install_command = install['command']

        self.is_need_recheck_install = True
        self.is_need_recheck_download = True

    def is_downloaded(self, files: list[str]) -> bool:
        if self.is_need_recheck_download:
            for file_name in files:
                if file_name.startswith(self.program_name):
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
        if self.downloadable:
            if not self.__is_downloaded and not self.__is_installed:
                downloader = AnimationDownloader(self.url)
                file_name = downloader.download_with_animation()
                self.installer(self.install_command, file_name)
            else:
                if not self.__is_installed:
                    self.installer(self.install_command, self.file_name)
        else:
            if not self.__is_installed:
                self.installer(self.install_command, self.program_name)
        # reset the condition for the rechecking
        self.is_need_recheck_download = True
        self.is_need_recheck_install = True

    # TODO add only download and only install -> separately

    @property
    def version(self):
        return self.__version

    def __set_version_and_is_installed(self) -> None:
        version_list = self.check_func(self.check_command) if self.check_command else self.check_func()
        version = ' '.join([version_list[s] for s in self.result_indices]) if version_list else ''
        if version and not self.__is_installed:
            if version != 'unknown':
                self.__is_installed = True
        else:
            self.__is_installed = False
        self.__version = version

    def __repr__(self):
        return f'{self.program_name} -> {self.__class__} - {id(self)}'
