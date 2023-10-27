import logging
import pathlib
import shutil
import typing as t

import yaml

from constants import DATA_DIR
from utils import (
    BookConfigParser,
    BookMetadata,
    TableOfContents,
    config_logging,
    create_book_subdir,
    subprocess_run_and_log,
)

config_logging()

logger = logging.getLogger("root.ipynb2html")


def _generate_yaml_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
) -> None:
    with open(f"{DATA_DIR}/jb/{slug}/_config.yml", "w") as f:
        yaml.dump(jb_config, f, default_flow_style=False)
    with open(f"{DATA_DIR}/jb/{slug}/_toc.yml", "w") as f:
        yaml.dump(jb_toc, f, default_flow_style=False)


def _copy_content_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    shutil.copytree(
        f"{DATA_DIR}/ipynb/{slug}/",
        f"{DATA_DIR}/jb/{slug}/",
        dirs_exist_ok=True,
    )


def _copy_root_file(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    root_file = next(
        _find_file(pathlib.Path(f"{DATA_DIR}/input/"), f"{jb_toc['root']}.*")
    )
    shutil.copy(
        root_file,
        f"{DATA_DIR}/jb/{slug}/{root_file.name}",
    )


def _find_file(src: pathlib.Path, lookup: str) -> t.Iterator[pathlib.Path]:
    for f in src.glob(lookup):
        yield f


def _copy_bibliography_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    for bibfile in jb_config.get("bibtex_bibfiles", []):
        shutil.copy(
            f"{DATA_DIR}/input/{bibfile}",
            f"{DATA_DIR}/jb/{slug}/{bibfile}",
        )


def _build_jupyter_book(slug):
    subprocess_run_and_log(
        [
            "jupyter-book",
            "build",
            f"{DATA_DIR}/jb/{slug}/",
        ],
        logger,
    )


if __name__ == "__main__":
    logger.info("New process: transforming .html files to a .pdf file.")
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
