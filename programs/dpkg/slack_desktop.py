from programs.common import CommonProgram


class Slack(CommonProgram):
    check_version_cmd = 'slack -v'
    result_indices = [0]
    downloadable = True
    url = 'https://downloads.slack-edge.com/releases/linux/4.35.131/prod/x64/slack-desktop-4.35.131-amd64.deb'
    title = 'Slack'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
