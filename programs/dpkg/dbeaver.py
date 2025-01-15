from programs.common import CommonProgram


class DBeaver(CommonProgram):
    check_version_cmd = 'dbeaver -version -nosplash'
    result_indices = [1]
    downloadable = True
    url = 'https://dbeaver.io/files/dbeaver-ce_latest_amd64.deb'
    title = 'DBeaver'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
