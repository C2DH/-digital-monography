# Concerns

## Dependencies

* MyST, mystmd and the whole ecosystem - currently open sourced, but the licencing can always change.
* docx - Microsoft can change the output of its word processor without notice.

## Data transformation (e.g. transforming file from .docx to .md)

Please remember that markdown is an ambiguous format.

### Break from WYSIWYG

In word processors like Microsoft Word - you truly get what you see. In Markdown (MyST or otherwise) it's about minimizing the syntax (making it easy to read in its source code form) and putting a lot of logic behind the scenes to render it in a certain way.

### Loss of flexibility

### Loss of data

### Unicode

The character U+2013 "–" could be confused with the ASCII character U+002d "-", which is more common in source code.

![Alt text](concerns_unicode_mojibake_1.png)

can be translated to

![Alt text](concerns_unicode_mojibake_2.png)

### Page breaking

![Alt text](concerns_page_breaking.png)

### Syntax conflicts

### Point-in-time dynamic parts

### Footnotes

At the end of a chapter or at the end of a current smallest part?

### Pdf converters are not great

![Alt text](concerns_pdf_tools.png)

### Count of references can break the sequence

### A symbol can have a special meaning in a templating language

For example, `#Memorecord` or `_something`

## MD validation / verification

CommonMark is a mature specification of markdown and as a result it benefits from mature software solutions for validating it's correctness. On the other hand, MyST specification and parser are volatile and can change. As consequence, the validation/verification tooling leaves a lot to be desired. 

Please see [this doc](https://github.com/C2DH/digital-monography/blob/develop/src/md_verifier/README.md) for the details from the research of the possible solutions.

Especially note that **most of the tooling (even utilities supported by _executablebooks_) is written in JavaScript**.
On of the reasons for this is that this makes MD verification easy to implement on the frontend. For example see this [online MD linter](https://dlaa.me/markdownlint/).
Note that with each change to the markdown content we get feedback imediately without having to send a request to the server.
Thus, we will have to decide to which extent we wish to use existing solutions and add write the verification/validation module in JavaScript and to what extent we wish to write our own solutions.

## MD rendering

### Reactivity

To offer users reactivity, MyST builds on top of many frontend technologies: `react`, `backbone.js`, `remix`, `tailwind`, etc. In order to render all MyST features in .md and .ipynb files, it hosts a small web server.
This might be great for digital journals that are viewed online, but might not work so well with a static book in a pdf format or even html but without a whole server behind it. There might be MyST markdown features that are supported when rendered dynamically, but not statically, without a live web server.

## Difficult tradeoffs

### Which markdown spec to use?: MyST (superset of CommonMark) instead of CommonMark/GitHub/Pandoc MD?

Pros
* made for scientific publications
* LATEX support
* extends Markdown with equations, cross-references, citations, footnotes, bibliographies, etc.
* good tools for exporting this format to other formats

Cons
* MyST AST is in development; any structures or features present in the JSON schema may change at any time without notice
* no validators
* immature tools
* pandoc does not support MyST markdown spec (see https://github.com/executablebooks/rst2myst/issues/2)
* jupyter nbconvert does not support MyST markdown spec
* not all syntax is supported, for example there are no ~~strikethroughs~~ in MyST
* some important features (like bibliography, charts) do not work 'out of the box' and need additional configuration to set up
* only limited image/video file formats are supported

### Store media with other files or on separate server (maybe 3rd party service)

Using external server/service for storing media

Pros
* probably safer (giving permissions to access isolated storage only)
* easier to develop (no data loss and no ref changes during transformations, we always point to the same place)

Cons
* harder to deploy, especially if we were to deploy on our storage servers
* if we were to use 3rd party storage (eg imgur), there is a copywright 

### Unittest vs pytest
