import shutil

from read_config import BookConfigParser, BookMetadata, TableOfContents
from utils import create_book_subdir


def _copy_content_files(slug: str, jb_config: BookMetadata, jb_toc: TableOfContents):
    for ch in jb_toc.get("chapters", []):
        fn = ch["file"]
        shutil.copy(
            f"/home/app_user/data/input/{fn}",
            f"/home/app_user/data/md/{slug}/{fn}",
        )


if __name__ == "__main__":
    bc = BookConfigParser()
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("md", slug)
    _copy_content_files(slug, jb_config, jb_toc)
