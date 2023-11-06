import argparse
import logging
import pathlib
import shutil

from constants import CONFIG_NAME, DATA_DIR
from src.md2ipynb import _copy_content_files, _transform_to_ipynb
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

logger = logging.getLogger("root.md2ipynb")
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_path",
    type=pathlib.Path,
    help=f"Select the project directory, in which there should be {CONFIG_NAME}, "
    "bibliography and content files.",
)


if __name__ == "__main__":
    logger.info("New process: transforming .md files to a .ipynb file.")
    args = parser.parse_args()
    bc = BookConfigParser(args.project_path)
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("ipynb", slug)
    copy_static_files(
        pathlib.Path(DATA_DIR) / "md" / args.project_path.name,
        pathlib.Path(DATA_DIR) / "ipynb" / args.project_path.name,
    )
    _copy_content_files(slug, jb_config, jb_toc)
    _transform_to_ipynb(slug, jb_config, jb_toc)
