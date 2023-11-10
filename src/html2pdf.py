import argparse
import logging
import pathlib
import sys

from constants import CONFIG_NAME, DATA_DIR
from utils import (
    BookConfigParser,
    config_logging,
    stdout_hero,
    subprocess_run_and_log,
)

config_logging()


logger = logging.getLogger("root.html2pdf")
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_path",
    type=pathlib.Path,
    help=f"Select the project directory, in which there should be {CONFIG_NAME}, "
    "bibliography and content files.",
)

if __name__ == "__main__":
    """
    From jupyter-book docs:
    PDF building is in active development, and may change or have bugs.
    https://jupyterbook.org/en/stable/advanced/pdf.html
    """
    stdout_hero("html2pdf")
    logger.info("New process: transforming .html files to a .pdf file.")
    args = parser.parse_args()
    bc = BookConfigParser(args.project_path)
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    bookpath = f"{DATA_DIR}/jb/{slug}/"
    subprocess_run_and_log(
        ["jupyter-book", "build", bookpath, "--builder", "pdfhtml"],
        logger,
    )
