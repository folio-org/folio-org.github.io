---
layout: page
title: Guidelines for Contributing Code
permalink: /guidelines/contributing/
menuInclude: no
menuTopTitle: Guidelines
---

## License

Copyright (C) 2015-2025 The Open Library Foundation

All software is distributed under the terms of the Apache License, Version 2.0.

See the top of each repository's README document and its LICENSE file.
See the [Contributor License Agreement](#contributor-license-agreement) section below.

## Issue tracker

The FOLIO Issue Tracker is at [https://folio-org.atlassian.net/jira](https://folio-org.atlassian.net/jira)
and see the usage [guidelines](/guidelines/issue-tracker/)
which encourage reports of various types of issue and explain how to.

## Git and branches

For all FOLIO code repositories, we are trying to follow
[GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow).

In short, the master branch is always the head of latest development. Anything
merged into master should be of such good quality that at any time a snapshot
from master passes all tests, and can be deployed. That is not to say that it
will be free of bugs; we are not superhuman.

All work is done in feature branches, and merged to master via pull requests.

### Fork GitHub repository

Most people have write permission to only the few
[https://github.com/folio-org](https://github.com/folio-org)
repositories that they regularly work on via their GitHub [Teams](/faqs/how-to-request-github-access/#manage-members-for-teams).
For contributions to any other repository you
will need to "fork" it to your personal GitHub account, see the GitHub notes about
[working with forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks).

The starting point is the cloned folio-org repository as `origin` on your local
machine and looks like this:

    git remote -v
    origin  https://github.com/folio-org/folio-ansible (fetch)
    origin  https://github.com/folio-org/folio-ansible (push)

These are the steps to convert it to a triangular workflow:

    git remote rename origin upstream
    git remote add origin https://github.com/YOUR_USERNAME/folio-ansible
    git config remote.pushdefault origin
    git config push.default current

This is the result:

    git remote -v
    origin  https://github.com/YOUR_USERNAME/folio-ansible (fetch)
    origin  https://github.com/YOUR_USERNAME/folio-ansible (push)
    upstream        https://github.com/folio-org/folio-ansible (fetch)
    upstream        https://github.com/folio-org/folio-ansible (push)

Now `fetch` and `pull` will use the folio-org `upstream` repository. A `push`
will use your personal `origin` fork from where you can create the pull request.
A maintainer will merge it to the `upstream` repository.

### Commit messages
Try to follow the commit message guidelines in
[https://chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/).
The key points are:
* Separate subject from body with a blank line
* Limit the subject line to 50 characters
* Capitalize the subject line
* Do not end the subject line with a period
* Use the imperative mood in the subject line
* Wrap the body at 72 characters
* Use the body to explain what and why vs. how

The last point is the most critical:
> A diff will tell you what changed, but only the commit message can properly tell you why.

Also consider mentioning relevant Issue identifiers (e.g. OKAPI-258).
This assists people to follow the reasons, and enables the issue tracker to
automatically link to the related commits.

### Retain git commit history

Make every effort to not lose the history.
The commit history is important for various reasons, not only that it shows the development track of resources, but also that it contains the attribution required by the Apache License.

For example when there is a need to rename a file, be sure to use 'git mv ...' to move the file content and its history, rather than simple filesystem rename or copy-and-remove commands.

### Feature branches

Feature branches should be branched off from the master. The naming of those
is not strict, but if you start a branch to fix Jira ticket OKAPI-99999
 then name the branch to include that ticket number plus something descriptive
such as OKAPI-99999-contrib-guidelines):

    git checkout -b OKAPI-99999-contrib-guidelines

You can commit stuff as you go, but try not to push obviously broken stuff into
GitHub, not even in your development branch -- that will be visible for the
whole world, and there is automatic CI testing for each branch so
pushing a broken commit will cause some emails. But if you need to share the
code, for example for collaborating, of course you need to push it. Naturally
you will write decent commit messages explaining what you have done.

The first time you want to push your branch to GitHub, you may encounter an
error "_The current branch OKAPI-99999-contrib-guidelines has no upstream branch_". Git tells you
what to do, namely:

    git push --set-upstream origin OKAPI-99999-contrib-guidelines

Once you have done that once, a simple `git push` will be sufficient
thereafter.

While developing your own branch, pull in the master every now and then, and
resolve any conflicts that may be there. If you don't, your branch
will diverge further from master, and the final merge of your work
back into master will be difficult to resolve.

When you are all done, pull master in again, to make sure your branch merges
cleanly and passes all tests. Commit the merge, and push to your branch:

    git push

You may also want to `git rebase` your branch, compressing multiple commits
into one, and editing the commit messages.

### git bisect finding a merge commit

`git bisect` helps to find a commit that has introduced a bug
([git bisect manual](https://git-scm.com/docs/git-bisect)).
When bisecting, the commits within a feature branch of a pull request should be
skipped because it is unknown whether they build successfully.  Ori from Smartly published
"[Git Bisect Debugging with Feature Branches](https://blog.smart.ly/2015/02/03/git-bisect-debugging-with-feature-branches/)"
with this code snippet that skips those feature branch commits:

    git bisect start master 75369f4a4c026772242368d870872562a3b693cb

    for rev in $(git rev-list 75369f4a4c026772242368d870872562a3b693cb..master --merges --first-parent); do
        git rev-list $rev^2 --not $rev^
    done | xargs git bisect skip

## Requesting a merge

Go to the relevant repository's GitHub page at the "Branches" tab.
It shows some recently pushed branches -- your one should be there too.
Ensure that the initial branch does build in the CI before proceeding.

Consider the items in the relevant [Pull requests checklists](/guidelines/pull-requests-checklists/) before proceeding,
and refer to the [Development, design, and review processes](/guidelines/development-design-review/).

When ready, next to your branch is a button "New pull request". Select that.
Provide a clear title for the PR, including a Jira ticket number, as explained in those checklists.

If you are using a fork, then the process is a little different.
Start from your fork and select "New pull request", then select your
head fork and branch.

It should show that it is _able to merge_, so select the "Create pull
request" button under the comment box.

If your pull request is instead to seek feedback, then say in the
description and title that it is not yet ready to merge.
Describe the items for which you want assistance.

After the pull request is created, add yourself as the first assignee.
Some repositories have explicit "code owners" which will be automatically invited to review.
If needed, then invite other specific reviewers.

## Merging pull requests

When someone has assigned a pull request to you or requested your review, check out the branch, and
look at the git log, and the code, and decide whether all is good.
You can also look at the commit messages and code changes in GitHub.

Consider the items in the relevant [Pull requests checklists](/guidelines/pull-requests-checklists/).

If there are small details, you can fix them yourself, commit and push to the
branch. Do not copy-and-paste the content as this loses the commit history that
contains the attribution required by the Apache License and is used for the
[merge check](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management)
of the `git branch` command; if needed create a new branch from pull request's branch.

If there are serious issues, you can close the pull request without
merging, with a comment explaining why you could not do it.

Once all is well, you can use GitHub's interface. Just go to the
conversation tab, and select "_Merge Pull Request_" (don't squash, don't rebase,
[learn why](https://git-scm.com/book/en/v2/Git-Branching-Rebasing#_rebase_peril)).
Edit the comment if
necessary, and select "_Confirm Merge_". GitHub should tell you that the
"_Pull request successfully merged and closed_". Next to it is a button to
"_Delete the Branch_". For a simple feature branch, you might as well delete
it now, it has served its purpose. But if you think there is more work that
should be done in this branch, of course you don't delete it.

This merging of the pull request's branch OKAPI-99999-contrib-guidelines can also be done on the
command line, if you prefer.

    git checkout master
    git merge OKAPI-99999-contrib-guidelines

When done, you probably want to delete the local branch from your own machine

    git branch -d OKAPI-99999-contrib-guidelines

Also tidy up to delete the remote branch.

## Contributor License Agreement

The FOLIO Project uses the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) for its code and requires developers to acknowledge their contributions to the project using this license.  The contents of the Contributor License Agreement (CLA) are stored in a Gist on GitHub:

{% gist a72174fc6b18f3a66f2f9d3db1c8f127 %}

See [accepting the contributor license agreement](/guidelines/cla-process) for more details.

## Automation

The FOLIO [build, test, and deployment infrastructure](/guides/automation/)
is described separately.

## Releasing

Refer to the specific [Release procedures](/guidelines/release-procedures/).

Later, if there are bugs in the released version, work can continue on the
version branch, and we can release a new minor version from the branch. Some
changes may be cherry-picked from the master, or from the version branch to the
master, as need be.

## Version numbers

Since (almost) all components have hard separation between interface and implementation,
we need to keep two kinds of version numbers, one for the API, and one for the implementation code.
To make matters worse, any FOLIO module may implement several interfaces.
The Okapi Guide further describes its handling of [Versioning and Dependencies](https://github.com/folio-org/okapi/blob/master/doc/guide.md#versioning-and-dependencies).

### API/interface versions

The API versions are two-part _major.minor_ numbers, such as `3.14`

The rules are simple:

- If you only add things to the interface -- e.g. a new resource or method on existing resources --
  then you increment the minor number, because the API is backwards compatible.
- If you remove or change anything, you must increment the major number,
  because now your API is no longer backwards compatible.

For example, you can add a new resource to `3.14`, and call it `3.15`.
Any module that requires `3.14` can also use `3.15`. But if you remove
anything from the API, or change the meaning of a parameter, you need to
bump the API version to `4.1`

### Implementation versions

We follow the rules commonly known as [_semantic versioning_](https://semver.org/)
to version both FOLIO
_modules_ (aka _apps_) and any other FOLIO software components (e.g. utility libraries of frameworks),
so-called _non-modules_.

The implementation versions are three-part part numbers: _major.minor.bugfix_, such as `2.7.18`.

FOLIO _modules_ may implement more than one interface so they are versioned independently from any
particular interface, they need to however follow the same rules:

- For _modules_, the major part should be incremented if you implemented a backwards incompatible
  change to the API(s), (this will be indicated by the major number change in the particular API).
  For non-modules this may also mean any major changes with respect to functionality or implementation that don't
  necessarily result in interface changes, e.g. migration to a new DB backend.

- For _modules_ the middle part should be incremented if you implemented an addition to the API(s),
  (the minor version of the particular API has been changed).
  For non-modules it may also mean any additional functionality. For both, the change must be backwards compatible with
  respect to any client code or agents.

- For _modules_ the bugfix part should be incremented if you haven't changed anything in
  the API or added any new functionality but only fixed implementation bugs, etc. The same applies for _non-modules_.

### Module implements one interface

In the simplest case, a module implements just one interface, but since we want to be able to register any functional changes to the module by
increasing the module's minor version number, we will keep two independent versions for the API and implementation. For example, a module with version `2.71.0`
may implement the checkout API at `3.14`. When the checkout API changes to `3.15`, and the module implements the change,
the module version becomes `2.72.0`. In the case where only the implementation is corrected (bugfixes with no functionality changes)
and the module still implements the checkout API at `3.14`, then the module version gets bumped to `2.71.1`.

### Module implements multiple interfaces

A module can implement [more](https://github.com/folio-org/okapi/blob/master/doc/guide.md#multiple-interfaces)
than one interface, and more than one major version
of any of them. In that case the version numbering is necessarily more complex.
Again, there does not have to be any correlation between the module version and the
version of the interfaces it implements.

For example, if the circulation module version `2.71.0` can implement the
checkout API version `3.14` and the checkin API version `1.41` then the
rules are still the same:

- If the change doesn't follow any change to any API and is merely a bugfix, increment the last part to `2.71.1`
- If you add new features that e.g. follow the extended APIs, increment the middle part to `2.72.0`
- If you implement any backwards-incompatible change to _any_ API, or drop _any_
  API at all, increment the module version to `3.0.0`

The most common case is probably when we need to add a new, incompatible API
to a module, but want to keep the old one too. In such cases we only increment
the module version to `2.72.0` but mark that it provides the API versions
`3.14` and `1.41`

### Trailing zero for module/non-module versions

Changes to major and minor version follow from adding new features or larger
code refactoring, usually planned in advance. The bugfix version number is reserved for
tracking changes caused by malfunction that may be hard to predict.

As such, every new version for a particular major.minor series (e.g. `2.71`) start with bugfix
version set as 0, effectively `2.71.0`. This indicates that no bugs have been discovered (yet)
and no hotfix releases provided.

## Naming conventions

There are guidelines for [Naming conventions](/guidelines/naming-conventions/) of modules, permissions, endpoints, etc.

## Coding style

### Style conventions

Follow the coding style that is being used by each repository for each file type.

For JSON key names we use camelCase.

For Java code we basically try to adhere to Sun Java coding
[conventions](https://www.oracle.com/technetwork/java/codeconvtoc-136057.html)
(that document is old and unmaintained, but seems to be good enough as it is).

For JavaScript code we follow [ESLint](https://eslint.org), with some exceptions.

### Code analysis and linting

All code repositories have linter and code-style analysis facilities implemented as part of their continuous integration build process.
The process is [explained](/guides/code-analysis), along with usage notes and configuration for running those tools locally.

### Consistent whitespace

- We indent with two spaces only, because vert.x uses deeply nested callbacks.
- We _do not_ use tab characters for indents, only spaces.

For XML and JSON and RAML files, the same: two-space indent and no tabs.

Some projects do [provide](/faqs/how-to-use-editorconfig/) a `.editorconfig` file.
Remember to set your IDE and editors to remove trailing spaces on saving files,
since those produce unnecessary diffs in Git.
Refer to coding style [configuration](/guides/developer-setup#coding-style) assistance.

### No license header

We do not use a license header in the top of each source code file.
Refer to the README and LICENSE file at the top of each repository.
See further [license](#license) information.
See [configuration](/guides/developer-setup#no-license-header) assistance for IDEs.

## Tests

We aim to write a lot of tests -- each module should have at least some kind of
test associated with it. These can be traditional unit tests, black-box tests
that talk through the WSAPI, and/or proper integration tests.

When hunting down problems, it is considered good form to write a test that
demonstrates the problem first, then a fix that makes the test pass.

We have a Jenkins test system that gets invoked when you push something
to a branch, and/or make a pull request. It should flag any errors, but be
nice and run a ```mvn install``` on your own machine before every
```git commit```

## RAML and Schema

Ensure thorough description of the API [RAML](/start/primer-raml/) files
and [describe schema](/guides/describe-schema/) properties.

Ensure that breaking changes in the API are reflected with a new interface version.

For Okapi, we keep the API specs in RAML files under `okapi-core/src/main/raml/`

For [server-side modules](/source-code#server-side),
the [raml](https://github.com/folio-org/raml)
repository is the master location for the shared traits and resource
types, while each module is the master for its own schemas, examples,
and actual RAML files.

[Reference API documentation](/reference/api/)
is automatically generated by the continuous integration,
for modules that are managed with the FOLIO CI.

