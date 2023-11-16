# Unsupported markdown features

## Non exhaustive list

This project uses the MyST variant of markdown, which is a superset of the CommonMark specification. 
Also, a support of a given feature might depend on a rendering medium. For example, MyST markdown displayed using a Jupyter Lab might differ in that regard with a markdown layed out in html.
As a result, we do not support all of markdown features that are usually commonly in use. Here is a non-exhaustive list of unsupported markdown features.

### TeX / LaTex cover page

\documentclass{article}
\begin{document}
It would be great if we could introduce a LaTex templates for example for handling title pages.
\end{document}

Read more:
* [How to use LaTeX with MyST Markdown](https://curvenote.com/blog/how-to-use-latex-with-myst-markdown)
* [Create a LaTeX template](https://mystmd.org/jtex/create-a-latex-template)
* [Plain LaTeX template](https://github.com/myst-templates/plain_latex)
* [Frontmatter](https://mystmd.org/guide/frontmatter)

## Table of contents <sup>(MyST feature)</sup>

Our software allows you to automatically generate and display table of contents. Note that the structure of the document will be determined by the heading and not by your configuration file.

**Syntax**

```
:::{tableofcontents}
:::
```

### Strikethrough

```
Strikethrough with ~~two tildes~~.
```

Strikethrough with ~~two tildes~~.

### Unsupported image formats

Please consult the [latest MyST documentation](https://mystmd.org/guide/figures#supported-image-formats) on which image formats are not supported. **Using an unsupported format can result in invalid rendering of an image.

### Videos

```
![](./videos/vid-sample.mp4) 
```

![](./videos/vid-sample.mp4)

### YouTube/Vimeo videos <sup>(MyST feature)</sup>

| ipynb | html |
| ----- | ---- |
| ✅    |  ❌ |

If your video is hosted on one of supported platforms (at the time of writing of this document: on YouTube and on Vimeo) you can embed the video using the url. Note that the book will then be dependent on that external source - if deleted, the video will not be rendered. Also, just copying the url to video might not work. You should create a special link. Usually, there is a `Share > Embed Video` option.

```
:::{iframe} https://www.youtube.com/embed/_TycjDn9WYE?si=HJAZlky46zWndbLE
:width: 50%
An embedded video with a caption
:::
```

:::{iframe} https://www.youtube.com/embed/_TycjDn9WYE?si=HJAZlky46zWndbLE
:width: 50%
An embedded video with a caption
:::

Please read the [MyST guide](https://mystmd.org/guide/figures#youtube-videos) for more details.

### Table alignment <sup>(MyST feature)</sup>

In theory, you should be able to align text in columns by adding a colon (`:`) to the hyphen characters:
* `:---` - align left
* `:---:` - center
* `---:` - align right

```
| Align left | Center | Align right |
| :---       | :---:  | ---:        |
| Text       | Text   | Text        |
```

| Align left | Center | Align right |
| :---       | :---:  | ---:        |
| Text       | Text   | Text        |

### CSV tables <sup>(MyST feature)</sup>

| ipynb | html |
| ----- | ---- |
| ❌    |  ✅ |

**Syntax**

```
:::{csv-table} Example of a csv table
:file: ./csv/csv-example.csv
:::
```

**Result**

:::{csv-table} Example of a csv table
:file: ./csv/csv-example.csv
:::

See the [MyST parser documentation](https://myst-parser.readthedocs.io/en/latest/syntax/tables.html#csv-tables) for more details.

### Diagrams <sup>(MyST feature)</sup>

It should be possible to include [mermaid diagrams](https://mermaid.js.org/) in your book/article using `{mermaid}` directive, for example
* flowcharts
* sequence diagrams
* class diagrams
* state diagrams
* entity relationship diagrams
* user journey diagrams
* Gantt
* pie charts
* quadrant charts
* requirement diagram
* Gitgraph (Git) diagrams
* C4 diagrams
* mindmaps
* timeline
* Zenuml
* Sankey
* XYCharts

Sadly, this does not always render properly. Some implementation examples can be found in [**the diagram chapter**](./diagrams.md) of the guidelines.

Be sure to check the [mermaid documentation](https://mermaid.js.org/intro/getting-started.html) and the [MyST guide](https://mystmd.org/guide/diagrams) for the more information.

### Proofs, Theorems and Algorithms <sup>(MyST feature)</sup>

**TODO, see e.g. https://mystmd.org/guide/proofs-and-theorems**

### Citations <sup>(MyST feature)</sup>

One of the requirements for a publication in this system is inclusion of a bibliography writen in the BibTeX syntax. We highly recommend managing your bibliographies using the [Zotero tool](https://www.zotero.org/), exporting `.bib` file and uploading this file alongside the rest of your book/article.

To cite your sources, use `@` character followed by the identifier from your BibTeX file. Prefixes and suffixes are also allowed. Take the example of such BibTex references:

```
@article{perneger_writing_2004,
	title = {Writing a research article: advice to beginners},
	volume = {16},
	issn = {1464-3677},
	url = {https://doi.org/10.1093/intqhc/mzh053},
	doi = {10.1093/intqhc/mzh053},
	abstract = {Writing research papers does not come naturally to most of us. The typical research paper is a highly codified rhetorical form. Knowledge of the rules—some explicit, others implied—goes a long way toward writing a paper that will get accepted in a peer-reviewed journal.},
	number = {3},
	urldate = {2023-11-16},
	journal = {International Journal for Quality in Health Care},
	author = {Perneger, Thomas V. and Hudelson, Patricia M.},
	month = jun,
	year = {2004},
	pages = {191--192},
}

@book{holliday_doing_2007,
	edition = {2},
	title = {Doing and {Writing} {Qualitative} {Research}},
	isbn = {978-1-4129-1130-6},
	url = {https://doi.org/10.4135/9781446287958},
	doi = {10.4135/9781446287958},
	abstract = {This book provides accessible advice for novice researchers on where to begin and how to proceed. But much more than a simple manual, it also guides the more experience researcher through the social, cultural, and political complexities involved in every step of the way. It is an essential tool for students in all disciplines that engage in qualitative research, including sociology, applied linguistics, management, sport science, health studies and education.},
	publisher = {SAGE Publications Ltd},
	author = {Holliday, Adrian},
	year = {2007},
}
```

With such definitions in your `.bib` file, you can reference these sources in your writing. Here are some ways in which you may want to format your citations (remember to follow the publisher guidelines and to stay consistent):

| Example | Render | Note |
|---|---|---|
| `@holliday_doing_2007` | @holliday_doing_2007 | Citation without brackets |
| `[@holliday_doing_2007]` | [@holliday_doing_2007] | Citation with brackets (*recommended*) |
| `[@holliday_doing_2007; @perneger_writing_2004]` | [@holliday_doing_2007; @perneger_writing_2004] | Multiple citations |
| `[@holliday_doing_2007, p. 100]` | [@holliday_doing_2007, p. 100] | Page number as a suffix example |
| `[@holliday_doing_2007, chap. 2]` | [@holliday_doing_2007, chap. 2] | Chapter as a suffix example |
| `[e.g. @holliday_doing_2007, p. 100; @perneger_writing_2004]` | [e.g. @holliday_doing_2007, p. 100; @perneger_writing_2004] | Example of 'e.g.' prefix |
| ``` {cite}`{see}holliday_doing_2007{fig 12}` ``` | {cite}`{see}holliday_doing_2007{fig 12}` | Example of 'see' prefix and 'figure 12' suffix combined |

Note that by citing the BibTeX sources the system automatically creates a bibliography at the end of the document. Scroll down to find it in this document.

For more information, see the [MyST guide](https://mystmd.org/guide/citations).

### Cross-references

There are three primary ways to create targets:
* Annotating a syntax block with `(target)=`
* Annotating a syntax bloc/inline/span with an `{#id}` attribute (using the [_attrs_block_](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-attributes-block) and [_attrs_inline_](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-attributes-inline) extensions)
* Adding a name option to a directive

**Syntax**

```
(heading-target)=
#### Target heading

{#paragraph-target}
This is a paragraph, with an `id` attribute.

This is a [span with an `id` attribute]{#span-target}.

:::{note}
:name: directive-target
This is a directive with a `name` option
:::

This should allow you to reference those elements from other parts of a book/article.

* [reference1](#heading-target)
* [reference2](#paragraph-target)
* [reference3](#span-target)
* [reference4](#directive-target)
```

**Result**

(heading-target)=
#### Target heading

{#paragraph-target}
This is a paragraph, with an `id` attribute.

This is a [span with an `id` attribute]{#span-target}.

:::{note}
:name: directive-target

This is a directive with a `name` option
:::

This should allow you to reference those elements from other parts of a book/article.

* [reference1](#heading-target)
* [reference2](#paragraph-target)
* [reference3](#span-target)
* [reference4](#directive-target)

See the [MyST documentation](https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html) for more details.

### Interactive notebooks (code blocks)

**Syntax**

```
:::{code-cell} ipython3
from myst_nb import glue
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y, 'b-', linewidth=2)

glue("glued_fig", fig, display=False)
:::
```

**Result**

:::{code-cell} ipython3
from myst_nb import glue
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y, 'b-', linewidth=2)

glue("glued_fig", fig, display=False)
:::

**TODO**

* https://mystmd.org/guide/interactive-notebooks
* https://mystmd.org/guide/reuse-jupyter-outputs
* https://mystmd.org/guide/integrating-jupyter
