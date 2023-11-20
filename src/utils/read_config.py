import dataclasses
import logging
import pathlib
import typing as t

import yaml

from src.constants import CONFIG_NAME, DEFAULT_MYSTMD_CONFIG

from .log_mgnt import config_logging

config_logging()


logger = logging.getLogger("utils.read_config")


@dataclasses.dataclass
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


@dataclasses.dataclass
class BookMetadataParse:
    myst_enable_extensions: t.Any
    myst_url_schemes: list[str]
    myst_dmath_double_inline: bool


@dataclasses.dataclass
class BookMetadataHtmlComments:
    hypothesis: bool
    utterances: bool


@dataclasses.dataclass
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


@dataclasses.dataclass
class BookMetadataLatex:
    use_jupyterbook_latex: bool
    latex_engine: t.Literal[
        "pdflatex", "xelatex", "luatex", "platex", "uplatex"
    ]


@dataclasses.dataclass
class BookMetadataLaunchButtons:
    notebook_interface: str
    binderhub_url: str
    jupyterhub_url: str
    thebe: str
    colab_url: str


@dataclasses.dataclass
class BookMetadataRepository:
    url: str
    path_to_book: str
    branch: str


@dataclasses.dataclass
class BookMetadataSphinx:
    extra_extensions: list[t.Any]
    local_extensions: list[t.Any]
    recursive_update: bool
    config: dict[str, t.Any]


@dataclasses.dataclass
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


@dataclasses.dataclass
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
        rawconfig = yaml.safe_load(
            self.config_path.read_text(encoding="utf-8")
        )
        jb_config = rawconfig["book_metadata"]
        jb_toc = rawconfig["table_of_contents"]
        return jb_config, jb_toc

    def _verify_config_syntax(self) -> None:
        # TODO # maybe recurse over kv of each config and assert the type?
        # `assert isinstance(arg, int)`
        # see https://mypy.readthedocs.io/en/stable/type_narrowing.html#type-narrowing-expressions
        pass

    def _get_book_slug(self) -> str:
        return self.project_path.name


def get_ordered_filename(
    order: int, fp: pathlib.Path, total_items: int
) -> str:
    """
    Generate a filename '01_filename' for arbitrary file ordering.
    """
    mask = "0" * len(str(total_items)) if total_items >= 10 else "00"
    name = fp.name.replace(fp.suffix, "")
    return "{nbr:0>{msk}}_{nme}".format(nbr=order, msk=len(mask), nme=name)


def is_root_in_chapters(
    jb_toc: TableOfContents,
) -> bool:
    try:
        chapters = jb_toc["chapters"]
        return next(f for f in chapters if f.get("file", "") == jb_toc["root"])
    except (KeyError, StopIteration):
        return False


def _update(d1: dict[str, t.Any], d2: dict[str, t.Any]) -> dict[str, t.Any]:
    """
    Recurse over dictionary d2 and update d1 with it's values.
    Return d1 updated with d2 values.
    Note that dictionaries inside a list
    will just be replaced without updating.
    """
    for k, v in d2.items():
        if isinstance(v, dict):
            d1[k] = _update(d1.get(k, {}), v)
        else:
            d1[k] = v
    return d1


def write_myst_yml_file(
    dst: pathlib.Path,
    custom_conf: dict[str, t.Any] = None,
) -> None:
    # TODO: read config from the config.yaml given in an author's package
    if custom_conf is None:
        custom_conf = {}
    updated_conf = _update(DEFAULT_MYSTMD_CONFIG, custom_conf)
    if not dst.is_dir():
        logger.error(
            f"Cannot write 'myst.yml' file to {dst}. Destination is not a directory."
        )
        raise
    with open(dst / "myst.yml", "w") as f:
        yaml.dump(updated_conf, f)
