from programs.common import CommonProgram


class Zoom(CommonProgram):
    check_version_cmd = 'dpkg -l | grep zoom'
    result_indices = [2, 3]
    downloadable = True
    # TODO update link
    url = 'https://zoom.us/client/5.17.1.1840/zoom_amd64.deb'
    title = 'Zoom'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
