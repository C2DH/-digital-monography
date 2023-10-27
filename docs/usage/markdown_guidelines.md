# Markdown guidelines

## Introduction

### What is Markdown

> Markdown is a plain text format for writing structured documents [...] The overriding design goal for Markdown’s formatting syntax is to make it as readable as possible. The idea is that a Markdown-formatted document should be publishable as-is, as plain text, without looking like it’s been marked up with tags or formatting instructions.

### Markdown's variant

The project supports MyST markdown, which is a superset of the CommonMark, a variant of the Markdown markup language. 

### This document

This document is meant as guidelines of features supported by our tool. It mostly repeats after the original specifiactions for [CommonMark](https://spec.commonmark.org/) and [MyST](https://github.com/executablebooks/myst-spec). Please treat the original specifications as an ultimate source of truth and this document as a way of facilitating user experience with our tool.

## Main features

### Headers

```
# Chapter 1 title
## Chapter 1 second header
### Chapter 1 third header
#### Chapter 1 section title
##### Chapter 1 section second header
```

# Chapter 1 title
## Chapter 1 second header
### Chapter 1 third header
#### Chapter 1 section title
##### Chapter 1 section second header

More than six `#` characters is not a heading.

For more details please read [the specification](https://spec.commonmark.org/0.30/#atx-heading). It might be also useful to read ["how headers and sections map onto to book structure"](https://jupyterbook.org/en/stable/structure/sections-headers.html#how-headers-and-sections-map-onto-to-book-structure).

### Code blocks

# TODO

### Emphasis

#### Italics

```
To write in italics, use single *asterisks* or _underscores_.
```

To write in italics, use single *asterisks* or _underscores_.

#### Bold

```
You can make text bold with double **asterisks** or __underscores__.
```

You can make text bold with **asterisks** or __underscores__.

#### Strikethrough

```
Strikethrough with ~~two tildes~~.
```

Strikethrough with ~~two tildes~~.

### Lists

### Links

#### Links to external resources

```
You can just paste a link to an external resource, e.g. to https://spec.commonmark.org/0.30/#links
```

You can just paste a link to an external resource, e.g. to https://spec.commonmark.org/0.30/#links

```
You can include a link with a [link text](https://spec.commonmark.org/0.30/#link-text) and a hidden link destination
```

You can include a link with a [link text](https://spec.commonmark.org/0.30/#link-text) and a hidden link destination

#### Links to internal resources

You can also have a link to a specified part of your work.

For example, let us assume that your book comprises of two chapters that are located on the same level of a directory:

```
/contents/
├── chapter_1.md
└── chapter_2.md
```

Then in your `chapter_1.md` file you can include a [link](./chapter_2.md) to a `chapter_2.md`.

# TODO: check if example is correct

### Images

You can embed an image by linking to an image file.

```
[Logo of the University](./university_of_luxembourg_logo_fr.svg)
```

[Logo of the University](./university_of_luxembourg_logo_fr.svg)

### Footnotes

### Tables

### Blockquotes

### Inline HTML

### Horizontal Rule

### Line Breaks

### Videos


## Disclaimer

This guidelines were prepared in Q4 2023 for CommonMark v0.30 and MyST v0.0.4. and are up to date as of the date of writing of this document. The guidelines herein and the Markdown specification is provided "as is", without warranty of any kind, express or implied.

