import logging
import pathlib
import shutil

from src.constants import DATA_DIR, STATIC_DIR_NAMES

from .log_mgnt import config_logging

config_logging()


logger = logging.getLogger("root.docx2md")


def create_book_subdir(ftype: str, slug: str) -> None:
    pathlib.Path(
        f"{DATA_DIR}/{ftype}/{slug}",
    ).mkdir(parents=True, exist_ok=True)


def copy_static_files(src: pathlib.PurePath, dst: pathlib.PurePath):
    for dir in STATIC_DIR_NAMES:
        if (src / dir).exists():
            shutil.copytree(src / dir, dst / dir, dirs_exist_ok=True)


def copy_bibliography(src: pathlib.PurePath, dst: pathlib.Path) -> None:
    if not dst.is_dir():
        logger.error(
            "copy_bibliography() accepts only directories as copy destinations.",
            f"{dst} should be an existing directory.",
        )
        raise Exception(
            "copy_bibliography() accepts only directories as copy destinations."
        )
    for bib in src.glob("*.bib"):
        if bib.exists():
            shutil.copyfile(bib, dst / bib.name)
