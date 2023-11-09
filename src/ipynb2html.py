import argparse
import logging
import pathlib
import shutil
import sys
import typing as t

import yaml

from constants import CONFIG_NAME, DATA_DIR
from utils import (
    BookConfigParser,
    BookMetadata,
    TableOfContents,
    config_logging,
    copy_static_files,
    create_book_subdir,
    subprocess_run_and_log,
)

config_logging()

logger = logging.getLogger("root.ipynb2html")
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_path",
    type=pathlib.Path,
    help=f"Select the project directory, in which there should be {CONFIG_NAME}, "
    "bibliography and content files.",
)


def _generate_yaml_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
) -> None:
    with open(f"{DATA_DIR}/jb/{slug}/_config.yml", "w") as f:
        yaml.dump(jb_config, f, default_flow_style=False)
    with open(f"{DATA_DIR}/jb/{slug}/_toc.yml", "w") as f:
        yaml.dump(jb_toc, f, default_flow_style=False)


def _copy_content_files(slug: str):
    shutil.copytree(
        f"{DATA_DIR}/ipynb/{slug}/",
        f"{DATA_DIR}/jb/{slug}/",
        dirs_exist_ok=True,
    )


def _copy_root_file(
    slug: str, project_path: pathlib.PurePath, jb_toc: TableOfContents
):
    root_file = next(_find_file(project_path, f"{jb_toc['root']}"))
    if not root_file.exists():
        logging.critical(
            f"File '{root_file}' mentioned in the '{CONFIG_NAME}' "
            "was not found."
        )
        raise FileNotFoundError()
    root_file_name = root_file.name.replace(root_file.suffix, "")
    shutil.copy(
        root_file,
        f"{DATA_DIR}/jb/{slug}/{root_file_name}",
    )


def _find_file(
    src: pathlib.PurePath, lookup: str
) -> t.Iterator[pathlib.PurePath]:
    for f in src.glob(lookup):
        yield f


def _copy_bibliography_files(
    slug: str,
    project_path: pathlib.PurePath,
    jb_config: BookMetadata,
):
    for bibfile in jb_config.get("bibtex_bibfiles", []):
        src = project_path / bibfile
        if not src.exists():
            logging.critical(
                f"Bibliography '{src}' mentioned in the '{CONFIG_NAME}' "
                "was not found."
            )
            raise FileNotFoundError()
        shutil.copy(
            src,
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
    args = parser.parse_args()
    bc = BookConfigParser(args.project_path)
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("jb", slug)
    copy_static_files(
        pathlib.Path(DATA_DIR) / "ipynb" / args.project_path.name,
        pathlib.Path(DATA_DIR) / "jb" / args.project_path.name,
    )
    _generate_yaml_files(slug, jb_config, jb_toc)
    _copy_bibliography_files(slug, args.project_path, jb_config)
    _copy_content_files(slug)
    _copy_root_file(slug, args.project_path, jb_toc)
    _build_jupyter_book(slug)
