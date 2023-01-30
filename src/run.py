import os
from pathlib import Path
from exemaker import ExeMaker, Settings


BASE_DIR = str(Path(__file__).resolve().parent.parent)


settings = Settings(
    nativefier_dir=os.path.join(BASE_DIR, 'nativefier-apps'),
    zip_dir=os.path.join(BASE_DIR, 'zips'),
)

maker = ExeMaker(
    url="https://translate.google.com/",
    os_type="linux",
    convert_mode="npm",
    config=settings,
)

# maker2 = ExeMaker(
#     url="https://kinokong.org/36851-na-nozhah-1-6-sezon.html",
#     os_type="windows",
#     convert_mode="docker",
#     config=settings,
# )

# maker3 = ExeMaker(
#     url="https://ubunlog.com/ru/pigz-%D1%81%D0%B6%D0%B8%D0%BC%D0%B0%D0%B5%D1%82-%D1%84%D0%B0%D0%B9%D0%BB%D1%8B-%D1%81-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D0%B0/",
#     os_type="mac",
#     convert_mode="npm",
#     config=settings,
# )
