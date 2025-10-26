import json
import os
import subprocess

from color_menu import FStyle
from programs.common import CommonProgram
from settings import DOWNLOAD_APPS_PATH, INSTALL_APPS_PATH


class CommonPycharm:
    downloadable = True

    @staticmethod
    def get_pycharm_version(pycharm_type: str) -> list[str]:
        versions = []
        # we don't check the cache
        # checking if the directory apps exists
        apps = os.path.join(INSTALL_APPS_PATH, DOWNLOAD_APPS_PATH)
        if not os.path.exists(apps):
            return versions
        start_folder_map = {'pro': 'pycharm-202', 'community': 'pycharm-community-202'}
        start_folder_name = start_folder_map[pycharm_type]
        pycharm_folders = [folder for folder in os.listdir(apps) if folder.startswith(start_folder_name)]
        for folder in pycharm_folders:
            # trying to get version from each folder
            goal_file = os.path.join(apps, folder, 'product-info.json')
            if os.path.exists(goal_file):
                with open(goal_file, 'r') as f:
                    json_data = f.read()
                    data = json.loads(json_data)
                    version = data['version']
                    versions.append(version)
        return versions

    @staticmethod
    def install_pycharm(command: str, file_name: str) -> None:
        # getting the name of folder
        result = subprocess.check_output(f'tar -tf {DOWNLOAD_APPS_PATH}/{file_name} | head -n 1', shell=True, text=True)
        folder_name = result.split('/')[0]
        # unpack an archive and create a symbol link
        command = command.format(path=DOWNLOAD_APPS_PATH, file_name=file_name, folder_name=folder_name)
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print(f'\n{FStyle.GREEN}SUCCESSFUL!!!{FStyle.RESET_ALL}\n')
        else:
            print(f'\n{FStyle.RED}SOMeTHING WENT WRONG!!!{FStyle.RESET_ALL}\n')


class PycharmCommunity(CommonProgram, CommonPycharm):
    check_version_cmd = 'community'
    result_indices = [0]
    url = 'https://download.jetbrains.com/product?code=PCC&latest&distribution=linux'
    title = 'pycharm-community'

    @property
    def install_cmd(self):
        return ('sudo tar -xf {path}/{file_name} -C /opt && '
                'sudo ln -s /opt/{folder_name}/bin/pycharm.sh /usr/local/bin/pycharm')

    def get_version(self):
        version = self.get_pycharm_version(self.check_version_cmd)
        return version

    def install(self, filename: str) -> None:
        command = self.install_cmd
        self.install_pycharm(command, filename)

    def __str__(self):
        return f"{self.title} program"


class PycharmProfessional(CommonProgram, CommonPycharm):
    check_version_cmd = 'pro'
    result_indices = [0]
    url = 'https://download.jetbrains.com/product?code=PC&latest&distribution=linux'
    title = 'pycharm-professional'

    @property
    def install_cmd(self):
        return ('sudo tar -xf {path}/{file_name} -C /opt && '
                'sudo ln -s /opt/{folder_name}/bin/pycharm /usr/local/bin/charm')

    def get_version(self):
        version = self.get_pycharm_version(self.check_version_cmd)
        return version

    def install(self, filename: str) -> None:
        command = self.install_cmd
        self.install_pycharm(command, filename)

    def __str__(self):
        return f"{self.title} program"
