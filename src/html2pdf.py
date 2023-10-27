import logging

from constants import DATA_DIR
from utils import BookConfigParser, config_logging, subprocess_run_and_log

config_logging()


logger = logging.getLogger("root.html2pdf")

if __name__ == "__main__":
    """
    From jupyter-book docs:
    PDF building is in active development, and may change or have bugs.
    https://jupyterbook.org/en/stable/advanced/pdf.html
    """
    logger.info("New process: transforming .html files to a .pdf file.")
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    bookpath = f"{DATA_DIR}/jb/{slug}/"
    subprocess_run_and_log(
        ["jupyter-book", "build", bookpath, "--builder", "pdfhtml"],
        logger,
    )
