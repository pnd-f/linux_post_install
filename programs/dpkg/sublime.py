from programs.common import CommonProgram


class Sublime(CommonProgram):
    check_version_cmd = 'subl -v'
    result_indices = [3]
    downloadable = True
    url = 'https://download.sublimetext.com/sublime-text_build-4189_amd64.debb'
    title = 'Sublime'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
