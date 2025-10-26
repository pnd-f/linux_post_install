from programs.common import CommonProgram


class Git(CommonProgram):
    check_version_cmd = 'git --version'
    result_indices = [2]
    downloadable = False
    apt_title = 'git'
    title = 'git'

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
