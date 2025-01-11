from programs.common import CommonProgram


class Sublime(CommonProgram):
    check_version_cmd = 'subl -v'
    result_indices = [3]
    downloadable = True
    # url = 'https://download.sublimetext.com/sublime-text_build-3211_amd64.deb'
    url = 'https://download.sublimetext.com/sublime-text_build-4189_amd64.debb'

    def __init__(self, title: str):
        self.title = title
        super().__init__()

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
