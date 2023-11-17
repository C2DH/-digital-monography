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

### Proofs, Theorems and Algorithms <sup>(MyST feature)</sup>

**TODO, see e.g. https://mystmd.org/guide/proofs-and-theorems**

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
