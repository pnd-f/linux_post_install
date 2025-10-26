from programs.common import CommonProgram


class Teams(CommonProgram):
    # TODO not for ubuntu, probably other OS
    check_version_cmd = 'dpkg -l | grep teams'
    result_indices = [2, 3]
    downloadable = False
    url = ''
    title = 'Teams'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
