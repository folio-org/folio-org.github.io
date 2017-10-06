---
layout: devtools
title: Coding Style
heading: Coding Style
permalink: /devtools/codingstyle/
---

## Style Guidelines and Configuration

Refer to the [coding style](/guidelines/codingstyle) section of the
[Guidelines for Contributing Code](/guidelines/contrib-code).

Some modules have linter and code-style tools implemented as part of their build process.
Some modules provide configuration files to assist code management tools.

## Use EditorConfig for Consistent Whitespace

Many FOLIO repositories have a `.editorconfig` configuration file at their top level. This enables consistent whitespace handling.

Refer to [EditorConfig.org](http://editorconfig.org) which explains that some text editors have native support, whereas others need a plugin.

Consult its documentation for each plugin. Note that some do not handle all EditorConfig properties.
In such cases refer to the documentation for the particular text editor, as it might have its own facilities.
For example, the Java text editor in Eclipse has its own configuration for `trim_trailing_whitespace`
(see [notes](http://stackoverflow.com/questions/14178839/is-there-a-way-to-automatically-remove-trailing-spaces-in-eclipse)).

## Use .gitignore

The `.gitignore` file in each repository can be minimal if each developer handles their own.
One way is to [configure](https://git-scm.com/docs/gitignore) a user-specific global file (i.e. add `core.excludesFile` to `~/.gitconfig`).

Then either use something like [gitignore.io](https://github.com/joeblau/gitignore.io),
or just use a simple set such as the following.
Add other specific ones for your particular operating system, text editors, and IDEs.

    ## general
    *.log

    ## macos
    *.DS_Store

    ## maven
    target/

    ## gradle
    .gradle/
    build/

    ## node
    node_modules/
    npm-debug.log

    ## vim
    *~
    .*.sw?

    ## folio
    **/src/main/java/org/folio/rest/jaxrs/
    .vertx/
	
## Update git submodules

Some FOLIO repositories utilize "git submodules" for sections of common code.

For example, each `mod-*` module and `raml-module-builder` include the "raml" repository as a git submodule as its `raml-util` directory.

Note that when originally cloning a repository, use 'git clone --recursive ...'
Some git clients do not. If you then have an empty "raml-util" directory, then do 'git submodule update --init'.

Thereafter updating that submodule is deliberately not automated, so that we can ensure a stable build when we git checkout in the future.

So when an update is needed to be committed, do this:

    cd mod-configuration (for example)
    git submodule foreach 'git checkout master && git pull origin master'
    git commit ...

Now when people update their local checkout, then some git clients do not automatically update the submodules. If that is the case, then follow with 'git submodule update'.

This part can be automated with client-side git hooks. Create the following two shell scripts:

    mod-configuration/.git/hooks/post-checkout
    mod-configuration/.git/hooks/post-merge

using this content:

    #!/bin/sh
    git submodule update

and make them executable: 'chmod +x post-checkout post-merge'

Now subsequent updates will also update the submodules to their declared revision.
