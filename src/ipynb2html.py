import pathlib
import shutil
import subprocess
import typing as t

import yaml

from read_config import BookConfigParser, BookMetadata, TableOfContents
from utils import create_book_subdir


def _generate_yaml_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
) -> None:
    with open(f"/home/app_user/data/jb/{slug}/_config.yml", "w") as f:
        yaml.dump(jb_config, f, default_flow_style=False)
    with open(f"/home/app_user/data/jb/{slug}/_toc.yml", "w") as f:
        yaml.dump(jb_toc, f, default_flow_style=False)


def _copy_content_files(slug: str, jb_config: BookMetadata, jb_toc: TableOfContents):
    shutil.copytree(
        f"/home/app_user/data/ipynb/{slug}/",
        f"/home/app_user/data/jb/{slug}/",
        dirs_exist_ok=True,
    )


def _copy_root_file(slug: str, jb_config: BookMetadata, jb_toc: TableOfContents):
    root_file = next(
        _find_file(pathlib.Path("/home/app_user/data/input/"), f"{jb_toc['root']}.*")
    )
    shutil.copy(
        root_file,
        f"/home/app_user/data/jb/{slug}/{root_file.name}",
    )


def _find_file(src: pathlib.Path, lookup: str) -> t.Iterator[pathlib.Path]:
    for f in src.glob(lookup):
        yield f


def _copy_bibliography_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    for bibfile in jb_config.get("bibtex_bibfiles", []):
        shutil.copy(
            f"/home/app_user/data/input/{bibfile}",
            f"/home/app_user/data/jb/{slug}/{bibfile}",
        )


def _build_jupyter_book(slug):
    subprocess.run(
        [
            "jupyter-book",
            "build",
            f"/home/app_user/data/jb/{slug}/",
        ]
    )


if __name__ == "__main__":
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("jb", slug)
    _generate_yaml_files(slug, jb_config, jb_toc)
    _copy_bibliography_files(slug, jb_config, jb_toc)
    _copy_content_files(slug, jb_config, jb_toc)
    _copy_root_file(slug, jb_config, jb_toc)
    _build_jupyter_book(slug)
