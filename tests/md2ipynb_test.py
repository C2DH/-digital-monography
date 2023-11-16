import pathlib
import shutil

import pytest

from src.constants import DATA_DIR
from src.md2ipynb import (
    _remove_md_files,
    _transform_md_files,
    _write_notebooks,
)


@pytest.mark.slow
@pytest.mark.integration
class TestClass:
    dst = pathlib.Path(DATA_DIR) / "ipynb" / "_fixtures"
    src = pathlib.Path("tests/_fixtures/")

    @classmethod
    def setup_class(cls):
        """
        1. delete all files in ipynb/slug/
        2. copy fixtures to ipynb/slug/
        3. transform md files to ipynb
        4. define variables for testing
        5. write ipynb to ipynb/slug/
        """
        shutil.rmtree(cls.dst, ignore_errors=True)
        shutil.copytree(cls.src, cls.dst)
        slug = "_fixtures"
        cls.notebooks = _transform_md_files(slug)
        for md_path, nb in cls.notebooks.items():
            if md_path.name == "simple_commonmark.ipynb":
                cls.simple_md = nb
            elif md_path.name == "myst_extensions.ipynb":
                cls.myst_md = nb
        _write_notebooks(cls.notebooks)
        _remove_md_files(slug)

    def test_h1_heading(self):
        h1 = self.simple_md["cells"][0]
        assert h1["cell_type"] == "markdown"
        assert h1["source"] == "# Simple CommonMark"

    def test_simple_paragraph(self):
        p = self.simple_md["cells"][1]
        assert p["cell_type"] == "markdown"
        assert p["source"] == "Simplest possible markdown."

    def test_write_notebooks(self):
        expected = [
            # we are copying from _fixtures dir, so files are not ordered
            "index.ipynb",
            "simple_commonmark.ipynb",
            "myst_extensions.ipynb",
        ]
        returned = [fp.name for fp in self.dst.glob("*.ipynb")]
        assert len(expected) == len(returned)
        assert expected[0] in returned
        assert expected[1] in returned
        assert expected[2] in returned

    def test_remove_md_files(self):
        assert len([fp.name for fp in self.dst.glob("*.md")]) == 0

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.dst, ignore_errors=True)
