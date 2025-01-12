from programs.common import CommonProgram


class Code(CommonProgram):
    check_version_cmd = 'code -v'
    result_indices = [0, 2]
    downloadable = True
    url = 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'

    def __init__(self, title: str):
        self.title = title
        super().__init__()

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
