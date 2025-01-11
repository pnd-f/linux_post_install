from programs.common import CommonProgram


class Curl(CommonProgram):
    check_version_cmd = 'curl -V'
    result_indices = [1, 2]
    downloadable = False
    apt_title = 'curl'

    def __init__(self, title: str):
        self.title = title
        super().__init__()

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
