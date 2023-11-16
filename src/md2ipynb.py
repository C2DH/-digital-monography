import argparse
import json
import logging
import pathlib
import re
import shutil
import typing as t
from textwrap import dedent

import markdown_it
import nbformat as nbf
import yaml
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin

from src.constants import CONFIG_NAME, DATA_DIR
from src.utils import (
    BookConfigParser,
    config_logging,
    copy_bibliography,
    copy_static_files,
    create_book_subdir,
    stdout_hero,
)

config_logging()

logger = logging.getLogger("root.md2ipynb")
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_path",
    type=pathlib.Path,
    help=f"Select the project directory, in which there should be {CONFIG_NAME}, "
    "bibliography and content files.",
)

CODE_DIRECTIVE = "{code-cell}"
RAW_DIRECTIVE = "{raw-cell}"


class MystMetadataParsingError(Exception):
    """Error when parsing metadata from myst formatted text"""


class MystParsingError(Exception):
    """Error when parsing myst formatted text"""


def strip_blank_lines(text: str) -> str:
    """Remove initial blank lines"""
    text = text.rstrip()
    while text and text.startswith("\n"):
        text = text[1:]
    return text


def read_fenced_cell(
    token: markdown_it.token.Token, cell_index: int, cell_type
) -> tuple[dict[str, t.Any], list[str]]:
    """Parse (and validate) the full directive text."""
    content = token.content
    if token.map is None:
        raise MystParsingError
    error_msg = "{} cell {} at line {} could not be read: ".format(
        cell_type, cell_index, token.map[0] + 1
    )

    body_lines, options = parse_directive_options(content, error_msg)

    # remove first line of body if blank
    # this is to allow space between the options and the content
    if body_lines and not body_lines[0].strip():
        body_lines = body_lines[1:]

    return options, body_lines


def get_parser() -> markdown_it.MarkdownIt:
    # def get_parser() -> list[markdown_it.token.Token]:
    """Return the markdown-it parser to use."""
    parser = (
        markdown_it.MarkdownIt("commonmark")
        .enable("table")
        .use(front_matter_plugin)
        .use(myst_block_plugin)
        .use(myst_role_plugin)
        # we only need to parse block level components (for efficiency)
        .disable("inline", True)
    )
    return parser


def parse_directive_options(
    content: str, error_msg: str
) -> tuple[list[str], dict[str, t.Any]]:
    """Parse (and validate) the directive option section."""
    options: dict[str, t.Any] = {}
    if content.startswith("---"):
        content = "\n".join(content.splitlines()[1:])
        match = re.search(r"^-{3,}", content, re.MULTILINE)
        if match:
            yaml_block = content[: match.start()]
            content = content[match.end() + 1 :]
        else:
            yaml_block = content
            content = ""
        yaml_block = dedent(yaml_block)
        try:
            options = yaml.safe_load(yaml_block) or {}
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as error:
            raise MystMetadataParsingError(
                error_msg + "Invalid YAML; " + str(error)
            )
    elif content.lstrip().startswith(":"):
        content_lines = content.splitlines()  # type: list
        yaml_lines = []
        while content_lines:
            if not content_lines[0].lstrip().startswith(":"):
                break
            yaml_lines.append(content_lines.pop(0).lstrip()[1:])
        yaml_block = "\n".join(yaml_lines)
        content = "\n".join(content_lines)
        try:
            options = yaml.safe_load(yaml_block) or {}
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as error:
            raise MystMetadataParsingError(
                error_msg + "Invalid YAML; " + str(error)
            )

    return content.splitlines(), options


def read_cell_metadata(
    token: markdown_it.token.Token, cell_index: int
) -> dict[str, t.Any]:
    """Return cell metadata"""
    metadata = {}
    if token.content and (token.map is not None):
        try:
            metadata = json.loads(token.content.strip())
        except Exception as err:
            raise MystMetadataParsingError(
                "Markdown cell {} at line {} could not be read: {}".format(
                    cell_index, token.map[0] + 1, err
                )
            )
        if not isinstance(metadata, dict):
            raise MystMetadataParsingError(
                "Markdown cell {} at line {} is not a dict".format(
                    cell_index, token.map[0] + 1
                )
            )

    return metadata


def is_code_directive(
    token: markdown_it.token.Token,
    nesting_level: int,
    code_directive: str = CODE_DIRECTIVE,
) -> bool:
    return (
        token.type == "fence"
        and token.info.startswith(code_directive)
        and nesting_level == 0
    )


def is_raw_directive(
    token: markdown_it.token.Token,
    nesting_level: int,
    raw_directive: str = RAW_DIRECTIVE,
) -> bool:
    return (
        token.type == "fence"
        and token.info.startswith(raw_directive)
        and nesting_level == 0
    )


def is_myst_block_break(token, nesting_level):
    return token.type == "myst_block_break" and nesting_level == 0


def myst_to_notebook(
    text: str,
    code_directive: str = CODE_DIRECTIVE,
    raw_directive: str = RAW_DIRECTIVE,
    add_source_map: bool = False,
) -> nbf.notebooknode.NotebookNode:
    """Convert text written in the myst format to a notebook.

    :param text: the file text
    :param code_directive: the name of the directive to search for containing code cells
    :param raw_directive: the name of the directive to search for containing raw cells
    :param add_source_map: add a `source_map` key to the notebook metadata,
        which is a list of the starting source line number for each cell.

    :raises MystMetadataParsingError if the metadata block is not valid JSON/YAML

    NOTE: we assume here that all of these directives are at the top-level,
    i.e. not nested in other directives.
    """
    logger.info(f"Opened {len(text.encode('utf-8'))} bytes of markdown text.")
    tokens = get_parser().parse(text + "\n")
    lines = text.splitlines()
    md_start_line = 0

    # get the document metadata
    metadata_nb = {}
    if tokens and tokens[0].type == "front_matter":
        metadata: markdown_it.token.Token = tokens.pop(0)
        if metadata and metadata.map:
            md_start_line = metadata.map[1]
        try:
            metadata_nb = yaml.safe_load(metadata.content)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as error:
            raise MystMetadataParsingError(f"Notebook metadata: {error}")

    # create an empty notebook
    nbf_version = nbf.v4
    kwargs = {"metadata": nbf.from_dict(metadata_nb)}
    notebook = nbf_version.new_notebook(**kwargs)
    # 'source_map' is a list of the starting line number for each cell
    source_map: list[int] = []

    def _flush_markdown(
        start_line: int,
        token: t.Optional[markdown_it.token.Token],
        md_metadata: dict[str, t.Any],
    ) -> None:
        """When we find a cell we check if there is preceding text.o"""
        endline = token.map[0] if token and token.map else len(lines)
        md_source = strip_blank_lines("\n".join(lines[start_line:endline]))
        meta = nbf.from_dict(md_metadata)
        if md_source:
            source_map.append(start_line)
            notebook.cells.append(
                nbf_version.new_markdown_cell(source=md_source, metadata=meta)
            )

    def _add_markdown_cell(
        token: t.Optional[markdown_it.token.Token],
        md_metadata: dict[str, t.Any],
    ) -> None:
        """Append notebook cells with a markdown block
        that corresponds to the `token.map[block_start, block_end]` values"""
        startline = token.map[0]
        endline = token.map[1]
        md_source = strip_blank_lines("\n".join(lines[startline:endline]))
        meta = nbf.from_dict(md_metadata)
        notebook.cells.append(
            nbf_version.new_markdown_cell(source=md_source, metadata=meta)
        )

    # iterate through the tokens to identify notebook cells
    nesting_level: int = 0
    md_metadata: dict[str, t.Any] = {}

    for token in tokens:
        # catch empty map attr before indexing it
        if not token or token.map is None:
            continue

        nesting_level += token.nesting

        if is_code_directive(token, nesting_level):
            _flush_markdown(md_start_line, token, md_metadata)
            options, body_lines = read_fenced_cell(
                token, len(notebook.cells), "Code"
            )
            meta = nbf.from_dict(options)
            source_map.append(token.map[0] + 1)
            notebook.cells.append(
                nbf_version.new_code_cell(
                    source="\n".join(body_lines), metadata=meta
                )
            )
            md_metadata = {}
            md_start_line = token.map[1]

        elif is_raw_directive(token, nesting_level):
            _flush_markdown(md_start_line, token, md_metadata)
            options, body_lines = read_fenced_cell(
                token, len(notebook.cells), "Raw"
            )
            meta = nbf.from_dict(options)
            source_map.append(token.map[0] + 1)
            notebook.cells.append(
                nbf_version.new_raw_cell(
                    source="\n".join(body_lines), metadata=meta
                )
            )
            md_metadata = {}
            md_start_line = token.map[1]

        elif is_myst_block_break(token, nesting_level):
            _flush_markdown(md_start_line, token, md_metadata)
            md_metadata = read_cell_metadata(token, len(notebook.cells))
            md_start_line = token.map[1]

        elif token.level == 0:
            # note the is MD cell metadata is always empty
            _add_markdown_cell(token, {})
            md_start_line = token.map[1]

    _flush_markdown(md_start_line, None, md_metadata)

    if add_source_map:
        notebook.metadata["source_map"] = source_map
    return notebook


def _write_notobook(
    nb: nbf.notebooknode.NotebookNode,
    fp: pathlib.PurePath,
    capture_validation_error=None,
    **kwargs,
) -> None:
    nbf.write(
        nb,
        fp,
        version=nb.get("nbformat", 4),
        capture_validation_error=capture_validation_error,
        **kwargs,
    )


def _copy_content_files(slug: str):
    src_dir = pathlib.Path(f"{DATA_DIR}/md/{slug}")
    for md in src_dir.glob("*.md"):
        shutil.copy(
            f"{DATA_DIR}/md/{slug}/{md.name}",
            f"{DATA_DIR}/ipynb/{slug}/{md.name}",
        )


def _transform_md_files(
    slug: str,
) -> dict[pathlib.PurePath, nbf.notebooknode.NotebookNode]:
    src_dir = pathlib.Path(f"{DATA_DIR}/ipynb/{slug}")
    notebooks = {}
    for md_path in src_dir.glob("*.md"):
        logger.info(f"Transforming the file '{md_path}' to '.ipynb'.")
        nb_path = _get_new_ipynb_filepath(md_path)
        with open(md_path, encoding="utf-8") as f:
            nb = myst_to_notebook(f.read())
            notebooks[nb_path] = nb
    return notebooks


def _write_notebooks(
    notebooks: dict[pathlib.PurePath, nbf.notebooknode.NotebookNode]
) -> None:
    for nb_path, nb in notebooks.items():
        _write_notobook(nb, nb_path)
        logger.info(f"Transforming the file to '{nb_path}' ended.")


def _get_new_ipynb_filepath(fp: pathlib.PurePath) -> pathlib.PurePath:
    return fp.parent / (fp.name.replace(fp.suffix, ".ipynb"))


def _remove_md_files(slug: str) -> None:
    src_dir = pathlib.Path(f"{DATA_DIR}/ipynb/{slug}")
    for md_path in src_dir.glob("*.md"):
        md_path.unlink(missing_ok=True)


if __name__ == "__main__":
    stdout_hero("md2ipynb")
    logger.info("New process: transforming .md files to a .ipynb files.")
    args = parser.parse_args()
    bc = BookConfigParser(args.project_path)
    bc.open_book_config()
    jb_config = bc.jb_config
    jb_toc = bc.jb_toc
    slug = bc.slug
    create_book_subdir("ipynb", slug)
    copy_static_files(
        pathlib.Path(DATA_DIR) / "md" / args.project_path.name,
        pathlib.Path(DATA_DIR) / "ipynb" / args.project_path.name,
    )
    copy_bibliography(
        pathlib.Path(DATA_DIR) / "md" / args.project_path.name,
        pathlib.Path(DATA_DIR) / "ipynb" / args.project_path.name,
    )
    _copy_content_files(slug)
    notebooks = _transform_md_files(slug)
    _write_notebooks(notebooks)
    _remove_md_files(slug)
