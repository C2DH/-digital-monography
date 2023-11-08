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
Such indentation has a special meaning. Using it might lead to unindended formatting.
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

A list containing non-ordered bullet points can be constructed with the following characters at the beginning of a line.

**Syntax**

```
- you can use `-` character
+ you can use `+` character
* you can use `*` character
```

**Result**

- you can use `-` character
+ you can use `+` character
* you can use `*` character

___

Lists can be indented using double spaces (`  `):

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

An ordered list can be written using an arabic numbered followed by `.` or `)`.

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
| `![Logo of the University](./img/uni_logo.png)` | ![Logo of the University](./img/uni_logo.png) |

### Using directives to format your image <sup>(MyST feature)</sup>

The `image` directive allows you to customize:
* `width`
* `alignment`
* `classes` to add to the image

**Syntax**

```
:::{image} ./img/uni_logo.png
:name: uni-logo
:width: 100px
:align: center
:::
```

**Result**

:::{image} ./img/uni_logo.png
:name: uni-logo
:width: 100px
:align: center
:::

## Tables <sup>(MyST feature)</sup>

### Markdown tables <sup>(MyST feature)</sup>

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

### CSV tables <sup>(MyST feature)</sup>

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

## Container blocks

### Block quotes

You can insert a block of text separate from the rest of the page with a use of the `> ` syntax.

**Syntax**

```
> Example of the `> ` syntax.
```

**Result**

> Example of the `> ` syntax.

**Syntax**

```
> You **can** also use *markdown* in your block quotes.
> 
> In addition,
> > you can also nest your block.
> 
> use `-` character to specify the author of a given quote.
> - Author Unknown
```

**Result**

> You **can** use *markdown* in your block quotes.
> 
> In addition,
> > you can nest your block.
> 
> use `-` character to specify the author of a given quote.
> - Author Unknown

See the details in the [CommonMark specification](https://spec.commonmark.org/0.30/#block-quotes).

### Admonitions <sup>(MyST feature)</sup>

> Admonitions highlight a particular block of text that exists slightly apart from the narrative of your page, such as a note or a warning.

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

## Math <sup>(MyST feature)</sup>

MyST syntax derives from the ${LaTeX}$. To get started with the math syntax, please see the [documentation](https://www.latex-project.org/help/documentation/).
See the [MyST guide](https://mystmd.org/guide/math) for more details on the MyST implementation.

### Inline math <sup>(MyST feature)</sup>

| Syntax | Result |
| --- | --- |
| ```{math}`e=mc^2` ``` | {math}`e=mc^2` |

<!-- {math}`e=mc^2`. -->

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

### Proofs, Theorems and Algorithms <sup>(MyST feature)</sup>

#### TODO

* https://mystmd.org/guide/proofs-and-theorems

## Diagrams <sup>(MyST feature)</sup>

#### TODO

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

## Table of contents <sup>(MyST feature)</sup>

Our software allows you to automatically generate and display table of contents. Note that the structure of the document will be determined by the heading and not by your configuration file.

**Syntax**

```
:::{tableofcontents}
:::
```

## Footnotes <sup>(MyST feature)</sup>

Using MyST[^ref-to-footnotes] variant enables us to use footnotes in our markdown files.

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

#### TODO

For more information, see the [MyST guide](https://mystmd.org/guide/citations).

## Cross-referencing

#### TODO

* https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html

## Interactive notebooks (code blocks)

#### TODO

* https://mystmd.org/guide/interactive-notebooks
* https://mystmd.org/guide/reuse-jupyter-outputs
* https://mystmd.org/guide/integrating-jupyter

## Disclaimer

This guidelines were prepared in Q4 2023 for CommonMark v0.30 and MyST v0.0.4. and are up to date as of the date of writing of this document. The guidelines herein and the Markdown specification is provided "as is", without warranty of any kind, express or implied.
