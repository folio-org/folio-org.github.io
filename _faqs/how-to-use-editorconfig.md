---
layout: page
title: How to use EditorConfig for consistent whitespace handling and coding-style
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: setup
faqOrder: 2
---

Many FOLIO repositories have a `.editorconfig` configuration file at their top level. This enables consistent whitespace handling and assists with consistent [coding-style](/guidelines/contributing/#coding-style).

## Configure your editor

Refer to [EditorConfig.org](http://editorconfig.org) which explains that some text editors have native support, whereas others need a plugin.

Consult its documentation for each plugin. Note that some do not handle all EditorConfig properties.
In such cases refer to the documentation for the particular text editor, as it might have its own facilities.
For example, the Java text editor in Eclipse has its own configuration for `trim_trailing_whitespace`
(see [notes](http://stackoverflow.com/questions/14178839/is-there-a-way-to-automatically-remove-trailing-spaces-in-eclipse)).

## Manage project .editorconfig file

This is the common configuration for the top-level `.editorconfig` configuration file for a FOLIO project repository.
Some repositories have other needs, so have different settings (e.g. [Okapi](https://github.com/folio-org/okapi/blob/master/.editorconfig)).

```
# http://editorconfig.org/

root = true

[*]
charset = utf-8
end_of_line = lf
indent_size = 2
indent_style = space
insert_final_newline = true
trim_trailing_whitespace = true
```

## Markdown line-break

The default Markdown specification has a peculiar syntax to enable a hard line-break in documents generated from Markdown. It uses two trailing spaces at the end-of-line.

That will conflict with the EditorConfig setting for `trim_trailing_whitespace`

A better solution is to terminate the line with a backslash `\`  rather than using other workarounds, such as\
the html `<br/>` element.

The line termination with backslash is declared in the [CommonMark](https://spec.commonmark.org/current/#hard-line-breaks) specification, and hence in GitHub Flavored Markdown [GFM](https://github.github.com/gfm/#hard-line-breaks).
Also [Pandoc Markdown](https://pandoc.org/MANUAL.html#extension-escaped_line_breaks) enables the `escaped_line_breaks` extension by default.

<div class="folio-spacer-content"></div>

