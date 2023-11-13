import logging
import pathlib
import tomllib
import typing as t
from dataclasses import dataclass

from src.constants import CONFIG_NAME

from .log_mgnt import config_logging

config_logging()


logger = logging.getLogger("utils.read_config")


@dataclass
class BookMetadataExecute:
    cache: str
    exclude_patterns: list[t.Any]
    timeout: int
    run_in_temp: bool
    allow_errors: bool
    stderr_output: t.Literal[
        "show", "remove", "remove-warn", "warn", "error", "severe"
    ]
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
    latex_engine: t.Literal[
        "pdflatex", "xelatex", "luatex", "platex", "uplatex"
    ]


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


class ConfigFileNotFoundError(FileNotFoundError):
    pass


class BookConfigParser:
    def __init__(self, source: pathlib.PurePath) -> None:
        self.config_name = CONFIG_NAME
        self.project_path: pathlib.PurePath = source
        self.jb_config: t.Optional[BookMetadata] = None
        self.jb_toc: t.Optional[TableOfContents] = None
        self.slug: str = ""

    def open_book_config(self) -> None:
        self._verify_config_existence()
        self.config_path = self._find_config_path()
        self.jb_config, self.jb_toc = self._open_book_config()
        self.slug = self._get_book_slug()
        self._verify_config_syntax()

    def _verify_config_existence(self) -> None:
        # if not issubclass(type(self.project_path), pathlib.PurePath):
        #     logger.error(
        #         f"Constructor of {self.__name__} class expects a pathlib.Path."
        #     )
        if not self.project_path.exists():
            logger.critical(
                "The selected project directory was "
                f"not found in selected path: '{self.project_path}'."
            )
            raise ConfigFileNotFoundError
        if not self.project_path.is_dir():
            logger.critical(
                "The selected project folder exists, "
                f"but is not a directory. Path: '{self.project_path}'."
            )
            raise ConfigFileNotFoundError
        config_path = self._find_config_path()
        if not config_path.exists():
            logger.critical(
                "The configuration file was not found "
                f"in selected path '{config_path}'."
            )
            raise ConfigFileNotFoundError
        if not config_path.is_file():
            logger.critical(
                "The configuration exists but is not a proper file."
                f"Path '{config_path}'."
            )
            raise ConfigFileNotFoundError

    def _find_config_path(self) -> pathlib.PurePath:
        return self.project_path / self.config_name

    def _open_book_config(self) -> tuple[BookMetadata, TableOfContents]:
        with open(self.config_path, "rb") as f:
            tomlconfig = tomllib.load(f)
        jb_config = tomlconfig["book_metadata"]
        jb_toc = tomlconfig["table_of_contents"]
        return jb_config, jb_toc

    def _verify_config_syntax(self) -> None:
        # TODO # maybe recurse over kv of each config and assert the type?
        # `assert isinstance(arg, int)`
        # see https://mypy.readthedocs.io/en/stable/type_narrowing.html#type-narrowing-expressions
        pass

    def _get_book_slug(self) -> str:
        return self.project_path.name
