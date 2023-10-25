import pathlib


def create_book_subdir(ftype: str, slug: str) -> None:
    pathlib.Path(
        f"/home/app_user/data/{ftype}/{slug}",
    ).mkdir(parents=True, exist_ok=True)
