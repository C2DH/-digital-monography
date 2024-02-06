import pathlib
import shutil

import pytest

from src.constants import DATA_DIR
from src.prepmd import copy_input_files_to_md_dir

# TODO: add github url as input tests


@pytest.mark.slow
@pytest.mark.integration
class TestClass:
    dst = pathlib.Path(DATA_DIR) / "md" / "_fixtures"

    @classmethod
    def setup_class(cls):
        """
        1. delete all files in md/slug/
        2. run the main function
        """
        shutil.rmtree(cls.dst, ignore_errors=True)
        copy_input_files_to_md_dir(pathlib.Path("tests/_fixtures/"))

    def test_copying_root_and_chapters(self):
        expected = [
            "00_index.md",
            "01_simple_commonmark.md",
            "02_myst_extensions.md",
        ]
        returned = [fp.name for fp in self.dst.glob("*.md")]
        assert len(expected) == len(returned)
        assert expected[0] in returned
        assert expected[1] in returned
        assert expected[2] in returned

    def test_md_is_non_empty(self):
        with open(self.dst / "00_index.md", encoding="utf-8") as f:
            text = f.read()
        assert text.startswith("# Index")

    def test_myst_yml_creation(self):
        assert pathlib.Path(self.dst / "myst.yml").exists()

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.dst, ignore_errors=True)
