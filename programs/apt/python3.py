from programs.common import CommonProgram


class Python3(CommonProgram):
    check_version_cmd = 'python3 -V'
    result_indices = [1]
    downloadable = False
    apt_title = 'python3'
    title = 'python3'

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
