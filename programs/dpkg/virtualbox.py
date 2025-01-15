from programs.common import CommonProgram


class Virtualbox(CommonProgram):
    check_version_cmd = 'dpkg -l | grep virtualbox'
    result_indices = [2, 3]
    downloadable = True
    url = ('https://download.virtualbox.org/virtualbox/7.0.12/'
           'virtualbox-7.0_7.0.12-159484~Ubuntu~jammy_amd64.deb')
    title = 'Virtualbox'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
