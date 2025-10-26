from programs.common import CommonProgram


class MongodbCompass(CommonProgram):
    check_version_cmd = 'dpkg -l | grep mongodb-compass'
    result_indices = [2, 3]
    downloadable = True
    url = 'https://downloads.mongodb.com/compass/mongodb-compass_1.41.0_amd64.deb'
    title = 'MongodbCompass'

    @property
    def install_cmd(self):
        return self.dpkg_install_command

    def __str__(self):
        return f"{self.title} program"
