import pathlib
import shutil

from src.constants import DATA_DIR, STATIC_DIR_NAMES


def create_book_subdir(ftype: str, slug: str) -> None:
    pathlib.Path(
        f"{DATA_DIR}/{ftype}/{slug}",
    ).mkdir(parents=True, exist_ok=True)


def copy_static_files(src: pathlib.PurePath, dst: pathlib.PurePath):
    for dir in STATIC_DIR_NAMES:
        if (src / dir).exists():
            shutil.copytree(src / dir, dst / dir, dirs_exist_ok=True)
