from programs.common import CommonProgram


class MicrosoftEdge(CommonProgram):
    check_version_cmd = 'microsoft-edge --version'
    result_indices = [2]
    downloadable = True
    url = 'https://go.microsoft.com/fwlink?linkid=2149051&brand=M102'
    title = 'MicrosoftEdge'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
