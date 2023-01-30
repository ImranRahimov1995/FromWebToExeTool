import os
import subprocess
import shutil

from urllib.parse import urlparse

from typing import Literal, Dict, Tuple
from dataclasses import dataclass

from django.shortcuts import HttpResponse
from django.conf import settings


# from src.exemaker import ExeMaker ,Settings
# maker = Exemaker()


@dataclass
class Settings:
    """
        zip_dir : is output directory which contain all zip files.

        nativefier_dir: is directory which folder with exe file after
        converting website to native app.

    """

    zip_dir: str
    nativefier_dir: str
    home_dir: str = os.path.expanduser('~')


class ExeMaker:
    def __init__(
            self,
            url: str,
            os_type: Literal["windows", "mac", "linux"],
            convert_mode: Literal["docker", "npm"] = "docker",
            config: Settings = None,
    ) -> None:
        self.url = url
        self.os_type = os_type
        self.mode = convert_mode
        self.config = config

        self.domain, self.app_name = self.url_extractor(url)

        self.home_dir, self.nativefier_dir, self.zip_dir = \
            self.configure_dirs()

        self.zip_file_path = os.path.join(self.zip_dir, self.app_name)
        self.zip_file = self.zip_file_path + ".zip"

        self.exe_dir = self.convert_website()

        self.app_pack_to_zip()

    @staticmethod
    def url_extractor(url: str) -> Tuple[str, str]:
        domain = urlparse(url).netloc
        app_name = domain.split('.')[-2]  # for example.com -> example

        return domain, app_name

    @staticmethod
    def get_or_create_dir(path: str) -> str:
        if os.path.isdir(path) is False:
            os.mkdir(path)
        return os.path.join(path)

    def configure_dirs(self) -> Tuple[str, str, str]:
        if isinstance(self.config, Settings):
            home_dir = self.config.home_dir
            nativefier_dir = self.get_or_create_dir(
                self.config.nativefier_dir
            )
            zip_dir = self.get_or_create_dir(
                self.config.zip_dir
            )

        else:
            home_dir = settings.HOME_DIR
            nativefier_dir = self.get_or_create_dir(
                settings.NATIVEFIER_DIR
            )
            zip_dir = self.get_or_create_dir(str(settings.ZIP_DIR))

        return home_dir, nativefier_dir, zip_dir

    def convert_website(self) -> str:
        if self.mode == "npm":
            cmd = \
                f"nativefier '{self.url}'" \
                f" {os.path.join(self.nativefier_dir,self.app_name)}" \
                f" --name '{self.app_name}'" \
                f" -p {self.os_type} --disable-dev-tools",

        else:
            cmd = \
                f"docker run --rm -v {self.nativefier_dir}:/target/" \
                f" nativefier/nativefier {self.url} /target/" \
                f"{self.app_name}" \
                f" --name {self.app_name} -p {self.os_type} " \
                f" --disable-dev-tools"

        print(cmd)
        subprocess.call(cmd, shell=True)

        self.exe_dir = os.listdir(
            os.path.join(self.nativefier_dir, self.app_name)
        )[0]

        return os.path.join(
            self.nativefier_dir, self.app_name, self.exe_dir
        )

    def app_pack_to_zip(self) -> None:
        os.chdir(self.exe_dir)
        shutil.make_archive(self.zip_file_path, 'zip', './')
        os.chdir(self.zip_dir)
        shutil.rmtree(self.exe_dir)

    def django_response(self) -> HttpResponse:
        file = open(self.zip_file, 'rb')

        response = HttpResponse(file.read())
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Length'] = os.path.getsize(self.zip_file)
        response['Content-Disposition'] = f"attachment; " \
                                          f"filename={self.app_name}.zip"

        file.close()

        return response

    def get_zip_filepath(self) -> str:
        return self.zip_file
