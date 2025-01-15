from programs.common import CommonProgram


class Htop(CommonProgram):
    check_version_cmd = 'htop -V'
    result_indices = [1]
    downloadable = False
    apt_title = 'htop'
    title = 'htop'

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
