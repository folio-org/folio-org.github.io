---
layout: guidelines
title: Contributing Code
heading: Contributing Code
permalink: /guidelines/contrib-code/
---

# Contributing Code

## License

Copyright (C) 2017 The Open Library Foundation

All software is distributed under the terms of the Apache License, Version 2.0.

See the top of each repository's README document and its LICENSE file.
See the [Contributor License Agreement](#contributor-license-agreement) section below.

## Issue tracker

The FOLIO Issue Tracker is at [issues.folio.org](https://issues.folio.org/)
and see the usage [guidelines](/guidelines/communityguidelines/#issue-tracker)
which encourage reports of various types of issue and explain how to.

## Git and Branching

For all FOLIO code repositories, we are trying to follow
[GitHub Flow](https://guides.github.com/introduction/flow/).

In short, the master branch is always the head of latest development. Anything
merged into master should be of such good quality that at any time a snapshot
from master passes all tests, and can be deployed. That is not to say that it
will be free of bugs; we are not superhuman.

All real work should be done in feature branches. It is still OK to make a
small trivial change directly in the master. Stuff like editing the README.

People who do not have direct write permissions will need to "fork" the
relevant repository. See the GitHub notes about
[working with forks](https://help.github.com/articles/working-with-forks/).

## Commit Messages

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

## Feature Branches

Feature branches should be branched off from the master. The naming of those
is not strict, but if you start a branch to fix issue okapi-xxx filed in
[issues.folio.org](https://issues.folio.org/) then you might well call the
branch _okapi-xxx_ (or if you want to be more descriptive, something
like _okapi-xxx-contribution-guidelines_):

    git checkout -b okapi-xxx

You can commit stuff as you go, but try not to push obviously broken stuff into
GitHub, not even in your development branch -- that will be visible for the
whole world, and we plan to set up automatic testing for each branch, so
pushing a broken commit will cause some emails. But if you need to share the
code, for example for collaborating, of course you need to push it. Naturally
you will write decent commit messages explaining what you have done.

The first time you want to push your branch to GitHub, you may encounter an
error _The current branch okapi-xxx has no upstream branch_. Git tells you
what to do, namely:

    git push --set-upstream origin okapi-xxx

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

## Requesting a Merge

Go to the GitHub page, and it shows some recently pushed branches -- your one should
be there too. Next to it is a button "New pull request". Click on that.

If you are using a fork, then the process is a little different.
Start from your fork and select "New pull request", then select your
head fork and branch.

It should show that it is _able to merge_, so click on the "Create pull
request" button under the comment box.

If your pull request is instead to seek feedback, then say in the
description that it is not yet ready to merge. Describe the items for which
you want assistance.

After the pull request is created, assign it to someone else.
Alternatively leave it for someone to pick up.

### Contributor License Agreement

The FOLIO Project uses the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) for its code and requires developers to acknowledge their contributions to the project using this license.  The contents of the Contributor License Agreement (CLA) are stored in a Gist on GitHub:

{% gist a72174fc6b18f3a66f2f9d3db1c8f127 %}

See [accepting the contributor license agreement](/guidelines/cla-process) for more details.

## Merging Pull Requests

When someone has assigned a pull request to you, check out the branch, and
look at the git log, and the code, and decide whether all is good.
You can also look at the commit messages and code changes in GitHub.

If there are small details, you can fix them yourself, commit and push to the
branch. Do not copy & paste the content as this loses the commit history that
contains the attribution required by the Apache License and is used for the
[merge check](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management)
of the `git branch` command; if needed create a new branch from pull request's branch.

If there are serious issues, you can close the pull request without
merging, with a comment explaining why you could not do it.

Once all is well, you can use GitHub's interface. Just go to the
conversation tab, and click on _Merge Pull Request_ (don't squash, don't rebase,
[learn why](https://git-scm.com/book/en/v2/Git-Branching-Rebasing#The-Perils-of-Rebasing)).
Edit the comment if
necessary, and click on _Confirm Merge_. GitHub should tell you that the
_Pull request successfully merged and closed_. Next to it is a button to
_Delete the Branch_. For a simple feature branch, you might as well delete
it now, it has served its purpose. But if you think there is more work that
should be done in this branch, of course you don't delete it.

This merging of the pull request's branch okapi-xxx can also be done on the
command line, if you prefer.

    git checkout master
    git merge okapi-xxx

When done, you probably want to delete the local branch from your own machine

    git branch -d okapi-xxx
	
## Automation

The FOLIO [build, test, and deployment infrastructure](/guides/system/#automation)
is described separately.
	
## Releasing

The exact procedure for making a release is not yet specified. It is likely to
be something like we are doing for other software:

- Freeze the master for a short while
- Make a release branch
- Make changes specific for this release in the branch
- Tag a version
- Package and release it

Refer to the specific [Release procedures](/guides/release-procedures/).

Later, if there are bugs in the released version, work can continue on the
version branch, and we can release a new minor version from the branch. Some
changes may be cherry-picked from the master, or from the version branch to the
master, as need be.
