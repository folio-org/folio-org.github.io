---
layout: page
title: Setup development environment
---

Collection of tips to assist developers to configure their local workstation setup environment for FOLIO development.

Assume already doing other development, so know how to keep the operating system up-to-date, know its quirks, know how to use the various package managers. So this document will not go into detail about that.

## Update git submodules

Some FOLIO repositories utilize "git submodules" for sections of common code.

For example, each `mod-*` module and `ram-module-builder` include the "raml" repository as a git submodule as its `./raml-util` directory.

Note that when originally cloning a repository, use 'git clone --recursive ...'
Some git clients do not. If you then have an empty "raml-util" directory, then do 'git submodule update --init'.

Thereafter updating that submodule is deliberately not automated, so that we can ensure a stable build when we git checkout in the future.

So when an update is needed to be committed, do this:

    cd mod-configuration (for example)
    git submodule foreach 'git checkout master && git pull origin master'
    git commit ...

Now when people update their local checkout, then some git clients do not automatically update the submodules. So they need to follow with 'git submodule update'.

This part can be automated with client-side git hooks. Create the following two shell scripts:

    mod-configuration/.git/hooks/post-checkout
    mod-configuration/.git/hooks/post-merge

using this content:

    #!/bin/sh
    git submodule update

and make them executable: 'chmod +x post-checkout post-merge'

Now subsequent updates will also update the submodules to their declared revision.
