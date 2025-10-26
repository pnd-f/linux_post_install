from programs.common import CommonProgram


class Telegram(CommonProgram):
    check_version_cmd = 'echo unknown' # TODO find a way
    result_indices = [0]
    downloadable = True
    url = 'https://telegram.org/dl/desktop/linux'
    title = 'docker'

    @property
    def install_cmd(self):
        return 'sudo apt install xz-utils -y && tar -xf apps/{} -C ~/Telegram'

    def __str__(self):
        return f"{self.title} program"
