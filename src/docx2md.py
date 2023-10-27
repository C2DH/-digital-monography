import logging
import shutil

from constants import DATA_DIR
from utils import (
    BookConfigParser,
    BookMetadata,
    TableOfContents,
    config_logging,
    create_book_subdir,
)

config_logging()


logger = logging.getLogger("root.docx2md")


def _copy_content_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    for ch in jb_toc.get("chapters", []):
        fn = ch["file"]
        shutil.copy(
            f"{DATA_DIR}/input/{fn}.md",
            f"{DATA_DIR}/md/{slug}/{fn}.md",
        )
    logger.info(
        "Found no errors while copying input files to 'md' subdirectory."
    )


if __name__ == "__main__":
    logger.info("New process: transforming input files to .md files.")
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("md", slug)
    _copy_content_files(slug, jb_config, jb_toc)
