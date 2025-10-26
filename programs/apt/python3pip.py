from programs.common import CommonProgram


class Python3Pip(CommonProgram):
    check_version_cmd = 'pip3 --version'
    result_indices = [1]
    downloadable = False
    apt_title = 'pip3'
    title = 'pip3'

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
