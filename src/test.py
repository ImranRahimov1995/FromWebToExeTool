import os
import pytest

from exemaker import ExeMaker, Settings

URL = "https://translate.google.com/"
ZIP_DIR = 'zip_dir'
NATIVEFIER_DIR = 'nativefier_dir'


@pytest.fixture
def exemaker(tmpdir):
    zip_dir = str(tmpdir.mkdir(ZIP_DIR))
    nativefier_dir = str(tmpdir.mkdir(NATIVEFIER_DIR))

    config = Settings(zip_dir=zip_dir, nativefier_dir=nativefier_dir)

    yield ExeMaker(URL, "windows", convert_mode='docker', config=config)


def test_url_extractor(exemaker):
    domain, app_name = exemaker.url_extractor(exemaker.url)
    assert domain == "translate.google.com"
    assert app_name == "google"


def test_get_or_create_dir(exemaker, tmpdir):
    path = str(tmpdir.mkdir("test_dir"))
    assert exemaker.get_or_create_dir(path) == path


def test_configure_dirs(exemaker):
    home_dir = os.path.expanduser("~")
    assert exemaker.home_dir == home_dir
    assert os.path.isdir(exemaker.zip_dir)
    assert os.path.isdir(exemaker.nativefier_dir)


def test_convert_website(exemaker):
    exe_dir = exemaker.convert_website()
    assert os.path.isdir(exe_dir)


def test_app_pack_to_zip(exemaker):
    assert os.path.isfile(exemaker.zip_file)

    with open(exemaker.zip_file, "rb") as f:
        file_content = f.read()
    assert len(file_content) > 0
