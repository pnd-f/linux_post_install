from programs.common import CommonProgram


class PycharmCommunity(CommonProgram):
    pass
    # check_version_cmd = 'virtualenv --version'
    # result_indices = [2]
    # downloadable = False
    # title = 'docker'
    #
    @property
    def install_cmd(self):
        return ''
    #
    # def __str__(self):
    #     return f"{self.title} program"

class PycharmProfessional(CommonProgram):
    pass
    # check_version_cmd = 'virtualenv --version'
    # result_indices = [2]
    # downloadable = False
    # title = 'docker'
    #
    @property
    def install_cmd(self):
        return ''
    #
    # def __str__(self):
    #     return f"{self.title} program"
