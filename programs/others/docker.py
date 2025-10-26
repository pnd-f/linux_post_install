from programs.common import CommonProgram


class Docker(CommonProgram):
    check_version_cmd = 'virtualenv --version'
    result_indices = [1]
    downloadable = False
    title = 'docker'

    @property
    def install_cmd(self):
        return '''# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
echo -e "\033[33mReRun group docker...\033[0m"
sg docker <<EOF
echo "Group docker activated for the current user."
EOF
echo -e "\033[32mSuccess.\033[0m"
    '''

    def __str__(self):
        return f"{self.title} program"
