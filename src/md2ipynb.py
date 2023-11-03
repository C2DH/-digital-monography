import argparse
import logging
import pathlib
import shutil

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

logger = logging.getLogger("root.md2ipynb")
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_path",
    type=pathlib.Path,
    help=f"Select the project directory, in which there should be {CONFIG_NAME}, "
    "bibliography and content files.",
)


def _copy_content_files(
    slug: str, jb_config: BookMetadata, jb_toc: TableOfContents
):
    for ch in jb_toc.get("chapters", []):
        fn = ch["file"]
        shutil.copy(
            f"{DATA_DIR}/md/{slug}/{fn}",
            f"{DATA_DIR}/ipynb/{slug}/{fn}",
        )
    logger.info("Found no errors while copying content files.")


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
        fn = f"{DATA_DIR}/ipynb/{slug}/{ch['file']}"
        # subprocess_run_and_log(
        #     ["jupyter-book", "myst", "init", fn], logger
        # ) # maybe this is the way? untested
        subprocess_run_and_log(["jupytext", fn, "--to", "ipynb"], logger)
    logger.info("Found no errors while transforming files to .ipynb.")


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
