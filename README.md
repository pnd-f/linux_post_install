# linux_post_install
Installing programs on a clean Linux system.

Python 3.10 and higher are required to run.
Support for version 3.8 is in progress...

To start, simply run
```shell
./run.py
```
or
```shell
python3 run.py
```
from the repo dir.
To select the list items, use the keys `up/down` and `space`. 
Use `Enter` for install , and `q` for exit.

You can install programs such as:
- **VS Code**
> The code editor is fast and universal.
- **dbeaver-community** 
> A free viewer and editor of a huge number of databases.
- **google-chrome**
> The name speaks for itself ;)
- **Insomnia**
> This is a short, poor-quality sleep, problems falling asleep,
regular awakenings in the middle of the night...
- **microsoft-edge**
> The browser.
- **mongodb-compass**
> A utility for viewing and editing the document-oriented
database MondoDB.
- **slack-desktop**
> Corporate Messenger.
- **sublime**
> A small and fast text editor, there are buns like
backlight, etc. Some even write code on it.
- **viber**
> Messenger.
- **virtualbox**
> Virtual machine manager for different operations.
- **zoom**:
> A utility for meetings.
- **telegramm**
> Messenger.
- **pycharm-professional & pycharm-community**
> IDE для python and not only.
- **virtualenv**
> Virtual environment for python, divide and conquer.
- **python3-pip**
> Package manager for python.
- **curl**
> A command-line utility that allows you to interact with 
lots of different servers over lots of different protocols
with URL syntax.
- **docker**
> Docker is an open platform for the development, delivery and
operation of applications, if you want to learn more and 
understand it better, Google it ;)
- **git**
> Version control system.
- **htop**
> Top-based system monitor.
- **xz-utils**
> The archiver supports tar.xz , not all systems have a default.


At the first launch, if you do not have a folder specified
in the settings (usually it is `apps`),
it will be created automatically.

P.S.

If you don't have the same folder in the user's root directory, 
it will also be created automatically.

When you install `docker`, `docker compose` is automatically installed as a plugin.
During the installation of docker, you will need to press CTRL + D on the keyboard,
this is due to the addition of a new group for the user and the ability
to run it without root rights.

`xz-utils` they are installed automatically when installing `telegram`,
because not all systems support unpacking tar.xz out of the box.
