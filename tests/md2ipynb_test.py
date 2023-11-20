import pathlib
import shutil
import typing as t

import nbformat as nbf
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

    def _find_cell(
        self, nb: nbf.notebooknode.NotebookNode, s: str
    ) -> dict[str, t.Any]:
        try:
            return next(c for c in nb["cells"] if c["source"].startswith(s))
        except StopIteration:
            return {"id": "", "cell_type": "", "source": "", "metadata": {}}

    def test_h1_heading(self):
        h1 = self._find_cell(self.simple_md, "# Simple CommonMark")
        assert h1["cell_type"] == "markdown"
        assert h1["source"] == "# Simple CommonMark"

    def test_simple_paragraph(self):
        p = self._find_cell(self.simple_md, "Simplest possible ")
        print('type(p["source"])', type(p["source"]))
        assert p["cell_type"] == "markdown"
        assert p["source"] == "Simplest possible markdown."

    def test_code_block_splitting(self):
        cb = self._find_cell(self.simple_md, "```python")
        assert cb["source"].endswith("cowsay('Code block')\n```")

    # def test_code_block_cell_type(self):
    #     """
    #     Currently the transformation does not properly assign cell type
    #     for other type than "markdown".
    #     TODO
    #     """
    #     cb = self._find_cell(self.simple_md, "python\nimport")
    #     assert cb["cell_type"] == "code"

    # def test_myst_code_block_splitting(self):
    #     """
    #     Currently the transformation splits myst directive blocks (incl. code-cells)
    #     on empty lines.
    #     TODO
    #     """
    #     print(self.myst_md)
    #     cb = self._find_cell(self.myst_md, ":::{code-cell}")
    #     assert cb["source"].endswith("display=False)\n:::")

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
