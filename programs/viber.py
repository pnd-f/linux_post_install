from programs.common import CommonProgram


class Viber(CommonProgram):
    check_version_cmd = 'dpkg -l | grep viber'
    result_indices = [2, 3]
    downloadable = True
    url = 'https://download.cdn.viber.com/cdn/desktop/Linux/viber.deb'

    def __init__(self, title: str):
        self.title = title
        super().__init__()

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
