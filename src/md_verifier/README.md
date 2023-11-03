# Main ideas

* custom rules for markdownlint (in JavaScript)
* find a way to validate against JSON schema
* AST + using assertion tools for writing custom rules (in JavaScript)

# Ideas

## mattbriggs/markdown-validator

|lang   |licence|health-score   |GitHub stars|approach   |
|-------|-------|---------------|-----------:|-----------|
|Python |MIT    |non-finished   |6           |declarative|

I can use [this project](https://github.com/mattbriggs/markdown-validator) to create my own markdown validator. Sadly, it is not available through pip. It is also uncertain, if it even works. Probably I will have to recreate the source code directly in my repo (patch or just copy) and amend it to my needs. Thankfully, it is under the MIT licence.

It works in an interesting way:
* step 1 - render a JSON array of the metadata, check for existance and values of the said metadata
* step 2 - unambiguate the MD by generating an XML tree that reflects the outline of the document. Nodes can be navigated using an XPath query.

You set the validation rules through an JSON array, for example

```
{
    "name": "H1 must begin with tutorial",
"type:" : "body",
    "id": "29",
    "query": " /html/body/h1",
    "filter": "/text",
    "flag": "",
    "operation": "regex",
    "value": "^Tutorial",
    "level": "Required",
    "mitigation": "The H3 headings aren't numbered"
},
{
    "name": "H1 must begin with tutorial",
"body",
    "id": "29",
    "query": "{29}",
    "filter": "",
    "flag": "text",
    "operation": "regex",
    "value": "Azure Monitor",
    "level": "Required",
    "mitigation": "The H3 headings aren't numbered"
}
```

When researching the source code, you can start with a [classes specification](https://github.com/mattbriggs/markdown-validator/blob/main/source/classes_markdown-validator.png) and the [workflow](https://github.com/mattbriggs/markdown-validator/blob/main/source/test.rst).

https://github.com/markdownlint/markdownlint
https://matthewsetter.com/tools-that-make-technical-writing-easier-markdown-linter/

## DavidAnson/markdownlint

|lang   |licence|health-score   |GitHub stars|approach  |
|-------|-------|---------------|-----------:|----------|
|JS     |MIT    |88/100         |4.1k        |imperative|

[`markdownlint`](https://github.com/DavidAnson/markdownlint) is a static analysis tool for Node.js. It's very well maintained. Can lint specified files synchronously or asynchronously.

### How `markdownlintSync()` (`markdownlint.sync()`) works

1. `markdownlintSync` calls lintInput with options obj.
1. import rules from .rules (array of require("./number-of-the-rule-")), concatenates with custom rules. Each rule has the following structure.

```
// @ts-check

"use strict";

const { addErrorDetailIf, filterTokens } = require("../helpers");

module.exports = {
  "names": [ "MD001", "heading-increment", "header-increment" ],
  "description": "Heading levels should only increment by one level at a time",
  "tags": [ "headings", "headers" ],
  "function": function MD001(params, onError) {
    let prevLevel = 0;
    filterTokens(params, "heading_open", function forToken(token) {
      const level = Number.parseInt(token.tag.slice(1), 10);
      if (prevLevel && (level > prevLevel)) {
        addErrorDetailIf(onError, token.lineNumber,
          "h" + (prevLevel + 1), "h" + level);
      }
      prevLevel = level;
    });
  }
};
```

1. normalize inputs.
1. call validateRuleList to check if the custom rules are compliant.
1. initiates [the parser](https://github.com/markdown-it/markdown-it)

```
const md = markdownit({ "html": true });
```

1. calls `mapAliasToRuleNames()` to map rule names/tags to canonical rule name.
1. create a `LintResults` instance which seems to be a mapping of all ___. This function has `toString()` for pretty display.
1. define `lintWorker()`. Each worker either calls `lintContent()` (it lints a string containging MD content) or `lintFile()` (it lints a single file containing MD content). `lintFile()` calls `lintContent()`.

### How `lintContent()` works

1. remove front matter (if present at beginning of content).
1. create a mapping of enabled rules per line. That includes handling inline comments (regex to find a comment in a line).
1. parse the content using the [markdown-it parser](https://github.com/markdown-it/markdown-it): `const markdownitTokens = md.parse(content, {});`
1. parse the content using the [micromark parser](https://github.com/micromark/micromark) for CommonMark: `const micromarkTokens = micromark.parse(content);`.
1. hide the content of HTML comments from rules.
1. parse content into lines and update markdown-it tokens : `const lines = content.split(helpers.newLineRe);`.
1. annotate tokens with line/lineNumber and freeze them.
1. call `getLineMetadata()` to get a line metadata array.
1. call `codeBlockAndSpanRanges()` to get an array of code block and span content ranges.
1. call `flattenLists()` to get (nested) lists as a flat array (in order).
1. call `getReferenceLinkImageData()` to get an object with information about reference links and images.
1. cache.
1. filter rules: `const ruleListSync = ruleList.filter((rule) => !rule.asynchronous);`. Concatenate `ruleListAsync` and `ruleListSync` to create `ruleListAsyncFirst`.
1. define callbacks for error and success (incl. formatting successful results using `formatResults()` function).
1. Call `forRule()` function as a map() to each rule list entry: `const ruleResults = ruleListAsyncFirst.map(forRule);` in a try-catch statement.
1. clear cache.

### How `forRule()` works

1. define `onError` behaviour.
1. retrieve the funtion from the given rule `const invokeRuleFunction = () => rule.function(params, onError);`
1. if asynchronous rule: `Promise.resolve().then(invokeRuleFunction);`
1. a sync rule: `invokeRuleFunction();`

## syntax-tree/mdast-util-assert

|lang   |licence|health-score   |GitHub stars|approach  |
|-------|-------|---------------|-----------:|----------|
|JS     |MIT    |63/100         |0           |imperative|

[This utility](https://github.com/syntax-tree/mdast-util-assert) is typically useful when you expect certain nodes in your APIs and want to make sure they’re valid and as expected.

> Fundamentally, the specification for MyST documents can be broken down into abstract syntax tree (AST) node types and their document-level counterparts. The myst-spec AST builds on Markdown AST, or [mdast](https://github.com/syntax-tree/mdast), an intermediate format that in turn builds upon the existing Universal Syntax Tree, or [unist](https://github.com/syntax-tree/unist) spec. unist is used throughout the unifiedjs Javascript community with hundreds of existing transformations, utilities and serializers. unist has a simple format, with a type defining the node optional properties on the node and optional children (a leaf node has a value).
> 
> The MyST AST introduces nodes for directives and roles, as well as numerous new features, like admonitions, citiations, and equations, all of which build upon mdast and other existing standards and nomenclature. The MyST AST, like mdast, is serializable to JSON or YAML, and can be effectively shared between projects, languages, and implementations.
> - [source](https://mystmd.org/spec#myst-abstract-syntax-tree)

Maybe then I should create a AST and use assertions to verify the user's markdown?

Btw, the docs also state:

> **The myst-spec AST is in development; any structures or features present in the JSON schema may change at any time without notice.**

## executablebooks/myst-spec

There is a JSON spec that includes CommonMark and MyST directives etc.
But how to verify .md files using an JSON schema? Maybe there is a solution for using JSON schemas for CommonMark?

#TODO

## executablebooks/mystmd

`executablebooks/mystmd` is a parser and CLI for MyST Markdown, built in Javascript.
It includes [simple-validators](https://github.com/executablebooks/mystmd/tree/main/packages/simple-validators).
The validators themselves are not very interesting:
* validate value is boolean
* validate value is number
* validates string value
* validate value is valid URL string of max length 2048
* validate subdomain
* validate value is valid email
* validate value against array of choices
* validate value against enum
* validate date string or object
* validate value is an object
* validate an object has all required keys
* validate value is an object and has all required keys
* validate value is a list

# Candidates for rules

For a complete set of common markdown rules, see [the documentation of the markdownlint library](https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md).

There is also an [official of MyST](https://github.com/executablebooks/myst-spec/tree/main) with a schema. **How to validate a .md file against that schema** I do not know.

* validate links to assets

This [repo](https://www.npmjs.com/package/markdownlint-rule-relative-links) might be helpful.

* “non-consecutive” headings in a document, such as:

```
# Heading 1
### Heading 3
```
