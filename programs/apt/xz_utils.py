from programs.common import CommonProgram


class XzUtils(CommonProgram):
    check_version_cmd = 'xz -V'
    result_indices = [3]
    downloadable = False
    apt_title = 'xz-utils'
    title = 'xz-utils'

    @property
    def install_cmd(self):
        return self.apt_install_command

    def __str__(self):
        return f"{self.title} program"
