import pathlib

from src.utils.read_config import (
    BookConfigParser,
    get_ordered_filename,
    is_root_in_chapters,
)

CONFIG_PATH = pathlib.Path("/tests/fixtures/")


def test_config_name():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    assert bc.config_name == "config.yaml"


def test_jb_config():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    jb_config = bc.jb_config
    assert jb_config["title"] == "Title of the book"
    assert jb_config["author"] == "Gallus Anonymus"
    assert jb_config["bibtex_bibfiles"][0] == "bibliography.bib"


def test_table_of_contents():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    jb_toc = bc.jb_toc
    assert jb_toc["format"] == "jb-book"
    assert jb_toc["root"] == "index.md"
    assert jb_toc["chapters"][0]["file"] == "simple_commonmark.md"
    assert jb_toc["chapters"][1]["file"] == "myst_extensions.md"
    assert jb_toc["chapters"][-1]["file"] == "myst_extensions.md"


def test_slug():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    assert bc.slug == CONFIG_PATH.name


def test_is_root_in_chapters_False():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    jb_toc = bc.jb_toc
    jb_toc["root"] = "x"
    jb_toc["chapters"] = [
        {"file": "ssdadsad"},
        {"file": "aasda"},
        {"file": "hrthrth"},
        {"file": "xxx"},
        {"file": "iiiiiioasid"},
    ]
    assert is_root_in_chapters(jb_toc) == False


def test_is_root_in_chapters_True():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    jb_toc = bc.jb_toc
    jb_toc["root"] = "xxx"
    jb_toc["chapters"] = [
        {"file": "ssdadsad"},
        {"file": "aasda"},
        {"file": "hrthrth"},
        {"file": "xxx"},
        {"file": "iiiiiioasid"},
    ]
    assert is_root_in_chapters(jb_toc)


def test_is_root_in_chapters_False_because_its_empty():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    jb_toc = bc.jb_toc
    jb_toc["root"] = "x"
    jb_toc["chapters"] = []
    assert is_root_in_chapters(jb_toc) == False


def test_get_ordered_name_1():
    fp = pathlib.Path(f"docs/usage/index.md")
    assert get_ordered_filename(0, fp, 5) == "00_index"


def test_get_ordered_name_2():
    fp = pathlib.Path(f"docs/usage/index.md")
    assert get_ordered_filename(99, fp, 99) == "99_index"


def test_get_ordered_name_3():
    fp = pathlib.Path(f"docs/usage/index.md")
    assert get_ordered_filename(0, fp, 100) == "000_index"


def test_get_ordered_name_4():
    fp = pathlib.Path(f"docs/usage/index.md")
    assert get_ordered_filename(1, fp, 1000) == "0001_index"
