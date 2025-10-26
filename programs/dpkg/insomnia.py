from programs.common import CommonProgram


class Insomnia(CommonProgram):
    # TODO I don't like how I handle this check
    check_version_cmd = 'dpkg -l | grep insomnia'
    result_indices = [2, 3]
    downloadable = True
    url = 'https://updates.insomnia.rest/downloads/ubuntu/latest?&app=com.insomnia.app&source=website'
    title = 'Insomnia'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
