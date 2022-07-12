---
layout: page
title: Setup development environment
permalink: /guides/developer-setup/
menuInclude: no
menuTopTitle: Guides
---

A collection of tips to assist developers to configure their local workstation setup environment for FOLIO development.

## Introduction

Assume already doing other development, so know how to keep the operating system up-to-date, know its quirks, know how to use the various package managers. So this document will not go into detail about that.

FOLIO modules can be developed in any suitable [programming language](/guides/any-programming-language).

The [FOLIO-Sample-Modules](https://github.com/folio-org/folio-sample-modules) explains about module development.
The various [Stripes](/guides#user-interface) documentation explains user-interface development.
Those also have more notes about setting up and managing the local development environment.

## Tools

Developers will probably want to explore the whole FOLIO system, so would need a local instance of Okapi and
[server-side](/source-code#server-side) modules,
and the [client-side](/source-code#client-side) Stripes toolkit.

Note that some parts of the development environment could be handled using
[folio-ansible](https://github.com/folio-org/folio-ansible) (virtual machines using Vagrant and Ansible).

Otherwise the development environment would need the following fundamental tools:

* Apache Maven (3.3+) -- For building and deploying Okapi and some server-side modules.
* Node.js ([Active LTS version](https://github.com/nodejs/Release#release-schedule)) -- For Stripes and for some modules, and for UI testing.
* Docker -- Recommended method for deployment.
* PostgreSQL (12) -- For running an external database to support storage modules.
This will enable faster startup and operations during development.

As each FOLIO component can utilise whatever suite of appropriate tools, refer to its requirements and notes to assist with setup.

### Minimum versions

Occasionally it becomes necessary to specify minimum versions of some tools:

* Java: [11](/faqs/how-to-specify-backend-java-ci/).
* Postgres: [12](https://github.com/folio-org/raml-module-builder#postgresql-integration).

### Other tools

* curl -- Many modules provide examples as curl requests. Alternatively those examples could be used with Postman via "import".

* Clone the [folio-tools](https://github.com/folio-org/folio-tools) repository parallel to your other clones.
This provides various helper tools, for example the "api-lint" to [Assess API descriptions, schema, and examples](/guides/api-lint/) -- both RAML and OpenAPI (OAS).

## Workstation capability

To use a local development workstation together with a localhost FOLIO installation, will need 16+ GB of local memory.

## Configuration for repository usage

FOLIO utilizes the Nexus OSS Repository Manager to host Maven artifacts and NPM packages for FOLIO projects.
Docker images are the primary distribution model for FOLIO modules.

See [Built artifacts](/download/artifacts/) for configuration details for accessing the released and snapshot FOLIO artifacts.

For developers needing to publish artifacts, an overview and usage configuration details are provided, see
[Build, test, and deployment infrastructure](/guides/automation/).

## Coding style

### Style guidelines and configuration

Refer to the [coding style](/guidelines/contributing#coding-style) sections of the
[Guidelines for Contributing Code](/guidelines/contributing).

### Code analysis and linting

All code repositories have linter and code-style analysis facilities implemented as part of their continuous integration build process.
The process is [explained](/guides/code-analysis), along with usage notes and configuration for running those tools locally.

### Use EditorConfig for consistent whitespace

Many FOLIO repositories have a `.editorconfig` [configuration](/faqs/how-to-use-editorconfig/) file at their top level. This enables consistent whitespace handling and assists with consistent [coding-style](/guidelines/contributing/#coding-style).

### No license header

As [explained](/guidelines/contributing#no-license-header), we do not use a license header in the top of each source code file.

Please configure your IDE to use an empty license header. Some IDEs have a default template to remind developers to add one. We do not.

## Use .gitignore

The `.gitignore` file in each repository can be minimal if each developer handles their own.

One way is to [configure](https://git-scm.com/docs/gitignore) your own user-specific global file (i.e. add `core.excludesFile` to `~/.gitconfig`).
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

    ## vim
    *~
    .*.sw?

    ## folio
    .vertx/

## Update git submodules

Some FOLIO repositories utilize "[git submodules](https://git-scm.com/docs/gitmodules)" for sections of common code.

For example, each `mod-*` module (and `raml-module-builder` itself) include the "raml" repository as a git submodule as its `ramls/raml-util` directory.
(See [notes](/start/primer-raml/).)

Note that when originally cloning a repository, use '`git clone --recursive ...`' which should automatically include any submodules.

Some git clients do not. If you then have an empty "raml-util" directory, then do '`git submodule update --init`'

Thereafter upgrading that submodule (i.e. moving the git pointer of the referenced repository) is deliberately not automated, so that we can ensure a stable build when we git checkout in the future.

So when an upgrade is needed to be committed, do this:

```
cd ramls/raml-util
git checkout raml1.0
git pull
cd ../..
git add ramls/raml-util
  now do RAML validation
  and run maven
git commit ...
```

Note that when locally testing an upgrade of a git submodule, then do '`git add ramls/raml-util`' before running 'mvn'.
Otherwise it will helpfully restore the referenced git pointer (which is not wanted).

Now when people update their local checkout, then some git clients do not automatically update the submodules. If that is the case for your client, then follow with 'git submodule update'.

For Maven-based modules, add to your POM file (copy the 'git submodule update' from mod-notes) to assist all git clients to update.

## Troubleshooting

See [notes](/guides/troubleshooting/).
