---
layout: tools
title: Setting Up the Developer Environment
heading: Developer Tools
permalink: /tools/setupdevenv/
---


# Setting Up the Dev Environment

A collection of tips to assist developers to configure their local workstation setup environment for FOLIO development.

Assume already doing other development, so know how to keep the operating system up-to-date, know its quirks, know how to use the various package managers. So this document will not go into detail about that.

FOLIO modules can be developed in any suitable [programming language](/source/components/#any-programming-language).

The [FOLIO-Sample-Modules](https://github.com/folio-org/folio-sample-modules) explains about module development.
The various [Stripes](/source/components/#client-side-1) documentation explains user-interface development.
Those also have more notes about setting up and managing the local development environment.

## Local Instances and Tooling

Developers will probably want to explore the whole FOLIO system, so would need a local instance of Okapi and
[server-side](/source/components) modules,
and the [client-side](/source/components) Stripes toolkit.

Note that some parts of the development environment could be handled using
[folio-ansible](https://github.com/folio-org/folio-ansible) (virtual machines using Vagrant and Ansible).

Otherwise the development environment would need the following fundamental tools:

* Apache Maven (3.3+) and Java (8+) -- For building and deploying Okapi and some server-side modules.
* Node.js (6+) -- For Stripes and for some modules.
* Docker -- Recommended method for deployment.

As each FOLIO component can utilise whatever suite of appropriate tools, refer to its requirements and notes to assist with setup.

## Minimum Versions

Occasionally it becomes necessary to specify minimum versions of some tools:

* Java: [1.8.0-101](/tools/setupdevenv/#missing-certificate---lets-encrypt)

## Other Tools

* PostgreSQL -- For running an external database to support storage modules.
This will enable faster startup and operations during development.
Note that this is not required to be installed for running modules using the "embed_postgres" option.

## Configuration

FOLIO utilizes the Nexus OSS Repository Manager to host Maven artifacts and NPM packages for FOLIO projects.
Docker images are the primary distribution model for FOLIO modules.

See [Built artifacts](/download/download-built-artifacts/) for configuration details for accessing the released and snapshot FOLIO artifacts.

For developers needing to publish artifacts, an overview and usage configuration details are provided, see
[Build, test, and deployment infrastructure](/guides/system/#automation).


## Coding style

### Style guidelines and configuration

Refer to the [coding style](/guidelines/codingconventions/#style-guidelines-and-configuration) sections of the
[Coding Conventions](/guidelines/codingconventions/#coding-conventions).

### Code analysis and linting

All code repositories have linter and code-style analysis facilities implemented as part of their continuous integration build process.
The process is [explained](/guidelines/codingconventions/#code-analysis-and-linting), along with usage notes and configuration for running those tools locally.

### Use EditorConfig for consistent whitespace

Many FOLIO repositories have a `.editorconfig` configuration file at their top level. This enables consistent whitespace handling.

Refer to [EditorConfig.org](http://editorconfig.org) which explains that some text editors have native support, whereas others need a plugin.

Consult its documentation for each plugin. Note that some do not handle all EditorConfig properties.
In such cases refer to the documentation for the particular text editor, as it might have its own facilities.
For example, the Java text editor in Eclipse has its own configuration for `trim_trailing_whitespace`
(see [notes](http://stackoverflow.com/questions/14178839/is-there-a-way-to-automatically-remove-trailing-spaces-in-eclipse)).

### No license header

As [explained](/guidelines/codingconventions/#no-license-header), we do not use a license header in the top of each source code file.

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
    # Until each mod-* has addressed RMB-130:
    **/src/main/java/org/folio/rest/jaxrs/
    **/src/main/java/org/folio/rest/client/
	
## Update git submodules

Some FOLIO repositories utilize "git submodules" for sections of common code.

For example, each `mod-*` module and `raml-module-builder` include the "raml" repository as a git submodule as its `raml-util` directory.

Note that when originally cloning a repository, use 'git clone --recursive ...'
Some git clients do not. If you then have an empty "raml-util" directory, then do `git submodule update --init`

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

For Maven-based modules, add to your POM file (copy the 'git submodule update' from mod-notes) to assist all git clients to update.

# Troubleshooting

A collection of general tips to assist developers to conduct troubleshooting.
Some FOLIO repositories also have specific notes.

## Other troubleshooting documents

* [Stripes troubleshooting](https://github.com/folio-org/stripes-core/blob/master/doc/troubleshooting.md)
* [Vagrant boxes troubleshooting](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#troubleshootingknown-issues)

## Keep system tools up-to-date

As [explained](/tools/setupdevenv/#setting-up-the-dev-environment) in the FOLIO setup documentation,
keeping the operating system and tools up-to-date will generally help to
avoid issues.
See [minimum versions](/tools/setupdevenv/#minimum-versions) of some tools.

## Update git submodules

Some FOLIO repositories utilize “git submodules” for sections of common code.
Some git clients do not handle this properly.
See [notes](/tools/setupdevenv/#update-git-submodules).

## Run as a regular user

As usual, do all development and running as a regular user, not as root.
Otherwise there will be strange behaviour, and various facilities and
tools might not be available.
For example, Postgres (including the embedded one) refuses to run as root.

## Launching Vagrant on Windows

If launching Vagrant from a Windows Command Prompt, be sure to use _Run As Administrator..._
when opening the Command Prompt itself (cmd.exe).
If you are seeing the error _"EPROTO: protocol error, symlink"_, the likely cause is that
Vagrant was not launched with administrator privileges.
See issue [STRIPES-344](https://issues.folio.org/browse/STRIPES-344) for details.

## Missing certificate - Let's Encrypt

If you are using a version of the Oracle JDK prior to `1.8.0_101`
then the [Let's Encrypt](https://letsencrypt.org/)
certificate authority is not in the Java trust store
([see notes](https://stackoverflow.com/questions/34110426/does-java-support-lets-encrypt-certificate)).
So it will not be possible to download components from the FOLIO Maven
repository. You will see error messages like:

> Could not resolve dependencies for project org.folio:mod-users:jar:0.1-SNAPSHOT: Failed to collect dependencies at org.folio:domain-models-api-interfaces:jar:0.0.1-SNAPSHOT: Failed to read artifact descriptor for org.folio:domain-models-api-interfaces:jar:0.0.1-SNAPSHOT: Could not transfer artifact org.folio:domain-models-api-interfaces:pom:0.0.1-SNAPSHOT from/to folio-nexus (https://repository.folio.org/repository/maven-folio): sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target -> [Help 1]

The fix is just to replace your JDK with a sufficiently recent replacement.
(Or you can use OpenJDK, which has supported Let's Encrypt for longer.)


