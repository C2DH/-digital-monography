import argparse
import logging
import pathlib
import shutil

from constants import CONFIG_NAME, DATA_DIR
from utils import (
    BookConfigParser,
    TableOfContents,
    config_logging,
    create_book_subdir,
)

config_logging()


logger = logging.getLogger("root.docx2md")
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_path",
    type=pathlib.Path,
    help=f"Select the project directory, in which there should be {CONFIG_NAME}, "
    "bibliography and content files.",
)


def _copy_content_files(
    project_path: pathlib.PurePath, jb_toc: TableOfContents
) -> None:
    slug = project_path.name
    for ch in jb_toc.get("chapters", []):
        fn = ch["file"]
        src = project_path / fn
        dst = pathlib.Path(DATA_DIR) / "md" / slug / fn
        if not src.exists():
            logger.error(
                f"Copy source not found. {src} does not exist. "
                f"Cannot copy to {dst}"
            )
        try:
            shutil.copy(src, dst)
        except FileNotFoundError as e:
            logger.error(
                f"Copy source not found. {src} does not exist. "
                f"Cannot copy to {dst}."
            )
            raise
    logger.info(
        "Found no errors while copying input files to 'md' subdirectory."
    )


if __name__ == "__main__":
    logger.info("New process: transforming input files to .md files.")
    args = parser.parse_args()
    bc = BookConfigParser(args.project_path)
    bc.open_book_config()
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("md", slug)
    _copy_content_files(args.project_path, jb_toc)
