---
layout: page
title: Setup development environment
---

A collection of tips to assist developers to configure their local workstation setup environment for FOLIO development.

<!-- ../../okapi/doc/md2toc -l 2 -h 3 setup.md -->
* [Introduction](#introduction)
* [Tools](#tools)
    * [Minimum versions](#minimum-versions)
    * [Other tools](#other-tools)
* [Configuration for repository usage](#configuration-for-repository-usage)
* [Coding style](#coding-style)
    * [Style guidelines and configuration](#style-guidelines-and-configuration)
    * [Use EditorConfig for consistent whitespace](#use-editorconfig-for-consistent-whitespace)
* [Use .gitignore](#use-gitignore)
* [Update git submodules](#update-git-submodules)
* [Troubleshooting](#troubleshooting)

## Introduction

Assume already doing other development, so know how to keep the operating system up-to-date, know its quirks, know how to use the various package managers. So this document will not go into detail about that.

FOLIO modules can be developed in any suitable programming language.

The [FOLIO-Sample-Modules](https://github.com/folio-org/folio-sample-modules) explains about module development.
The various [Stripes](/doc#user-interface) documentation explains user-interface development.
Those also have more notes about setting up and managing the local development environment.

## Tools

Developers will probably want to explore the whole FOLIO system, so would need a local instance of Okapi and
[server-side](/source-code#server-side) modules,
and the [client-side](/source-code#client-side) Stripes toolkit.

Note that some parts of the development environment could be handled using
[folio-ansible](https://github.com/folio-org/folio-ansible) (virtual machines using Vagrant and Ansible).

Otherwise the development environment would need the following fundamental tools:

* Apache Maven (3.3+) and Java (8+) -- For building and deploying Okapi and some server-side modules.
* Node.js (6+) -- For Stripes and for some modules.
* Docker -- Recommended method for deployment.

As each FOLIO component can utilise whatever suite of appropriate tools, refer to its requirements and notes to assist with setup.

### Minimum versions

Occasionally it becomes necessary to specify minimum versions of some tools:

* Java: [1.8.0-101](troubleshooting#missing-certificate-authority-for-lets-encrypt)

### Other tools

* PostgreSQL -- For running an external database to support storage modules.
This will enable faster startup and operations during development.
Note that this is not required to be installed for running modules using the "embed_postgres" option.

## Configuration for repository usage

FOLIO utilizes the Nexus OSS Repository Manager to host Maven artifacts and NPM packages for FOLIO projects.
Docker images are the primary distribution model for FOLIO modules.

See [Built artifacts](artifacts) for configuration details for accessing the released and snapshot FOLIO artifacts.

For developers needing to publish artifacts, an overview and usage configuration details are provided, see
[Build, test, and deployment infrastructure](automation).

## Coding style

### Style guidelines and configuration

Refer to the [coding style](/community/contrib-code#coding-style) section of the
[Guidelines for Contributing Code](/community/contrib-code).

Some modules have linter and code-style tools implemented as part of their build process.
Some modules provide configuration files to assist code management tools.

### Use EditorConfig for consistent whitespace

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

## Troubleshooting

See [notes](troubleshooting).
