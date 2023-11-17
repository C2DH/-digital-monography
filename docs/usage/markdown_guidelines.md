# Markdown guidelines

## Headers

**Syntax**

```
# Chapter 1 title
## Chapter 1 second header
### Chapter 1 third header
#### Chapter 1 section title
##### Chapter 1 section second header
```

**Result**

# Chapter 1 title (only an example of heading syntax)
## Chapter 1 second header
### Chapter 1 third header
#### Chapter 1 section title
##### Chapter 1 section second header

More than six `#` characters is not a heading.

For more details please read [the specification](https://spec.commonmark.org/0.30/#atx-heading). It might be also useful to read ["how headers and sections map onto to book structure"](https://jupyterbook.org/en/stable/structure/sections-headers.html#how-headers-and-sections-map-onto-to-book-structure).

## Typography

### Paragraphs

It is recommended to divide each paragraph with an empty line.

Please remember that reading continuous blocks of text from a screen can be more eye-straining than reading it from a book.

```
    Do not add tabs or spaces at the start of a paragraph.
Such indentation has a special meaning. Using it might lead to unintended formatting.
```

### Italics

| Syntax | Result |
| --- | --- |
| `To write in italics, use single *asterisks* or _underscores_.` | To write in italics, use single *asterisks* or _underscores_. |

### Bold

| Syntax | Result |
| --- | --- |
| `You can make text bold with double **asterisks** or __underscores__.` | You can make text bold with double **asterisks** or __underscores__. |

### Escaping symbols

Sometimes you might want to use \*asterisks\*, \_\_underscores\_\_, etc. without special formatting. To do this, place the backslash (`\`) before a special character.

| Syntax | Result |
| --- | --- |
| `\*asterisks\*` | \*asterisks\* |
| `\_\_underscores\_\_` | \_\_underscores\_\_ |

### Subscript

| Syntax | Result |
| --- | --- |
| ```H{sub}`2`O``` | H{sub}`2`O |

### Superscript

| Syntax | Result |
| --- | --- |
| ```11{sup}`th` of November``` | 11{sup}`th` of November |

## Horizontal Rule

To indicate section breaks in your work, you can use the horizontal rule. To form a visible break within a part of your book/article, use `***`, `---` or `___`.

**Syntax**

```
Text
***
More text (note that we have to put blank lines around the horizontal lines).

---

Even more text
___
```

**Result**

Text
***
More text (note that we have to put blank lines around the horizontal lines).

---

Even more text
___

## Lists

### Bullet list marker

A list containing non-ordered bullet points can be constructed with the `-`, `+` or `*` character at the beginning of a line.

**Syntax**

```
- you can use `-` character
+ you can use `+` character
* you can use `*` character
* whatever you will choose...
* ...be consistent
```

**Result**

- you can use `-` character
+ you can use `+` character
* you can use `*` character
* whatever you will choose...
* ...be consistent

Note that using different characters for each bullet point can cause the software to treat the list as a collection of independent bullets (e.g. each bullet can have it's own Jupyter Lab cell). You should be consistent in the bullet character to use.

___

Lists can be indented using double spaces:

**Syntax**

```
- point 1.
  - point 1.2. 
    - point 1.3.
      - point 1.4.
- point 2.
```

**Result**

- point 1.
  - point 1.2. 
    - point 1.3.
      - point 1.4.
- point 2.

### Ordered list marker

An ordered list can be written using an arabic numbered followed by `"."` or `")"`.

**Syntax**

```
1. First item.
1. Second item.
1. Third item.
```

**Result**

1. First item.
1. Second item.
1. Third item.

Note that using only `1.` leads to an auto-incremented list. To reduce errors and time spent on error-checking, it is recommended to use automatic list numbering instead of writing numbers manually. 

___

Also note that lists can be continued after a block of text:

**Syntax**

```
  1.  A point
containing multiple lines.

          including code blocks

      > and quote blocks

  1. Second point (*continuation of the list*).
```

**Result**

  1.  A point
containing multiple lines.

          including code blocks

      > and quote blocks

  1. Second point (*continuation of the list*).


For more details read the [CommonMark documentation](https://spec.commonmark.org/0.30/#list-items).

## Links

### Links to external resources

You can just paste a link to an external resource.

| Syntax | Result |
| --- | --- |
| `Link to https://spec.commonmark.org/0.30/#links` | Link to https://spec.commonmark.org/0.30/#links |

You can include a link with a link text and a hidden link destination.

| Syntax | Result |
| --- | --- |
| `[Some link text](https://www.uni.lu/en/)` | [Some link text](https://www.uni.lu/en/) |

### Links to internal resources

You can also have a link to a specified part of your work.

For example, let us assume that your book comprises of two chapters that are located on the same level of a directory:

```
/contents/
├── chapter_1.md
└── chapter_2.md
```

Then in your `chapter_1.md` file you can include a link to the `chapter_2.md` using the `[some-text](./chapter_2.md)`.

| Syntax | Result |
| --- | --- |
| `[This text will be displayed](./diagrams.md)` | [This text will be displayed](./diagrams.md) |

## Multimedia

### Images

You can embed an image by linking to an image file.

| Syntax | Result |
| --- | --- |
| `![Logo of the University](./images/uni_logo.png)` | ![Logo of the University](./images/uni_logo.png) |

### Using directives to format your image <sup>(MyST feature)</sup>

The `image` directive allows you to customize:
* `width`
* `alignment`
* `classes` to add to the image

**Syntax**

```
:::{image} ./images/uni_logo.png
:name: uni-logo
:width: 100px
:align: center
:::
```

**Result**

:::{image} ./images/uni_logo.png
:name: uni-logo
:width: 100px
:align: center
:::

### Videos

**Syntax**

```
![](./videos/vid-sample.mp4) 
```

**Result**

![](./videos/vid-sample.mp4)

### YouTube/Vimeo videos <sup>(MyST feature)</sup>

If your video is hosted on one of supported platforms (at the time of writing of this document: on YouTube and on Vimeo) you can embed the video using the url. Note that the book will then be dependent on that external source - if deleted, the video will not be rendered. Also, just copying the url to video might not work. You should create a special link. Usually, there is a `Share > Embed Video` option.

**Syntax**

```
:::{iframe} https://www.youtube.com/embed/_TycjDn9WYE?si=HJAZlky46zWndbLE
:width: 50%
An embedded video with a caption
:::
```

**Result**

:::{iframe} https://www.youtube.com/embed/_TycjDn9WYE?si=HJAZlky46zWndbLE
:width: 50%
An embedded video with a caption
:::

Please read the [MyST guide](https://mystmd.org/guide/figures#youtube-videos) for more details.

## Tables

### Markdown tables

For tables, MyST uses the [GitHub Markdown syntax](https://github.github.com/gfm/#tables-extension-).

To add a table, use three or more hyphens (`---`) to create each column’s header, and use pipe characters (`|`) to separate each column. You should also add a pipe character on the start and the end of each row.

**Syntax**

```
| Header 1        | Header 2        |
| --------------- | --------------- |
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |
```

**Result**

| Header 1        | Header 2        |
| --------------- | --------------- |
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |

You don't have to be strict with formatting the table, as long as you use the proper syntax. For example, the following table will be rendered the same as the one above.

**Syntax**

```
| Header 1| Header 2 |
| --- | -------- |
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |
```

**Result**

| Header 1| Header 2 |
| --- | -------- |
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |

### MyST tables <sup>(MyST feature)</sup>

It is advisable to use the "`{list-table}`" directive. The following syntax is currently supported:

**Syntax**

```
:::{list-table} Table caption
:header-rows: 1
:name: examplary-table

* - Header 1
  - Header 2
* - Row 1, Column 1
  - Row 1, Column 2
* - Row 2, Column 1
  - Row 2, Column 2
:::
```

**Result**

:::{list-table} Table caption
:header-rows: 1
:align: center
:name: examplary-table

* - Header 1
  - Header 2
* - Row 1, Column 1
  - Row 1, Column 2
* - Row 2, Column 1
  - Row 2, Column 2
:::

This will allow you to reference the table in your book. 

| Syntax | Result |
| --- | --- |
| `Mention of [your table](#examplary-table) in text` | Mention of [your table](#examplary-table) in text |

Moreover, the table label will auto increment itself.

## Container blocks

### Block quotes

You can insert a block of text separate from the rest of the page with a use of the `> ` syntax.

**Syntax**

```
> Example of the `> ` syntax.
> - CommonMark specification
```

**Result**

> Example of the `> ` syntax.
> - CommonMark specification

**Syntax**

```
> Here is extended example of the "> " syntax. Note that
> > you can nest your blocks.
> 
> Use the "-" character to specify the author of a given quote.
> - Author Unknown
```

**Result**

> Here is extended example of the "> " syntax. Note that
> > you can nest your blocks.
> 
> Use the "-" character to specify the author of a given quote.
> - Author Unknown

See the details in the [CommonMark specification](https://spec.commonmark.org/0.30/#block-quotes).

### Admonitions <sup>(MyST feature)</sup>

Admonitions highlight a particular block of text that exists slightly apart from the narrative of your page, such as a note or a warning.

**Syntax**

```
:::{tip}
Block of text that is separated from the rest of the page.
:::

:::{attention}
Text.
:::

:::{caution}
Text.
:::

:::{danger}
Text.
:::

:::{error}
Text.
:::

:::{hint}
Text.
:::

:::{important}
Text.
:::

:::{note}
Text.
:::

:::{seealso}
Text.
:::

:::{warning}
Text.
:::
```

**Result**

:::{tip}
Block of text that is separated from the rest of the page.
:::

:::{attention}
Text.
:::

:::{caution}
Text.
:::

:::{danger}
Text.
:::

:::{error}
Text.
:::

:::{hint}
Text.
:::

:::{important}
Text.
:::

:::{note}
Text.
:::

:::{seealso}
Text.
:::

:::{warning}
Text.
:::

See the [MyST guide](https://mystmd.org/guide/admonitions) for the implementation details.

## Diagrams <sup>(MyST feature)</sup>

MyST supports [mermaid diagrams](https://mermaid.js.org/). Therefore, it should be possible to include diagrams in your book/article using the `{mermaid}` directive, for example
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

Sadly, this does not always render properly. Be sure to check the [mermaid documentation](https://mermaid.js.org/intro/getting-started.html) and the [MyST guide](https://mystmd.org/guide/diagrams) for the more information.

Below you can find some implementation examples.

### Flowchart

**Syntax**

```
:::{mermaid}
flowchart LR
    A[Hard edge] -->|Link text| B(Round edge)
    B --> C{Decision}
    C -->|One| D[Result one]
    C -->|Two| E[Result two]
:::
```

**Result**

:::{mermaid}
flowchart LR
    A[Hard edge] -->|Link text| B(Round edge)
    B --> C{Decision}
    C -->|One| D[Result one]
    C -->|Two| E[Result two]
:::

See [docs](https://mermaid.js.org/syntax/flowchart.html).

### Sequence diagrams

**Syntax**

```
:::{mermaid}
sequenceDiagram
    participant Alice
    participant John
    link Alice: Dashboard @ https://dashboard.contoso.com/alice
    link Alice: Wiki @ https://wiki.contoso.com/alice
    link John: Dashboard @ https://dashboard.contoso.com/john
    link John: Wiki @ https://wiki.contoso.com/john
    Alice->>John: Hello John, how are you?
    John-->>Alice: Great!
    Alice-)John: See you later!
:::
```

**Result**

:::{mermaid}
sequenceDiagram
    participant Alice
    participant John
    link Alice: Dashboard @ https://dashboard.contoso.com/alice
    link Alice: Wiki @ https://wiki.contoso.com/alice
    link John: Dashboard @ https://dashboard.contoso.com/john
    link John: Wiki @ https://wiki.contoso.com/john
    Alice->>John: Hello John, how are you?
    John-->>Alice: Great!
    Alice-)John: See you later!
:::

See [docs](https://mermaid.js.org/syntax/sequenceDiagram.html)

### Gantt diagram

**Syntax**

```
:::{mermaid}
gantt
    title A Gantt Diagram
    dateFormat YYYY-MM-DD
    section Section
        A task          :a1, 2014-01-01, 30d
        Another task    :after a1, 20d
    section Another
        Task in Another :2014-01-12, 12d
        another task    :24d
:::
```

**Result**

:::{mermaid}
gantt
    title A Gantt Diagram
    dateFormat YYYY-MM-DD
    section Section
        A task          :a1, 2014-01-01, 30d
        Another task    :after a1, 20d
    section Another
        Task in Another :2014-01-12, 12d
        another task    :24d
:::

See [docs](https://mermaid.js.org/syntax/gantt.html).

### Pie chart

**Syntax**

```
:::{mermaid}
pie showData
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" :  5
:::
```

**Result**

:::{mermaid}
pie showData
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" :  5
:::

See [docs](https://mermaid.js.org/syntax/pie.html).

## Math <sup>(MyST feature)</sup>

MyST syntax derives from the ${LaTeX}$. To get started with the math syntax, please see the [documentation](https://www.latex-project.org/help/documentation/).
See the [MyST guide](https://mystmd.org/guide/math) for more details on the MyST implementation.

### Inline math <sup>(MyST feature)</sup>

| Syntax | Result |
| --- | --- |
| ```{math}`e=mc^2` ``` | {math}`e=mc^2` |

### Equation blocks <sup>(MyST feature)</sup>

**Syntax**

```
:::{math}
:label: euler-identity-equation
e^{i\pi}+1 =0
:::
```

**Result**

:::{math}
:label: euler-identity-equation
e^{i\pi}+1 =0
:::

### Dollar math equation <sup>(MyST feature)</sup>

**Syntax**

```
$$
\label{maxwell}
\begin{aligned}
\nabla \times \vec{e}+\frac{\partial \vec{b}}{\partial t}&=0 \\
\nabla \times \vec{h}-\vec{j}&=\vec{s}\_{e}
\end{aligned}
$$

$$ \label{one-liner} Ax=b $$
```

**Result**

$$
\label{maxwell}
\begin{aligned}
\nabla \times \vec{e}+\frac{\partial \vec{b}}{\partial t}&=0 \\
\nabla \times \vec{h}-\vec{j}&=\vec{s}\_{e}
\end{aligned}
$$

$$ \label{one-liner} Ax=b $$

## Glossaries, Terms and Abbreviations

**Syntax**

```
:::{glossary}
Term1
: some term that need to be defined.
:::
:::{glossary}
Term2
: another definition.
:::
:::{glossary}
Term3
: yet another definition.
:::
```

**Result**

:::{glossary}
Term1
: some term that need to be defined.
:::
:::{glossary}
Term2
: another definition.
:::
:::{glossary}
Term3
: yet another definition.
:::

A use of glossaries enables us to reference certain terms in our books/articles. For example, we can now reference {term}`Term2`.

| Syntax | Result |
| --- | --- |
| Some sentence that mentiones ```{term}`Term2` ``` | Some sentence that mentiones {term}`Term2` |

Please see the [MyST guide](https://mystmd.org/guide/glossaries-and-terms) on how to create a glossary.

## Footnotes <sup>(MyST feature)</sup>

Using MyST[^ref-to-footnotes] markdown variant enables us to use footnotes in our files.

Please note the syntax of the footnotes. `My content.[^some-text]` in your content's body and `[^some-text]: Footnote.` after it.

[^ref-to-footnotes]: A first footnote.

**Syntax**

```
My content.[^some-text]
[^some-text]: A second footnote.
```

**Result**

My content.[^some-text]
[^some-text]: A second footnote.

See the [the MyST guide](https://mystmd.org/guide/typography#footnotes) for more details.

## Citations <sup>(MyST feature)</sup>

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

| Example | Renders | Note |
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

## Disclaimer

The herein guidelines were prepared in Q4 2023 for CommonMark v0.30 and MyST v0.0.4. and are up to date as of the date of writing of this document. The guidelines and the Markdown specification is provided "as is", without warranty of any kind, express or implied.
