import pathlib
import shutil
import subprocess

import yaml

from constants import DATA_DIR
from read_config import BookConfigParser, BookMetadata, TableOfContents
from utils import create_book_subdir


# TODO: move to ipynb 2 html
def _generate_yaml_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
) -> None:
    with open(f"{DATA_DIR}/jb/{slug}/_config.yml", "w") as f:
        yaml.dump(jb_config, f, default_flow_style=False)
    with open(f"{DATA_DIR}/jb/{slug}/_toc.yml", "w") as f:
        yaml.dump(jb_toc, f, default_flow_style=False)


def _copy_content_files(slug: str, jb_config: BookMetadata, jb_toc: TableOfContents):
    for ch in jb_toc.get("chapters", []):
        fn = ch["file"]
        shutil.copy(
            f"{DATA_DIR}/md/{slug}/{fn}.md",
            f"{DATA_DIR}/ipynb/{slug}/{fn}.md",
        )


# TODO: move to ipynb 2 html
def _copy_bibliography_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    for bibfile in jb_config.get("bibtex_bibfiles", []):
        shutil.copy(
            f"{DATA_DIR}/input/{bibfile}",
            f"{DATA_DIR}/ipynb/{slug}/{bibfile}",
        )


def _transform_to_ipynb(slug: str, jb_config: BookMetadata, jb_toc: TableOfContents):
    """
    https://myst-nb.readthedocs.io/en/v0.10.1/use/markdown.html#convert-between-ipynb-and-myst-notebooks
    """
    for ch in jb_toc.get("chapters", []):
        fn = f"{DATA_DIR}/ipynb/{slug}/{ch['file']}.md"
        subprocess.run(["jupytext", fn, "--to", "ipynb"])
        fp = pathlib.Path(fn)
        if fp.suffix != ".ipynb":
            fp.unlink(missing_ok=True)


"""
# to convert MyST-markdown to .ipynb
jupytext mystfile.md --to ipynb
# convert notebook.ipynb to a .py file
jupytext --to py notebook.ipynb
# convert all .md files to paired notebooks and execute them
jupytext --set-formats ipynb,md --execute *.md
# Test the ipynb -> py:percent -> ipynb round trip conversion
jupytext --test notebook.ipynb --to py:percent
# Test the ipynb -> (py:percent + ipynb) -> ipynb (à la paired notebook) conversion
jupytext --test --update notebook.ipynb --to py:percent
"""

# def _build_jupyter_book(slug):
#     subprocess.run(
#         [
#             "jupyter-book",
#             "build",
#             f"{DATA_DIR}/jb/{slug}/",
#         ]
#     )
# "--builder=pdfhtml",


if __name__ == "__main__":
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("ipynb", slug)
    # _generate_yaml_files(slug, jb_config, jb_toc)
    # _copy_bibliography_files(slug, jb_config, jb_toc)
    _copy_content_files(slug, jb_config, jb_toc)
    _transform_to_ipynb(slug, jb_config, jb_toc)
    # _build_jupyter_book(slug)
