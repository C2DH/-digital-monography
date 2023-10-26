import pathlib
import shutil
import subprocess

from constants import DATA_DIR
from utils import (
    BookConfigParser,
    BookMetadata,
    TableOfContents,
    create_book_subdir,
)


def _copy_content_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    for ch in jb_toc.get("chapters", []):
        fn = ch["file"]
        shutil.copy(
            f"{DATA_DIR}/md/{slug}/{fn}.md",
            f"{DATA_DIR}/ipynb/{slug}/{fn}.md",
        )


def _transform_to_ipynb(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    """
    https://myst-nb.readthedocs.io/en/v0.10.1/use/markdown.html#convert-between-ipynb-and-myst-notebooks

    Some examples of jupytext CLI cmds:
        to convert MyST-markdown to .ipynb
            jupytext mystfile.md --to ipynb
        convert notebook.ipynb to a .py file
            jupytext --to py notebook.ipynb
        convert all .md files to paired notebooks and execute them
            jupytext --set-formats ipynb,md --execute *.md
        Test the ipynb -> py:percent -> ipynb round trip conversion
            jupytext --test notebook.ipynb --to py:percent
        Test the ipynb -> (py:percent + ipynb) -> ipynb (à la paired notebook) conversion
            jupytext --test --update notebook.ipynb --to py:percent
    """
    for ch in jb_toc.get("chapters", []):
        fn = f"{DATA_DIR}/ipynb/{slug}/{ch['file']}.md"
        subprocess.run(["jupytext", fn, "--to", "ipynb"])
        fp = pathlib.Path(fn)
        if fp.suffix != ".ipynb":
            fp.unlink(missing_ok=True)


if __name__ == "__main__":
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("ipynb", slug)
    _copy_content_files(slug, jb_config, jb_toc)
    _transform_to_ipynb(slug, jb_config, jb_toc)
