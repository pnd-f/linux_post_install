from programs.common import CommonProgram


class Virtualenv(CommonProgram):
    check_version_cmd = 'virtualenv --version'
    result_indices = [1]
    downloadable = False
    apt_title = 'virtualenv'
    title = 'Virtualenv'

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
