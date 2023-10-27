# Concerns

## .docx to .md

Markdown is an ambiguous format.
Word Document is also ambiguous.

### Loss of flexibility

### Loss of data

### Unicode

The character U+2013 "–" could be confused with the ASCII character U+002d "-", which is more common in source code.

![Alt text](image.png)

can be translated to

![Alt text](image-1.png)

### Page breaking

![Alt text](image-2.png)

### Syntax conflicts

### Point-in-time dynamic parts

### Footnotes

at the end of a chapter or at the end of a current smallest part

### Pdf converters are not great

![Alt text](image-4.png)

### Count of references can break the sequence

# Difficult tradeoffs

## Which markdown spec to use?

### MyST (superset of CommonMark)

Pros
* made for scientific publications
* LATEX support
* extends Markdown with equations, cross-references, citations
* tools to export to a preprint or rich, interactive website or book

Cons
* MyST AST is in development; any structures or features present in the JSON schema may change at any time without notice
* no validators
* immature tools
* pandoc does not support MyST markdown spec (see https://github.com/executablebooks/rst2myst/issues/2)
* jupyter nbconvert does not support MyST markdown spec

### Unittest vs pytest

### Store media with other files or on separate server (maybe 3rd party service)


