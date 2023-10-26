import pathlib

from constants import DATA_DIR


def create_book_subdir(ftype: str, slug: str) -> None:
    pathlib.Path(
        f"{DATA_DIR}/{ftype}/{slug}",
    ).mkdir(parents=True, exist_ok=True)
