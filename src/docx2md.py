import argparse
import logging
import pathlib
import shutil

from src.constants import CONFIG_NAME, DATA_DIR
from src.utils import (
    BookConfigParser,
    TableOfContents,
    config_logging,
    copy_static_files,
    create_book_subdir,
    get_ordered_filename,
    is_root_in_chapters,
    stdout_hero,
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
    """
    Copy files indicated in the configuration file as chapters and additional files.
    """
    slug = project_path.name
    total_files = _count_files_to_copy(jb_toc)
    _copy_root_file(jb_toc, project_path, total_files, slug)
    _copy_chapters(jb_toc, project_path, total_files, slug)
    logger.info(
        "Found no errors while copying input files to 'md' subdirectory."
    )


def _count_files_to_copy(jb_toc: TableOfContents) -> int:
    """
    By default, MyST orders files by their names.
    """
    if is_root_in_chapters(jb_toc):
        additional_files = 0
    else:
        additional_files = 1  # +1 for the root file
    return len(jb_toc.get("chapters", [])) + additional_files


def _copy_root_file(
    jb_toc: TableOfContents,
    project_path: pathlib.PurePath,
    total_files: int,
    slug: str,
) -> None:
    """
    Copy the file described in the config as 'root' to the 'md/slug/' directory.
    """
    if not is_root_in_chapters(jb_toc):
        src = project_path / jb_toc["root"]
        new_fn = get_ordered_filename(0, src, total_files) + src.suffix
        dst = pathlib.Path(DATA_DIR) / "md" / slug / new_fn
        _copy(src, dst)


def _copy_chapters(
    jb_toc: TableOfContents,
    project_path: pathlib.PurePath,
    total_files: int,
    slug: str,
) -> None:
    """
    Copy files included in the config as 'chapters' to the 'md/slug/' directory.
    """
    additional_files = total_files - len(jb_toc.get("chapters", []))
    for idx, ch in enumerate(jb_toc.get("chapters", []), additional_files):
        fn = ch["file"]
        src = project_path / fn
        new_fn = get_ordered_filename(idx, src, total_files) + src.suffix
        dst = pathlib.Path(DATA_DIR) / "md" / slug / new_fn
        _copy(src, dst)


def _copy(src: pathlib.PurePath, dst: pathlib.PurePath) -> None:
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


def copy_input_files_to_md_dir(project_path: pathlib.PurePath) -> None:
    bc = BookConfigParser(project_path)
    bc.open_book_config()
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("md", slug)
    copy_static_files(
        project_path,
        pathlib.Path(DATA_DIR) / "md" / project_path.name,
    )
    _copy_content_files(project_path, jb_toc)


if __name__ == "__main__":
    stdout_hero("docx2md")
    logger.info("New process: transforming input files to .md files.")
    args = parser.parse_args()
    project_path = args.project_path
    copy_input_files_to_md_dir(project_path)
