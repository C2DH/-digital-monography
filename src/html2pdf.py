import subprocess

from constants import DATA_DIR
from utils import BookConfigParser

if __name__ == "__main__":
    """
    From jupyter-book docs:
    PDF building is in active development, and may change or have bugs.
    https://jupyterbook.org/en/stable/advanced/pdf.html
    """
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    bookpath = f"{DATA_DIR}/jb/{slug}/"
    subprocess.run(["jupyter-book", "build", bookpath, "--builder", "pdfhtml"])
