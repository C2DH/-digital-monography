import json
import re
from textwrap import dedent

import nbformat as nbf
import yaml

try:
    from markdown_it import MarkdownIt
    from mdit_py_plugins.front_matter import front_matter_plugin
    from mdit_py_plugins.myst_blocks import myst_block_plugin
    from mdit_py_plugins.myst_role import myst_role_plugin
except ImportError:
    MarkdownIt = None


CODE_DIRECTIVE = "{code-cell}"
RAW_DIRECTIVE = "{raw-cell}"


class MystMetadataParsingError(Exception):
    """Error when parsing metadata from myst formatted text"""


def is_myst_available():
    """Whether the markdown-it-py package is available."""
    return MarkdownIt is not None


def raise_if_myst_is_not_available():
    if not is_myst_available():
        raise ImportError(
            "The MyST Markdown format requires python >= 3.6 and markdown-it-py~=1.0"
        )


def strip_blank_lines(text):
    """Remove initial blank lines"""
    text = text.rstrip()
    while text and text.startswith("\n"):
        text = text[1:]
    return text


def read_fenced_cell(token, cell_index, cell_type):
    """Parse (and validate) the full directive text."""
    content = token.content
    error_msg = "{} cell {} at line {} could not be read: ".format(
        cell_type, cell_index, token.map[0] + 1
    )

    body_lines, options = parse_directive_options(content, error_msg)

    # remove first line of body if blank
    # this is to allow space between the options and the content
    if body_lines and not body_lines[0].strip():
        body_lines = body_lines[1:]

    return options, body_lines


def get_parser():
    """Return the markdown-it parser to use."""
    parser = (
        MarkdownIt("commonmark")
        .enable("table")
        .use(front_matter_plugin)
        .use(myst_block_plugin)
        .use(myst_role_plugin)
        # we only need to parse block level components (for efficiency)
        .disable("inline", True)
    )
    return parser


def parse_directive_options(content, error_msg):
    """Parse (and validate) the directive option section."""
    options = {}
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


def read_cell_metadata(token, cell_index):
    """Return cell metadata"""
    metadata = {}
    if token.content:
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


def myst_to_notebook(
    text,
    code_directive=CODE_DIRECTIVE,
    raw_directive=RAW_DIRECTIVE,
    add_source_map=False,
):
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
    raise_if_myst_is_not_available()

    tokens = get_parser().parse(text + "\n")
    lines = text.splitlines()
    md_start_line = 0

    # get the document metadata
    metadata_nb = {}
    if tokens and tokens[0].type == "front_matter":
        metadata = tokens.pop(0)
        md_start_line = metadata.map[1]
        try:
            metadata_nb = yaml.safe_load(metadata.content)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as error:
            raise MystMetadataParsingError(f"Notebook metadata: {error}")

    # create an empty notebook
    nbf_version = nbf.v4
    kwargs = {"metadata": nbf.from_dict(metadata_nb)}
    notebook = nbf_version.new_notebook(**kwargs)
    source_map = []  # this is a list of the starting line number for each cell

    def _flush_markdown(start_line, token, md_metadata):
        """When we find a cell we check if there is preceding text.o"""
        endline = token.map[0] if token else len(lines)
        md_source = strip_blank_lines("\n".join(lines[start_line:endline]))
        meta = nbf.from_dict(md_metadata)
        if md_source:
            source_map.append(start_line)
            notebook.cells.append(
                nbf_version.new_markdown_cell(source=md_source, metadata=meta)
            )

    # iterate through the tokens to identify notebook cells
    nesting_level = 0
    md_metadata = {}

    for token in tokens:
        nesting_level += token.nesting

        if nesting_level != 0:
            # we ignore fenced block that are nested, e.g. as part of lists, etc
            continue

        if token.type == "fence" and token.info.startswith(code_directive):
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

        elif token.type == "fence" and token.info.startswith(raw_directive):
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

        elif token.type == "myst_block_break":
            _flush_markdown(md_start_line, token, md_metadata)
            md_metadata = read_cell_metadata(token, len(notebook.cells))
            md_start_line = token.map[1]

    _flush_markdown(md_start_line, None, md_metadata)

    if add_source_map:
        notebook.metadata["source_map"] = source_map
    return notebook
