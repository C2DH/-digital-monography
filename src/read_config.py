import tomllib
import typing as t
import uuid
from dataclasses import dataclass


@dataclass
class BookMetadataExecute:
    cache: str
    exclude_patterns: list[t.Any]
    timeout: int
    run_in_temp: bool
    allow_errors: bool
    stderr_output: t.Literal["show", "remove", "remove-warn", "warn", "error", "severe"]
    execute_notebooks: t.Literal["auto", "force", "cache", "off"]


@dataclass
class BookMetadataParse:
    myst_enable_extensions: t.Any
    myst_url_schemes: list[str]
    myst_dmath_double_inline: bool


@dataclass
class BookMetadataHtmlComments:
    hypothesis: bool
    utterances: bool


@dataclass
class BookMetadataHtml:
    favicon: str
    use_edit_page_button: bool
    use_repository_button: bool
    use_issues_button: bool
    use_multitoc_numbering: bool
    extra_footer: str
    google_analytics_id: str
    home_page_in_navbar: bool
    baseurl: str
    analytics: t.Any
    comments: BookMetadataHtmlComments
    announcement: str


@dataclass
class BookMetadataLatex:
    use_jupyterbook_latex: bool
    latex_engine: t.Literal["pdflatex", "xelatex", "luatex", "platex", "uplatex"]


@dataclass
class BookMetadataLaunchButtons:
    notebook_interface: str
    binderhub_url: str
    jupyterhub_url: str
    thebe: str
    colab_url: str


@dataclass
class BookMetadataRepository:
    url: str
    path_to_book: str
    branch: str


@dataclass
class BookMetadataSphinx:
    extra_extensions: list[t.Any]
    local_extensions: list[t.Any]
    recursive_update: bool
    config: dict[str, t.Any]


@dataclass
class BookMetadata:
    """
    https://jupyterbook.org/en/stable/customize/config.html
    """

    title: str
    author: str
    copyright: str
    logo: str
    exclude_patterns: list[t.Any]
    only_build_toc_files: bool
    bibtex_bibfiles: list[str]
    execute: BookMetadataExecute
    parse: BookMetadataParse
    html: BookMetadataHtml
    latex: BookMetadataLatex
    launch_buttons: BookMetadataLaunchButtons
    repository: BookMetadataRepository
    sphinx: BookMetadataSphinx


@dataclass
class TableOfContents:
    """
    https://jupyterbook.org/en/stable/structure/toc.html
    """

    format: t.Literal["jb-book", "jb-article"]
    root: str
    chapters: list[str]


class BookConfigParser:
    def __init__(self):
        self.jb_config: BookMetadata = None
        self.jb_toc: TableOfContents = None
        self.slug: str = str(uuid.uuid4())

    def open_book_config(self):
        self.jb_config, self.jb_toc = self._open_book_config()
        self._verify_book_config()
        self.slug: str = self._get_book_slug()

    def _open_book_config(self) -> tuple[BookMetadata, TableOfContents]:
        with open("/home/app_user/data/input/config.toml", "rb") as f:
            tomlconfig = tomllib.load(f)
        jb_config = tomlconfig["book_metadata"]
        jb_toc = tomlconfig["table_of_contents"]
        return jb_config, jb_toc

    def _verify_book_config(self) -> bool:
        # TODO # maybe recurse over kv of each config and assert the type?
        # `assert isinstance(arg, int)`
        # see https://mypy.readthedocs.io/en/stable/type_narrowing.html#type-narrowing-expressions
        return True

    def _get_book_slug(self) -> str:
        return "lucchesi_for-a-new-hermeneutics-of-practice-in-digital-public-history"
