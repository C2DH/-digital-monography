import subprocess

from read_config import BookConfigParser  # , BookMetadata, TableOfContents

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
    bookpath = f"/home/app_user/data/jb/{slug}/"
    subprocess.run(["jupyter-book", "build", bookpath, "--builder", "pdfhtml"])
