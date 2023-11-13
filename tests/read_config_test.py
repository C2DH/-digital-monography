import pathlib

from src.utils.read_config import BookConfigParser

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
    assert jb_toc["chapters"][0]["file"] == "input_guidelines.md"
    assert jb_toc["chapters"][1]["file"] == "what_is_md.md"
    assert jb_toc["chapters"][2]["file"] == "markdown_guidelines.md"
    assert jb_toc["chapters"][-1]["file"] == "diagrams.md"


def test_slug():
    bc = BookConfigParser(CONFIG_PATH)
    bc.open_book_config()
    assert bc.slug == CONFIG_PATH.name
