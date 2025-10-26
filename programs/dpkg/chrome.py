from programs.common import CommonProgram


class Chrome(CommonProgram):
    check_version_cmd = 'google-chrome --version'
    result_indices = [2]
    downloadable = True
    url = 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
    title = 'Chrome'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
