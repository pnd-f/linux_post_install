import asyncio
import os
import re
from urllib.request import urlopen

from color_menu import FStyle


class AnimationDownloader:
    """
    How to check:
    _url = 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'
    downloader = AnimationDownloader(_url)

    file_name = downloader.download_with_animation()
    """
    animation_version: int
    __is_downloaded: bool = False
    file_name: str
    total_size: float = 0  # Bytes

    downloaded_size: float = 0  # Bytes

    progress: str = ''

    kilobyte_size: int = 1024
    megabyte_size: int = kilobyte_size * 1024

    def __init__(self, url: str, file_name: str = '', animation_version: int = 3):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.file_name = file_name
        self.animation_version = animation_version

    async def __show_animation(self):
        async def animation_1():
            animation_list = ['\\', '|', '/', '-']

            i = 0
            while True:
                await asyncio.sleep(0.1)

                if i == len(animation_list) - 1:
                    i = 0
                    continue
                i += 1
                print(self.progress, animation_list[i], end='\r')
                if self.total_size != 0 and self.downloaded_size == self.total_size:
                    break

        async def animation_2():

            animation_list = [
                f'{FStyle.go_to_up_screen}{FStyle.clear_row_after}\\  \n'
                f'{FStyle.clear_row_after} \\ \n'
                f'{FStyle.clear_row_after}  \\\n',

                f'{FStyle.go_to_up_screen}{FStyle.clear_row_after} | \n'
                f' | \n{FStyle.clear_row_after}'
                f' | \n{FStyle.clear_row_after}',

                f'{FStyle.go_to_up_screen}{FStyle.clear_row_after}  /\n'
                f' / \n{FStyle.clear_row_after}'
                f'/  \n{FStyle.clear_row_after}',

                f'{FStyle.go_to_up_screen}{FStyle.clear_row_after}   \n'
                f'---\n{FStyle.clear_row_after}'
                f'   \n{FStyle.clear_row_after}',

            ]

            i = 0
            while True:
                await asyncio.sleep(0.1)

                print(self.progress, animation_list[i])

                if i == len(animation_list) - 1:
                    i = 0
                    continue
                i += 1
                if self.total_size != 0 and self.downloaded_size == self.total_size:
                    print(self.progress, animation_list[i])
                    break

        async def animation_3():

            while True:
                await asyncio.sleep(0.3)

                # Getting the size of the console
                console_size = os.get_terminal_size()
                free_wide = console_size.columns - 1

                if len(self.progress) > console_size.columns or self.total_size == 0:
                    continue
                # calculate percents and show it
                # the one square equal to X Bytes
                one_square = self.total_size / free_wide
                filled_squares = int(self.downloaded_size / one_square)
                print(self.progress, FStyle.clear_row_after)
                print(f'{FStyle.GREEN}{FStyle.full_symbol * filled_squares}{FStyle.RESET_ALL}'
                      f'{FStyle.empty_symbol * (free_wide - filled_squares)}{FStyle.go_to_up_row}',
                      end='')
                if self.downloaded_size == self.total_size:
                    print(self.progress, FStyle.clear_row_after)
                    print(f'{FStyle.GREEN}{FStyle.full_symbol * filled_squares}'
                          f'{FStyle.empty_symbol * (free_wide - filled_squares)}{FStyle.go_to_up_row}'
                          f'{FStyle.RESET_ALL}')
                    print('\nThe download is complete\\m/')

                    break

        map_animation = {
            1: animation_1,
            2: animation_2,
            3: animation_3,
        }
        animation = map_animation[self.animation_version]
        await animation()

    async def __download_by_url(self):
        await self.loop.run_in_executor(None, self.__download_sync)

    def __download_sync(self):
        response = urlopen(self.url)
        print('The download has started')
        self.total_size = float(response.info().get('Content-Length', 0))
        total_size_str = round(self.total_size / self.megabyte_size, 1)
        self.downloaded_size = 0

        if not self.file_name:
            self.__set_file_name_from_response(response)

        with open(f'./apps/{self.file_name}', 'wb') as file:
            while True:
                buffer = response.read(8196)
                if not buffer:
                    break
                self.downloaded_size += len(buffer)
                downloaded_str = round(self.downloaded_size / self.megabyte_size, 1)
                file.write(buffer)
                self.progress = f"Downloaded {downloaded_str} / {total_size_str} mb"

    def __set_file_name_from_response(self, response) -> None:
        result = response.info().get('Content-Disposition')
        if result and 'filename' in result:
            # insomnia case
            self.file_name = re.search(r'filename=(.*?\.deb)', result)[1]
        else:
            self.file_name = response.url.split('/')[-1]

    def download_with_animation(self) -> str:
        try:
            self.loop.run_until_complete(self.__tasker())
            self.__is_downloaded = True
        except Exception as e:
            print(e)
        return self.file_name

    async def __tasker(self):
        show_animation = asyncio.create_task(self.__show_animation())
        await self.__download_by_url()
        await show_animation
